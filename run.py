# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import wget
import time
import dlib
import cv2
import os
import datetime as dt


def download_facelandmark_model():
	if(os.path.exists("model/shape_predictor_68_face_landmarks.dat")):
		print("Yes")
	else:
		try:
			url='https://github.com/italojs/facial-landmarks-recognition/raw/master/shape_predictor_68_face_landmarks.dat'
			wget.download(url)
			os.rename("shape_predictor_68_face_landmarks.dat", "model/shape_predictor_68_face_landmarks.dat")
		except:
			print("Please connect to the internet...")
			exit()


download_facelandmark_model()

def eye_aspect_ratio(eye):


	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])



	C = dist.euclidean(eye[0], eye[3])


	ear = (A + B) / (2.0 * C)


	return ear


EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

COUNTER = 0
TOTAL = 0

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


cap = cv2.VideoCapture(0)
t = dt.datetime.now()

# loop over frames from the video stream
MIN_WISE = {}
while True:

	ret,frame = cap.read()

	delta = dt.datetime.now()-t
	if delta.seconds >= 20:
		print("20 S Crossed")
		print(dt.datetime.now())
		print(TOTAL)
		x = str(dt.datetime.now())
		MIN_WISE.update( {""+x : TOTAL} )
		TOTAL = 0
		# Update 't' variable to new time
		t = dt.datetime.now()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


	rects = detector(gray, 0)


	for rect in rects:

		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)


		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)


		ear = (leftEAR + rightEAR) / 2.0


		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)


		if ear < EYE_AR_THRESH:
			COUNTER += 1


		else:

			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				TOTAL += 1


			COUNTER = 0




		cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	if key == ord("q"):

		break


cv2.destroyAllWindows()
vs.stop()
