import json
import os
import traceback
import uuid

from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from . import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

# encoding=utf-8
import random
# import matplotlib.pyplot as plt
import string
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

filename = "D:/pycharm/workprojects/University/static/yzm/"
# 字体的位置，不同版本的系统会有不同BuxtonSketch.ttf
font_path = 'C:/Windows/Fonts/Georgia.ttf'
# font_path = 'C:/Windows/Fonts/默陌肥圆手写体.ttf'
# 生成几位数的验证码
number = 4
# 生成验证码图片的高度和宽度
size = (129, 53)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (0, 0, 0)
# 干扰线颜色。默认为红色
linecolor = (0, 0, 0)
# 是否要加入干扰线
draw_line = True
# 加入干扰线条数的上下限
line_number = (1, 5)


# 用来随机生成一个字符串
def gene_text():
    # source = list(string.letters)
    # for index in range(0,10):
    #     source.append(str(index))
    source = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # source = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J', 'K','L', 'M', 'N','O','P','Q','R',
    #           'S', 'T', 'U', 'V', 'W', 'Z','X', 'Y']
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


# 用来绘制干扰线
def gene_line(draw, width, height):
    # begin = (random.randint(0, width), random.randint(0, height))
    # end = (random.randint(0, width), random.randint(0, height))
    begin = (0, random.randint(0, height))
    end = (74, random.randint(0, height))
    draw.line([begin, end], fill=linecolor, width=3)


def createVerify():
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片
    font = ImageFont.truetype(font_path, 40)  # 验证码的字体
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = gene_text()  # 生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text, \
              font=font, fill=fontcolor)  # 填充字符串
    if draw_line:
        gene_line(draw, width, height)
    image = image.transform((width + 30, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    # image = image.transform((width+20,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    # a = str(m)
    aa = str(".png")
    path = filename + text + aa
    # path = filename + 'yzm' + aa;
    # cv2.imwrite(path, I1)
    # image.save('idencode.jpg') #保存验证码图片
    image.save(path)
    return text


def getVerify(request):
    text = createVerify()
    aa = str(".png")
    request.session['yzm'] = text;
    return JsonResponse({"code": 200, "message": "获取验证码成功", 'data': '/static/yzm/' + text + aa}, safe=False)


def getUserInfo(request):
    username = request.session['loginAccount'];
    type = request.session['loginType'];
    id = request.session['loginId'];
    data = "{\"username\":\"" + username + "\",\"type\":\"" + type + "\",\"id\":" + str(id) + "}";
    return JsonResponse({"code": 200, "message": "获取用户数据成功", 'data': data}, safe=False);


def logout(request):
    request.session['loginId'] = None;
    request.session['loginType'] = None;
    request.session['loginAccount'] = None;
    return JsonResponse({"code": 200, "message": "账号退出成功"}, safe=False)


def loginCon(request):
    if request.method == 'POST':
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        verify = request.POST.get("verify", None)
        type = request.POST.get("type", None)
        if verify == None:
            return JsonResponse({"code": 400, "message": "验证码不能为空"}, safe=False)
        if username == None or password == None:
            return JsonResponse({"code": 400, "message": "用户名或密码不能为空"}, safe=False)
        yzm = request.session['yzm'];
        print('yzm', yzm)
        if yzm != verify:
            return JsonResponse({"code": 400, "message": "验证码不正确"}, safe=False)
        if type == 'student':
            studentList = models.Student.objects.filter(sno=username, spassword=password).values()
            if studentList.count() > 0:
                print(studentList[0])
                print(studentList[0]['id'])
                request.session['loginId'] = studentList[0]['id'];
                request.session['loginType'] = 'student'
                request.session['loginAccount'] = username
                return JsonResponse({"code": 200, "message": "账号验证成功", 'data': list(studentList)},
                                    safe=False)
            else:
                return JsonResponse({"code": 400, "message": "用户名或密码不正确"}, safe=False)
        else:
            teacherList = models.Teacher.objects.filter(tno=username, tpassword=password).values()
            if teacherList.count() > 0:

                request.session['loginId'] = teacherList[0]['id'];
                request.session['loginType'] = 'teacher'
                request.session['loginAccount'] = username
                print(request.session.get('loginAccount'))
                return JsonResponse({"code": 200, "message": "账号验证成功", 'data': list(teacherList)},
                                    safe=False)
            else:
                return JsonResponse({"code": 400, "message": "用户名或密码不正确"}, safe=False)


def addStudent(request):
    if request.method == 'POST':
        sno = request.POST.get("sno", None)
        spassword = request.POST.get("spassword", None)
        sname = request.POST.get("sname", None)
        sgrade = request.POST.get("sgrade", None)
        sbirthday = request.POST.get("sbirthday", None)

        studentList = models.Student.objects.filter(sno=sno).values()
        if studentList.count() > 0:
            return JsonResponse({"code": 401, "message": "该学号已经存在"}, safe=False)

        print(sno, spassword, sname, sgrade, sbirthday)
        if models.Student.objects.create(sno=sno, spassword=spassword, sname=sname, sgrade=sgrade, sbirthday=sbirthday):
            return JsonResponse({"code": 200, "message": "添加成功"}, safe=False)
        else:
            return JsonResponse({"code": 400, "message": "添加失败"}, safe=False)


def editStudent(request):
    if request.method == 'POST':
        id = request.POST.get("id", None)
        sno = request.POST.get("sno", None)
        spassword = request.POST.get("spassword", None)
        sname = request.POST.get("sname", None)
        sgrade = request.POST.get("sgrade", None)
        sbirthday = request.POST.get("sbirthday", None)

        if models.Student.objects.filter(id=int(id)).update(sno=sno, spassword=spassword, sname=sname, sgrade=sgrade,
                                                            sbirthday=sbirthday):

            return JsonResponse({"code": 200, "message": "编辑成功"}, safe=False)
        else:
            return JsonResponse({"code": 400, "message": "编辑失败"}, safe=False)


def getStudent(request):
    id = request.GET.get("id", None)
    student = models.Student.objects.values().get(id=int(id))
    return JsonResponse({"code": 200, "message": "查询成功", 'data': student}, safe=False)


def delStudent(request):
    if request.method == 'POST':
        id = request.POST.get("id", None)
        if models.Student.objects.filter(id=int(id)).delete():
            return JsonResponse({"code": 200, "message": "删除成功"}, safe=False)
        else:
            return JsonResponse({"code": 400, "message": "删除失败"}, safe=False)


def selectStudentByLike(request):
    nowPage = request.GET.get("page")
    limit = request.GET.get("limit")
    param = request.GET.get("param")
    if nowPage == "":
        nowPage = 1
    if limit == "":
        limit = 5
    nowPage = int(nowPage)
    limit = int(limit)
    student = "";
    if param:
        student = models.Student.objects.filter(Q(sno__contains=param) | Q(sname__contains=param)).values()
    else:
        student = models.Student.objects.values()
    paginator = Paginator(list(student), int(limit))
    print(list(student))
    if int(nowPage) >= int(paginator.num_pages):
        nowPage = paginator.num_pages
    try:
        page = paginator.page(nowPage)
    except:
        page = paginator.page(paginator.num_pages)

    data = {
        'data': list(page),
        'code': "0",
        'message': '查询成功',
        'total': paginator.count,
        'page': page.number,
        'limit': page.__len__(),
        'pages': paginator.num_pages

    }
    return JsonResponse(data)


basedir = os.path.abspath(os.path.dirname(__file__))


def up_photo(request):
    try:
        img = request.files.get('photo')
        path = basedir + "/static/upload/"
        print(path)
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))

        file_path = path + suid + '_' + img.filename
        img.save(file_path)
        print(img.filename + "," + img.__sizeof__())
        return JsonResponse({"code": 200, "message": "照片上传成功", "url": suid + '_' + img.filename}, safe=False)

    except:
        traceback.print_exc()
        return JsonResponse({"code": 400, "message": "照片上传失败"}, safe=False)


