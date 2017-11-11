# SinaWeiboSpider
新浪微博较为完善的爬虫，持续改进，欢迎star~

## 安装
## pip install weibospider

## 特色

+ 模仿77的zhihu-oauth， 用户提供微博id构用于建对应类的对象，可以获取到某些需要的数据
+ 需要手动粘贴cookie， 下文有对应教程。因为自动登录WAP版微博到现在还没有一个很好的办法。加密方式未知，且验证码反人类。
+ 用到了许多装饰器与生成器的有关知识，可以学习参考

## 简单例子

```
    from weibospider import WeiboClient
   
    cookies = 'xxxxxxxxxxxx'  # 通过在weibo.cn登录后，F12查看network选项获取

    myclient = WeiboClient(cookies)

    people_1 = myclient.people('1884866222')  #某目标用户的uid

    print(people_1.name)    #打印people_1的用户名

    print(people_1.weibo_count)   #打印people_1的发表的微博数

    for index, weibo in zip(range(10), people_1.weibo):

        print(weibo.text)         #打印people_1发表的最近10条微博

        for index_2, comment in zip(range(5), weibo.comment):

            print(comment.text)   #打印此微博的最近5条评论

            print(comment.author_name) #打印此评论对应的作者


```

如有疑问可邮箱 or QQ联系