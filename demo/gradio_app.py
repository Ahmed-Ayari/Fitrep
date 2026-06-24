import gradio as gr
import requests
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from app import config
API_URL = os.getenv("API_URL")

exercice_list = config.EXERCISES.keys()

def analyze_video(video_path, exercise):
    with open(video_path, "rb") as video_file:
        files = {"file": (Path(video_path).name, video_file, "video.mp4")}
        data = {"exercise": exercise}

        try:
            response = requests.post(API_URL, files=files, data=data)
        except requests.exceptions.RequestException as e:
            raise gr.Error(f"Request failed: {e}")
    
    if response.status_code == 200:
        result = response.json()
        return result["rep_count"], result["avg_confidence"], result["min_confidence"]
    else:
        raise gr.Error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")

with gr.Blocks(css=".video-container { height: 500px !important; }") as demo:
    # inputs
    video_input = gr.Video(label="Upload Video")
    exercise_dropdown = gr.Dropdown(choices=list(exercice_list), label="Exercise")
    submit_btn = gr.Button("Analyze")
    
    # outputs
    rep_count = gr.Number(label="Reps")
    avg_confidence = gr.Number(label="Avg Confidence")
    min_confidence = gr.Number(label="Min Confidence")

    submit_btn.click(fn=analyze_video, inputs=[video_input, exercise_dropdown], outputs=[rep_count, avg_confidence, min_confidence])

demo.launch()