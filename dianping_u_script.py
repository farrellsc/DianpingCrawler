import dianping_u_crawler_main
import time


f = open('./starting_time.txt','a')
f.write(str(time.ctime()))
f.write('\n')
f.close()
current_id = open('status.txt').readlines()[0]
current_id = int(current_id.strip())
dianping_u_crawler_main.getInRange('./inputfile.txt' , current_id)
#deleted command lines considering 'status.txt'
