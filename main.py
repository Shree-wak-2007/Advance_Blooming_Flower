import cv2
from hand_tracking import HandTracker
from flower import Flower

# Open webcam
camera = cv2.VideoCapture(0)

tracker = HandTracker()
flower = Flower()

MAX_DISTANCE = 180  # Maximum finger distance for full growth

while True:

    success, frame = camera.read()

    if not success:
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Detect hand
    frame, hand = tracker.detect(frame)

    if hand is not None:

        # Finger distance
        distance = hand["distance"]

        # Convert distance to growth (0 to 1)
        growth = distance / MAX_DISTANCE
        growth = max(0, min(growth, 1))

        flower.growth = growth

        # Flower position follows fingers
        flower.x = hand["center_x"]
        flower.y = hand["center_y"] + 120

    else:
        # No hand detected
        flower.growth = 0

    # Draw flower
    flower.draw(frame)

    cv2.imshow("BloomSense AI", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
