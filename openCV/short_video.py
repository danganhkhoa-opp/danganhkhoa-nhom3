import cv2
import mediapipe as mp
import pyautogui
import time

# Cấu hình
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Biến kiểm soát hành động
last_action_time = 0
action_delay = 1.0  # Thời gian chờ giữa 2 lần lướt (giây)
ready_for_next = True # Trạng thái sẵn sàng cho lần lướt tiếp theo

while True:
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1)
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    current_time = time.time()

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Lấy tọa độ đầu ngón trỏ (8) và cổ tay (0)
            index_tip = handLms.landmark[8]
            wrist = handLms.landmark[0]

            # VẼ ĐỂ THEO DÕI
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # LOGIC ĐIỀU KHIỂN BẰNG CỬ CHỈ
            # 1. Nếu giơ ngón tay lên cao hẳn so với cổ tay -> NEXT
            if index_tip.y < wrist.y - 0.25:
                if current_time - last_action_time > action_delay and ready_for_next:
                    print(">>> ĐANG LƯỚT XUỐNG (NEXT)")
                    pyautogui.press('down') # Facebook Shorts dùng phím xuống để chuyển
                    last_action_time = current_time
                    ready_for_next = False # Khóa lại để tránh lướt liên tục

            # 2. Đưa tay về vị trí trung tâm để reset trạng thái sẵn sàng
            elif wrist.y - 0.1 < index_tip.y < wrist.y + 0.1:
                ready_for_next = True

            # 3. Nếu hạ tay xuống thấp -> PREVIOUS
            elif index_tip.y > wrist.y + 0.2:
                if current_time - last_action_time > action_delay and ready_for_next:
                    print("<<< ĐANG LƯỚT LÊN (BACK)")
                    pyautogui.press('up')
                    last_action_time = current_time
                    ready_for_next = False

    # Hiển thị trạng thái lên màn hình camera
    status = "READY" if ready_for_next else "WAITING..."
    cv2.putText(img, f"STATUS: {status}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Facebook Shorts Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()