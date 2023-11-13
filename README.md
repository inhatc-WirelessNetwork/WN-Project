# Raspberry Pi를 활용한 거북목 증후군, 척추측만증 예방 프로젝트: <br> 너 자세가 왜그래? 🤷

#### 팀원: 박인수, 정상윤, 정찬호, 한소희, 한우빈

<br>

## ☑️ 프로젝트 목적 

현대 사회에서는 컴퓨터와 핸드폰과 같은 전자기기가 더 이상 떼어낼 수 없는 필수품으로 자리 잡았습니다. 이들 전자기기는 우리의 삶을 풍요롭게 만들어주지만, 그 반면에 척추와 관련된 질병을 유발할 수 있습니다. '척추 측만증', '거북목 증후군', '허리 디스크' 등이 그 예시입니다. VDT(비주얼 디스플레이 터미널) 증후군으로 인해 몸에 부담이 가면서도, 우리는 이러한 전자기기를 계속 사용하고 있습니다.

이러한 질환을 예방하고 사용자의 목, 등, 허리를 보호하기 위해서는 바른 자세 유지가 필수적입니다. 컴퓨터 및 휴대폰 사용자들에게 바른 자세 유지의 중요성을 알리며, 건강한 습관을 통해 척추와 관련된 문제를 예방하고 개선하는 것이 중요합니다.

<br>

## ☑️ 필요 물품
<li> Raspberry Pi </li>
<li> Arduino Uno </li>
<li> 라즈베리파이 카메라모듈 V2 </li>
<li> 라즈베리파이 카메라용 아크릴 거치대 케이스 </li>
<li> 압력센서 FSR 406 Solder Tabs </li>

<br>

## ☑️ 사용 파이썬 프레임워크&라이브러리
<li> Telegram APIs </li>
<li> MediaPipe </li>

<br>

## ☑️ "너 자세가 왜그래?"에는 무슨 기능이 있을까요? 🧐

<b> 1. 척추측만증 예방 모드와 거북목 증후군 예방 모드 중 선택하기 </b>

사용자가 원하는 모드를 선택할 수 있어요.

<hr>

<b> 2. 척추측만증 예방 모드 </b>

압력센서를 이용하여 척추측만증 유발 자세인 다리 꼬는 습관을 예방해요.

![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/90045a82-34c4-4ec5-bbf7-b2023da7a860)

<a href="https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11512962"> 출처: 2023년도 대한전기학회 하계학술대회 - 압력센서를 활용한 앉은 자세 별 압력 분포에 대한 기초연구
 </a>

 (1) 압력 센서 2개를 이용하여 의자에 왼쪽 둔근, 오른쪽 둔근 위치에 하나씩 부착합니다. 다리를 꼬는 자세를 하면, 다리를 올린 쪽의 압력 센서의 값이 상대적으로 낮아질 것입니다. 양쪽 압력 센서의 입력값의 차이가 200이상 될 경우, 라즈베리파이와 아두이노의 시리얼 통신으로 라즈베리파이에서 값을 읽어와 사용자에게 다리를 꼬는 자세를 했다는 메시지를 텔레그램을 통해 보내줍니다. 
 
 <br>
 
 추가로 양 발밑에도 압력센서를 부착하여 일정 비율 이상 압력이 발에 가해지게 되면, 자리에서 일어나는 것으로 판단하여 둔근 사이에 압력 차이가 생겨도 라즈베리파이에서 메시지를 보내지 않습니다.

 <hr>

 ![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/9fc51940-4b36-4f9a-bf57-6d6187387c1e)

<a href="http://www.good-spine.co.kr/?page_id=12606"> 출처: 허리편한병원 <a>

(2) 팔거치대를 한쪽 방향으로만 과도하게 장시간 이용했을 시 한쪽 어깨만 올라가게 되어 척추측만증의 발생 가능성이 높아집니다. 이러한 비정상적인 자세를 감지하였을시 사용자에게 텔레그램을 통해 알림을 보내줍니다.

![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/6b8c70ff-0b99-46e1-b263-0274254ec35f)

<hr>

<b> 3. 거북목 증후군 예방모드 </b>

<img width="613" alt="image" src="https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/3f94aab8-56aa-4825-a551-a49abb679369">

<a href="https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do"> 출처: 질병관리청 국가건강정보포털 </a>

거북목 상태는 외이도에서 내린 수직선이 어깨의 중심에서 내린 수직선보다 앞에 놓인 상태입니다. Python 기반으로 MediaPipe프레임워크를 활용하여 거북목 상태인지 아닌지를 구별합니다. 어깨를 중심으로 그어진 수평선과 귀-어깨를 잇는 선의 각도를 구해 거북목 여부를 판별합니다.

<카메라가 왼쪽에 있을 경우>

<img width="783" alt="image" src="https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/9d006c5e-8a57-429b-b239-529f566131a6">


<카메라가 오른쪽에 있을 경우>


<img width="515" alt="image" src="https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/20e56a4f-5894-489e-8a63-8047b9f5074e">

![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/15c63091-d678-415d-af0f-9f929c7dda44)

거북목 자세를 하면 각도가 70도 이하로 확연하게 낮아지는 것을 알 수 있습니다. 70도 이하로 내려가면 사용자에게 거북목 의심 메시지를 텔레그램을 통해 보내줍니다.


<카메라가 정면에 있을 경우>

<img width="435" alt="스크린샷 2023-11-13 오후 9 38 02" src="https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/6a29ad22-a127-438b-bce7-a36d9008718b">

정면을 바라보고 있을 경우에는 사용자의 어깨 중심과 턱 좌표의 거리를 재서 거리가 짧아지면 거북목으로 구분하여 사용자에게 거북목 의심 메시지를 텔레그램을 통해 보내줍니다. 

<hr>

## 🧑‍🤝‍🧑 역할 분담

<li> 한소희: 카메라가 측면에 있을 경우의 거북목 증후군 여부 판별 </li>
<li> 박인수: 카메라가 정면에 있을 경우의 거북목 증후군 여부 판별 </li>

<li> 한우빈: 어깨의 기울기로 척추측만증 유발 자세인 허리가 휘어진 자세 판별 </li>
<li> 정상윤, 정찬호: 압력센서를 이용하여 척추측만증 유발 자세인 다리 꼬는 자세 판별 </li>

<li> 정찬호: 텔레그램 API 연동 </li>



