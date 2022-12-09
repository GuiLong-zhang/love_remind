import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():

    # appId
    # app_id = config["app_id"]
    app_id = "wx85fe515f01a962eb"
    # appSecret
    # app_secret = config["app_secret"]
    app_secret = "f8627cb23fb4662fc17baccdec1abb38"
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def send_message(to_user, access_token, remind):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    time_hour = int(datetime.now().strftime("%H"))+8
    if time_hour > 24:
        time_hour = time_hour - 24
    time_now = str(str(time_hour)+":" + datetime.now().strftime("%M"))
    template = "aGrgx9QvtfBZsw-h4J83ojoqExdZ6Ua2xYx69vKPop0"
    data = {
        "touser": to_user,
        "template_id": template,
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "time_now": {
                "value": time_now,
                "color": get_color()
            },
            "remind": {
                "value": remind,
                "color": get_color()
            }
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)

def time():
    timer = datetime.now()
    timer = int(timer.strftime('%H'))
    print(timer)
    if timer < 8:
        timer = 1
    elif 8 < timer < 12:
        timer = 2
    else:
        timer = 3
    return timer

if __name__ == "__main__":
    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = ["o31k-5ovUr7P4_cnyMvRfl2zUFnA", "o31k-5kec9LRbztWlvRiGctiX5L8"]
    timer = time()
    remind = "该喝今天第{}顿药了！别忘了哟！！！".format(timer)
    print(remind)
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, remind)


