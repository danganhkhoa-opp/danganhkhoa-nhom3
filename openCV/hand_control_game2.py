import cv2
import mediapipe as mp
import pyautogui
import time

# CẤU HÌNH AN TOÀN QUAN TRỌNG
pyautogui.FAILSAFE = False # Tắt tự ngắt khi chuột vào góc
pyautogui.PAUSE = 0

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Camera
cap = cv2.VideoCapture(0)
cam_w, cam_h = 640, 480
cap.set(3, cam_w); cap.set(4, cam_h)
screen_w, screen_h = pyautogui.size()

is_slashing = False

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Lấy vị trí đầu ngón trỏ (số 8)
            tip = handLms.landmark[8]
            
            # Map tọa độ có vùng đệm (Margin) để di chuyển mượt hơn
            margin = 80
            x = int(tip.x * cam_w)
            y = int(tip.y * cam_h)
            
            # Nội suy tọa độ màn hình
            # screen_x = (x - margin) * screen_w / (cam_w - 2 * margin)
            # screen_y = (y - margin) * screen_h / (cam_h - 2 * margin)
            
            # Giới hạn tọa độ trong phạm vi an toàn (tránh sát mép 0)
            screen_x = max(10, min(screen_w - 10, int(tip.x * screen_w)))
            screen_y = max(10, min(screen_h - 10, int(tip.y * screen_h)))

            # Thực hiện chém
            if not is_slashing:
                pyautogui.mouseDown(screen_x, screen_y, button='left')
                is_slashing = True
            else:
                pyautogui.moveTo(screen_x, screen_y)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
    else:
        if is_slashing:
            pyautogui.mouseUp()
            is_slashing = False

    cv2.putText(img, "CONTROLLER ACTIVE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Hand Control Tracker", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
pyautogui.mouseUp()