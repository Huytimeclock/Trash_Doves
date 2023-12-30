import cv2
import mediapipe as mp

class FaceDetector:
    def __init__(self, min_face_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face.FaceMesh(
            min_detection_confidence=min_face_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def detect_face(self, image):
        results = self.face_mesh.process(image)
        return results

    def draw_face_landmarks(self, image, results):
        left_eye_landmark, right_eye_landmark = None, None  # Initialize landmarks as None

        if results.multi_face_landmarks:
            # Assuming the landmark IDs for left and right eyes are provided in the documentation
            left_eye_id = 159

            right_eye_id= 386

            for face_landmarks in results.multi_face_landmarks:
                # Extract center of left and right eye landmarks using specific landmark IDs
                left_eye_landmark = (
                    int(face_landmarks.landmark[left_eye_id].x * image.shape[1]),
                    int(face_landmarks.landmark[left_eye_id].y * image.shape[0]),
                )
                right_eye_landmark = (
                    int(face_landmarks.landmark[right_eye_id].x * image.shape[1]),
                    int(face_landmarks.landmark[right_eye_id].y * image.shape[0]),
                )

                # Draw circles or lines if needed
                # self.mp_drawing.draw_landmarks(image, face_landmarks)

        return left_eye_landmark, right_eye_landmark  # Return the landmarks
