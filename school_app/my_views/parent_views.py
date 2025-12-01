from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from school_app.models import Class

@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        search_item = request.POST.get('search_item', '')
        classes = Class.objects.filter(class_name__icontains=search_item)
    else:
        classes = Class.objects.all()

    paginator = Paginator(classes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {"classes": page_obj}

    return render(request, "pages/classes/index.html", data)

@login_required(login_url="/login/")
def show(request):
    return render(request, "pages/classes/create.html")

@login_required(login_url="/login/")
def create(request):
    if request.method == "POST":
        class_obj = Class()
        class_obj.class_name = request.POST.get('class_name')
        try:
            class_obj.full_clean()
            class_obj.save()
            messages.success(request, "Class created successfully")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("/classes/show")
    return redirect("/classes/index")

@login_required(login_url="/login/")
def delete(request, id):
    try:
        class_obj = Class.objects.get(pk=id)
        class_obj.delete()
        messages.success(request, "Class deleted successfully")
    except ObjectDoesNotExist:
        messages.error(request, "Class not found")
    return redirect("/classes/index")

@login_required(login_url="/login/")
def edit(request, id):
    try:
        class_obj = Class.objects.get(pk=id)
        data = {"class": class_obj}
        return render(request, "pages/classes/edit.html", data)
    except ObjectDoesNotExist:
        messages.error(request, "Class not found")
        return redirect("/classes/index")

@login_required(login_url="/login/")
def update(request, id):
    try:
        class_existing = Class.objects.get(pk=id)
        class_existing.class_name = request.POST.get('class_name')
        class_existing.full_clean()
        class_existing.save()
        messages.success(request, "Class updated successfully")
        return redirect(f"/classes/edit/{id}")
    except ObjectDoesNotExist:
        messages.error(request, "Class not found")
        return redirect("/classes/index")
