from ultralytics import YOLO
import cv2

def get_display_frame(frame, display_height=700):
    scale = display_height / frame.shape[0]
    new_width = int(frame.shape[1] * scale)
    display_frame = cv2.resize(frame, (new_width, display_height))
    return display_frame

model = YOLO("yolov8n-pose.pt")  # downloads automatically

cap = cv2.VideoCapture("footage/test2.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break

    display_frame = get_display_frame(frame)
    results = model(display_frame)
    annotated_frame = results[0].plot()  # draws skeleton keypoints

    for person_idx, keypoints in enumerate(results[0].keypoints.xy):
        print(f"\n--- Person {person_idx} ---")
        
        keypoint_names = [
            "nose", "left_eye", "right_eye", "left_ear", "right_ear",
            "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
            "left_wrist", "right_wrist", "left_hip", "right_hip",
            "left_knee", "right_knee", "left_ankle", "right_ankle"
        ]
    
        for name, coords in zip(keypoint_names, keypoints):
            print(f"  {name}: x={coords[0]:.1f}, y={coords[1]:.1f}")

    cv2.imshow("Pose Test", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()