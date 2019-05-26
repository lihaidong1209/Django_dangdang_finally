from django.db import transaction
from django.shortcuts import render,HttpResponse
import random,string
import os
from captchaapp.captcha.image import ImageCaptcha

def getcaptcha(request):
    try:
        with transaction.atomic():
            image = ImageCaptcha()
            random_code = random.sample(string.ascii_letters + string.digits,5)
            random_code = "".join(random_code)
            print(random_code)
            request.session["number"] = random_code
            data = image.generate(random_code)

            return HttpResponse(data, "image/png")
    except:
        return HttpResponse("请重试")



