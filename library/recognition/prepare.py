import pandas as pd
import face_recognition
import os


def load_db():
    """
    This function loads the data base and returns a dictionary
    :return: the dictionary
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../../database/database.xlsx')
    filename = os.path.normpath(filename)
    database = pd.read_excel(filename, sheet_name='Лист1')
    database.head()

    known_face_encodings = []
    known_face_names = []
    emails = []
    full_names = []
    ids = []
    for i in range(0, database['path to photo'].size):
        filename = os.path.join(dirname, '../../database/faces/' + database['path to photo'][i])
        filename = os.path.normpath(filename)
        known_face_encodings.append(
            face_recognition.face_encodings(
                face_recognition.load_image_file(filename))[0])
        known_face_names.append(database['last name'][i])
        emails.append(database['email'][i])
        ids.append(database["id"][i])
        full_names.append(database["first name"][i])

    d = dict([("ids", ids), ("names", known_face_names), ("full_names", full_names), ("emails", emails),
              ("encodings", known_face_encodings)])

    return d
