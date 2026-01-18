# 📸 Face Recognition Attendance System (Cloud-Integrated)

![Python](https://img.shields.io/badge/Language-Python-blue) ![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green) ![Supabase](https://img.shields.io/badge/Database-Supabase-emerald) ![Face Recognition](https://img.shields.io/badge/Lib-Face_Recognition-yellow)

> A smart attendance system that uses real-time face recognition to verify identity and logs attendance instantly to a cloud database (Supabase).

---

## 📖 Overview

This project automates the traditional attendance process. It captures video from a webcam, detects faces, compares them against a known database of encodings, and retrieves student details from the cloud.



If a match is found:
1.  The system fetches the student's profile (Name, Major, Year) from **Supabase**.
2.  It downloads the student's profile picture for verification.
3.  It updates the **Total Attendance** count and **Last Login Time** in the database.
4.  A dynamic UI overlay displays the student's information on the screen.

---

## ⚙️ How It Works

The project is divided into three distinct modules:

### 1. 🗄️ Database Management (`AddDatatoDatabse.py`)
* **Purpose:** Uploads student metadata (ID, Name, Major, Year, etc.) to the Supabase SQL table.
* **Tech:** `requests` library to hit Supabase REST endpoints.

### 2. 🧠 Encoding Generator (`EncodeGenerator.py`)
* **Purpose:**
    1.  Reads student images from the `Images/` directory.
    2.  Uploads these images to the Supabase Storage bucket.
    3.  Generates **128-d face encodings** for each image.
    4.  Saves the encodings and Student IDs into a pickle file (`EncodeFile.p`) for fast loading.

### 3. 🎥 Real-Time Recognition (`main.py`)
* **Purpose:** The core engine. It runs the webcam loop, performs face matching, and handles the UI/Database updates.
* **Features:**
    * **Cooldown Timer:** Prevents spamming attendance updates (only updates if >30 seconds have passed since last login).
    * **Dynamic Graphics:** Uses `cvzone` and background overlays to show a professional dashboard.

---

## 🛠️ Tech Stack & Prerequisites

* **Python 3.8+**
* **Supabase:** Backend-as-a-Service (PostgreSQL + Storage).
* **Libraries:**
    * `opencv-python` (Computer Vision)
    * `face-recognition` (dlib-based recognition)
    * `cvzone` (UI elements)
    * `numpy` (Data handling)
    * `requests` (API calls)

---

## 🚀 Setup & Installation

### 1. Install Dependencies
```bash
pip install opencv-python face-recognition cvzone numpy requests
