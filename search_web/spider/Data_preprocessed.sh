#！/bin/sh

#Download Dataset
wget -w 2 -m -P /home/data -H "http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en"
#Unzip All zip file
cd /home/data
find . -name "*.zip" | xargs -n1 unzip
#Copy all file
find /home/data/ -type f -name '*.txt' -exec cp -at/home/newdata {} +