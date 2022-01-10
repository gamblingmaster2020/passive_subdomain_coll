# passive_subdomain_coll
利用subfinder、httpx来进行子域名收集，查询ip归属地和服务商并将结果进行格式化输出

# usage

![在这里插入图片描述](https://img-blog.csdnimg.cn/05a96681362140b3a5524e0cee9a84b1.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAU2hhbmZlbmdsYW43,size_20,color_FFFFFF,t_70,g_se,x_16)


修改代码中的cmd为需要执行的命令，例如：

```
echo hackerone.com | subfinder  -silent -t 20| httpx -silent -title -ip -nc -cdn -fc 403,404
cat 1.txt| subfinder  -silent -t 20| httpx -silent -title -ip -nc -cdn -fc 403,404
```

# 结果如下
一共找到5个数据，能访问的有3个，消耗时间47秒
![在这里插入图片描述](https://img-blog.csdnimg.cn/e6afaefdc9ac498ab543f0a57095ce57.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAU2hhbmZlbmdsYW43,size_20,color_FFFFFF,t_70,g_se,x_16)




oneforall看起来找到了70多个子域名，其实能访问的就3个，消耗时间90秒，没有开爆破功能。

![在这里插入图片描述](https://img-blog.csdnimg.cn/352a94f792e240dd922b8f6c791079c8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAU2hhbmZlbmdsYW43,size_19,color_FFFFFF,t_70,g_se,x_16)
