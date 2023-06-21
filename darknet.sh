# #!/bin/bash

# #Tested on Ubuntu 16.04.




# echo -e "\n\nDownloading darknet\n\n"
# wget https://www.dropbox.com/s/9nxzvyyi53bi4p4/darknet?dl=0
# mv darknet?dl=0 darknet
# chmod 755 darknet


# #needed darknet. Moved to pwd.

#!/bin/bash

# Clone Darknet repository
git clone https://github.com/AlexeyAB/darknet.git

# Navigate to Darknet directory
cd darknet

# Modify the Makefile (if necessary)
# Uncomment and set the options as needed
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile

# Build Darknet
make

# Verify if the build was successful
if [ -f darknet ]; then
  echo "Darknet executable generated successfully."
   # Execute the darknet command
  ./darknet detector test /Users/vishalkumawat/spacy-ai/server/yolo/obj.names /Users/vishalkumawat/spacy-ai/server/yolo/custom-yolo.cfg /Users/vishalkumawat/spacy-ai/server/yolo/custom-yolo.weights -thresh 0.1 -dont_show temp/aadhar3.jpg

else
  echo "Failed to generate Darknet executable."
fi