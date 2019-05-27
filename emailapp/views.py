import hashlib
import time

from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render
from emailapp.models import Email
from datetime import datetime
# Create your views here.


def make_confirm_string(re_name):
    '''
    利用hash和时间盐生成随机的验证码
    :param re_name: 用户昵称
    :return:
    '''
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    h = hashlib.md5()
    re_name += now_time
    h.update(re_name.encode())
    return h.hexdigest()

def post_email(username,code):
    '''
    邮件发送函数
    :param username:  用户名
    :param code:   验证码
    :return:
    '''
    subject =  '来自的注册激活邮件'
    from_email = 'lihaidong1209@sina.com'
    to = '{}'.format(username)
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://{}/userapp/registerlogic/?code={}"target=blank>点击这里激活</a>，\欢迎你来验证你的邮箱，验证结束你就可以登录了！</p>'.format("127.0.0.1:8000",code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def register_verify(request):
    '''
    接受注册表单信息，并生成验证码，保存到临时数据库
    :param request:
    :return:
    '''
    flag = request.GET.get("flag")
    request.session["flag"] = flag
    username = request.POST.get("username")
    request.session["name_code"] = username
    re_name = request.POST.get("re_name")
    password = request.POST.get("password")
    reg = request.POST.get("reg")
    request.session["reg"] = reg
    code = make_confirm_string(re_name)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Email.objects.create(username=username,name=re_name,password=password,email="2709444653@qq.com",code=code,c_time=now_time)
    if "@" in username:
        post_email(username,code)
        return render(request,"userapp/register_verify.html",{"flag":flag,"username":username, "re_name":re_name})
    request.session["code_phone"] = code
    return render(request, "userapp/register_verify.html", {"flag": flag, "username": username, "re_name": re_name, "code":code})

# 手机验证码验证
def changeCaptcha_phone(request):
    '''
    接受ajax请求，手机验证码是否正确判断
    :param request:
    :return:
    '''
    time.sleep(2)
    captcha = request.POST.get("txt_vcode")
    code_phone = request.session.get("code_phone")
    if captcha:
        if code_phone == captcha:
            return JsonResponse({"result": 1})  # 正确
        return JsonResponse({"result": 2})  # 不对
    return JsonResponse({"result": 4})  # 不能为空