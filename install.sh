mkdir ~/geckodriver
wget -P ~/geckodriver/ https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
tar -xzf ~/geckodriver/geckodriver-v0.11.1-linux64.tar.gz -C ~/geckodriver/
export PATH=$PATH:~/geckodriver/geckodriver

mkdir Data
mkdir Data/Shops
sudo apt-get update -y
sudo apt-get install python-pip firefox xvfb openssh-server -y
sudo pip install selenium
sudo pip install httplib
sudo pip install urllib