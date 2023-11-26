import cv2
import mediapipe as mp

# MediaPipe Pose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 비디오 캡처 초기화
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 흑백 이미지를 사용하여 Pose estimation 적용
    results = pose.process(frame)

    # 결과 처리 및 시각화
    if results.pose_landmarks:
        # 어깨 랜드마크 추출
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # 좌표를 화면에 표시
        h, w, _ = frame.shape
        left_shoulder_x, left_shoulder_y = int(left_shoulder.x * w), int(left_shoulder.y * h)
        right_shoulder_x, right_shoulder_y = int(right_shoulder.x * w), int(right_shoulder.y * h)

        # 어깨 좌표에 점 그리기
        cv2.circle(frame, (left_shoulder_x, left_shoulder_y), 5, (0, 255, 0), -1)
        cv2.circle(frame, (right_shoulder_x, right_shoulder_y), 5, (0, 255, 0), -1)

    cv2.imshow('Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # 'Esc' 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
