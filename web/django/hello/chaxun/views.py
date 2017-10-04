import string
from io import BytesIO
from django.shortcuts import render, get_object_or_404
import os
import random
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import chaxun.captcha
from .models import AccountInfo
from django.contrib.auth.decorators import login_required



def captcha(request):
    """Captcha"""
    size = (120, 40)
    img, chars = chaxun.captcha.create(size=size)
    request.session['captcha'] = chars   # store the content in Django's session store
    buf = BytesIO()  # a memory buffer used to store the generated image
    img.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')  # return the image data stream as image/jpeg format, browser
    # will treat it as an image

@login_required
def index(request):
    return render(request, 'chaxun/index.html')


def query(request):
    identify_number = request.POST['identify_number']
    name = request.POST['name']
    captcha_input = request.POST['captcha']
    if 'captcha' in request.session:
        captcha_stored = request.session['captcha']
        del request.session['captcha']
        if captcha_input.strip() == captcha_stored:
            try:
                query_account = AccountInfo.objects.get(identify_number=identify_number)
            except (KeyError, AccountInfo.DoesNotExist):
                return HttpResponse('身份证信息未找到。')
            if name == query_account.full_name:
                render(request, 'chaxun/account_detail.html', {'account_info': query_account})
            else:
                return HttpResponse('身份信息错误。')
    else:
        return HttpResponse('not found')


