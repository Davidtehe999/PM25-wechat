import requests
from bs4 import BeautifulSoup
from wxpy import *

class PM25:
    def __init__(self, city):
        #city用拼音，这个网站支持很多城市
        self.url = "http://www.pm25.com/" + str(city) + ".html/"
        self.web = requests.get(self.url).text
        self.soup = BeautifulSoup(self.web, "html.parser")
        self.aqi = self.soup.find(name="a", attrs={"class": "bi_aqiarea_num"}).text
        self.weather = self.soup.find(name="p", attrs= {"class": "bi_info_weather"}).text

    def show_aqi(self):
        city_aqi = self.aqi
        return city_aqi

    def show_weather(self):
        city_weather = self.weather[1:]
        return city_weather

def wechat(groupName, cityName):
    '''
    wxpy的文档:https://wxpy.readthedocs.io/zh/latest/index.html
    Bot()方法的几个参数:
    console_qr=2:在终端显示二维码，命令行必用
    cache_pate=True:一次登陆以后缓存一定时间
    '''
    bot = Bot(cache_path=True, console_qr=2)

    group = bot.groups().search(groupName)[0]
    @bot.register(group, TEXT)
    def reply_api(msg):
        if msg.text == "天气":
            pM25 = PM25(cityName)
            aqi = pM25.show_aqi()
            weather = pM25.show_weather()

            air_index = int(aqi)
            message = {"good":"空气很好，适宜出门！",
                       "normal":"空气一般，户外时间不宜过长。",
                       "bad":"空气不好，不建议出门。",
                       "worse":"空气很糟糕，不要出门，家里开空气净化器！"}
            if air_index <= 40:
                air_msg = message["good"]
            elif 40 < air_index <= 70:
                air_msg = message["normal"]
            elif 70 < air_index <= 100:
                air_msg = message["bad"]
            elif air_index > 100:
                air_msg = message["worse"]
            group.send("当前重庆空气质量指数:" + aqi + "@" + air_msg +"@     本日天气:" + weather)
    
    embed()


wechat("groupName", "city")
