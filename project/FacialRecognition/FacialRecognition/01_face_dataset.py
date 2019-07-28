import cv2

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")

font = cv2.QT_FONT_NORMAL

count = 0

WHITE = (255, 255, 255)

positions = {
    "init": "Place your face close and straight",
    "right": "Turn your face right",
    "left": "Turn your face left",
}

current_position = "init"

while True:
    ret, img = cam.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.ellipse(img, (x + w // 2, y + h // 2), (w - 50, h - 30), 0, 0, 360, WHITE, 1)
        count += 1

        cv2.imwrite(f"dataset/Users/{str(face_id)}_{str(count)}.jpg", gray[y:y + h, x:x + w])

        cv2.putText(img, f"{positions[current_position]}", (100, 50), font, 1, WHITE, 1)
        cv2.imshow('image', img)

    k = cv2.waitKey(100)
    if k == 27:
        break
    elif count >= 45:
        break
    elif count > 30:
        current_position = "left"
    else:
        current_position = "right"

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
