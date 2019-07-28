import cv2


def default():
    default_cap = cv2.VideoCapture('default.mp4')
    interframe_wait_ms = 30

    while default_cap.isOpened():

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        default_cap = cv2.VideoCapture('default.mp4')
        while True:

            ret, frame = default_cap.read()
            if not ret:
                print("Reached end of video, exiting.")
                break

            cv2.imshow("window", frame)
            if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
                print("Exit requested.")
                break

    default_cap.release()
    # talk_cap.release()
    cv2.destroyAllWindows()

