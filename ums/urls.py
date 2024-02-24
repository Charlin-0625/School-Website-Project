# coding=utf-8
from django.urls import include, re_path
from . import views
from . import crud

urlpatterns = [
    # re_path(r'^$', views.home),
    re_path(r'^home/$', views.home),
    re_path(r'^detail/$', views.detail),
    re_path(r'^index/$', views.index),
    re_path(r'^studentManager/$', views.studentManager),
    re_path(r'^studentAdd/$', views.studentAdd),
    re_path(r'^studentEdit/$', views.studentEdit),
    re_path(r'^login/$', views.login),
    re_path(r'^register/$', views.register),
    re_path(r'^welcome/$', views.welcome),

    re_path(r'^taskManager/$', views.taskManager),
    re_path(r'^taskAdd/$', views.taskAdd),
    re_path(r'^taskEdit/$', views.taskEdit),

    re_path(r'^logout/$', crud.logout),
    re_path(r'^loginCon/$', crud.loginCon),
    re_path(r'^addStudent/$', crud.addStudent),
    re_path(r'^editStudent/$', crud.editStudent),
    re_path(r'^getStudent/$', crud.getStudent),
    re_path(r'^delStudent/$', crud.delStudent),
    re_path(r'^selectStudentByLike/$', crud.selectStudentByLike),
    re_path(r'^getVerify/$', crud.getVerify),
    re_path(r'^getUserInfo/$', crud.getUserInfo),

    re_path(r'^addTask/$', crud.addTask),
    re_path(r'^editTask/$', crud.editTask),
    re_path(r'^getTask/$', crud.getTask),
    re_path(r'^delTask/$', crud.delTask),
    re_path(r'^selectTaskByLike/$', crud.selectTaskByLike),

]
