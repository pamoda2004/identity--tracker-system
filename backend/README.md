# Backend - Persistent Identity Tracker

This backend is built with **FastAPI + Python + YOLO**.

It is responsible for:

- reading the input video
- detecting people using YOLO
- extracting appearance features
- matching identities across frames
- optionally using gait/movement information
- marking unmatched detections as `Unknown`
- saving unknown person crops
- generating annotated output frames
- serving API responses for the frontend dashboard

---

## Main Responsibilities

The backend performs the following pipeline for each frame:

1. Read the next frame from the video
2. Detect all persons using YOLO
3. Crop each detected person
4. Extract features such as:
   - upper body color
   - lower body color
   - aspect ratio
   - height
5. Extract movement / gait-related features
6. Compare the current detection with existing tracked persons
7. If similarity score is at least the threshold, keep the same `PersonID`
8. Otherwise, mark the detection as `Unknown`
9. Save unknown crops into `assets/unlabeled_captures/`
10. Draw bounding boxes and labels on the frame
11. Save the annotated frame into `assets/output_frames/`
12. Send frame information to the frontend

---

