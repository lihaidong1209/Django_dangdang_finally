import re, time
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from modelsapp.models import TUser
from emailapp.models import Email

# Create your views here.
# 注册
def register(request):
    '''
    注册页面渲染函数
    :param request:
    :return:
    '''
    flag = request.GET.get("flag")
    if not flag:
        flag = 1
    return render(request, 'userapp/register.html', {"flag": flag})

def registerlogic(request):
    '''
    注册逻辑函数，
    在点击邮件或者输入手机号的验证码正确后调用，判断验证码是否一致，然后根据flag渲染不同页面
    需要勾选同意条款
    :param request:
    :return:
    '''
    # 获得页面标签
    flag = request.session.get("flag")
    print(flag)
    # 如果没有默认为首页
    if not flag:
        flag = "1"
    # 从数据库查出
    code1 = request.GET.get("code")
    username = request.session.get("name_code")
    result_code = Email.objects.filter(username=username)[0]
    Email.objects.filter(username=username).delete()
    re_name = result_code.name
    password = result_code.password
    code2 = result_code.code
    if code1 == code2:
        # 七天自动登录变量
        reg = request.session.get("reg")
        # 加密密码
        password_salt = make_password(password)
        # 再次验证用户信息
        result = TUser.objects.filter(username=username,name=re_name)
        # 如果符合要求，信息不存在
        if not result:
        # 将用户信息存入数据库
            TUser.objects.create(username=username, name=re_name, password=password_salt)
            request.session["re_name"] = re_name
            request.session["stats"] = username
            # 用于保存cookie
            re = redirect("/userapp/register_ok/?flag=" + str(flag) + "&username=" + username+ "&re_name="+re_name)
            # 如果勾选了七天自动登录，则存cookie
            if reg:
                re.set_cookie("name", username)
                re.set_cookie("password", password)
            return re
    return redirect("/userapp/register/?flag=" + str(flag))

# 登录
def login(request):
    '''
    登录页面函数
    :param request:
    :return:
    '''
    flag = request.GET.get("flag")
    if not flag:
        flag = "1"
    username = request.COOKIES.get("username")
    password = request.COOKIES.get("password")
    if username:
        re_pwd = TUser.objects.filter(username=username)[0].password
        result = check_password(password,re_pwd)
        if result:
            request.session["re_name"] = re_name
            request.session["stats"] = username
            if flag == "1":
                return redirect("indexapp:index")
            elif flag =="2":
                return redirect("indexapp:book_list")
            elif flag =="3":
                return redirect("indexapp:book_details")
            elif flag =="4":
                return redirect("orderapp:car")
            elif flag =="5":
                return redirect("orderapp:indent")
            else:
                return redirect("indexapp:index")
    return render(request,"userapp/login.html",{"flag": flag})

def loginlogic(request):
    '''
    登录逻辑函数，若果直接登录 没有flag，则要求直接跳到首页
    :param request:
    :return:
    '''
    flag = request.GET.get("flag")
    if not flag:
        flag = "1"
    username = request.POST.get("txtUsername")
    password = request.POST.get("txtPassword")
    reg = request.POST.get("reg")
    if username:
        re_pwd = TUser.objects.filter(username=username)[0].password
        result = check_password(password,re_pwd)
        if result:
            re_name = TUser.objects.filter(username=username)[0].name
            request.session["re_name"] = re_name
            request.session["stats"] = username
            if flag == "1":
                re = redirect("indexapp:index")
                if reg:
                    re.set_cookie("name", username)
                    re.set_cookie("password", password)
                return re
            elif flag =="2":
                re = redirect("indexapp:book_list")
                if reg:
                    re.set_cookie("name", username)
                    re.set_cookie("password", password)
                return re
            elif flag =="3":
                re = redirect("indexapp:book_details")
                if reg:
                    re.set_cookie("name", username)
                    re.set_cookie("password", password)
                return re
            elif flag =="4":
                re = redirect("orderapp:car")
                if reg:
                    re.set_cookie("name", username)
                    re.set_cookie("password", password)
                return re
            else:
                re = redirect("orderapp:indent")
                if reg:
                    re.set_cookie("username", username)
                    re.set_cookie("password", password)
                return re
    return redirect("/userapp/login/?flag=" + str(flag))

