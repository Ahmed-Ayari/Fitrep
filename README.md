# FitRep

A real-time AI-powered rep counter that uses pose estimation to track your workout reps from video input.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Pose-red)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Gradio](https://img.shields.io/badge/Gradio-Demo-yellow)

---

## What it does

Upload a workout video, select your exercise, and FitRep will:

- Detect your body keypoints using YOLOv8-Pose
- Calculate joint angles frame by frame
- Count reps using a state machine with configurable angle thresholds
- Return rep count, confidence scores, and angle statistics
- Log every run to MLflow for experiment tracking

---

## Supported Exercises

| Exercise | Keypoints Used |
|----------|---------------|
| Bicep Curl | Shoulder, Elbow, Wrist |
| Squat | Hip, Knee, Ankle |
| Push Up | Shoulder, Elbow, Wrist |

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Pose Estimation | YOLOv8-Pose (Ultralytics) |
| Angle Calculation | NumPy + arctan2 |
| Rep Counting | Custom state machine |
| API | FastAPI + Uvicorn |
| Experiment Tracking | MLflow |
| Demo UI | Gradio |
| Containerization | Docker |

---

## Project Structure

```
fitrep/
├── app/
│   ├── main.py              # FastAPI app
│   ├── pose_estimator.py    # YOLOv8 inference + keypoint extraction
│   ├── config.py            # Exercise configs and thresholds
│   ├── angle_calculator.py  # Joint angle logic
│   └── rep_counter.py       # Rep counting state machine
├── demo/
│   └── gradio_app.py        # Gradio frontend
├── mlflow/
│   └── tracking.py          # MLflow experiment logging
├── tests/
│   └── test_rep_counter.py  # Unit tests
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## How it works

1. Video is uploaded and passed to the pose estimator
2. YOLOv8-Pose extracts body keypoints per frame
3. A confidence filter drops frames with unreliable keypoints
4. Joint angles are calculated using arctan2 on the three relevant keypoints
5. A rolling average smooths the angle signal to reduce noise
6. The state machine transitions between `init`, `DOWN`, and `UP` states to count reps
7. MLflow logs the exercise, thresholds, rep count, confidence, and angle stats

---

## Setup

### Local

```bash
# Clone the repo
git clone https://github.com/yourusername/fitrep.git
cd fitrep

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Start the API
fastapi dev

# In a separate terminal, start the Gradio demo
python demo/gradio_app.py
```

### Docker

```bash
docker build -t fitrep .
docker run -p 8000:8000 fitrep
```

---

## API

### `POST /analyze`

Analyzes a workout video and returns rep count and angle statistics.

**Request**

| Field | Type | Description |
|-------|------|-------------|
| `file` | video file | `.mp4`, `.avi`, `.mkv`, or `.mov` |
| `exercise` | string | `bicep_curl`, `squat`, or `push_up` |

**Response**

```json
{
  "exercise": "bicep_curl",
  "up_threshold": 50,
  "down_threshold": 140,
  "rep_count": 10,
  "final_state": "DOWN",
  "max_angle": 158.3,
  "min_angle": 28.7,
  "average_up_angle": 42.1,
  "average_down_angle": 151.6,
  "avg_confidence": 0.87,
  "min_confidence": 0.61
}
```

---

## Experiment Tracking

FitRep logs every analysis run to MLflow with:

- **Params:** exercise type, up/down thresholds
- **Metrics:** rep count, avg confidence, min confidence, max/min/average angles

To view the MLflow dashboard:

```bash
mlflow ui
```

Then open `http://localhost:5000` in your browser.

---

## Tests

```bash
pytest tests/test.py -v
```

Covers angle calculation correctness and rep counter state machine logic.

---

## Environment Variables

Copy `.env.example` to `.env` and update the values:

```env
API_URL=http://localhost:8000/analyze
```

---

## Roadmap

- [ ] Automatic exercise detection via keypoint-based classifier
- [ ] Real-time webcam support
- [ ] Rep tempo tracking (time under tension)
- [ ] Mobile frontend via React Native
- [ ] Multi-person support

---

## License

MIT