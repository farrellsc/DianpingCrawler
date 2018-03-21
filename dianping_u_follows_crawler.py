# encoding: utf-8
import random
import time


class Connection(object):
    def __init__(self):
        super(Connection, self).__init__()
        self.follows = []

    def getstr(self):
        result = "{\n    \"followsID\": \n    [\n"
        if len(self.follows) == 0:
            result = result + "    \n    ]\n}"
            return result
        for fol in list(self.follows)[:-1]:
            result = result + "        \"" + str(fol) + '\",\n'
        result = result + "        \"" + str(list(self.follows)[-1]) + "\"\n    ]\n}"
        return result


def get_follows(ID, driver, follows_count):
    url = "http://www.dianping.com/member/" + str(ID) + "/follows"
    driver.get(url)
    content = driver.page_source
    content = content.split("\n")
    beginning_point = 0
    connection = Connection()
    empty = 0
    for line in content:
        beginning_point = beginning_point + 1
        if line.find("modebox empty") != -1:
            empty = 1
    if empty == 1 and follows_count != 0:
        connection.follows = set([-1, -1])
        print 'this guy did not make his follows public'
        return connection
    pages = follows_count / 30
    for i in range(1, pages + 2):
        if i % 5 == 0:
            print 'follows:' + str(i) + '/' + str(pages+1)
        time.sleep(random.randint(3, 4))
        url = "http://www.dianping.com/member/" + str(ID) + "/follows?pg=" + str(i)
        driver.get(url)
        content = driver.page_source
        content = content.split("\n")
        beginning_point = 0
        for line in content:
            beginning_point = beginning_point + 1;
            if line.find("href=\"/member/") != -1 and line.find("fans") != -1:
                break
        for line in content[beginning_point + 2:]:
            if line.find("href=\"/member/") != -1:
                connection.follows = connection.follows + [get_number(line, "href=\"/member/", "\"")]
    connection.follows = set(connection.follows)
    return connection


def get_number(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return int(line[i+len(pre):j])
