from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pathlib import Path
import os

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
    try:
        if not Path(file.filename.lower()).suffix.lstrip('.') in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")
        
        if exercise and exercise not in config.EXERCISES:
            raise HTTPException(status_code=400, detail=f"Invalid exercise type. Supported exercises: {', '.join(config.EXERCISES.keys())}")

        file_location = upload_path / file.filename

        with open(file_location, "wb") as f:
            f.write(await file.read())

        response = pose_estimator.process_video(file_location, exercise)
    except Exception:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the uploaded file
        if file_location and os.path.exists(file_location):
            os.remove(file_location)    

    return {"rep_count": response["total_reps"], "final_state": response["final_state"]}