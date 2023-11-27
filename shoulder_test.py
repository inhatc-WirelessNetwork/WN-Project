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

        # 어깨 좌표에 원 그리기
        cv2.circle(frame, (left_shoulder_x, left_shoulder_y), 5, (0, 255, 0), -1)
        cv2.circle(frame, (right_shoulder_x, right_shoulder_y), 5, (0, 255, 0), -1)

        # 어깨 간의 선 그리기
        cv2.line(frame, (left_shoulder_x, left_shoulder_y), (right_shoulder_x, right_shoulder_y), (0, 255, 0), 2)

        # 어깨 간의 기울기 계산
        slope = (right_shoulder_y - left_shoulder_y) / (right_shoulder_x - left_shoulder_x)
        #한쪽 팔거치대에 과하게 중심이 쏠렸을때 기울기가 0.1정도였음 (10번중에 7번이상)
        if slope < 0 :
            #-0.1의 기울기도 있어서 계산하기 쉽게 음수를 양수로 변환작업
            slope = slope * -1

        if slope >=0.10:
            #텔레그램 전송
            temp=0
            cv2.putText(frame, f"dangerous: {slope:.2f}", (250, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                

            

        # 결과 출력
        cv2.putText(frame, f"Slope: {slope:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # 얼굴 감지 결과를 화면에 출력
    cv2.imshow('Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # 'Esc' 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
