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

## ☑️ 사용 소프트웨어
<li> Telegram APIs </li>
<li> MediaPie </li>

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

 <hr>

 ![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/9fc51940-4b36-4f9a-bf57-6d6187387c1e)

<a href="http://www.good-spine.co.kr/?page_id=12606"> 출처: 허리편한병원 <a>

(2) 양쪽 어깨의 기울기가 한쪽으로 올라가면 척추측만증의 질환이 생길 수 있는 가능성이 높아지게 됩니다. 따라서 한쪽 어깨가 지나치게 올라갔을 때 사용자에게 어깨가 올라갔다는 메시지를 텔레그램을 통해 보내줍니다.

![image](https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/6b8c70ff-0b99-46e1-b263-0274254ec35f)

<hr>

<b> 3. 거북목 증후군 예방모드 </b>

<img width="613" alt="image" src="https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/3f94aab8-56aa-4825-a551-a49abb679369">

<a href="https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do"> 출처: 질병관리청 국가건강정보포털 </a>

거북목 상태는 외이도에서 내린 수직선이 어깨의 중심에서 내린 수직선보다 앞에 놓인 상태입니다. Python 기반으로 MediaPipe프레임워크를 활용하여 거북목 상태인지 아닌지를 구별합니다. 어깨를 중심으로 그어진 수평선과 귀-어깨를 잇는 선의 각도를 구해 거북목 여부를 판별합니다.

<카메라가 왼쪽에 있을 경우>

<img width="783" alt="image" src="https://github.com/inhatc-WirelessNetwork/WN-Project/assets/90755590/9d006c5e-8a57-429b-b239-529f566131a6">


<카메라가 오른쪽에 있을 경우>

❌사진 필요

(왼쪽 오른쪽 둘 다 70도 이하면 거북목으로 인식)

<카메라가 정면에 있을 경우>

❌사진 필요

<br>




