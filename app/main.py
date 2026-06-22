from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import os

import schemas
from pose_estimator import PoseEstimator

upload_path = Path("uploads")
upload_path.mkdir(exist_ok=True) 

allowed_extensions = ["mp4", "avi", "mkv", "mov"]

app = FastAPI()

pose_estimator = PoseEstimator()

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...), exercise: schemas.Exercice = None):
    try:
        if not Path(file.filename.lower()).suffix.lstrip('.') in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")

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

    return schemas.ResponseModel(rep_count=response["total_reps"], final_state=response["final_state"])