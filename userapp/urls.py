from django.contrib import admin
from django.urls import path
from userapp import views

app_name = 'userapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    # 注册
    path('register/', views.register, name='register'),
    path('registerlogic/', views.registerlogic, name='registerlogic'),

    path('register_ok/', views.register_ok, name='register_ok'),
    # 登录
    path('login/', views.login, name='login'),
    path('loginlogic/', views.loginlogic, name='loginlogic'),
    # ajax异步验证路径
    path('email/', views.email, name='email'),     #邮箱
    path('re_name/', views.re_name, name='re_name'),  # 昵称
    path('re_password/', views.re_password, name='re_password'),  # 密码
    path('changeCaptcha/', views.changeCaptcha, name='changeCaptcha'),  # 验证码
    path('login_email/', views.login_email, name='login_email'),  # 验证码
    path('del_cookie/', views.del_cookie, name='del_cookie'),  # 验证码

]