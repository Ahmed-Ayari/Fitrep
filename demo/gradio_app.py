import gradio as gr
import requests
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Use a relative URL path so it works perfectly locally AND on Hugging Face Spaces
API_URL = "/analyze" 

# Pass choices as a list directly or pass them dynamically later to avoid importing app here
def analyze_video(video_path, exercise):
    if not video_path:
        raise gr.Error("Please upload a video first.")
        
    # On Hugging Face, we resolve the local routing or absolute URL dynamically
    # A cleaner approach since we are on the same server is to point to the server route:
    with open(video_path, "rb") as video_file:
        files = {"file": (Path(video_path).name, video_file, "video.mp4")}
        data = {"exercise": exercise}
        try:
            # Using a relative endpoint requires a full URL context from requests, 
            # so we target localhost port 7860 safely ONLY at runtime execution block
            response = requests.post("http://127.0.0.1:7860/analyze", files=files, data=data)
        except requests.exceptions.RequestException as e:
            raise gr.Error(f"Request failed: {e}")
        
        if response.status_code == 200:
            result = response.json()
            return result["rep_count"], result["avg_confidence"], result["min_confidence"]
        else:
            raise gr.Error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")

with gr.Blocks() as demo:
    video_input = gr.Video(label="Upload Video", height=500)
    # We can populate this dynamically or hardcode standard options to prevent importing config
    exercise_dropdown = gr.Dropdown(choices=["squat", "bicep_curl"], label="Exercise") 
    submit_btn = gr.Button("Analyze")
    
    rep_count = gr.Number(label="Reps")
    avg_confidence = gr.Number(label="Avg Confidence")
    min_confidence = gr.Number(label="Min Confidence")
    
    submit_btn.click(fn=analyze_video, inputs=[video_input, exercise_dropdown], outputs=[rep_count, avg_confidence, min_confidence])