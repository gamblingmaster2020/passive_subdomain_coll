#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Shanfenglan
# datetime:2022/1/10 2:45 PM
# In god's hands.


import os,xlwt,requests,json,threading,tqdm



semaphore=threading.Semaphore(20)

def org_city(ip):
    ip=ip.strip("[]")
    a = []
    url = "https://ipinfo.io/"
    r = requests.get(url + ip )
    data = json.loads(r.text)
    city = str(data['city'])
    a.append(city)
    a.append(str(data['org']))
    return a

def optmize(a):
    if "[cdn]" != a[len(a)-1]:
        a.append(" ")


def formatting():
    #得到httpx的解析数据
    buf=[]
    with  open("2.txt","r") as f:
        for i in f:
            i=i.strip()
            i=i.split(" ")
            optmize(i)
            c = "".join(i[1:-2])
            b = []
            b.append(c)
            del i[1:-2]
            i[1:1] = b
            buf.append(i)
    print("收集完毕，共有{0}条数据".format(len(buf)))
    return buf

def fun2(i,buf):
    buf[i][3:3] = org_city((buf[i][2]))

def zengjiashuju(buf):
    #增加解析数据
    hang = len(buf)
    t=''
    tt=[]
    print("正在进行运营商与归属地查询......")
    for i in tqdm.tqdm(range(hang)):
    # for i in range(hang):
        t= threading.Thread(target=fun2, args=(i,buf,))
        t.start()
        tt.append(t)
    for i in tt:
        i.join()
    print("运营商与归属地查询完成.......")
    return buf



def output_excel(buf,name):
    print("正在将结果转化为excel文件......")
    workbook = xlwt.Workbook(encoding='utf-8')       #新建工作簿
    sheet1 = workbook.add_sheet("测试表格")          #新建sheet
    sheet1.write(0,0,"url")      #第1行第1列数据
    sheet1.write(0,1,"title")      #第1行第2列数据
    sheet1.write(0,2,"ip")      #第1行第2列数据
    sheet1.write(0,3,"归属地")      #第1行第2列数据
    sheet1.write(0,4,"服务商")      #第1行第2列数据
    sheet1.write(0,5, "cdn")  # 第1行第2列数据
    hang=len(buf)
    for i in tqdm.tqdm(range(hang)):
    # for i in range(hang):

        for ii in range(6):
            # print(buf[i][ii])
            sheet1.write(i + 1, ii, buf[i][ii].strip("[]"))

    path = os.getcwd()+'/'+name+'.xlsx'
    workbook.save(path)   #保存
    print("结果保存到："+path)

if __name__ == '__main__':
    # print("开始进行子域名收集")
    # cmd = "echo hackerone.com | subfinder  -silent -t 20| httpx -silent -title -ip -nc -cdn -fc 403,404"
    # p = os.popen(cmd)
    # x = p.read()
    # with  open("2.txt", "w+") as f:
    #     f.write(x)
    buf = formatting()
    buf = zengjiashuju(buf)
    output_excel(buf=buf,name='1')