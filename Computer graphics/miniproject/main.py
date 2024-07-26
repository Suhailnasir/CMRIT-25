"""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
import numpy as np  # Import numpy for the welcome screen
from signature import match

# Match Threshold
THRESHOLD = 90

def show_welcome_screen():
    # Create a blank black image
    welcome_screen = np.zeros((600, 800, 3), dtype=np.uint8)

    # Add text to the welcome screen
    cv2.putText(welcome_screen, "CMR INSTITUTE OF TECHNOLOGY", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(welcome_screen, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", (140, 150), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 1)
    cv2.putText(welcome_screen, "21CSL66 - Computer Graphics and Image Processing Laboratory", (75, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.line(welcome_screen, (10, 230), (780, 230), (255, 255, 255), 1)
    cv2.putText(welcome_screen, "   VERIFICATION OF SIGNATURE USING", (70, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(welcome_screen, "  IMAGE PROCESSING", (230, 318), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Created By
    cv2.putText(welcome_screen, "Created By", (35, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(welcome_screen, "Stephen V (1CR21CS187)", (35, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(welcome_screen, "Suhail Nasir (1CR21CS188)", (35, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Guided By
    cv2.putText(welcome_screen, "Guided By", (400, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(welcome_screen, "Dr. Preethi Sheba Hepsiba, Associate Professor", (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(welcome_screen, "Mrs. Sridevi, Assistant professor", (400, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(welcome_screen, "PRESS <<Enter>> TO BEGIN", (200, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Display the welcome screen
    cv2.imshow('Welcome Screen', welcome_screen)

    # Wait for the user to press the "a" key
    while True:
        key = cv2.waitKey(1)
        if key == 32:  # "a" key
            print("a key pressed")
            break
        elif key == 27:  # ESC key to exit
            print("ESC key pressed")
            cv2.destroyAllWindows()
            exit()

    cv2.destroyAllWindows()
    print("Welcome screen closed")

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)  # make sure the directory exists
            if(sign == 1):
                img_name = "./temp/test_img1.png"
            else:
                img_name = "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    if(sign == 1):
        filename = os.getcwd()+'\\temp\\test_img1.png'
    else:
        filename = os.getcwd()+'\\temp\\test_img2.png'
    
    res = None
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if(result <= THRESHOLD):
        messagebox.showerror("Failure: Signatures Do Not Match",
                             "Signatures are "+str(result)+f" % similar!!")
        pass
    else:
        messagebox.showinfo("Success: Signatures Match",
                            "Signatures are "+str(result)+f" % similar!!")
    return True

# Show the welcome screen
show_welcome_screen()

# Tkinter GUI code
root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")  # 300x200
uname_label = tk.Label(root, text="Compare Two Signatures:", font=10)
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Signature 1", font=10)
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=400, y=140)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.place(x=150, y=240)

img2_message = tk.Label(root, text="Signature 2", font=10)
img2_message.place(x=10, y=250)

img2_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=400, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=400, y=260)

compare_button = tk.Button(
    root, text="Compare", font=10, command=lambda: checkSimilarity(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get(),))

compare_button.place(x=200, y=320)
root.mainloop()
"""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2
import numpy as np  # Import numpy for the welcome screen
from signature import match

# Match Threshold
THRESHOLD = 85

def show_welcome_screen():
    # Create a blank black image
    welcome_screen = np.zeros((600, 800, 3), dtype=np.uint8)

    # Add colored text to the welcome screen
    cv2.putText(welcome_screen, "    CMR INSTITUTE OF TECHNOLOGY", (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(welcome_screen, "         DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 0), 1)
    cv2.putText(welcome_screen, "     21CSL66 - Computer Graphics and Image Processing Laboratory", (25, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.line(welcome_screen, (10, 230), (780, 230), (255, 255, 255), 1)
    cv2.putText(welcome_screen, "MARKING SYSTEM OF ATTENDANCE USING", (70, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(welcome_screen, "IMAGE PROCESSING", (230, 318), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Created By
    cv2.putText(welcome_screen, "Created By", (35, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(welcome_screen, "Suhail Nasir (1CR21CS188)", (35, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
    cv2.putText(welcome_screen, "Stephen V (1CR21CS187)", (35, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

    # Guided By
    cv2.putText(welcome_screen, "Guided By", (400, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(welcome_screen, "Dr. Preethi Sheba Hepsiba, Associate Professor", (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(welcome_screen, "Mrs. Sridevi, Assistant professor", (400, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(welcome_screen, "PRESS <<SPACE>> TO BEGIN", (200, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Display the welcome screen
    cv2.imshow('Welcome Screen', welcome_screen)

    # Wait for the user to press the Space bar
    while True:
        key = cv2.waitKey(1)
        if key == 32:  # Space bar
            print("Space bar pressed")
            break
        elif key == 27:  # ESC key to exit
            print("ESC key pressed")
            cv2.destroyAllWindows()
            exit()

    cv2.destroyAllWindows()
    print("Welcome screen closed")

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)  # make sure the directory exists
            if(sign == 1):
                img_name = "./temp/test_img1.png"
            else:
                img_name = "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    if(sign == 1):
        filename = os.getcwd()+'\\temp\\test_img1.png'
    else:
        filename = os.getcwd()+'\\temp\\test_img2.png'
    
    res = None
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if(result <= THRESHOLD):
        messagebox.showerror("Failure: Signatures Do Not Match",
                             "Signatures are "+str(result)+f" % similar!!")
        pass
    else:
        messagebox.showinfo("Success: Signatures Match",
                            "Signatures are "+str(result)+f" % similar!!")
    return True

# Show the welcome screen
show_welcome_screen()

# Tkinter GUI code
root = tk.Tk()
root.title("Signature Matching")
root.geometry("600x800")

# Add background image
bg_image = Image.open("pen_and_paper.jpg")  # Load your image here
bg_image = bg_image.resize((600, 800))
bg_image = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

uname_label = tk.Label(root, text="Verification of Signatures:", font=("Helvetica", 16, "bold"), fg="blue", bg="lightyellow")
uname_label.place(x=120, y=50)

img1_message = tk.Label(root, text="Signature 1", font=("Helvetica", 12), fg="green", bg="lightyellow")
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=("Helvetica", 12))
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(
    root, text="Capture", font=("Helvetica", 12), bg="lightblue", command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=("Helvetica", 12), bg="lightblue", command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=400, y=140)

image2_path_entry = tk.Entry(root, font=("Helvetica", 12))
image2_path_entry.place(x=150, y=240)

img2_message = tk.Label(root, text="Signature 2", font=("Helvetica", 12), fg="green", bg="lightyellow")
img2_message.place(x=10, y=250)

img2_capture_button = tk.Button(
    root, text="Capture", font=("Helvetica", 12), bg="lightblue", command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=400, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=("Helvetica", 12), bg="lightblue", command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=400, y=260)

compare_button = tk.Button(
    root, text="Compare", font=("Helvetica", 12, "bold"), bg="yellow", command=lambda: checkSimilarity(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get(),))

compare_button.place(x=250, y=320)
root.mainloop()
