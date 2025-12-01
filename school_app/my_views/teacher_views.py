from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from school_app.models import Teacher, Subject

@login_required(login_url="/login/")
def index(request):
    search_item = request.POST.get('search_item', '') if request.method == "POST" else ''
    teachers = Teacher.objects.filter(name__icontains=search_item) if search_item else Teacher.objects.all()

    paginator = Paginator(teachers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {"teachers": page_obj}
    return render(request, "pages/teachers/index.html", data)

@login_required(login_url="/login/")
def show(request):
    teachers = Teacher.objects.all()
    return render(request, "pages/teachers/create.html", {"teachers": teachers})

@login_required(login_url="/login/")
def create(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            teacher = Teacher()
            teacher.name = request.POST['name']
            teacher.email = request.POST['email']
            teacher.gender = request.POST['gender']
            teacher.phone = request.POST.get('phone', '')
            teacher.address = request.POST.get('address', '')

            # Assign the selected subject object
            subject_id = request.POST.get('subject')
            teacher.subject = Subject.objects.get(pk=subject_id) if subject_id else None

            teacher.full_clean()
            teacher.save()
            messages.success(request, 'Teacher successfully created!')
            return redirect('show')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, "pages/teachers/create.html", {"subjects": subjects})

    else:
        return render(request, "pages/teachers/create.html", {"subjects": subjects})



@login_required(login_url="/login/")
def delete_by_id(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    teacher.delete()
    messages.success(request, 'Teacher successfully deleted!')
    return redirect('/teachers/index')

@login_required(login_url="/login/")

def edit_by_id(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            teacher.name = request.POST['name']
            teacher.email = request.POST['email']
            teacher.gender = request.POST['gender']
            teacher.phone = request.POST.get('phone', '')
            teacher.address = request.POST.get('address', '')

            subject_id = request.POST.get('subject')
            teacher.subject = Subject.objects.get(pk=subject_id) if subject_id else None

            teacher.full_clean()
            teacher.save()
            messages.success(request, 'Teacher successfully updated!')
            return redirect('show')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "pages/teachers/edit.html", {"teacher": teacher, "subjects": subjects})

@login_required(login_url="/login/")
def update_by_id(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    try:
        teacher.name = request.POST['name']
        teacher.email = request.POST['email']
        teacher.gender = request.POST['gender']
        teacher.address = request.POST.get('address', '')

        subject_id = request.POST.get('subject')
        teacher.class_assigned = Subject.objects.get(pk=subject_id) if subject_id else None

        teacher.full_clean()
        teacher.save()
        messages.success(request, 'Teacher successfully updated!')
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect(f'/teachers/edit_by_id/{teacher_id}')
