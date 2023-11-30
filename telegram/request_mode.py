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

stop_event = threading.Event()
stop_event.clear()
processing_thread = None
# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from turtle_neck.face_right_left_test2 import degreetest


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def test(update):
    last_message_time = 0
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
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

async def start_mod2(update):
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
            
async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        due = float(context.args[0])
        if due == 1:
            text = "거북목 모드 설정이 완료됐어요!"
            await update.effective_message.reply_text(text)

            stop_event.clear()

            loop = asyncio.get_event_loop()
            loop.create_task(test(update))

            return

        elif due == 2:
            text = "척추측만증 모드 설정이 완료됐어요!"
            await update.effective_message.reply_text(text)

            loop = asyncio.get_event_loop()
            loop.create_task(start_mod2(update))

            return
        else:
            await update.message.reply_text("1 또는 2를 입력해주세요 :) ")
            return

    except (IndexError, ValueError):
        await update.effective_message.reply_text("오류발생")

# /unset : 종료함수
async def unset_turtle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("unset_turtle")
    stop_event.set()
    await update.message.reply_text("거북목 프로그램이 종료 되었습니다.")
        
async def unset_scoliosis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("unset_scoliosis")
    stop_event.set()
    await update.message.reply_text("척추측만증 프로그램이 종료 되었습니다.")

def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    # 6339954049:AAEQDHDgbeklS3_Xeum0QwBIrPdjTulWg4M 인수 토큰
    # 6819441562:AAGTiWeoinUOE3W22M0L3R7u4CErKWSMzTw 찬호 토큰
    application = Application.builder().token("6339954049:AAEQDHDgbeklS3_Xeum0QwBIrPdjTulWg4M").build()

    print('main start')

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_mode))
    application.add_handler(CommandHandler("unset_turtle", unset_turtle))
    application.add_handler(CommandHandler("unset_scoliosis", unset_scoliosis))
    
    application.run_polling()

if __name__ == "__main__":
    main()