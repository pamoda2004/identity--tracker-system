
```md id="pcqymy"
# Frontend - Persistent Identity Tracker

This frontend is built with **React + Vite**.

It provides the dashboard for the project and communicates with the backend API.

The dashboard is responsible for showing:

- processed video frames
- current active tracked IDs
- unknown person captures
- start/stop controls for video processing

---

## Main Responsibilities

The frontend performs the following tasks:

1. Starts video processing
2. Polls the backend for the latest processed frame
3. Displays the latest annotated frame
4. Displays the currently active tracked IDs
5. Displays the gallery of unknown captured persons
6. Stops processing when requested

---

