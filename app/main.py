from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "app"))
sys.path.append(str(PROJECT_ROOT / "mlflow_tracking"))

import tracking
import config
from pose_estimator import PoseEstimator
import gradio as gr
from demo.gradio_app import demo

upload_path = Path("uploads")
upload_path.mkdir(exist_ok=True) 
allowed_extensions = ["mp4", "avi", "mkv", "mov"]

app = FastAPI()

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...), exercise: str = Form(None)):
    pose_estimator = PoseEstimator()
    if exercise not in config.EXERCISES:
        raise HTTPException(status_code=400, detail=f"Invalid exercise type.")
        
    run_id = tracking.start_run(exercise, config.EXERCISES[exercise]["up_threshold"], config.EXERCISES[exercise]["down_threshold"])
    file_location = upload_path / file.filename
    
    try:
        if not Path(file.filename.lower()).suffix.lstrip('.') in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type.")
            
        with open(file_location, "wb") as f:
            f.write(await file.read())
            
        response = pose_estimator.process_video(file_location, exercise)
        
        tracking.log_rep_metrics(response["total_reps"], response["avg_confidence"], response["min_confidence"])
        tracking.log_angle_metrics(response["max_angle"], response["min_angle"], response["average_up_angle"], response["average_down_angle"])
        
        return {
            "exercise": response["exercise"],
            "up_threshold": response["up_threshold"],
            "down_threshold": response["down_threshold"],
            "rep_count": response["total_reps"],
            "final_state": response["final_state"],
            "max_angle": response["max_angle"],
            "min_angle": response["min_angle"],
            "average_up_angle": response["average_up_angle"],
            "average_down_angle": response["average_down_angle"],
            "avg_confidence": response["avg_confidence"],
            "min_confidence": response["min_confidence"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        tracking.end_run()
        if file_location.exists():
            os.remove(file_location)

# Mount Gradio safely at the very bottom
app = gr.mount_gradio_app(app, demo, path="/")