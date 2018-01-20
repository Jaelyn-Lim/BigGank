#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/01/2018 22:49
# @Author  : Jaelyn
# @Site    : 
# @File    : catchData.py
# @Software: PyCharm

import urllib.request, json, pymysql

'''
{'source': 'web', 'publishedAt': '2017-12-19T12:00:28.893Z', 'who': 'D_clock', 'desc': '酷酷的Android Loading动画，让用户摆脱无聊等待', 'used': True, '_id': '5a3875e6421aa90fe72536c4', 'type': 'Android', 'url': 'http://mp.weixin.qq.com/s/S6NCv-o_kp22hFtwn-84Mg', 'createdAt': '2017-12-19T10:13:58.688Z'}
'''


class Catch:

    def __init__(self):
        self.url = 'http://gank.io/api/data/all/200/1'
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='gank', charset='utf8')
        self.cursor = self.db.cursor()
        # cursor.execute("SELECT VERSION()")
        # data = cursor.fetchone()
        # print("Database version : %s " % data)

    def catchdata(self):
        stdout = urllib.request.urlopen(self.url)
        dataInfo = stdout.read().decode('utf-8')
        # print(dataInfo)
        self.jsonData = json.loads(dataInfo)
        # print(self.jsonData["results"][0])

    def save(self):
        for i in range(100):
            _id = self.jsonData["results"][i]["_id"]
            source = self.jsonData["results"][i]["source"]
            publishedAt = self.datatimeset(self.jsonData["results"][i]["publishedAt"])
            who = self.jsonData["results"][i]["who"]
            desc = self.jsonData["results"][i]["desc"]
            used = self.jsonData["results"][i]["used"]
            text_type = self.jsonData["results"][i]["type"]
            createdAt = self.datatimeset(self.jsonData["results"][i]["createdAt"])
            url = self.jsonData["results"][i]["url"]

            if used:
                used = 1
            else:
                used = 0

# INSERT INTO `info` (`id`, `_id`, `createdAt`, `desc`, `publishedAt`, `source`, `typy`, `url`, `used`, `who`) VALUES (NULL, '123123', '2018-01-01 00:00:00', 'awe', '2018-01-03 00:00:00', 'and', 'awe', 'awe', '1', 'awe');
# INSERT INTO `info` (`id`, `_id`, `source`, `publishedAt`, `who`, `desc`, `used`, `type`, `createdAt`, `url`) VALUES (NULL, '576e5468421aa931d70b5f52', 'api', '2018-01-16 08:40:08', 'tripleCC', 'iOS应用架构谈 view层的组织和调用方案 - Casa Taloyum', '1', 'iOS', '2016-06-25 17:52:40', 'http://casatwy.com/iosying-yong-jia-gou-tan-viewceng-de-zu-zhi-he-diao-yong-fang-an.html')

            sql = "INSERT INTO `info` (`id`, `_id`, `source`, `publishedAt`, `who`, `desc`, `used`, `typy`, `createdAt`, `url`)" \
                  " VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(_id, source, publishedAt, who, desc,
                                                                                    used, text_type,
                                                                                    createdAt, url)

            print(sql)

            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
                print(i, _id, source, publishedAt, who, desc, used, text_type, createdAt, url)
            except:
                # 如果发生错误则回滚
                self.db.rollback()
                print(i, '错误')

        self.db.close()


    def datatimeset(self, str):
        list = str.split('T')
        dataa = list[0]
        timee = list[1][0:8]
        return('{} {}'.format(dataa, timee))


if __name__ == '__main__':
    catch = Catch()
    catch.catchdata()
    catch.save()
    # print(catch.datatimeset('2016-06-25T17:52:40.885Z'))
