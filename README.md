Week 1: Core ML Pipeline
Day 1 -- Setup + YOLOv8 inference working
Goal: a single script that takes a video file, runs YOLOv8-Pose on each frame, and prints keypoint coordinates to console.
Tasks:

Create the venv, install Ultralytics, OpenCV, NumPy
Read the YOLOv8-Pose docs and understand the 17 COCO keypoints and their index numbers (this is mandatory, you'll be asked about this in interviews)
Write pose_estimator.py: load model, run inference on a video frame by frame, extract keypoints array
Test on any video of a person moving

Deliverable: terminal output showing keypoint coordinates updating per frame.
Day 2 -- Joint angle calculator
Goal: calculate the angle at any joint given three keypoints.
Tasks:

Write angle_calculator.py with a calculate_angle(a, b, c) function where b is the vertex joint. This uses the dot product / arctan2 approach, I'll explain the math if needed.
Map the exercises to their relevant keypoints:

Bicep curl: shoulder (5/6), elbow (7/8), wrist (9/10)
Squat: hip (11/12), knee (13/14), ankle (15/16)
Pushup: shoulder (5/6), elbow (7/8), wrist (9/10) + hip angle for form


Visualize the angle overlaid on the video frame using OpenCV so you can see it working

Deliverable: video output with joint angles displayed on screen in real time.
Day 3 -- Rep counting state machine
Goal: count reps reliably without false positives.
Tasks:

Write rep_counter.py as a simple state machine: two states, UP and DOWN, defined by angle thresholds

Example for curl: DOWN when elbow angle < 50 degrees, UP when elbow angle > 150 degrees
A rep completes on the UP to DOWN to UP transition


Handle edge cases: keypoint confidence thresholds (ignore low-confidence detections), smoothing with a small angle buffer to avoid jitter triggering false counts
Test on multiple videos with different people and lighting

Deliverable: terminal shows rep count incrementing correctly on a test video.
Day 4 -- FastAPI backend
Goal: expose the pipeline as a REST API.
Tasks:

Write schemas.py with Pydantic models for request (video file upload, exercise type) and response (rep count, average angle range, keypoints per frame, processing time)
Write main.py with two endpoints:

POST /analyze -- accepts video file upload, returns full analysis JSON
GET /health -- returns service status


Add exercise type selection: curl, squat, pushup
Test with curl or Postman

Deliverable: API running locally, returning JSON rep count from a video upload.
Day 5 -- MLflow tracking + tests
Goal: add observability and basic test coverage.
Tasks:

Write tracking.py: log each analysis run to MLflow with parameters (exercise type, video length, fps) and metrics (rep count, avg confidence score, processing time per frame)
Run MLflow UI locally and verify runs are logging correctly
Write unit tests in tests/ for the angle calculator and rep counter state machine, these are pure logic functions so they're easy to test
Fix any bugs surfaced by the tests

Deliverable: MLflow UI showing logged runs, all tests passing.

Week 2: Engineering Layer
Day 6-7 -- Docker

Write the Dockerfile: Python base image, copy app, install requirements, expose port, run Uvicorn
Test the container locally: build, run, hit the API from outside the container
Write docker-compose.yml to run the API and MLflow server together

Day 8-9 -- Gradio frontend

Write gradio_app.py: video upload input, exercise type dropdown, submit button, output shows rep count + annotated video with pose overlay and angle display
Make it visually clean, this is what people see in your README

Day 10 -- Polish and README

Record a demo GIF of the Gradio app working (use a screen recorder, keep it under 5 seconds, shows pose overlay + rep counter incrementing)
Write the README: what it does, how to run locally, how to run with Docker, architecture diagram (optional but impressive), demo GIF at the top
Push everything to GitHub with a clean commit history, not one giant initial commit


Week 3: Deployment + CV Integration
Day 11-12 -- Hugging Face Spaces deployment

Create a Hugging Face account if you don't have one
Deploy the Gradio app to HF Spaces (it supports Gradio natively, free tier is enough)
Include sample videos in the repo so reviewers can test it without needing their own footage

Day 13 -- Stress test and edge cases

Test with varied videos: different lighting, different body sizes, partial occlusion, fast vs slow reps
Document known limitations honestly in the README, interviewers respect this more than overclaiming

Day 14 -- CV and GitHub update
Update both CVs with the project:
FitRep: AI Exercise Rep Counter
- Built a real-time pose estimation pipeline using YOLOv8-Pose and OpenCV, 
  detecting 17 body keypoints to classify and count exercise repetitions 
  across 3 movement types.
- Implemented a joint angle state machine in NumPy handling confidence 
  thresholding and jitter smoothing for robust rep detection.
- Deployed as a FastAPI service containerized with Docker, with experiment 
  tracking via MLflow and a live Gradio demo on Hugging Face Spaces.
- Stack: Python, YOLOv8, OpenCV, FastAPI, Docker, MLflow, Gradio, 
  Hugging Face Spaces