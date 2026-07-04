import cv2
import mediapipe as mp
import math


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        hand_data = None

        if results.multi_hand_landmarks:

            hand_landmarks = results.multi_hand_landmarks[0]

            self.drawer.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            # Thumb tip
            thumb = hand_landmarks.landmark[4]

            # Index finger tip
            index = hand_landmarks.landmark[8]

            thumb_x = int(thumb.x * w)
            thumb_y = int(thumb.y * h)

            index_x = int(index.x * w)
            index_y = int(index.y * h)

            # Distance between fingers
            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )

            # Midpoint between fingers
            center_x = (thumb_x + index_x) // 2
            center_y = (thumb_y + index_y) // 2

            # Draw helper points
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 0, 255), -1)
            cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), -1)

            cv2.line(
                frame,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (0, 255, 0),
                3
            )

            cv2.circle(frame, (center_x, center_y), 6, (0, 255, 255), -1)

            cv2.putText(
                frame,
                f"Distance : {int(distance)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            hand_data = {
                "thumb_x": thumb_x,
                "thumb_y": thumb_y,
                "index_x": index_x,
                "index_y": index_y,
                "center_x": center_x,
                "center_y": center_y,
                "distance": distance
            }

        return frame, hand_data
