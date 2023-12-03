# 거북목 증후군 모드


<p align="center">
  
  <img src="https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/26eec28a-0249-4f09-98e7-7e8807ca4347">
  
</p>

## 1. 미디어파이프 포즈 모델, 비디오 캡처 초기화
미디어파이프 포즈 모델 및 관련 모듈의 인스턴스를 생성합니다.

```python
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)
```

<br>

## 2. 웹캠이 열려 있다면, 루프에 진입
```python
while cap.isOpened():
```

### 2-1. 포즈 랜드마크 추출
미디어파이프 포즈 모델을 사용하여 포즈 랜드마크를 얻습니다.
```python
...
results = pose.process(frame_rgb)

    if results.pose_landmarks:
...
```

### 2-2. 머리 방향 검출
위에어 얻은 포즈 랜드마크를 이용하여 코, 왼쪽 눈, 오른쪽 눈의 위치를 기반으로 머리 방향을 판단합니다.
nose_x: 감지된 포즈에서 코를 나타내는 랜드마크의 x좌표
eye_midpoint_x: 왼쪽 눈과 오른쪽 눈 랜드마크의 x좌표 평균값
따라서 `nose_x < eye_midpoint_x`는 코가 인쪽 눈과 오른쪽 눈 중간지점의 왼쪽에 있는지를 평가하여 이 조건이 참이라면 머리의 방향이 왼쪽인 것입니다.

```python
nose_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
left_eye_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE].x
right_eye_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE].x

eye_midpoint_x = (left_eye_x + right_eye_x) / 2

# 머리 방향 왼쪽일 때
if nose_x < eye_midpoint_x:
...
```

### 2-3. 어깨 및 귀 랜드마크 추출 및 포즈 랜드마크 그리기
머리 방향을 기반으로 어깨와 귀 랜드마크를 얻습니다. `mp_drawing.draw_landmarks`를 사용하여 프레임에 포즈 랜드마크를 그립니다.

```python
...
# 머리 방향 왼쪽일 경우의 어깨, 귀 랜드마크
shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
```

### 2-4. 선 그리기
위에서 얻은 랜드마크를 이용하여 선들을 그립니다. 어깨 랜드마크에서 수직선을 그리고, 귀와 어깨를 연결하는 선과 어깨를 수평선을 그립니다.

### 2-5. 각도 계산
위에서 그린 수평선과 귀-어깨를 연결하는 선 사이의 각도를 계산합니다.

```python
 horizontal_line_angle_radians = math.atan2(shoulder_landmark.y - ear_landmark.y,
                                            shoulder_landmark.x - ear_landmark.x)

# 머리 방향 왼쪽인 경우
horizontal_line_angle_degrees = math.degrees(horizontal_line_angle_radians)

# 머리 방향 오른쪽인 경우
 horizontal_line_angle_degrees = abs((math.degrees(horizontal_line_angle_radians)) - 180)
```

### 2-6. 루프가 돌아가는 동안 'q' 키가 눌리면 루프 종료

```python
 if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

<br>

## 3. 웹캠 해체 및 창 닫기
프로그램을 종료합니다.

```python
cap.release()
cv2.destroyAllWindows()
```






