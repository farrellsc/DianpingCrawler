# encoding: utf-8
from dianping_u_utils.translate_time import *


class Reviews(object):
    def __init__(self):
        super(Reviews, self).__init__()
        self.reviews = []

    def getstr(self):
        result = "{\n"
        result = result + "    \"count\": " + str(len(self.reviews)) + ",\n"
        result = result + "    \"reviews\": \n    [\n"
        if len(self.reviews) == 0:
            result = result + "    \n    ]\n}"
            return result
        for i in range(len(self.reviews)-1):
            result = result + "        {\n            \"date\": \"" + self.reviews[i][4] + '\",\n            \"shopName\": \"' + self.reviews[i][1] + "\",\n" + "            \"shopID\": \"" + self.reviews[i][0] + "\",\n" + "            \"stars\": " + str(self.reviews[i][2]) + ",\n" + "            \"comments\": \"" + self.reviews[i][3] + '\"\n        },\n'
        result = result + "        {\n            \"date\": \"" + self.reviews[len(self.reviews)-1][4] + '\",\n            \"shopName\": \"' + self.reviews[len(self.reviews)-1][1] + "\",\n" + "            \"shopID\": \"" + self.reviews[len(self.reviews)-1][0] + "\",\n" + "            \"stars\": " + str(self.reviews[len(self.reviews)-1][2]) + ",\n" + "            \"comments\": \"" + self.reviews[len(self.reviews)-1][3] + '\"\n        }\n    ]\n}'
        return result


def get_reviews(ID, driver):
    url = "http://www.dianping.com/member/" + str(ID) + "/reviews"
    driver.get(url)
    content = driver.page_source
    reviews_count = 0
    reviews = Reviews()
    
    #get reviews_count
    filter_count = re.compile(u">点评\((.*?)\)<")
    if len(filter_count.findall(content)) != 0:
        reviews_count = int(filter_count.findall(content)[0])
    
    pages = int(reviews_count / 15)
    for i in range(1, pages + 2):
        if i % 5 == 0:
            print 'review,'+str(i)+'/'+str(pages+1)
        time.sleep(random.randint(3, 4))
        url = "http://www.dianping.com/member/" + str(ID) + "/reviews?pg=" + str(i)
        driver.get(url)
        #crawl reviews into lists
        nameId_raw = driver.find_elements_by_class_name('J_rpttitle')
        star_raw = driver.find_elements_by_css_selector('span[title = \"\"]')
        comment_raw = driver.find_elements_by_css_selector('div[class = \"mode-tc comm-entry\"]')
        date_raw = driver.find_elements_by_css_selector('span[class = \"col-exp\"]')[:-1]
        #save lists into Reviews
        for i in range(0, len(nameId_raw)):
            temp = []
            temp.append(nameId_raw[i].get_attribute('href').split('/')[-1])
            temp.append(nameId_raw[i].text)
            try:temp.append(int(star_raw[i].get_attribute('class')[-2:]))
            except:temp.append(-1)
            temp.append(comment_raw[i].text)
            temp.append(translate_review_time(date_raw[i].text))
            reviews.reviews.append(temp)
        # store shop profiles
        '''
        for each_id in nameId:
            try:
                testf = open("./Data/Shops/" + str(each_id[0]))
                testf.close()
                continue
            except:
                "do nothing ..."
            time.sleep(random.randint(3, 4))
            try:
                print("now getting " + str(each_id[0]))
                s = Shop(driver, str(each_id[0]))
                outf = codecs.open("./Data/Shops/" + str(each_id[0]), 'w', 'utf-8')
                outf.write(s.getstr() + "\n")
                outf.close()
            except:
                continue
        '''
    return reviews.getstr()
