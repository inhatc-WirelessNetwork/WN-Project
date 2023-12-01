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
from turtle_neck.calculate_degree import cal_degree
import telegram_token

stop_event = threading.Event()
stop_event.clear()
processing_thread = None
# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def turtle_mode(update):
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

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
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
            
            degree = cal_degree(direction_left, direction_right, shoulder_landmark, ear_landmark)

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

async def scoliosis_mode(update):
    seri = serial.Serial('COM4', baudrate=9600, timeout=None)
    while not stop_event.is_set():
        time.sleep(1)
        if seri.in_waiting != 0:
            val1 = int(seri.readline().decode())
            val2 = int(seri.readline().decode())

            print("다리 측정", val1)
            print("허리 측정", val2)

            if val1 >= 400:
                text = "다리 꼬지 마세요"
                await update.effective_message.reply_text(text)

            if val2 >= 800:
                text = "허리 피세요"
                await update.effective_message.reply_text(text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("모드를 선택해 주세요 :)\n 1. 거북목 모드 \n2. 척추측만증 모드 \n 예시: /set 1")

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        due = float(context.args[0])
        if due == 1:
            text = "거북목 모드 설정이 완료됐어요! 사용을 중단하고 싶다면 /unset_turtle 을 입력하세요."
            await update.effective_message.reply_text(text)

            stop_event.clear()

            loop = asyncio.get_event_loop()
            loop.create_task(turtle_mode(update))

            return

        elif due == 2:
            text = "척추측만증 모드 설정이 완료됐어요! 사용을 중단하고 싶다면 /unset_scoliosis 을 입력하세요."
            await update.effective_message.reply_text(text)

            loop = asyncio.get_event_loop()
            loop.create_task(scoliosis_mode(update))

            return
        else:
            await update.message.reply_text("1 또는 2를 입력해주세요 :) ")
            return

    except (IndexError, ValueError):
        print('Index ERROR:', IndexError)
        print('Value ERROR: ', ValueError)
        await update.effective_message.reply_text("오류가 발생하였습니다. 잠시후에 이용해 주세요.")

# /unset : 종료함수
async def unset_turtle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("unset_turtle")
    stop_event.set()
    await update.message.reply_text("거북목 프로그램이 종료되었습니다.")
        
async def unset_scoliosis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("unset_scoliosis")
    stop_event.set()
    await update.message.reply_text("척추측만증 프로그램이 종료되었습니다.")

def main() -> None:
    token = telegram_token.insoo_token
    # token = telegram_token.chanho_token
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_mode))
    application.add_handler(CommandHandler("unset_turtle", unset_turtle))
    application.add_handler(CommandHandler("unset_scoliosis", unset_scoliosis))
    
    application.run_polling()

if __name__ == "__main__":
    main()