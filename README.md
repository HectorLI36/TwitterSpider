# 一个简单的tweepy示范(Turtioul for tweepy by python)
## 内容描述
    本项目使用Twitter官方的api获取数据，并对数据进行简要的分析，最终生成词频报告，可视化为图云的形式。
    几个步骤将分别进行介绍几个脚本所做的事情。
    


##tweepy_data_source.py

<h4>准备工作<h4>

    此脚本主要做的是获取某一用户（此项目以曼联官方推特账户为例）发送的所有tweet，并将点赞数量超过1k的推文保存下来。
    值得注意的是，由于众所周知的原因，国内访问Twitter并不是那么顺畅。本机配置了shadowsocks代理，由于ss使用sock5协议，
    tweepy包使用http/https协议，ss将不会对其进行代理。有相同情况的朋友需要为shadowsocks配置http代理。
    参考 http://blog.csdn.net/shaobo8910/article/details/53908639
    
    获取数据时，tweepy采用大家比较熟悉的游标Cursor形式，函数中若干参数请自己体会，需要用时调用即可。


##selenium_spider.py

<h4>脚本描述<h4>

    本脚本使用著名的抓取动态网页的插件selenium抓取Twitter内容，好处是不需要登录和使用tweepy，并且理论上不受Twitter对抓取
    数量的限制。实机应用时发现，此脚本虽然可以完成相关任务,但由于Twitter的策略，当某个未登录用户访问时，返回的不是严格且完整
    的时间线（参考微博）。由于时（lan）间（de）紧（gao）张（le），最终放弃这个脚本，仅为测试selenium的用法和一种思路的验证。
    理论上来讲，加入去重机制，慢慢爬取很多页面，也能完成任务。
    
    具体而言，首先，代码中定义好浏览器driver在本地的存储路径以便调用。实例化后绑定在driver上，剩下的使用步骤请参考代码。
```
def crawl(url):
    chromedriverPath = "你的本地driver地址"
    # twitter每次更新13条
    eachCount = 13
    # 滚动几次。滚动次数越多，采集的数据越多
    scrollTimes = 100
    # driver = webdriver.Firefox()
    driver = webdriver.Chrome(chromedriverPath)
    driver.get(url)
    try:
        for i in range(scrollTimes):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            lastTweetCss = "#stream-items-id >li:nth-of-type(" + str(eachCount * (i + 2) + 1) + ") .tweet-text"
            print lastTweetCss
            elem = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, lastTweetCss)))
            printTweet(driver)
    finally:
        driver.close()
```
    
##生成词云
词云是一种分析文章关键字生成的一张图片，图片上关键字大小反映了词频。生成的图云对于直观分析数据内容有很大的帮助，并且看上去非常高大上，适合做在ppt中。
生成的方法也非常简单：
首先是导入几个需要的包：

```
import sys
sys.setdefaultencoding( "utf-8" )

from PIL import Image
import numpy as np

from wordcloud import WordCloud, ImageColorGenerator
```
这几个包都很有名，不需要赘述了。下面是生成图片的过程：
```
my_mask = np.array(Image.open('你的mask图片路径'))
world_cloud = WordCloud(background_color='white',
                        max_words=2000, scale=3
	                    ).generate(text)  # text为读入的文本文件
world_cloud.to_file("存储路径")
image_colors = ImageColorGenerator(my_mask)
# 这一行可以生成与mask图片色调相符的字体颜色，效果见下面的图片。

plt.imshow(world_cloud, interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(world_cloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(my_mask, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()
world_cloud.to_file("存储路径2")
```
这段代码生成了两种词云图，并且可以在一个‘mask’基础上生成，效果不错。

![这里写图片描述](http://img.blog.csdn.net/20170802175558498?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvaGVjdG9ybGkzNg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
硕大的何塞·穆里尼奥。。。

![这是采用了mask图片后生成的，较为美观](http://img.blog.csdn.net/20170802175629160?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvaGVjdG9ybGkzNg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
本次做的是英文项目，所以不存在中文分词的问题。如果需要生成针对中文的词云图，请使用结巴分词。

##生成词频报告

人生苦短，我用Python。直接用collection里的Counter就好了。
需要将文件读入并打散成list的形式。对于中文，请采用结巴分词。

```
    with open('report_final.txt', 'w') as report:
        c = Counter(total)
        for tmp in c.most_common():
            print （tmp）
            report.write(str(tmp) + '\n')
```

