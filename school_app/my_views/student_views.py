from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from school_app.models import Student, Class, Attendance


# ----------------------------
# List Students with Pagination
# ----------------------------
@login_required(login_url="/login/")
def index(request):
    search_item = request.POST.get('search_item', '') if request.method == "POST" else ''
    students = Student.objects.filter(name__icontains=search_item) if search_item else Student.objects.all()

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {"students": page_obj}
    return render(request, "pages/students/index.html", data)


# ----------------------------
# Show Add Student Form
# ----------------------------
@login_required(login_url="/login/")
def show(request):
    classes = Class.objects.all()
    return render(request, "pages/students/create.html", {"classes": classes})


# ----------------------------
# Create New Student
# ----------------------------
@login_required(login_url="/login/")
def create(request):
    if request.method == 'POST':
        try:
            student = Student()
            student.name = request.POST['name']
            student.email = request.POST['email']
            student.gender = request.POST['gender']
            student.phone = request.POST.get('phone', '')
            student.address = request.POST.get('address', '')

            class_id = request.POST.get('class_assigned')
            student.class_assigned = Class.objects.get(pk=class_id) if class_id else None

            student.dob = request.POST.get('dob')

            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']

            student.full_clean()
            student.save()
            messages.success(request, 'Student successfully created!')
            return redirect('show')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            classes = Class.objects.all()
            return render(request, "pages/students/create.html", {"classes": classes})
    else:
        classes = Class.objects.all()
        return render(request, "pages/students/create.html", {"classes": classes})

# ----------------------------
# Delete Student
# ----------------------------
@login_required(login_url="/login/")
def delete_by_id(request, id):
    student = get_object_or_404(Student, pk=id)
    if student.photo:
        student.photo.delete()
    student.delete()
    messages.success(request, 'Student successfully deleted!')
    return redirect('/students/index')


# ----------------------------
# Show Edit Student Form
# ----------------------------
@login_required(login_url="/login/")
def edit_by_id(request, id):
    student = get_object_or_404(Student, pk=id)
    classes = Class.objects.all()
    data = {"student": student, "classes": classes}
    return render(request, "pages/students/edit.html", context=data)


# ----------------------------
# Update Student
# ----------------------------
@login_required(login_url="/login/")
def update(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    try:
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.gender = request.POST['gender']
        student.phone = request.POST.get('phone', '')
        student.address = request.POST.get('address', '')

        class_id = request.POST.get('class_assigned')
        student.class_assigned = Class.objects.get(pk=class_id) if class_id else None

        student.dob = request.POST.get('dob')

        if 'photo' in request.FILES:
            if student.photo:
                student.photo.delete()
            student.photo = request.FILES['photo']

        student.full_clean()
        student.save()
        messages.success(request, 'Student successfully updated!')
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect(f'/students/edit_by_id/{student_id}')


from django.shortcuts import redirect
from django.contrib import messages

def save_attendance(request):
    if request.method == "POST":
        # Loop through POST data to find attendance status updates
        for key, value in request.POST.items():
            if key.startswith("status_"):
                try:
                    attendance_id = key.split("_")[1]
                    attendance = Attendance.objects.get(id=attendance_id)
                    attendance.status = value
                    attendance.save()
                except Attendance.DoesNotExist:
                    continue

        messages.success(request, "Attendance records saved successfully!")
        return redirect("attendance_index")

    messages.error(request, "Invalid request method.")
    return redirect("attendance_index")