import os
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--darknet', dest='DARKNET', action='store_true', help="Specifies to use the Darknet classifier")
	
	parser.add_argument('-t', '--tesseract', dest='TESSERACT', action='store_true', help="Use the local Tesseract OCR engine")
	
	parser.add_argument('-l', '--dbl', dest="DARKNET_BINARY_LOCATION", default=None, help="Location of Darknet Binary")
	parser.add_argument('--thresh', dest="DARKNET_THRESH", default=.2, type=float, help="Darknet threshold for successful classification (lower = more bounding boxes)")
	parser.add_argument('--data', dest="DARKNET_DATA_FILE", default="data/obj.data", help="Darknet data file")
	parser.add_argument('--cfg', dest="DARKNET_CFG_FILE", default="yolo-obj.cfg", help="Darknet configuration file")
	parser.add_argument('--weights', dest="DARKNET_WEIGHTS", default="yolo-obj_8000.weights", help="Weights for Darknet")
	
	args = parser.parse_args()
	# if args.DARKNET == False:
	# 	parser.error("Darknet must be set, add -d")
	# if args.TESSERACT == False:
	# 	parser.error("Tesseract must be set, add -t")
	
	return args


## Change the following variable based on what algorithms you want to use ##
global DARKNET, TESSERACT, DARKNET_BINARY_LOCATION, DARKNET_THRESH, DARKNET_DATA_FILE, \
		DARKNET_CFG_FILE, DARKNET_WEIGHTS
		

args = parse_args()


DARKNET = 'd'



TESSERACT = 't'


############################################################################

##### Darknet Information - Change if necessary to fit your needs #####

if DARKNET:
	if args.DARKNET_BINARY_LOCATION == None:
		DARKNET_BINARY_LOCATION = "./darknet/darknet"
	else:
		DARKNET_BINARY_LOCATION = "./dartnet/darknet"

	#### Change the following attributes if you move the files/weights ####
	DARKNET_THRESH    = args.DARKNET_THRESH
	DARKNET_DATA_FILE = 'data/names.list'
	DARKNET_CFG_FILE  = 'data/custom-yolov4-tiny-detector.cfg'
	DARKNET_WEIGHTS   = 'data/custom-yolov4-tiny-detector_final.weights'
	
#######################################################################



