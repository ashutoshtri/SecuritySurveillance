
  
import face_recognition
import cv2
import os
import numpy as np
from hack import hack
import csv
from playsound import playsound


video_capture = cv2.VideoCapture(0)
known_face_encodings = []
known_face_names = []
c=1
while c == 1:
    img=input("Enter image name ")
    name = input("Enter the name ")
    criminal = input("Press 1 for criminal and 2 for non-criminal ")

    image = face_recognition.load_image_file(img+".jpg")
    encoding = face_recognition.face_encodings(image)[0]
    face_locations = []
    face_encodings = []

    criminal_data= []

    counter = 0

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)


    
    known_face_encodings.append(encoding)
    known_face_names.append(name)
    criminal_data.append(criminal)
    
    fields=[]
    fields.append(encoding)
    fields.append(name)

    with open('facedatatest.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    c = 0
    c = input("Enter 1 to add more picture data, else press any key to exit")
video_capture = cv2.VideoCapture(0)


process_this_frame = True

while True:
    ret, frame = video_capture.read()

   
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        haha= 0
        face_names = []
        for face_encoding in face_encodings:
            haha= haha + 1
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
                
            f = "alert.mp3"
            os.system(f) 


            face_names.append(name)

    process_this_frame = not process_this_frame



    for (top, right, bottom, left), name in zip(face_locations, face_names):
        
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


