from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pathlib import Path
import os
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root/"mlflow"))

import tracking
import config
#import schemas
from pose_estimator import PoseEstimator



upload_path = Path("uploads")
upload_path.mkdir(exist_ok=True) 

allowed_extensions = ["mp4", "avi", "mkv", "mov"]

app = FastAPI()

pose_estimator = PoseEstimator()

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...), exercise : str = Form(None)):
    run_id = tracking.start_run(exercise, config.EXERCISES[exercise]["up_threshold"], config.EXERCISES[exercise]["down_threshold"])
    try:
        if not Path(file.filename.lower()).suffix.lstrip('.') in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")
        
        if exercise and exercise not in config.EXERCISES:
            raise HTTPException(status_code=400, detail=f"Invalid exercise type. Supported exercises: {', '.join(config.EXERCISES.keys())}")

        file_location = upload_path / file.filename

        with open(file_location, "wb") as f:
            f.write(await file.read())
    
        response = pose_estimator.process_video(file_location, exercise)
        tracking.log_rep_metrics(response["total_reps"], response["avg_confidence"], response["min_confidence"])
        tracking.log_angle_metrics(response["max_angle"], response["min_angle"], response["average_up_angle"], response["average_down_angle"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        tracking.end_run()
        if file_location and os.path.exists(file_location):
            os.remove(file_location)    

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