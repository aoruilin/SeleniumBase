if __name__ == '__main__':
    # coding=utf8
    # 12306查票爬虫
    import requests, json
    import sys

    # 获取地址代码
    # https://kyfw.12306.cn/otn/resources/js/framework/favorite_name.js

    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9025'
    url_tmp = str(requests.get(url, verify=False).content, encoding='utf-8').replace("var station_names ='@",
                                                                                     '').replace(
        "';", '')
    url_tmp = list(url_tmp.split('@'))


    def dizhi_code(dizhi):
        '''
        通过站点名字获取code
        '''
        for i in url_tmp:
            if dizhi == i.split('|')[1]:
                return i.split('|')[2]


    def code_dizhi(code):
        '''
        通过code获取站点名字
        '''
        #    print (url_tmp)
        for i in url_tmp:
            if code == i.split('|')[2]:
                return i.split('|')[1]


    def get_lieche(start_che, end_che, date):

        start_che = dizhi_code(start_che)
        end_che = dizhi_code(end_che)
        #   print (start_che,end_che)
        try:
            url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_' \
                f'station={start_che}&leftTicketDTO.to_station={end_che}&purpose_codes=ADULT'
            #       print (url)
            data = json.loads(requests.get(url, verify=False).content)
        except Exception as e:
            print("获取数据失败，可能网络错误或者请求太频繁", e)
            sys.exit(2)

        chuli_data = []
        for i in data['data']['result']:
            list_che = list(i.strip('|').split('|'))
            if list_che[0] == "23:00-06:00系统维护时间" or list_che[0] == "预订":
                # 时间         列车班号    始发站                  终点站                  始发时间     终点时间    一共时间    商务座      一等座        二等座       软卧          硬卧
                chuli_data.append((che_time, list_che[2], code_dizhi(list_che[3]), code_dizhi(list_che[4]), list_che[7],
                                   list_che[8], list_che[9], list_che[-4], list_che[-5], list_che[-6], list_che[-13],
                                   list_che[-8], list_che[-7]))
            else:
                chuli_data.append((che_time, list_che[3], code_dizhi(list_che[4]), code_dizhi(list_che[5]), list_che[8],
                                   list_che[9], list_che[10], list_che[-4], list_che[-5], list_che[-6], list_che[-13],
                                   list_che[-8], list_che[-7]))
        #        print (list_che)
        #   print (chuli_data)
        print("时间   \t\t始发站\t终点站\t始发时间\t终点时间\t一共时间\t商务座\t一等座\t二等座\t软卧\t硬卧\t硬座\t列车班号")
        for i in chuli_data:
            #        print (i)
            print("%s\t%s\t%s\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s" % (
                i[0], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[1]))


    if __name__ == '__main__':
        # get_lieche("重庆","北京",'2017-09-06')
        start_zhan = input("请输入起始站：")
        end_zhan = input("请输入终点站：")
        che_time = input("请输入时间范例2017-09-03：")
        if start_zhan == "" or end_zhan == "" or che_time == "":
            print("站点名错误")
            sys.exit(1)
        #   elif che_time=="":
        #        che_time=datetime.date()

        get_lieche(start_zhan, end_zhan, che_time)
