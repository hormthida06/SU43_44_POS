from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from school_app.models import Class, Fee, Student

@login_required(login_url="/login/")
def index(request):
   search_item = request.GET.get("search_item", "")
   qs = Fee.objects.all()

   if search_item:
       qs = qs.filter(student__name__icontains=search_item)

   paginator = Paginator(qs, 10)
   page_number = request.GET.get("page")
   fees = paginator.get_page(page_number)

   return render(request, "pages/fees/index.html", {"fees": fees})

@login_required(login_url="/login/")
def show(request):
    return render(request, "pages/fees/create.html")

@login_required(login_url="/login/")
def create(request):
    if request.method == "POST":
        student_id = request.POST['student']
        amount = request.POST['amount']
        status = request.POST['status']

        Fee.objects.create(
            student_id=student_id,
            amount=amount,
            status=status
        )

        return redirect("/fees/index")

    # GET request → load students
    students = Student.objects.all()
    return render(request, "pages/fees/create.html", {"students": students})


@login_required(login_url="/login/")
def delete(request, id):
    try:
        fee_obj = Fee.objects.get(pk=id)
        fee_obj.delete()
        messages.success(request, "Fee deleted successfully")
    except ObjectDoesNotExist:
        messages.error(request, "Fee not found")
    return redirect("/fees/index")

@login_required(login_url="/login/")
def edit(request, id):
    try:
        fee_obj = Fee.objects.get(pk=id)
        data = {"fee": fee_obj}
        return render(request, "pages/fees/edit.html", data)
    except ObjectDoesNotExist:
        messages.error(request, "Fee not found")
        return redirect("/fees/index")

@login_required(login_url="/login/")
def update(request, id):
    try:
        class_existing = Class.objects.get(pk=id)
        class_existing.class_name = request.POST.get('fee_name')
        class_existing.full_clean()
        class_existing.save()
        messages.success(request, "Fee updated successfully")
        return redirect(f"/fees/edit/{id}")
    except ObjectDoesNotExist:
        messages.error(request, "Fee not found")
        return redirect("/fees/index")
