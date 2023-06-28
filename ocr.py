#!/bin/bash
from config import *
# from utils.darknet_classify_image import *
from utils.tesseract_ocr import *
import utils.logger as logger
import sys
from PIL import Image
import time
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
from typing import Tuple

PYTHON_VERSION = sys.version_info[0]
OS_VERSION = os.name

app = Flask(__name__)

CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class OCR():
	''' Finds and determines if given image contains required text and where it is. '''

	def init_vars(self):
		try:			
			self.TESSERACT = TESSERACT
			

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
		if self.init_ocr() != 0:
			logger.fatal("Init OCR")
	

	def find_and_classify(self, cropped_images):
		''' find the required text field from given image and read it through tesseract.
		    Results are stored in a dicionary. '''
		start = time.time()
		
		#----------------------------Perform OCR-------------------------------------------#
		ocr_results = None
		if cropped_images == []:
			logger.bad("No text found!")
			return None 	 
		else:
			logger.good("Performing OCR")
			ocr_results = self.OCR.ocr(cropped_images)
	    
		end = time.time()
		logger.good("OCR time: " + str(end-start))
		return ocr_results
		
		
			
		#----------------------------------------------------------------#

	def __init__(self):
		''' Run AadharOCR '''
		self.initialize()
		
def remove_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)

def crop_image(image_path, area:Tuple) -> object:
    image = cv2.imread(image_path)
    x1, y1, x2, y2 = area
    cropped_img = image[y1:y2, x1:x2]
    
    return cropped_img

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
		
@app.route('/ocr', methods=['POST'])
def upload_file():
    extracter = OCR()
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    image = Image.open(file)
    file_path = f"temp/{file.filename}"
    image.save(file_path)
    cropped_areas = request.form.getlist('cropped_area')

    if not cropped_areas:
        return jsonify({'error': 'No cropped areas provided'}), 400
    cropped_images = []
    for cropped_area_str in cropped_areas:
        cropped_area = eval(cropped_area_str)
        cropped_img = crop_image(file_path, cropped_area)
        cropped_images.append((cropped_area, cropped_img))
    result=extracter.find_and_classify(cropped_images)
    remove_file(file_path)
    return jsonify({'data': result}), 200

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')
