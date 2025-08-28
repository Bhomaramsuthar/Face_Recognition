import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import requests
from datetime import datetime

# ------------------- Supabase Config -------------------
SUPABASE_URL = "https://vcucpobbtjizdsfjnzcs.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZjdWNwb2JidGppemRzZmpuemNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQwNzExNjQsImV4cCI6MjA2OTY0NzE2NH0.crFu0s5kqyBGdysZpgusK_XRuNnspvYlP-cQDjxv3CM"
STORAGE_BUCKET = "images"

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}"
}

# ------------------- Camera Setup -------------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# ------------------- Load Graphics -------------------
imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/Modes'
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in os.listdir(folderModePath)]

# ------------------- Load Encoded Faces -------------------
with open('EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)

# ------------------- Variables -------------------
modeType = 0
counter = 0
id = -1
imgStudent = None
studentInfo = {}

# ------------------- Main Loop -------------------
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Webcam feed on background
    imgBackground[162:162 + 480, 55:55 + 640] = img
    # Mode panel
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                id = studentIds[matchIndex]
                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                if counter == 0:
                    modeType = 1
                    counter = 1

                    # ------------------- Fetch Student Info -------------------
                    response = requests.get(
                        f"{SUPABASE_URL}/rest/v1/students?id=eq.{id}",
                        headers={**headers, "Accept": "application/json"}
                    )
                    if response.status_code == 200 and response.json():
                        studentInfo = response.json()[0]
                    else:
                        print(f"[ERROR] Student with ID {id} not found")
                        studentInfo = {}
                        continue

                    # ------------------- Fetch Image -------------------
                    image_url = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{id}.png"
                    image_response = requests.get(image_url)

                    if image_response.status_code == 200:
                        imgArr = np.asarray(bytearray(image_response.content), dtype=np.uint8)
                        imgStudent = cv2.imdecode(imgArr, cv2.IMREAD_COLOR)
                        if imgStudent is not None:
                            imgStudent = cv2.resize(imgStudent, (216, 216))
                    else:
                        print(f"[ERROR] Could not load student image for ID {id}")
                        imgStudent = np.full((216, 216, 3), 128, dtype=np.uint8)  # gray placeholder

                    # ------------------- Update Attendance -------------------
                    try:
                        last_time = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        last_time = datetime(2000, 1, 1)

                    secondsElapsed = (datetime.now() - last_time).total_seconds()

                    if secondsElapsed > 30:
                        updated_data = {
                            "total_attendance": studentInfo['total_attendance'] + 1,
                            "last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                        update_res = requests.patch(
                            f"{SUPABASE_URL}/rest/v1/students?id=eq.{id}",
                            headers={**headers, "Content-Type": "application/json"},
                            json=updated_data
                        )

                        if update_res.status_code not in [200, 204]:
                            print(f"[ERROR] Failed to update attendance for ID {id}")

    # ------------------- Display Student Info -------------------
    if counter != 0:
        if 10 < counter < 20:
            modeType = 2

        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if counter <= 10 and studentInfo:
            cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(id), (1006, 493),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

            (w, _), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = (414 - w) // 2
            cv2.putText(imgBackground, studentInfo['name'], (808 + offset, 445),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

            # ------------------- Display Student Image -------------------
            if imgStudent is not None:
                imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

        counter += 1
        if counter >= 20:
            counter = 0
            modeType = 0
            studentInfo = {}
            imgStudent = None
    else:
        modeType = 0
        counter = 0

    # ------------------- Show Window -------------------
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
