# 🎉 Telegram API Process

### 1️⃣ 기본 사용법     
```
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 봇 토큰을 설정합니다.
TOKEN = 'your_bot_token'
updater = Updater(token=TOKEN, use_context=True)

# /start 명령어 핸들러 함수
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('안녕하세요! 봇이 시작되었습니다.')

# /help 명령어 핸들러 함수
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('도움말을 표시합니다.')

# 명령어 핸들러를 봇에 추가합니다.
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help_command))

# 봇을 시작합니다.
updater.start_polling()

# 봇이 계속 실행되도록 유지합니다.
updater.idle()

```
|Method|기능|
|--|--|
|Updater  |텔레그램 봇과 텔레그램 서버 간의 통신을 관리하고 업데이트를 수신|
|Update |텔레그램에서 오는 모든 업데이트(메시지, 채팅 상태 변경, 새로운 멤버 등)를 수신|
|CommandHandler |텔레그램에서 오는 모든 업데이트(메시지, 채팅 상태 변경, 새로운 멤버 등)를 수신|
|CallbackContext |이벤트 핸들러 함수에 CallbackContext를 사용하여 콜백 데이터를 전달<br>비동기 작업을 수행 후 작업이 완료시 작업의 결과를 통해 추가적인 동작을 수행|
|dispatcher| EventListener 등록 / 호출하여 적절한 응답을 생성|

### 2️⃣ 비동기 프로그래밍
> 파이썬에서 텔레그램 API를 사용하여 텔레그램에 메시지를 보낼 때 비동기로 작성해야 한다
#### 🤔 Why? 
* 응답 대기 시간 해소
  + 텔레그램 API 호출은 외부 서버와의 통신을 필요로 하며, 텔레그램 API는 메시지를 송수신하고 알람만 보내는 등   
    네트워크 요청이 잦습니다.   
  + 비동기 방식을 사용하면 네트워크 요청을 기다리는 동안 다른 작업을 수행할 수 있어  
    프로그램이 더 효율적으로 동작할 수 있습니다.
* 다중 요청 관리:
  + 비동기 작업을 사용하면 여러 개의 API 호출을 동시에 수행할 수 있습니다.
  + 동기적인 방식에서는 한 번에 하나의 API 호출만 처리할 수 있어 여러 요청을 동시에   
    처리하기 위해서는 별도의 쓰레드나 프로세스를 사용해야 합니다.

