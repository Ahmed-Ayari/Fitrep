---
title: FitRep
emoji: 💪
colorFrom: blue
colorTo: green
sdk: docker
app-port: 7860
pinned: false
---

# FitRep

An AI-powered workout rep counter using pose estimation. Upload a video of your exercise and FitRep will count your reps automatically.

---

## How to use

1. Upload a workout video (`.mp4`, `.avi`, `.mkv`, or `.mov`)
2. Select your exercise from the dropdown
3. Click **Analyze**
4. View your rep count, confidence scores, and angle statistics

---

## Supported Exercises

- Bicep Curl
- Squat
- Push Up

---

## How it works

FitRep uses YOLOv8-Pose to extract body keypoints from each frame, calculates joint angles using arctan2, and counts reps using a state machine that tracks the up/down cycle of each exercise.

---

## Source Code

Full source code, architecture details, and setup instructions available on [GitHub](https://github.com/Ahmed-Ayari/Fitrep).
