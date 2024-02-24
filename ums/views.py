from django.shortcuts import render


# Create your views here.
def register(request):
    return render(request, "register.html")


def login(request):
    type = request.GET.get("type")
    context = {}
    if type == 'teacher':
        context['type'] = 'teacher'
        return render(request, "login.html", context)
    else:
        context['type'] = 'student'
        return render(request, "login.html", context)


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def welcome(request):
    return render(request, "welcome.html")


def detail(request):
    return render(request, "detail.html")


def studentManager(request):
    return render(request, "studentManager.html")


def studentAdd(request):
    return render(request, "studentAdd.html")


def studentEdit(request):
    return render(request, "studentEdit.html")


def taskManager(request):
    return render(request, "taskManager.html")


def taskAdd(request):
    return render(request, "taskAdd.html")


def taskEdit(request):
    return render(request, "taskEdit.html")