### 3️⃣ Code   
```
# use asyncio ver
import logging
from telegram import Update
import mediapipe as mp
from telegram.ext import Application, CommandHandler, ContextTypes
import sys, os
import asyncio
import cv2
import threading
import time
import serial

# 스레드 간에 통신을 위한 이벤트 객체를 생성합니다.
# 스레드 중지 여부를 위한 flag
stop_event = threading.Event()

# 스레드 초기화 -> 쓰레드가 중지되지 않음을 의미
stop_event.clear()

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 거북목 계산 함수 import
from turtle_neck.face_right_left_test import degreetest

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start_tutle(update):
    last_message_time = 0
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    
    #mp_drawing_styles = mp.solutions.drawing_styles

    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(1)
    while cap.isOpened() and not stop_event.is_set():
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

            direction_left = nose_x < eye_midpoint_x
            direction_right = nose_x > eye_midpoint_x

            # 머리가 왼쪽을 바라볼 때
            if direction_left:
                cv2.putText(frame, "head to left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # 귀(ear)와 어깨(shoulder) 관절의 인덱스를 얻기
                shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                ear_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR]
            # 머리가 오른쪽을 바라볼 때
            elif direction_right:
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
            
            degree = degreetest(direction_left, direction_right, shoulder_landmark, ear_landmark)

            # 각도를 화면에 표시
            cv2.putText(frame,
                        f" {degree:.2f} degrees",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)

            if degree < 70 and time.time() - last_message_time >= 5:
                await update.effective_message.reply_text('거북목 주의')
                last_message_time = time.time()

            else:
                print('정상')


        cv2.imshow('Webcam Pose Estimation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
            
# /start 메시지 전송
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("모드를 선택해 주세요 :)\n 1. 거북목 모드 \n2. 척추측만증 모드")

# 척추 측만증 모도 실행
async def start_scoliosis(update):
    seri = serial.Serial('COM4', baudrate=9600, timeout=None)
    while not stop_event.is_set():
        time.sleep(1)
        if seri.in_waiting != 0:
            val1 = int(seri.readline().decode())
            val2 = int(seri.readline().decode())

            print("Value 1:", val1)
            print("Value 2:", val2)

            if val1 >= 400:
                text = "다리 꼬지 마세요"
                await update.effective_message.reply_text(text)

            if val2 >= 800:
                text = "허리 피세요"
                await update.effective_message.reply_text(text)

# 거북목 / 척추측만증 모드 선택            
async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        due = float(context.args[0])
        if due == 1:
            text = "거북목 모드 설정이 완료됐어요!"
            await update.effective_message.reply_text(text)

            stop_event.clear()

            loop = asyncio.get_event_loop()
            loop.create_task(start_tutle(update))

            return

        elif due == 2:
            text = "척추측만증 모드 설정이 완료됐어요!"
            await update.effective_message.reply_text(text)

            loop = asyncio.get_event_loop()
            loop.create_task(start_scoliosis(update))

            return
        else:
            await update.message.reply_text("1 또는 2를 입력해주세요 :) ")
            return

    except (IndexError, ValueError):
        await update.effective_message.reply_text("오류발생")

# 거북목 모드 종료함수
async def unset_turtle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("unset_turtle")
    stop_event.set()
    await update.message.reply_text("거북목 프로그램이 종료 되었습니다.")

# 척추 층만증 모드 종료함수        
async def unset_scoliosis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("unset_scoliosis")
    stop_event.set()
    await update.message.reply_text("척추측만증 프로그램이 종료 되었습니다.")

def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    # 6339954049:AAEQDHDgbeklS3_Xeum0QwBIrPdjTulWg4M 인수 토큰
    # 6819441562:AAGTiWeoinUOE3W22M0L3R7u4CErKWSMzTw 찬호 토큰
    application = Application.builder().token("6819441562:AAGTiWeoinUOE3W22M0L3R7u4CErKWSMzTw").build()

    print('main start')

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_mode))
    application.add_handler(CommandHandler("unset_turtle", unset_turtle))
    application.add_handler(CommandHandler("unset_scoliosis", unset_scoliosis))
    
    application.run_polling()

if __name__ == "__main__":
    main()
```

### 4️⃣ Thread Process
![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/84930748/69d8c563-dc10-4734-8562-53d19e0f73dc)

#### ✔ 초기 프로세스 구성
* 사용자가 ```/start``` 명령어를 호출하면 사용자에게 mode를 선택을 요청하고      
 ```/set 1``` 또는 ```/set 2``` 명령어를 통해 거복목과 척추측만증 모드 중 선택을 하게 됩니다.   
 모드 선택 후, 프로그램이 실행되며 ```/unset``` 명령어를 입력 하면 프로그램이 종료됩니다.

* 그러나 이렇게 구현 시 ```/unset```을 전달해도 **프로그램이 종료**되지 않습니다.

* 그 이유인 즉, ```[start_tutle, start_scoliosis]``` 함수를 메인 메인 스레드에서 진행한다면,   
  해당 작업이 끝날 때까지 다음 명령을 처리하지 못하게(Bloking) 됩니다. 

* 즉, ```[start_tutle, start_scoliosis]``` 함수가 동작하는 동안 메인 스레드는 다른 작업을   
  수행하지 못하게 되므로, 텔레그램 봇이 다른 명령을 받거나 사용자와 상호작용하는 일이 불가능해집니다.

#### ✔ 프로세스 개선

![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/84930748/47dcc10a-eaab-4819-81fa-b54f7485082b)

* ```[start_tutle, start_scoliosis]```을 동작할 스레드를 별도로 만들어 
  메인 스레드와 병렬로 동작하게 구성하면 ```/unset``` 으로 종료가 가능해집니다.

