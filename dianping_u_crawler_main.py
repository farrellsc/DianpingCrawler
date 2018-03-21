# encoding: utf-8
import time
import codecs
import random
import json
import dianping_u_profile_crawler
import dianping_u_follows_crawler
import dianping_u_fans_crawler
import dianping_u_checkins_crawler
import dianping_u_reviews_crawler
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def getInRange(inputfile,current_id):
    switch = 0
    f=open(inputfile)
    ###
    # stores all IDs as a list, elements as int
    IDpool=[]    
    while 1:
        line=f.readline()
        line=str(line).strip('\n')
        if line: IDpool.append(int(line))
        else: break
    if len(IDpool)==0:
        print 'Error! Inputfile is empty!'
        raise
    ###
    ID_number = len(IDpool)
    ID_count = 0
    binary = FirefoxBinary('/opt/firefox46/firefox')
    #driver = webdriver.Firefox(firefox_binary = binary)
    driver = webdriver.Firefox(executable_path = '/root/geckodriver/geckodriver', firefox_binary = binary)
    for i in IDpool:
        ID_count += 1
        print('ID:'+str(ID_count)+'/'+str(ID_number))+'    '+str(i)
        if switch == 0 and i != current_id: continue
        if switch ==0 and i == current_id:
            switch = 1
        if switch == 1: pass
        f = open('./status.txt','w')
        f.write(str(i))
        f.close()
        try:
            time.sleep(random.randint(3, 4))
            profile_str = dianping_u_profile_crawler.get_page(i, driver).getstr()
            ###
            out = codecs.open("./Data/%s_profile.txt"%str(i), 'w', 'utf-8')
            out.write(profile_str + "\n")
            out.close()
            ###
            # threshold
            file_threshold = open("./Data/%s_profile.txt"%str(i))
            content_json = json.loads(file_threshold.read())
            file_threshold.close()
            if content_json['Checkin'] < 5 or content_json['Review'] < 5:
                continue
            ###
            print("... processing an active user ...")
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_follows.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_follows_crawler.get_follows(i, driver, content_json['Follows']).getstr() + "\n")
            out.close()
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_fans.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_fans_crawler.get_fans(i, driver).getstr() + "\n")
            out.close()
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_checkins.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_checkins_crawler.get_checkins(i, driver, content_json['Checkin']) + '\n')
            out.close()
            time.sleep(random.randint(3, 4))
            out = codecs.open("./Data/%s_reviews.txt"%str(i), 'w', 'utf-8')
            out.write(dianping_u_reviews_crawler.get_reviews(i, driver) + "\n")
            out.close()
        
        except Exception as e:
            print e
            error_log = open('./error_log.txt','a')
            error_log.write(str(time.ctime())+'\n')
            error_log.write(str(i) + ' ' + 'main  ' + '\n')
            error_log.write(str(e))
            error_log.write('\n\n')
            error_log.close()
        

