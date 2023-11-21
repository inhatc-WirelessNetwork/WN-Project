import mediapipe as mp
import cv2
import math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        continue

    # 프레임을 RGB 형식으로 변환
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 관절 추출
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        # 머리의 위치 확인
        nose_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
        left_eye_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE].x
        right_eye_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE].x

        # 왼쪽 눈과 오른쪽 눈의 중점 계산
        eye_midpoint_x = (left_eye_x + right_eye_x) / 2

        # 머리가 왼쪽을 바라볼 때
        if nose_x < eye_midpoint_x:
            cv2.putText(frame, "head to left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # 귀(ear)와 어깨(shoulder) 관절의 인덱스를 얻기
            shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
        # 머리가 오른쪽을 바라볼 때
        elif nose_x > eye_midpoint_x:
            cv2.putText(frame, "head to right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]

        # 이미지에 관절 그리기
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 어깨를 기준으로 수직선 그리기
        x = int(shoulder_landmark.x * frame.shape[1])
        cv2.line(frame, (x, 0), (x, frame.shape[0]), (0, 255, 0), 2)

        # 귀와 어깨를 연결하는 선 그리기
        cv2.line(frame, (int(ear_landmark.x * frame.shape[1]), int(ear_landmark.y * frame.shape[0])),
                 (int(shoulder_landmark.x * frame.shape[1]), int(shoulder_landmark.y * frame.shape[0])), (0, 255, 0), 2)

        # 수평선 그리기
        cv2.line(frame, (0, int(shoulder_landmark.y * frame.shape[0])),
                 (frame.shape[1], int(shoulder_landmark.y * frame.shape[0])), (0, 0, 255), 2)

        # 수평선과 귀-어깨 선 사이의 각도 계산
        horizontal_line_angle_radians = math.atan2(shoulder_landmark.y - ear_landmark.y,
                                                   shoulder_landmark.x - ear_landmark.x)
        if nose_x < eye_midpoint_x:
            horizontal_line_angle_degrees = math.degrees(horizontal_line_angle_radians)
        elif nose_x > eye_midpoint_x:
            horizontal_line_angle_degrees = abs((math.degrees(horizontal_line_angle_radians)) - 180)

        # 각도를 화면에 표시
        cv2.putText(frame,
                    f" {horizontal_line_angle_degrees:.2f} degrees",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)

    cv2.imshow('Webcam Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()