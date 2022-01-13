#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Shanfenglan
# datetime:2022/1/10 2:45 PM
# In god's hands.


import os,xlwt, threading,tqdm, time,ip2Region,sys
from xml import dom




def org_city(ip):
    dbfile = "/Users/zhujiayu/tools/others/ip2region/data/ip2region.db"
    ip = ip.strip("[]")
    test = ip2Region.Ip2Region(dbfile)
    c = test.memorySearch(ip)
    out = c['region'].decode("utf-8")
    out = out.split('|')
    a = []
    a.append("/".join(out[0:4]))
    out[0:4] = a
    b= []
    # ip=ip.strip("[]")
    # a = []
    # url = "https://ipinfo.io/"
    # token = "?token=c1ad3714f3944c"
    #
    # r = requests.get(url + ip +token)
    #
    # data = json.loads(r.text)
    # # print(data)
    try:
        city = str(out[0])
    except:
        city="无数据"
    b.append(city)
    try:
        org = str(out[1])
    except:
        org="无数据"
    b.append(org)
    return b

def optmize(a):
    if "[cdn]" != a[len(a)-1]:
        a.append(" ")


def formatting():
    #得到httpx的解析数据
    buf=[]
    with  open("2.txt", "r") as f:
        for i in f:
            i=i.strip()
            i=i.split(" ")
            optmize(i)
            c = "".join(i[2:-2])
            b = []
            b.append(c)
            del i[2:-2]
            i[2:2] = b
            buf.append(i)
    print("收集完毕，共有{0}条数据".format(len(buf)))
    return buf


def fun2(i,buf):
    lock.acquire()
    # print("传入前{0}".format(buf[i]))
    buf[i][4:4] = org_city((buf[i][3]))
    # print("增加后{0}".format(buf[i]))
    lock.release()

def zengjiashuju(buf):
    #增加解析数据
    hang = len(buf)
    t=''
    tt=[]
    print("正在进行运营商与归属地查询......")
    for i in tqdm.tqdm(range(hang)):
    # for i in range(hang):
        t= threading.Thread(target=fun2, args=(i,buf,))
        # time.sleep(0.01)
        t.start()
        tt.append(t)
    for i in tt:
        # print("等待线程{0}执行完成".format(i.getName()))
        i.join()
    print("运营商与归属地查询完成.......")
    return buf



def output_excel(buf,name):
    print("正在将结果转化为excel文件......")
    workbook = xlwt.Workbook(encoding='utf-8')       #新建工作簿
    sheet1 = workbook.add_sheet("测试表格")          #新建sheet
    sheet1.write(0,0,"url")      #第1行第1列数据
    sheet1.write(0,1,"状态码")  # 第1行第2列数据
    sheet1.write(0,2,"title")      #第1行第2列数据
    sheet1.write(0,3,"ip")      #第1行第2列数据
    sheet1.write(0,4,"归属地")      #第1行第2列数据
    sheet1.write(0,5,"服务商")      #第1行第2列数据
    sheet1.write(0,6, "cdn")  # 第1行第2列数据
    hang=len(buf)
    for i in tqdm.tqdm(range(hang)):
    # for i in range(hang):

        for ii in range(7):
            # print(buf[i][ii])
            sheet1.write(i + 1, ii, buf[i][ii].strip("[]"))

    path = os.getcwd()+'/'+name+'.xlsx'
    workbook.save(path)   #保存
    print("结果保存到："+path)


if __name__ == '__main__':
    lock = threading.Semaphore(20)

# port = "80,81,82,83,84,85,86,87,88,89,90,91,92,98,99,443,800,801,808,880,888,889,1000,1010,1080,1081,1082,1118,1888,2008,2020,2100,2375,2379,3000,3008,3128,3505,5555,6080,6648,6868,7000,7001,7002,7003,7004,7005,7007,7008,7070,7071,7074,7078,7080,7088,7200,7680,7687,7688,7777,7890,8000,8001,8002,8003,8004,8006,8008,8009,8010,8011,8012,8016,8018,8020,8028,8030,8038,8042,8044,8046,8048,8053,8060,8069,8070,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8096,8097,8098,8099,8100,8101,8108,8118,8161,8172,8180,8181,8200,8222,8244,8258,8280,8288,8300,8360,8443,8448,8484,8800,8834,8838,8848,8858,8868,8879,8880,8881,8888,8899,8983,8989,9000,9001,9002,9008,9010,9043,9060,9080,9081,9082,9083,9084,9085,9086,9087,9088,9089,9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,9100,9200,9443,9448,9800,9981,9986,9988,9998,9999,10000,10001,10002,10004,10008,10010,10250,12018,12443,14000,16080,18000,18001,18002,18004,18008,18080,18082,18088,18090,18098,19001,20000,20720,21000,21501,21502,28018,20880"
    start = time.time()
    print("开始进行子域名收集")


    domain = sys.argv[1]

    cmd = "echo {0} | subfinder  -silent -t 20| httpx -silent -status-code -title -ip -nc -cdn -fc 403,404,400".format(domain)
    print("执行的命令为："+cmd)
    p = os.popen(cmd)
    x = p.read()
    with  open("2.txt", "w+") as f:
        f.write(x)
    buf = formatting()
    buf = zengjiashuju(buf)
    output_excel(buf=buf,name=domain)
    end = time.time()
    print("\n\n\n总共花费{0}秒".format(int(end - start)))