# 注册成功
def register_ok(request):
    '''
    注册成功后渲染函数，包含自动购物按钮也自动跳转
    :param request:
    :return:
    '''
    flag = request.GET.get("flag")
    username = request.GET.get("username")
    return render(request, 'userapp/register ok.html', {"flag": flag, "username": username})


# ========================异步验证======================

#   1  注册异步验证
# 邮箱/手机号验证
def email(request):
    '''
    邮箱与手机号是否可用、是否合法的验证
    :param request:
    :return:
    '''
    time.sleep(2)
    username = request.POST.get("username")
    result = TUser.objects.filter(username=username)
    if username:
        if "@" in username:
            if not result:
                if re.match(r'^\w+@(\w+\.)+(com|cn|net)$', username):
                    return JsonResponse({"result": 1})  # 邮箱可用
                return JsonResponse({"result": 2})  # youxiang格式错误
            return JsonResponse({"result": 3})  # 邮箱被使用
        else:
            if not result:
                if re.match(r'1\d{10}', username):
                    return JsonResponse({"result": 4})  # 手机号可用
                return JsonResponse({"result": 5})  # 手机号格式错误
        return JsonResponse({"result": 6})  # 手机号被使用
    return JsonResponse({"result": 7})  # 不能为空


# 昵称验证
def re_name(request):
    '''
    昵称的验证
    :param request:
    :return:
    '''
    time.sleep(2)
    txt_re_username = request.POST.get("txt_re_username")
    result = TUser.objects.filter(username=txt_re_username)
    if txt_re_username:
        if not result:
            if 4 <= len(txt_re_username) <= 10:
                return JsonResponse({"result": 1})  # 合理,可用
            return JsonResponse({"result": 2})  # 不合理  4-10之间
        return JsonResponse({"result": 3})  # 已存在
    return JsonResponse({"result": 4})  # 不能为空


# 密码验证
def re_password(request):
    '''
    密码要求验证
    :param request:
    :return:
    '''
    time.sleep(2)
    txt_password = request.POST.get("txt_password")
    if txt_password:
        if 6 <= len(txt_password) <= 12:
            if txt_password[0].isalnum():
                if re.match(r'^[a-zA-Z0-9]{1,6}\w{5,6}$', txt_password):
                    return JsonResponse({"result": 1})  # 符合要求
            return JsonResponse({"result": 2})  # 不能以下划线开头
        return JsonResponse({"result": 3})  # 密码长度需要在6-12    --不合理
    return JsonResponse({"result": 4})  # 不能为空

# 验证码验证
def changeCaptcha(request):
    '''
    验证码是否正确的验证
    :param request:
    :return:
    '''
    time.sleep(2)
    captcha = request.POST.get("txt_vcode")
    code = request.session.get("number")
    if captcha:
        if len(captcha) == 5:
            if code.upper() == captcha.upper():
                return JsonResponse({"result": 1})  # 正确
            return JsonResponse({"result": 2})  # 不对
        return JsonResponse({"result": 3})  # 5位
    return JsonResponse({"result": 4})  # 不能为空


# 2       登录异步验证

def login_email(request):
    '''
    登录邮箱、手机号验证
    :param request:
    :return:
    '''
    time.sleep(2)
    username = request.POST.get("username")
    result = TUser.objects.filter(username=username)
    if username:
        if "@" in username:
            if result:
                return JsonResponse({"result": 1})  # 可以使用
            return JsonResponse({"result": 2})  # 不存在
        else:
            if result:
                return JsonResponse({"result": 3})  # 手机号可用
            return JsonResponse({"result": 4})  # 手机号不存在
    return JsonResponse({"result": 5})  # 不能为空

# 退出

def del_cookie(request):
    '''
    点击退出后删除session,包括用户状态，添加的临时购物车状态及恢复区session
    :param request:
    :return:
    '''
    del request.session["re_name"]
    del request.session["stats"]
    cart = request.session.get("cart")
    cart1 = request.session.get("cart1")
    if cart:
        del request.session["cart"]
    if cart1:
        del request.session["cart1"]
    return JsonResponse({"result": 1})
