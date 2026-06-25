# YOLOv8 inference + keypoint extraction
from ultralytics import YOLO
import numpy as np
import cv2
from angle_calculator import calculate_angle
import rep_counter 
import config
from collections import deque

class PoseEstimator:
    def __init__(self, model_path="yolov8n-pose.pt"):
        self.model = YOLO(model_path)  # load the YOLOv8n-pose model

    def process_video(self, video_path, exercise):

        angle_buffer = deque(maxlen=5)

        angle_list = []
        filtered_keypoints = []
        confidence_list = []

        down_threshold = config.EXERCISES[exercise]["down_threshold"]
        up_threshold = config.EXERCISES[exercise]["up_threshold"]

        rep_count = rep_counter.RepCounter(
            down_threshold=down_threshold,
            up_threshold=up_threshold
        )
    
        cap = cv2.VideoCapture(video_path)  # open the video file
        frame_index = 0  # initialize frame index

        if exercise:
            both_keypoints = config.EXERCISES[exercise]["keypoints"]  # dict with left/right tuples
        else:
            both_keypoints = None

        while cap.isOpened():
            ret, frame = cap.read()  # read a frame from the video
            if not ret:
                break  # exit loop if no more frames are available

            results = self.model(frame, verbose=False)  # predict on the current frame
            
            keypoints_list = self.extract_keypoints(results)
            filtered_keypoints = self.confidence_filter(keypoints_list, both_keypoints)
            
            if filtered_keypoints:
                angle = calculate_angle(
                    filtered_keypoints[0][0][0],  # point a
                    filtered_keypoints[0][0][1], # point b
                    filtered_keypoints[0][0][2]  # point c
                )
                angle_buffer.append(angle)
                smoothed_angle = float(np.mean(angle_buffer))
                rep_count.update(smoothed_angle)
                angle_list.append(angle)
                confidence_list.extend([conf for _, conf, _ in filtered_keypoints])

            frame_index += 1 
        cap.release()

        angle_list.sort()

        max_angle = float(np.max(angle_list).item(), ) if angle_list else None
        min_angle = float(np.min(angle_list).item()) if angle_list else None
        average_up_angle = float(np.mean(angle_list[:len(angle_list)//2]).item()) if angle_list else None
        average_down_angle = float(np.mean(angle_list[len(angle_list)//2:]).item()) if angle_list else None

        avg_confidence = float(np.mean(confidence_list)) if confidence_list else None
        min_confidence = float(np.min(confidence_list)) if confidence_list else None

        return {
            "exercise": exercise,
            "up_threshold": up_threshold,
            "down_threshold": down_threshold,
            "total_reps": rep_count.get_count(),
            "final_state": rep_count.get_state(),
            "max_angle": max_angle,
            "min_angle": min_angle,
            "average_up_angle": average_up_angle,
            "average_down_angle": average_down_angle,
            "avg_confidence": avg_confidence,
            "min_confidence": min_confidence
        }

    def confidence_filter(self, keypoints_list, both_keypoints=None, confidence_threshold=0.5):
        filtered_keypoints = []
        for keypoints, confidences in keypoints_list:
            if both_keypoints:
                right_idx = list(both_keypoints["right_keypoints"])
                left_idx  = list(both_keypoints["left_keypoints"])
 
                right_confs = confidences[right_idx]
                left_confs  = confidences[left_idx]
 
                # pick the side with higher mean confidence
                if np.mean(right_confs) >= np.mean(left_confs):
                    selected_keypoints  = keypoints[right_idx]
                    selected_confidences = right_confs
                    chosen_side = "right"
                else:
                    selected_keypoints  = keypoints[left_idx]
                    selected_confidences = left_confs
                    chosen_side = "left"
            else:
                selected_keypoints   = keypoints
                selected_confidences = confidences
                chosen_side = None
 
            if all(conf > confidence_threshold for conf in selected_confidences):
                filtered_keypoints.append((selected_keypoints, selected_confidences, chosen_side))
 
        return filtered_keypoints
        
    def extract_keypoints(self, results):
        keypoints_list = []
        for result in results:
            if result.keypoints is not None:
                keypoints = result.keypoints.xy[0].cpu().numpy()  
                confidences = result.keypoints.conf[0].cpu().numpy()
                
                keypoints_list.append((keypoints, confidences))
        
        return keypoints_list