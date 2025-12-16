from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.http import HttpResponse
from django.shortcuts import render

from school_app.models import Class

@login_required(login_url="/login/")
def home(request):
    # return HttpResponse("Hello, this is my_app home page!")
    data = {"name": "Coca"}
    return render(request, "index.html", context=data)


def find_by_id(request, id):
    return HttpResponse(f"Id{id}")

@login_required(login_url="/login/")
def content(request):
    return render(request, "pages/main_content.html")
@login_required(login_url="/login/")
def report(request):
    return render(request, "pages/report.html")
@login_required(login_url="/login/")
def teacher_report(request):
    return render(request, "pages/teacher_report.html")
@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "pages/dashboard.html")
@login_required(login_url="/login/")

def login(request):
    return render(request, "pages/auths/Login.html")
@login_required(login_url="/login/")
def contact_us(request):
    return render(request, "pages/contact_us.html")
@login_required(login_url="/login/")
def about_us(request):
    return render(request, "pages/about_us.html")
@login_required(login_url="/login/")
def academic(request):
    return render(request, "pages/academic.html")
@login_required(login_url="/login/")
def internship(request):
    return render(request, "pages/internship.html")
@login_required(login_url="/login/")
def st_dashboard(request):
    return render(request, "pages/st_dashboard.html")
@login_required(login_url="/login/")
def leactur_dashboard(request):
    return render(request, "pages/Leactur_dashboard.html")
@login_required(login_url="/login/")
def video_for_st(request):
    return render(request, "pages/video_for_ST.html")
@login_required(login_url="/login/")
def teacher_class(request):
    classes = Class.objects.all()
    data = {
        "classes": classes
    }
    return render(request, "pages/class_for_teacher.html", data)
@login_required(login_url="/login/")
def teacher_upload(request):
    return render(request, "pages/teacher_Upload.html")

