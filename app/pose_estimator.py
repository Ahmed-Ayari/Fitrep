# YOLOv8 inference + keypoint extraction
from ultralytics import YOLO
import cv2
from angle_calculator import calculate_angle
import rep_counter 
import config

class PoseEstimator:
    def __init__(self, model_path="yolov8n-pose.pt"):
        self.model = YOLO(model_path)  # load the YOLOv8n-pose model
        self.rep_counter = rep_counter.RepCounter()  # initialize rep counter

    def process_video(self, video_path, exercise = "bicep_curl"):
        cap = cv2.VideoCapture(video_path)  # open the video file
        frame_index = 0  # initialize frame index

        if exercise:
            exercise_keypoints = config.EXERCISES[exercise]["keypoints"]
        else:
            exercise_keypoints = None

        while cap.isOpened():
            ret, frame = cap.read()  # read a frame from the video
            if not ret:
                break  # exit loop if no more frames are available

            results = self.model(frame, verbose=False)  # predict on the current frame
            
            keypoints_list = self.extract_keypoints(results)
            filtered_keypoints = self.confidence_filter(keypoints_list, exercise_keypoints)
            
            if filtered_keypoints:
                angle = calculate_angle(
                    filtered_keypoints[0][0],  # point a
                    filtered_keypoints[0][1], # point b
                    filtered_keypoints[0][2]  # point c
                )
                self.rep_counter.update(angle)

            frame_index += 1 
        cap.release()

        return {
            "total_reps": self.rep_counter.get_count(),
            "final_state": self.rep_counter.get_state()
        }

    def confidence_filter(self, keypoints_list, exercise_keypoints = None, confidence_threshold=0.5):
        filtered_keypoints = []
        for keypoints, confidences in keypoints_list:
            if exercise_keypoints:
                selected_keypoints = keypoints[list(exercise_keypoints)]
                selected_confidences = confidences[list(exercise_keypoints)]
            else:
                selected_keypoints = keypoints
                selected_confidences = confidences

            if all(conf > confidence_threshold for conf in selected_confidences):
                filtered_keypoints.append(selected_keypoints)
        
        return filtered_keypoints
        
    def extract_keypoints(self, results):
        keypoints_list = []
        for result in results:
            if result.keypoints is not None:
                keypoints = result.keypoints.xy[0].cpu().numpy()  
                confidences = result.keypoints.conf[0].cpu().numpy()
                
                keypoints_list.append((keypoints, confidences))
        
        return keypoints_list