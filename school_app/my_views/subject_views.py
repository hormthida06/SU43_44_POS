from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from school_app.models import Subject
@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        subject = Subject()
        subject.category = request.POST['search_item']
        subjects = subject.objects.filter(category__icontains =subject.subject_name)
        paginator = Paginator(subjects, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {"subjects": page_obj}
    else:
        subjects = Subject.objects.all()
        paginator = Paginator(subjects, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {"subjects":page_obj}
    return render(request,"pages/subjects/index.html",data)

@login_required(login_url="/login/")
def show(request):
    return render(request, "pages/subjects/create.html")

@login_required(login_url="/login/")
def create(request):
    subject = Subject()
    subject.subject_name = request.POST['subject_name']
    subject.full_clean()
    subject.save()
    if(subject.pk):
        messages.success(request, "Subject created successfully")
    return redirect("/subjects/show")

@login_required(login_url="/login/")
def delete(request, id):
    try:
        subject = Subject.objects.get(pk=id)
        subject.delete()
        messages.success(request, "Subject deleted successfully")
    except ObjectDoesNotExist:
        messages.error(request, "Subject not found")
    return redirect("/subjects/index")

@login_required(login_url="/login/")
def edit(request, id):
    try:
        subject = Subject.objects.get(pk=id)
        data = {"subject": subject}
        return render(request, "pages/subjects/edit.html", data)
    except ObjectDoesNotExist:
        messages.error(request, "Subject not found")
        return redirect("/subjects/index")

@login_required(login_url="/login/")
def update(request, id):
    subject_existing = Subject.objects.get(pk=id)
    subject_existing.subject = request.POST['subject_name']
    subject_existing.full_clean()
    subject_existing.save()
    messages.success(request, "Subject Updated successfully")
    return redirect("/subjects/edit/{id}")
