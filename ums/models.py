from django.db import models


# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True, max_length=32)  # id
    sno = models.CharField(max_length=32)  # 学号
    spassword = models.CharField(max_length=32)  # 密码
    sname = models.CharField(max_length=32)  # 姓名
    sgrade = models.CharField(max_length=32)  # 年级
    sbirthday = models.CharField(max_length=32)  # 生日

    @staticmethod
    def get_title_list():
        return ["id", "学号", "密码", "姓名", "年级", "生日"]


class Teacher(models.Model):
    id = models.AutoField(primary_key=True, max_length=32)  # id
    tno = models.CharField(max_length=32)  # 工号
    tpassword = models.CharField(max_length=32)  # 密码
    tname = models.CharField(max_length=32)  # 姓名
    tcollege = models.CharField(max_length=32)  # 学院
    tbirthday = models.CharField(max_length=32)  # 生日

    @staticmethod
    def get_title_list():
        return ["id", "工号", "密码", "姓名", "学院", "生日"]


class Task(models.Model):
    id = models.AutoField(primary_key=True, max_length=32)  # id
    title = models.CharField(max_length=1024)  # 任务名称
    content = models.CharField(max_length=2048)  # 任务内容
    exectime = models.CharField(max_length=32)  # 执行时间
    studentid = models.IntegerField(max_length=11)  # 创建学生

    @staticmethod
    def get_title_list():
        return ["id", "任务名称", "任务内容", "执行时间", "创建学生"]
