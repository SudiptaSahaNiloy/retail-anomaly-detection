from ultralytics import YOLO
import cv2

# Load pretrained YOLOv8 model (downloads automatically first run)
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture("footage/test2.mp4")

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, classes=[0])  # class 0 = person only

    annotated_frame = results[0].plot()

    # Resize to fit screen while keeping aspect ratio
    scale = 700 / annotated_frame.shape[0]  # target height 700px
    new_width = int(annotated_frame.shape[1] * scale)
    display_frame = cv2.resize(annotated_frame, (new_width, 700))
                               
    cv2.imshow("Detection Test", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()