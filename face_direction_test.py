import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
pose = mp_pose.Pose()

def right_left(direction: str):
    if direction == 'left':
        cv2.putText(frame, 'LEFT', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
        horizontal_line_angle_degrees = math.degrees(create_horizontal_line(shoulder_landmark, ear_landmark))

    elif direction == 'right':
        cv2.putText(frame, 'RIGHT', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR]
        horizontal_line_angle_degrees = abs(
            (math.degrees(create_horizontal_line(shoulder_landmark, ear_landmark))) - 180)

    # 어깨를 기준으로 수직선 그리기
    x = int(shoulder_landmark.x * frame.shape[1])
    cv2.line(frame, (x, 0), (x, frame.shape[0]), (0, 255, 0), 2)

    # 귀와 어깨를 연결하는 선 그리기
    cv2.line(frame, (int(ear_landmark.x * frame.shape[1]), int(ear_landmark.y * frame.shape[0])),
             (int(shoulder_landmark.x * frame.shape[1]), int(shoulder_landmark.y * frame.shape[0])),
             (0, 255, 0), 2)

    # 수평선 그리기
    cv2.line(frame, (0, int(shoulder_landmark.y * frame.shape[0])),
             (frame.shape[1], int(shoulder_landmark.y * frame.shape[0])), (0, 0, 255), 2)

    cv2.putText(frame,
                f" {horizontal_line_angle_degrees:.2f} degrees",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)

def create_horizontal_line(shoulder_landmark, ear_landmark):
    horizontal_line_angle_radians = math.atan2(shoulder_landmark.y - ear_landmark.y,
                                               shoulder_landmark.x - ear_landmark.x)
    return horizontal_line_angle_radians

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("웹캠에서 프레임을 읽을 수 없습니다.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # 왼쪽 끝점 (가장 왼쪽 얼굴 랜드마크)
            leftmost_point = face_landmarks.landmark[0]
            leftmost_x = int(leftmost_point.x * frame.shape[1])

            # 오른쪽 끝점 (가장 오른쪽 얼굴 랜드마크)
            rightmost_point = face_landmarks.landmark[16]
            rightmost_x = int(rightmost_point.x * frame.shape[1])

            results = pose.process(frame)

            # 얼굴이 정면, 왼쪽 측면, 오른쪽 측면인지 구별
            if leftmost_x > frame.shape[1] * 0.6:
                if results.pose_landmarks:
                    right_left("right")

            elif rightmost_x < frame.shape[1] * 0.4:
                if results.pose_landmarks:
                    right_left("left")

            else:
                cv2.putText(frame, "FRONT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Face Direction Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
