import cv2
from deepface import DeepFace

# Initialize the video capture object for webcam (use 0 for default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Press 'q' to exit.")

try:
    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Analyze the current frame with DeepFace
        try:
            results = DeepFace.analyze(img_path=frame, actions=['age', 'gender', 'emotion', 'race'], enforce_detection=False)
            # Access the first (and only) result
            result = results[0]

            # Display the analysis results on the frame
            text = f"Age: {result['age']}, Gender: {result['gender']}, Emotion: {result['dominant_emotion']}, Race: {result['dominant_race']}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        except Exception as e:
            print("Analysis error:", str(e))

        # Display the video frame
        cv2.imshow("Real-Time Analysis", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting the program.")

# Release the webcam and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
