import os

import pandas as pd
import plotly.express as px
import pydeck as pdk
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")

st.set_page_config(page_title="Smart Waste Management", layout="wide")
st.title("♻️ Smart Waste Management System")
st.caption("AI-enabled complaint management, assignment workflow, analytics, and route optimization.")

role = st.sidebar.selectbox("Login as", ["User", "Admin", "Worker"])


def load_complaints():
    response = requests.get(f"{API_BASE}/complaints", timeout=20)
    response.raise_for_status()
    return response.json()


if role == "User":
    st.subheader("Report Waste")
    with st.form("complaint_form", clear_on_submit=True):
        user_id = st.text_input("User ID", "user_1003")
        description = st.text_area("Complaint Description")
        latitude = st.number_input("Latitude", value=28.6139)
        longitude = st.number_input("Longitude", value=77.2090)
        address = st.text_input("Address / Landmark")
        image = st.file_uploader("Upload Waste Image", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Submit Complaint")

        if submitted:
            if not image:
                st.error("Please upload an image.")
            else:
                files = {"image": (image.name, image.getvalue(), image.type)}
                data = {
                    "user_id": user_id,
                    "description": description,
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": address,
                }
                result = requests.post(f"{API_BASE}/complaints", data=data, files=files, timeout=30)
                if result.ok:
                    prediction = result.json().get("predicted_class")
                    st.success(f"Complaint created successfully. Predicted waste class: {prediction}")
                else:
                    st.error(result.text)

elif role == "Admin":
    st.subheader("Admin Console")
    complaints = load_complaints()
    complaint_df = pd.json_normalize(complaints)

    if complaint_df.empty:
        st.info("No complaints found.")
    else:
        st.dataframe(
            complaint_df[["id", "description", "predicted_class", "status", "assigned_worker_id"]],
            use_container_width=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Assign Worker")
            complaint_id = st.selectbox("Complaint ID", complaint_df["id"].tolist())
            worker_id = st.text_input("Worker ID", "worker_01")
            if st.button("Assign"):
                response = requests.patch(
                    f"{API_BASE}/complaints/{complaint_id}/assign",
                    json={"worker_id": worker_id},
                    timeout=20,
                )
                st.success("Assigned successfully") if response.ok else st.error(response.text)

        with col2:
            st.markdown("#### Dashboard Analytics")
            analytics = requests.get(f"{API_BASE}/analytics/dashboard", timeout=20).json()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total", analytics["total_complaints"])
            m2.metric("Pending", analytics["pending"])
            m3.metric("In Progress", analytics["in_progress"])
            m4.metric("Completed", analytics["completed"])

            trend_df = pd.DataFrame(analytics["trend"])
            if not trend_df.empty:
                st.plotly_chart(px.line(trend_df, x="day", y="complaints", markers=True), use_container_width=True)

            area_df = pd.DataFrame(analytics["area_wise"])
            if not area_df.empty:
                st.plotly_chart(px.bar(area_df, x="area", y="complaints"), use_container_width=True)

            map_df = complaint_df[["location.latitude", "location.longitude"]].dropna()
            if not map_df.empty:
                st.pydeck_chart(
                    pdk.Deck(
                        map_style="mapbox://styles/mapbox/light-v9",
                        initial_view_state=pdk.ViewState(
                            latitude=float(map_df["location.latitude"].mean()),
                            longitude=float(map_df["location.longitude"].mean()),
                            zoom=10,
                            pitch=35,
                        ),
                        layers=[
                            pdk.Layer(
                                "HeatmapLayer",
                                data=map_df.rename(
                                    columns={"location.latitude": "lat", "location.longitude": "lon"}
                                ),
                                get_position="[lon, lat]",
                                radiusPixels=50,
                            )
                        ],
                    )
                )

elif role == "Worker":
    st.subheader("Worker Task Board")
    worker_id = st.text_input("Worker ID", "worker_01")

    if st.button("Load Tasks"):
        response = requests.get(f"{API_BASE}/workers/{worker_id}/tasks", timeout=20)
        if response.ok:
            tasks = response.json()
            task_df = pd.json_normalize(tasks)
            st.dataframe(task_df[["id", "description", "status", "location.address"]], use_container_width=True)
        else:
            st.error(response.text)

    st.markdown("#### Update Task Status")
    complaint_id = st.text_input("Complaint ID to Update")
    status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
    if st.button("Update Status"):
        response = requests.patch(
            f"{API_BASE}/complaints/{complaint_id}/status",
            json={"status": status},
            timeout=20,
        )
        st.success("Status updated") if response.ok else st.error(response.text)

st.sidebar.markdown("---")
st.sidebar.markdown("### Route Optimization Demo")
start = st.sidebar.selectbox("Start", ["Depot", "Zone-A", "Zone-B", "Zone-C"])
end = st.sidebar.selectbox("End", ["Zone-A", "Zone-B", "Zone-C", "Landfill"])
if st.sidebar.button("Get Best Route"):
    result = requests.post(
        f"{API_BASE}/optimize-route",
        data={"start": start, "end": end},
        timeout=20,
    )
    if result.ok:
        payload = result.json()
        st.sidebar.success(f"Distance: {payload['distance']} km")
        st.sidebar.write(" → ".join(payload["path"]))
    else:
        st.sidebar.error(result.text)
