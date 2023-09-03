import requests
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from app01.models import UserInfo


def index(request):
    return HttpResponse("Welcome")


def news(request):
    url = "https://gec.10010.com/content/recommendInfoList"
    payload_header = {
        'Accept': r'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '20',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': r'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36''',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': r'''"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"'''
    }
    payload_data = {
        'pageNum': 1,
        'pageSize': 10
    }
    res = requests.post(url, headers=payload_header, data=payload_data)
    content = res.text
    content_json = res.json()
    print("content:", content)
    print("content_json:", content_json)
    data_list = content_json['data']['list']
    print("data_list:", data_list)
    return render(request, 'news.html', {'news_list': data_list})


def news_unicom(request):
    url = "http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2023/08/news"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    res = requests.get(url, header)
    data_list = res.json()
    print(data_list)
    return render(request, 'news_unicom.html')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        print("request.POST:", request.POST)
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if user == "admin" and pwd == "admin":
            return redirect("https://www.bilibili.com/")
        else:
            return render(request, 'login.html', {"error_msg": "用户名或密码错误"})


def info_list(request):
    # 创建数据
    # UserInfo.objects.create(name="武沛齐", password="123", age=19)
    # UserInfo.objects.create(name="朱虎飞", password="666", age=29)
    # UserInfo.objects.create(name="吴阳军", password="666")

    data_list = UserInfo.objects.all()
    print(data_list)
    return render(request, "info_list.html", {"data_list": data_list})


def info_add(request):
    if request.method == "GET":
        return render(request, 'info_add.html')

    if request.method == "POST":
        print("request.POST:", request.POST)
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        age = request.POST.get("age")

        UserInfo.objects.create(name=user, password=pwd, age=age)
        return redirect("/info/list")


def info_delete(request):
    id = request.GET.get("id")
    UserInfo.objects.filter(id=id).delete()
    return redirect("/info/list")
