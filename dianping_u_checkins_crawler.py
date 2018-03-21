# encoding: gb2312
from dianping_u_utils.translate_time import *
import time


def toJSON(elements):
    count = min(len(elements[0]),len(elements[1]),len(elements[2]),len(elements[3]))
    print count
    if count == 0: return '{\"count\":0, \"checkins\":[]}'
    result = "{\n"
    result = result + "    \"count\": " + str(count) + ",\n"
    result = result + "    \"checkins\": \n    [\n"
    for i in range(count-1):
        time = elements[0][i]
        place = elements[1][i]
        shopID = elements[2][i]
        address = elements[3][i]
        result = result + "        {\n            \"time\": \"" + time + '\",\n            \"place\": \"' + place + "\",\n" + "            \"shopID\": \"" + shopID + "\",\n" + "            \"address\": \"" + address + '\"\n        },\n'
    result = result + "        {\n            \"time\": \"" + elements[0][-1] + '\",\n            \"place\": \"' + elements[1][-1] + "\",\n" + "            \"shopID\": \"" + elements[2][-1] + "\",\n" + "            \"address\": \"" + elements[3][-1] + '\"\n        }\n    ]\n}'
    return result


def get_checkins(ID, driver, count):
    driver.get("http://www.dianping.com/member/" + str(ID) + "/checkin")
    pageno = count/20 + 1
    if pageno > 400:
        pageno = 400
    for i in range(1, pageno):
        if i % 5 == 0:
            print 'checkin,'+str(i)+'/'+str(pageno)
        try:
            button = driver.find_element_by_id("J_more")
            button.click()
            time.sleep(1)
        except:
            break
    html = driver.page_source
    name_rawraw = driver.find_elements_by_css_selector('a[target=\"_blank\"]')
    time_raw = driver.find_elements_by_class_name('time')
    address_raw = driver.find_elements_by_css_selector('p[class = \"addres col-exp\"]')

    name_raw = []
    for one in name_rawraw:
        if 'shop' in one.get_attribute('href'):
            name_raw.append(one)
    
    shopID = []
    places = []
    times = []
    address = []
    
    for i in range(len(name_raw)):
        shopID.append(name_raw[i].get_attribute('href').split('/')[-1])
        places.append(name_raw[i].text)
        times.append(translate_checkin_time(time_raw[i].text[:-1]))
        address.append(address_raw[i].text)
    return toJSON([times, places, shopID, address])

