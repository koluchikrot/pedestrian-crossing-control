"""
This file is responsible for processing video and face capture
We use the library face_recognition which was originally developed by ageitgey
"""
import face_recognition
import cv2
import numpy as np
import transliterate
from _datetime import datetime
import os


def recognition(video_capture, d):
    """
    This function recognizes people on video
    :param video_capture: access to the camera
    :param d: dictionary of data base
    :return: names of detected people
    """
    face_locations = []
    face_ids = []
    process_this_frame = True
    known_face_encodings = d["encodings"]
    ids = d["ids"]
    dirname = os.path.dirname(__file__)

    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < 10:
        _, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_ids = []
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                id_person = -1

                if True in matches:
                    first_match_index = matches.index(True)
                    id_person = ids[first_match_index]

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    id_person = ids[best_match_index]

                face_ids = set(face_ids)
                k = 0
                for n in face_ids:
                    if n == id_person:
                        k = k + 1

                if k == 0:
                    filename = os.path.join(dirname, '../../database/recognized_faces/' + str(id_person) + '.jpeg')
                    filename = os.path.normpath(filename)
                    cv2.imwrite(filename, frame)
                face_ids.add(id_person)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), id_person in zip(face_locations, face_ids):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            name = "Unknown"
            if id_person != -1:
                for i in range(0, len(ids)):
                    if ids[i] == id_person:
                        name = d["full_names"][i]  # d["names"][i]

                name = transliterate.translit(name, reversed=True)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)
        # early exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    return set(face_ids)
