import os
import cv2
import face_recognition
import pickle
import requests

SUPABASE_URL = "https://vcucpobbtjizdsfjnzcs.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZjdWNwb2JidGppemRzZmpuemNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQwNzExNjQsImV4cCI6MjA2OTY0NzE2NH0.crFu0s5kqyBGdysZpgusK_XRuNnspvYlP-cQDjxv3CM"
STORAGE_BUCKET = "images"

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}"
}

folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    imgList.append(img)

    student_id = os.path.splitext(path)[0]
    studentIds.append(student_id)

    with open(os.path.join(folderPath, path), 'rb') as f:
        res = requests.post(
            f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{student_id}.png",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "apikey": API_KEY,
                "Content-Type": "image/png"
            },
            data=f.read()
        )
        print(f"Uploaded {path}: {res.status_code}")

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("File Saved")
