# SinaWeiboSpider
新浪微博较为完善的爬虫，持续改进，欢迎star~

注：由于本人没注意自动登录获取的cookies是wp极简版的，而不是普通网页版的
    所以在自动登录情况下 SinaPeople类无法使用
    SinaWeibo类仍可以正常使用（因其不需登录即可查看，新浪的BUG）
    
    解决方法：
       手动利用chrome工具获取极简版登录后的cookies，将base.SinaBaseObject中的cookies改成此值即可
       优点：由于是极简版，速度快
       缺点：需要手动，每天更新cookies


最近是考试月。。过了6月29日 再更新一下使用说明 万分抱歉！
