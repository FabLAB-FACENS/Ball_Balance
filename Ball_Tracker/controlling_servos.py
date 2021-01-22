import cv2
import numpy as np
import imutils
from pyfirmata import ArduinoMega
from pyfirmata import SERVO

cap = cv2.VideoCapture(0)
board = ArduinoMega('COM20')        # comunicação com o arduino mega
board.digital[6].mode = SERVO       # habilitando a porta digital "6" da placa para o controle do servo
board.digital[7].mode = SERVO       # habilitando a porta digital "7" da placa para o controle do servo
pin6 = board.get_pin('d:6:o')       # definindo como saída digital
pin7 = board.get_pin('d:7:o')       # definindo como saída digital

x = 0                               # variável do eixo x da webcam (640 pixels)
y = 0                               # variável do eixo y da webcam (480 pixels)


def move_servo1(a):                 # função do funcionamento do servo 1
    board.digital[6].write(a)


def move_servo2(b):                 # função do funcionamento do servo 2
    board.digital[7].write(b)


while True:
    Xmotor = int(x/3.65)            # valor do ângulo de rotação do servo 1
    Ymotor = int(y/2.74)            # valor do ângulo de rotação do servo 2

    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_b = np.array([32, 35, 153])
    u_b = np.array([78, 255, 255])

    mask = cv2.inRange(hsv, l_b, u_b)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 2, (0, 0, 255), -1)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.putText(res, str(center), center, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, str(center), center, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    move_servo1(a=Xmotor)           # movimenta o servo 1 de acordo com a posição na tela
    move_servo2(b=Ymotor)           # movimenta o servo 2 de acordo com a posição na tela

    print('', Xmotor, Ymotor)       # mostra o valor do ângulo dos servos 1 e 2

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
