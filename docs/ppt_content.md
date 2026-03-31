# Final Year Project PPT Content

## Slide 1: Title
- Smart Waste Management System using AI and Data Analytics
- Your name, university, guide name

## Slide 2: Problem Statement
- Manual waste reporting is slow and unstructured
- No real-time tracking for municipal teams
- No intelligent categorization of waste types

## Slide 3: Proposed Solution
- Web platform for users, admins, and workers
- AI model for waste classification (Plastic / Metal / Organic)
- Data analytics dashboard + route optimization

## Slide 4: System Architecture
- Frontend: Streamlit
- Backend: FastAPI
- Database: MongoDB
- ML Engine: PyTorch CNN (ResNet18 transfer learning)

## Slide 5: Modules
- User: report complaints with image and location
- Admin: assign tasks and monitor statuses
- Worker: update assigned tasks

## Slide 6: AI/ML Pipeline
- Dataset: TrashNet (with 3 mapped classes)
- Preprocessing: resize, normalize, augmentation
- Training: transfer learning with ResNet18
- Output: class prediction + confidence

## Slide 7: Advanced Feature
- Dijkstra route optimization for waste pickup
- Heatmap for garbage hotspots on dashboard

## Slide 8: Results
- Faster issue reporting and tracking
- Automated waste category identification
- Better decision making via analytics

## Slide 9: Deployment Plan
- Backend: Render/Railway
- Frontend: Streamlit Cloud
- DB: MongoDB Atlas

## Slide 10: Future Scope
- Real-time IoT smart bins
- Notification system (SMS/email)
- Multi-class segmentation model
