from django.db import models

# Create your models here.
#用户验证邮箱
class Email(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True ,verbose_name="用户名")
    name = models.CharField(max_length=30, blank=True, null=True,verbose_name="昵称")
    password = models.CharField(max_length=100, blank=True, null=True,verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")
    code = models.CharField (max_length=256,verbose_name="用户注册码")
    c_time  =models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "t_email"


