#libraries
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # 0 is main camera
        self.video_source = 0  
        self.vid = cv2.VideoCapture(self.video_source) # capture vid using cv2
        
        # make canvas using tk, showcase live cam
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack() # pack canvas to window
        
        # make button to take pics
        self.btn_snapshot = tk.Button(window, text="Take Photo", width=20, command=self.snapshot) 
        self.btn_snapshot.pack(pady=10) # pack button to window

        # Create a frame to contain the filter buttons
        self.filter_frame = tk.Frame(window)
        self.filter_frame.pack() # pack to window

        # Pack filter buttons in a single row
        filter_buttons = [
            ("Anonymous Filter", self.apply_filter_anonymous),
            ("Clown Filter", self.apply_filter_clown),
            ("Ayam Filter", self.apply_filter_ayam),
            ("Luffy Filter", self.apply_filter_luffy),
            ("Gojo Filter", self.apply_filter_gojo)
        ]

        # make and pack filter button using for loop with corresponding commands
        for text, command in filter_buttons:
            btn = tk.Button(self.filter_frame, text=text, width=20, command=command)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # make status label
        self.status_label = tk.Label(window, text="", font=("Arial", 12))
        self.status_label.pack(pady=5) # pack
        
        # initilialise flags for photo counter + application of filters
        self.photo_counter = 0
        self.apply_anonymous_flag = False
        self.apply_clown_flag = False
        self.apply_ayam_flag = False
        self.apply_luffy_flag = False
        self.apply_gojo_flag = False

        #start update loop to continuously refresh video feed
        self.update()
        
        self.window.protocol("WM_DELETE_WINDOW", self.exit_app) # close window
        self.window.mainloop() # start mainloop of window
    
    def snapshot(self): # this method takes pic from video feed
        ret, frame = self.vid.read() # capture frame from video feed
        if ret: # if sucessful
            frame = self.apply_filters(frame) # apply the filter to the frame
            self.photo_counter += 1 # increase photo counter whenever photo taken
            filename = f"snapshot_{self.photo_counter}.png" # create file name (based on photo counter)
            cv2.imwrite(filename, frame) # save captured frame as image using filename
            self.update_status(f"Snapshot {self.photo_counter} taken!") # update status label
    
    def apply_filter_anonymous(self):
        self.apply_anonymous_flag = not self.apply_anonymous_flag # flips the state true to false, vice versa
        if self.apply_anonymous_flag: # if click on, turn off other filters
            self.apply_ayam_flag = False
            self.apply_clown_flag = False
            self.apply_luffy_flag = False
            self.apply_gojo_flag = False
            self.update_status("Anonymous Filter applied.") # update status
        else: # if click off
            self.update_status("Anonymous Filter turned off.") # update status
    
    def apply_filter_clown(self):
        self.apply_clown_flag = not self.apply_clown_flag
        if self.apply_clown_flag:
            self.apply_ayam_flag = False
            self.apply_anonymous_flag = False
            self.apply_luffy_flag = False
            self.apply_gojo_flag = False
            self.update_status("Clown Filter applied.")
        else:
            self.update_status("Clown Filter turned off.")

    def apply_filter_ayam(self):
        self.apply_ayam_flag = not self.apply_ayam_flag
        if self.apply_ayam_flag:
            self.apply_anonymous_flag = False
            self.apply_clown_flag = False
            self.apply_luffy_flag = False
            self.apply_gojo_flag = False
            self.update_status("Ayam Filter applied.")
        else:
            self.update_status("Ayam Filter turned off.")
    
    def apply_filter_luffy(self):
        self.apply_luffy_flag = not self.apply_luffy_flag
        if self.apply_luffy_flag:
            self.apply_anonymous_flag = False
            self.apply_clown_flag = False
            self.apply_ayam_flag = False
            self.apply_gojo_flag = False
            self.update_status("Luffy Filter applied.")
        else:
            self.update_status("Luffy Filter turned off.")

    def apply_filter_gojo(self):
        self.apply_gojo_flag = not self.apply_gojo_flag
        if self.apply_gojo_flag:
            self.apply_anonymous_flag = False
            self.apply_clown_flag = False
            self.apply_ayam_flag = False
            self.apply_luffy_flag = False
            self.update_status("Gojo Filter applied.")
        else:
            self.update_status("Gojo Filter turned off.")

    def apply_filters(self, frame): # apply filter to frame
        if self.apply_anonymous_flag: # if active
            frame = self.apply_anonymous_filter(frame) # apply
        elif self.apply_clown_flag:
            frame = self.apply_clown_filter(frame)
        elif self.apply_ayam_flag:
            frame = self.apply_ayam_filter(frame)
        elif self.apply_luffy_flag:
            frame = self.apply_luffy_filter(frame)
        elif self.apply_gojo_flag:
            frame = self.apply_gojo_filter(frame)
        return frame
    
    def update(self): #updates video feed
        ret, frame = self.vid.read() #read frame
        if ret: #if sucessful
            frame = self.apply_filters(frame) #apply filter to frame
            #convert frame to image compatible w tk (BGR to RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW) #display image
            self.canvas.image = self.photo  # Keep a reference to the image to prevent garbage collection
        self.window.after(10, self.update) #updates every 10 miliseconds
    
    def apply_anonymous_filter(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grayscale for detection

        #load face detection Haar Cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        #detect the faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        #covers eye region with black rectangle
        for (x, y, w, h) in faces:
            eye_region_y = y + int(h * 1 / 4)
            eye_region_h = int(h * 1 / 3)
            cv2.rectangle(frame, (x, eye_region_y), (x + w, eye_region_y + eye_region_h), (0, 0, 0), -1)

        #convert to grayscale then to color BGR format
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return frame # return w anonymous filter applied

    def apply_clown_filter(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # calc coordinates of nose in detected face rectangle
            nose_x = x + w // 2 #width divide by 2 (top left)
            nose_y = y + 3 * h // 5 #height div by 3 (top left)
            cv2.circle(frame, (nose_x, nose_y), 30, (0, 0, 255), -1)  # red circle for nose

            eye_y = y + h // 3 #height div by 3

            # Blue triangles for eyes
            cv2.drawContours(frame, [
                np.array([
                    (x + w // 4, eye_y), #left
                    (x + w // 4 + 30, eye_y - 30), #top
                    (x + w // 4 + 50, eye_y) #right
                ])
            ], 0, (255, 0, 0), -1)
            cv2.drawContours(frame, [
                np.array([
                    (x + 3 * w // 4, eye_y), 
                    (x + 3 * w // 4 - 30, eye_y - 30), 
                    (x + 3 * w // 4 - 50, eye_y)
                ])
            ], 0, (255, 0, 0), -1)

            eye_bottom_y = y + h // 2 - 10

            # Inverted blue triangles for eye bottoms
            cv2.drawContours(frame, [
                np.array([
                    (x + w // 4, eye_bottom_y), 
                    (x + w // 4 + 30, eye_bottom_y + 30), 
                    (x + w // 4 + 50, eye_bottom_y)
                ])
            ], 0, (255, 0, 0), -1)
            cv2.drawContours(frame, [
                np.array([
                    (x + 3 * w // 4, eye_bottom_y), 
                    (x + 3 * w // 4 - 30, eye_bottom_y + 30), 
                    (x + 3 * w // 4 - 50, eye_bottom_y)
                ])
            ], 0, (255, 0, 0), -1)

        return frame

    def apply_ayam_filter(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        eye_img = cv2.imread('ayameye.PNG', -1)  # Load the eye image with alpha channel
        nose_img = cv2.imread('ayamnose.PNG', -1)  # Load the nose image with alpha channel

        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w] # area of frame that encompasses the detected face

            # Resize the eye image to match the size of the detected face region
            eye_resized = cv2.resize(eye_img, (w, h))

            # Create a mask using the alpha channel of the eye image
            eye_mask = eye_resized[:, :, 3]  # Alpha channel of the eye image
            eye_mask = cv2.cvtColor(eye_mask, cv2.COLOR_GRAY2BGR)  # Convert to 3-channel mask

            # Use the mask to blend the eye image and the frame
            eye_overlay = eye_resized[:, :, 0:3]  # Extract RGB channels
            eye_background = cv2.bitwise_and(face_roi, 255 - eye_mask)  # Invert mask and extract region from the frame
            face_roi[:] = cv2.add(eye_overlay, eye_background)  # Blend the image onto the frame

            # Place the resized nose image over the nose area same cuz manual positioning
            nose_resized = cv2.resize(nose_img, (w, h))

            # Create a mask using the alpha channel of the nose image
            nose_mask = nose_resized[:, :, 3]  # Alpha channel of the nose image
            nose_mask = cv2.cvtColor(nose_mask, cv2.COLOR_GRAY2BGR)  # Convert to 3-channel mask

            # Use the mask to blend the nose image and the frame
            nose_overlay = nose_resized[:, :, 0:3]  # Extract RGB channels
            nose_background = cv2.bitwise_and(face_roi, 255 - nose_mask)  # Invert mask and extract region from the frame
            face_roi[:] = cv2.add(nose_overlay, nose_background)  # Blend the image onto the frame

        return frame

    def apply_luffy_filter(self, frame):
        # Load hat image with transparent background
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        hat_img = cv2.imread('luffyhat.PNG', -1)  # read hat image
        hat_img = cv2.resize(hat_img, (300, 300))  # Adjust the size
        scar_img = cv2.imread('luffyscar.PNG', -1)  # read scar image
        scar_img = cv2.resize(scar_img, (50, 50))  # Adjust size as needed
        

        for (x, y, w, h) in faces:
            # Adjust the hat position and size based on face detection
            hat_width = int(2 * w)  # hat twice the face width
            hat_height = int(1.25 * h) # hat 1.25 times the face height

            # Resize the hat image based on the calculated width and height
            resized_hat = cv2.resize(hat_img, (hat_width, hat_height))

            # Calculate adjusted x-coordinate to ensure the hat remains within the frame
            hat_x = max(0, x - int((hat_width - w) / 2))
            
            # Overlay the hat onto the frame
            for i in range(hat_height):
                for j in range(hat_width):
                    if hat_x + j < frame.shape[1]:  # Ensure x-coordinate is within frame width
                        if resized_hat[i, j][3] != 0:  # Check alpha channel for transparency
                            frame[y + i - int(0.7 * h), hat_x + j] = resized_hat[i, j, 0:3]

            # Add the scar under the right eye
            scar_x = x + int(w * 0.6)  # x-coordinate for scar placement
            scar_y = y + int(h * 0.4)  # y-coordinate for scar placement

            # Overlay the scar onto the frame
            for i in range(scar_img.shape[0]):
                for j in range(scar_img.shape[1]):
                    if scar_y + i < frame.shape[0] and scar_x + j < frame.shape[1]:
                        if scar_img[i, j][3] != 0:  # Check alpha channel for transparency
                            frame[scar_y + i, scar_x + j] = scar_img[i, j, 0:3]

        return frame

    def apply_gojo_filter(self, frame):
        gojo_img = cv2.imread('gojo.png', -1)  # Load the Gojo image with alpha channel

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        gojo_img = cv2.resize(gojo_img, (300, 300))  # Adjust size
        

        for (x, y, w, h) in faces:
            # Adjust the gojo position and size based on face detection
            gojo_width = int(2 * w)  #hat twice as wide
            gojo_height = int(1.5 * h) # hat 1.5 times taller

            # Resize the hat image based on the calculated width and height
            resized_gojo = cv2.resize(gojo_img, (gojo_width, gojo_height))

            # Calculate adjusted x-coordinate to ensure the hat remains within the frame
            gojo_x = max(0, x - int((gojo_width - w) / 2))
            
            # Overlay gojo onto the frame
            for i in range(gojo_height):
                for j in range(gojo_width):
                    if gojo_x + j < frame.shape[1]:  # Ensure x-coordinate is within frame width
                        if resized_gojo[i, j][3] != 0:  # Check alpha channel for transparency
                            frame[y + i - int(0.7 * h), gojo_x + j] = resized_gojo[i, j, 0:3]

        return frame

    def exit_app(self): # for closing
        self.vid.release()
        self.window.destroy()
    
    def update_status(self, message): # update status labe;
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Camera Filter App")