def addTask(request):
    if request.method == 'POST':
        title = request.POST.get("title", None)
        content = request.POST.get("content", None)
        exectime = request.POST.get("exectime", None)
        studentid = request.session['loginId'];

        print(title, content, exectime, studentid)
        if models.Task.objects.create(title=title, content=content, exectime=exectime, studentid=studentid):
            return JsonResponse({"code": 200, "message": "添加成功"}, safe=False)
        else:
            return JsonResponse({"code": 400, "message": "添加失败"}, safe=False)


def editTask(request):
    if request.method == 'POST':
        id = request.POST.get("id", None)
        title = request.POST.get("title", None)
        content = request.POST.get("content", None)
        exectime = request.POST.get("exectime", None)
        studentid = request.session['loginId'];

        if models.Task.objects.filter(id=int(id)).update(title=title, content=content, exectime=exectime,
                                                         studentid=studentid):

            return JsonResponse({"code": 200, "message": "编辑成功"}, safe=False)
        else:
            return JsonResponse({"code": 400, "message": "编辑失败"}, safe=False)


def getTask(request):
    id = request.GET.get("id", None)
    task = models.Task.objects.values().get(id=int(id))
    return JsonResponse({"code": 200, "message": "查询成功", 'data': task}, safe=False)


def delTask(request):
    if request.method == 'POST':
        id = request.POST.get("id", None)
        if models.Task.objects.filter(id=int(id)).delete():
            return JsonResponse({"code": 200, "message": "删除成功"}, safe=False)
        else:
            return JsonResponse({"code": 400, "message": "删除失败"}, safe=False)


def selectTaskByLike(request):
    nowPage = request.GET.get("page")
    limit = request.GET.get("limit")
    param = request.GET.get("param")
    studentid = request.session['loginId'];
    if nowPage == "":
        nowPage = 1
    if limit == "":
        limit = 5
    nowPage = int(nowPage)
    limit = int(limit)
    task = "";
    if param:
        task = models.Task.objects.filter(Q(studentid=studentid), Q(title__contains=param)).values()
    else:
        task = models.Task.objects.filter(studentid=studentid).values()
    paginator = Paginator(list(task), int(limit))
    print(list(task))
    if int(nowPage) >= int(paginator.num_pages):
        nowPage = paginator.num_pages
    try:
        page = paginator.page(nowPage)
    except:
        page = paginator.page(paginator.num_pages)

    data = {
        'data': list(page),
        'code': "0",
        'message': '查询成功',
        'total': paginator.count,
        'page': page.number,
        'limit': page.__len__(),
        'pages': paginator.num_pages
    }
    return JsonResponse(data)
