import math

def cal_degree(direction_left, direction_right, shoulder_landmark, ear_landmark):
    # 수평선과 귀-어깨 선 사이의 각도 계산
    horizontal_line_angle_radians = math.atan2(shoulder_landmark.y - ear_landmark.y,
                                                    shoulder_landmark.x - ear_landmark.x)

    if direction_left:
        horizontal_line_angle_degrees = math.degrees(horizontal_line_angle_radians)
    elif direction_right:
        horizontal_line_angle_degrees = abs((math.degrees(horizontal_line_angle_radians)) - 180)
    return horizontal_line_angle_degrees