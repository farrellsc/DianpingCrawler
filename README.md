## Dianping_Crawler  
Tested on Ubuntu 14.04 with python2.7 and firefox46

### Usage  
Install environmental requirements by `sudo bash install.sh`  
Set IDs in `inputfile.txt`, one dianping ID each line.  
If it's the first time you run the crawler, set an ID to `status.txt` to start with. This ID should be in `inputfile.txt`. Afterwards the crawler will automatically record its status.  
To start crawling use `python2.7 dianping_u_script.py`  
