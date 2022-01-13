#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Shanfenglan
# datetime:2022/1/10 2:45 PM
# In god's hands.


import os,xlwt,requests,json,threading,tqdm,datetime,time,ip2Region,sys




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


def formatting(pathh):
    #得到httpx的解析数据
    print("深度收集原始数据信息:"+pathh)
    buf=[]
    with  open(pathh, "r") as f:
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

    path1 = os.getcwd()+'/result/'+name+'.xlsx'
    workbook.save(path1)   #保存
    print("最终结果保存到："+path1)

if __name__ == '__main__':
    lock = threading.Semaphore(20)
    start = time.time()

    domain = sys.argv[1]

    path = os.getcwd()+'/raw/'+domain+'.txt'
    buf = formatting(path)
    buf = zengjiashuju(buf)
    output_excel(buf=buf,name=domain)
    end = time.time()
    print("\n\n\n总共花费{0}秒".format(int(end - start)))
