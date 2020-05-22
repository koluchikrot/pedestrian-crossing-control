import pandas as pd
import face_recognition


def load_db():
    """
    This function loads the data base and returns a dictionary
    :return: the dictionary
    """
    database = pd.read_excel('../database/database.xlsx', sheet_name='Лист1')
    database.head()

    known_face_encodings = []
    known_face_names = []
    emails = []
    full_names = []
    ids = []
    for i in range(0, database['path to photo'].size):
        known_face_encodings.append(
            face_recognition.face_encodings(
                face_recognition.load_image_file('../database/faces/' + database['path to photo'][i]))[0])
        known_face_names.append(database['last name'][i])
        emails.append(database['email'][i])
        ids.append(database["id"][i])
        full_names.append(database["first name"][i])

    d = dict([("ids", ids), ("names", known_face_names), ("full_names", full_names), ("emails", emails),
              ("encodings", known_face_encodings)])

    return d
