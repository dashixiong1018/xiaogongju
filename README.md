# xiaogongju
豆瓣读书爬虫  
此项目使用python3，采用很牛逼的scrapy框架  
运行方法:  
1.将项目下载到本地，cd到项目目录下，安装依赖库pip3 install -r request.txt  
2.在项目目录下，运行命令：scrapy crawl doubanBook  
3.此项目已部署在云服务器上，本地安装scrapyd-client，在终端运行：curl http://34.80.13.90:6800/schedule.json -d project=xiaogongju -d spider=doubanBook  
打开浏览器，输入：http://34.80.13.90:6800/ -->Jobs中就能看到此项目的运行情况  

  

  
  
  
  
改进:  
1.爬取豆瓣所有标签下的图书，但是只能每个标签下前50页的图书  
2.爬取十万数据，每个链接的访问延迟是2s，总共花费3+H  
3.所有图书存储在doubanBook数据库的book表中  
4.浏览器中，log显示中文乱码，下周再改  
