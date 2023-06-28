from utils.ocr import OCR
# import pyocr
# import pyocr.builders
# import sys
# from PIL import Image
# from typing import Tuple
import pytesseract

class TesseractOCR(OCR):

	def initialize(self):
		# ''' Initialize Tesseract and load it up for speed '''
		# print("get_available_tools")
		# tools = pyocr.get_available_tools()
		# print("get_available_tools", tools)
		# if len(tools) == 0:
		# 	print("No tools found, do you have Tesseract installed?")
		# 	sys.exit(1)
		# self.tool = tools[0]
		# self.langs = self.tool.get_available_languages()
		return

	def ocr_one_image(self, area, image, threadList=-1, threadNum=None):
		print("Starting image...")
		txt = pytesseract.image_to_string(image, config="--psm 6 --oem 3")
		txt = txt.replace('\n', '')
		# txt = self.tool.image_to_string(image, lang=self.langs[0], builder=pyocr.builders.TextBuilder())
		print("==RESULT==" + str(area) + "\n" + txt + "\n==========================")
		if threadList != -1:
			threadList[threadNum] = txt
		return txt
