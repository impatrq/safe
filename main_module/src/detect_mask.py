# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import random
from os import listdir
from os.path import isfile, join

from tensorflow.python.keras.backend import print_tensor


FILE_DIR = os.path.dirname(__file__) + "/"

def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

# load our serialized face detector model from disk
def process_images():
	prototxtPath = FILE_DIR + "face_detector/deploy.prototxt"
	weightsPath = FILE_DIR + "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
	faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
	output = dict()
	output["files"] = list()
	# load the face mask detector model from disk
	maskNet = load_model(FILE_DIR + "mask_detector.model")

	# initialize the video stream
	path = FILE_DIR + "images/input/"
	path_save = FILE_DIR + "images/output/"
	files = [f for f in listdir(path) if isfile(join(path, f))]
	print("[SYSTEM] doing magic things...")
	number = 0
	result = bool()
	label = str()
	percentage = str()
	final_result = bool()
	final_label = str()
	final_percentage = str()
	for file in files:
		frame = cv2.imread(f"{path}{file}")
		print(file)

		people = 0
		# loop over the frames from the video stream

		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 400 pixels
		frame = imutils.resize(frame, width=1920)

		# detect faces in the frame and determine if they are wearing a
		# face mask or not
		(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

		# loop over the detected face locations and their corresponding
		# locations
		area = 0
		for (box, pred) in zip(locs, preds):
			# unpack the bounding box and predictions
			final_result = ""
			final_label = ""
			final_percentage = ""
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred
			people = people + 1
			# determine the class label and color we'll use to draw
			# the bounding box and text
			result = True if mask > withoutMask else False
			label = "Barbijo Detectado" if mask > withoutMask else "Barbijo NO Detectado"
			color = (0, 255, 0) if label == "Barbijo Detectado" else (0, 0, 255)
			percentage = "{:.2f}%".format(max(mask, withoutMask) * 100)
			# include the probability in the label
			# label = "{}: {:.2f}%".format(label, percentage)

			# display the label and bounding box rectangle on the output
			# frame
			cv2.putText(frame, label, (startX, startY - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 1, color, 5)
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 5)
			x = endX - startX
			y = endY - startY
			if (x * y) > area:
				area = x * y
				final_result = result
				final_label = label
				final_percentage = percentage
		# show the output frame
		new_file = f"image_{str(number)}.jpeg"
		name = f"{path_save}{new_file}"
		cv2.imwrite(name, frame)
		output["files"].append({"file":name,"people":people,"result":final_result,"label":final_label, "percetage":final_percentage})
		number += 1
		key = cv2.waitKey(1) & 0xFF
	mask = 0
	withoutMask = 0
	for img in output["files"]:
		if img["result"]:
			mask = mask + 1
		else:
			withoutMask = withoutMask + 1
	ok = False
	while(not ok):
		choice = random.choice(output["files"])
		if (mask > withoutMask) == choice["result"]:
			print(choice["result"])
			output["average"] = {"file": choice["file"],"result":mask > withoutMask}
			ok = True
	return output