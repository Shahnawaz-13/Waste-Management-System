# Viva Questions and Answers

1. **Why did you choose FastAPI?**  
   FastAPI is lightweight, fast, async-friendly, and automatically generates API docs, which made backend development cleaner and faster.

2. **Why is AI used in your project?**  
   AI helps automatically classify the waste type from uploaded images, reducing manual sorting effort.

3. **Which model did you use and why?**  
   I used ResNet18 transfer learning because it gives strong accuracy even with small datasets and trains faster.

4. **What dataset did you use?**  
   I used TrashNet and mapped images into Plastic, Metal, and Organic classes.

5. **How does role-based workflow work?**  
   Users create complaints, admins assign workers, and workers update task status from Pending to In Progress to Completed.

6. **What is the use of route optimization?**  
   It finds the shortest path between waste pickup zones and landfill to reduce fuel and time.

7. **How did you store location data?**  
   Latitude, longitude, and optional address are stored in MongoDB under the location object.

8. **What analytics are shown in dashboard?**  
   Total complaints, status split, time trend, area-wise counts, and garbage heatmap.

9. **What are limitations of your system?**  
   Prediction accuracy depends on data quality, and current route graph is static demo data.

10. **How can this project be improved?**  
   Add live GPS tracking, push notifications, IoT integration, and a larger custom-trained dataset.
