import cv2
from recognition import recognition, prepare
import send_email
import os


def main():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../database/source/red.jpg')
    filename = os.path.normpath(filename)
    red = cv2.imread(filename)
    filename = os.path.join(dirname, '../database/source/green.jpg')
    filename = os.path.normpath(filename)
    green = cv2.imread(filename)
    d = prepare.load_db()

    while True:
        img = green
        cv2.imshow('green light', img)
        cv2.waitKey(5000)
        cv2.destroyWindow('green light')

        img = red
        cv2.imshow('red light', img)
        cv2.waitKey(2000)
        cv2.destroyWindow('red light')

        video_capture = cv2.VideoCapture(0)
        ids = recognition.recognition(video_capture, d.copy())

        for i in range(0, len(d["ids"])):
            for id_person in ids:
                if id_person != -1:
                    if d["ids"][i] == id_person:
                        filename = os.path.join(dirname, '../database/recognized_faces/' + str(id_person) + '.jpeg')
                        filename = os.path.normpath(filename)
                        send_email.send(d["emails"][i], d["full_names"][i], filename)

        video_capture.release()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
