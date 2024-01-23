import cv2
import time
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Inisialisasi objek deteksi wajah
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inisialisasi objek kamera (ganti angka 0 dengan indeks kamera jika menggunakan kamera eksternal)
cap = cv2.VideoCapture(0)

# Fungsi untuk mendeteksi wajah dan memperbarui GUI
def update_gui():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah dalam frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Gambar kotak di sekitar wajah yang terdeteksi
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Tampilkan frame yang telah diproses di GUI
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

    # Perbarui FPS di GUI
    current_time = time.time()
    elapsed_time = current_time - start_time[0]
    frames[0] += 1
    fps = frames[0] / elapsed_time
    fps_label.config(text=f"FPS: {fps:.2f}")

    # Jadwalkan pemanggilan fungsi ini lagi setelah 10ms
    root.after(10, update_gui)

# Buat GUI
root = tk.Tk()
root.title("Face Detection with FPS")

# Buat label untuk menampilkan frame yang telah diproses
label = Label(root)
label.pack()

# Inisialisasi variabel untuk mengukur FPS
start_time = [time.time()]
frames = [0]

# Buat label untuk menampilkan FPS
fps_label = tk.Label(root, text="FPS: 0.00")
fps_label.pack()

# Mulai pembaruan GUI
update_gui()

# Mulai loop GUI
root.mainloop()

# Bebaskan sumber daya
cap.release()
cv2.destroyAllWindows()
