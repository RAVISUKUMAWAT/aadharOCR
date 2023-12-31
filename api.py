#!/bin/bash
from config import *
from utils.darknet_classify_image import *
# from utils.tesseract_ocr import *
import utils.logger as logger
import sys
from PIL import Image
import time
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from dotenv import load_dotenv

PYTHON_VERSION = sys.version_info[0]
OS_VERSION = os.name

app = Flask(__name__)

CORS(app)
load_dotenv()

ocr_api = os.getenv('OCR_API')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class_mapping = {
    0: 'AadharNo',
    1: 'DOB',
    2: 'Gender',
    3: 'Name',
    4: 'Address'
}

class AadharOCR():
	''' Finds and determines if given image contains required text and where it is. '''

	def init_vars(self):
		try:
			self.DARKNET = DARKNET
			
			self.TESSERACT = TESSERACT
			

			return 0
		except:
			return -1

	def init_classifier(self):
		''' Initializes the classifier '''
		try:
			if self.DARKNET:
			# Get a child process for speed considerations
				logger.good("Initializing Darknet")
				self.classifier = DarknetClassifier()
			
			if self.classifier == None or self.classifier == -1:
				return -1
			return 0
		except:
			return -1

	def init_ocr(self):
		''' Initializes the OCR engine '''
		try:
			if self.TESSERACT:
				logger.good("Initializing Tesseract")
				self.OCR = TesseractOCR()
			
			if self.OCR == None or self.OCR == -1:
				return -1
			return 0
		except:
			return -1

	def init_tabComplete(self):
		''' Initializes the tab completer '''
		try:
			if OS_VERSION == "posix":
				global tabCompleter
				global readline
				from utils.PythonCompleter import tabCompleter
				import readline
				comp = tabCompleter()
				# we want to treat '/' as part of a word, so override the delimiters
				readline.set_completer_delims(' \t\n;')
				readline.parse_and_bind("tab: complete")
				readline.set_completer(comp.pathCompleter)
				if not comp:
					return -1
			return 0
		except:
			return -1

	def prompt_input(self):
		
		
			filename = str(input(" Specify File >>> "))
		

	from utils.locate_asset import locate_asset

	def initialize(self):
		if self.init_vars() != 0:
			logger.fatal("Init vars")
		if self.init_tabComplete() != 0:
			logger.fatal("Init tabcomplete")
		if self.init_classifier() != 0:
			logger.fatal("Init Classifier")
	

	def find_and_classify(self, filename):
		''' find the required text field from given image and read it through tesseract.
		    Results are stored in a dicionary. '''
		start = time.time()
		

		#------------------------------Classify Image----------------------------------------#

                
		logger.good("Classifying Image")
		
		coords = self.classifier.classify_image(filename)
		# print("coords", coords)
		#lines=str(coords).split('\n')
		inf=[]
		for line in str(coords).split('\n'):
			if 'left_x' in line:
				info=line.split()
				left_x = int(info[3])
				top_y = int(info[5])
				inf.append((info[0],left_x,top_y))
		

		time1 = time.time()
		print("Classify Time: " + str(time1-start))

		# ----------------------------Crop Image-------------------------------------------#
		logger.good("Finding required text")
		cropped_area = self.locate_asset(filename, self.classifier, lines=coords)
		print("cropped_area", cropped_area)
		
		time2 = time.time()
		

		
		#----------------------------Perform OCR-------------------------------------------#
		
		ocr_results = None
		response = None
		ocr_results = []
		
		if cropped_area == []:
			logger.bad("No text found!")
			return None 	 
		else:
			logger.good("Performing OCR")
			try:
				url = f"{ocr_api}/ocr"
				files = {'file': open(filename, 'rb')}
				data = {'cropped_area': cropped_area}
				
				response = requests.post(url, files=files, data=data)
				result = response.json()
				if result['data'] != []:
					ocr_results = result['data']
			except Exception as e:
				print("An error occurred:", str(e))

			k=[]
			v=[]
			
			for i in range(len(ocr_results)):
				v.append(ocr_results[i][1])
				k.append(class_mapping[int(inf[i][0][:-1])])
			t=dict(zip(k, v))

		time3 = time.time()
		print("OCR Time: " + str(time3-time2))

		end = time.time()
		logger.good("Elapsed: " + str(end-start))
		return t
		
		
			
		#----------------------------------------------------------------#

	def __init__(self):
		''' Run AadharOCR '''
		self.initialize()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
    if os.path.exists('bad.list'):
	    os.remove('bad.list')
		
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    time1 = time.time()
    image = Image.open(file)
    file_path = f"temp/{file.filename}"
    image.save(file_path)
    time2 = time.time()
    print("save image: " + str(time2-time1))

    extracter = AadharOCR()
    result=extracter.find_and_classify(file_path)
    time3 = time.time()
    print("result get: " + str(time3-time1))
    remove_file(file_path)
    if result==None:
        return jsonify({'error': 'Not found'}), 404
    time4 = time.time()
    print("response get: " + str(time4-time1))
    return jsonify({'data': result}), 200

if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')
