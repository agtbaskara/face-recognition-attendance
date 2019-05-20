import face_recognition
import cv2
import numpy as np
import time
import os
from threading import Thread

class FrameCapture:
    """
    Class for getting frame from cap
    """
    def __init__(self):
        self.video_capture_face = cv2.VideoCapture(0)
        (self.grabbed_face, self.frame_face) = self.video_capture_face.read()
        self.stopped = False

        self.frame_face_small = cv2.resize(self.frame_face.copy(), (0, 0), fx=0.25, fy=0.25)
    
    def start(self):
        """
        Start get thread
        """
        Thread(target = self.get, args = ()).start()
        return self

    def stop(self):
        """
        Stop Image Processing thread
        """
        self.stopped = True
        self.video_capture_face.release()
    
    def get(self):
        """
        Thread to capture frame from camera
        """
        while not self.stopped:
            if not (self.grabbed_face):
                self.stop()
            else:
                (self.grabbed_face, self.frame_face) = self.video_capture_face.read()
            self.frame_face_small = cv2.resize(self.frame_face.copy(), (0, 0), fx=0.7, fy=0.7)
            cv2.imshow('Preview', self.frame_face_small)
            cv2.waitKey(1)

def print_daftar_hadir(kehadiran_temp):
    print()
    print("Status Kehadiran :")
    for i in range(0,len(kehadiran_temp)):
        print(known_face_names[i],":" ,kehadiran_temp[i])

# Initialize Frame Capture Thread
FrameThread = FrameCapture()
FrameThread.start()

# Load Face Image
baskara_image = face_recognition.load_image_file("face/baskara.jpg")
emerald_image = face_recognition.load_image_file("face/emerald.jpg")
jota_image = face_recognition.load_image_file("face/jota.jpg")

# Recognize Face Image
baskara_face_encoding = face_recognition.face_encodings(baskara_image)[0]
emerald_face_encoding = face_recognition.face_encodings(emerald_image)[0]
jota_face_encoding = face_recognition.face_encodings(jota_image)[0]

# Create List Of Face Encoding
known_face_encodings = [
    baskara_face_encoding,
    emerald_face_encoding,
    jota_face_encoding
]

# Create List Names
known_face_names = [
    "Baskara",
    "Emerald",
    "Jota"
]

# Create List Absen
kehadiran_kelas_a = [
    False,
    False,
    False
]

kehadiran_kelas_b = [
    False,
    False,
    False
]

kehadiran_kelas_c = [
    False,
    False,
    False
]

# Initialize variable
face_locations = []
face_encodings = []
face_names = []
nama_kelas_temp = ""

os.system('clear')
print("Face Recognition Attendance Version 0.0.0.1")
print("Kelas Tersedia :")
print("a. Manajemen Proyek")
print("b. Filsafat Ilmu Komputer")
print("c. Kalkulus 5")
while True:
    pilihan = input("Pilih Kelas: ")
    if pilihan == "a":
        kehadiran_temp = kehadiran_kelas_a
        nama_kelas_temp = "Manajemen Proyek"
        break
    elif pilihan == "b":
        kehadiran_temp = kehadiran_kelas_b
        nama_kelas_temp = "Filsafat Ilmu Komputer"
        break
    elif pilihan == "c":
        kehadiran_temp = kehadiran_kelas_c
        nama_kelas_temp = "Kalkulus 5"
        break
    else:
        print("Error, Pilih Ulang")

while True:
    # Get Frame from Frame Capture Thread
    frame_face = FrameThread.frame_face

    # Resize then convert to RGB
    small_frame = cv2.resize(frame_face, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Detect All Face
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Match Face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)
    
    os.system('clear')
    print("Absensi Kelas", nama_kelas_temp)
    
    if face_names == []:
        print("Tidak Ada Wajah Terdeteksi")
        print_daftar_hadir(kehadiran_temp)
    elif "Unknown" in face_names:
        print("Terdapat Wajah Yang Tidak Dikenali")
        print_daftar_hadir(kehadiran_temp)
    else:
        scan_time = 3
        start_time = time.time()
        print("Halo", face_names[0], "Kehadiran Anda Telah Tercatat Pada Sistem")
        kehadiran_temp[first_match_index] = True
        print_daftar_hadir(kehadiran_temp)
        time.sleep(scan_time)

    time.sleep(0.5)