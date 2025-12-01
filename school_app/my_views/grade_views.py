from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from school_app.models import Grade, Student, Subject, Teacher, Class
from django.contrib import messages
from django.http import JsonResponse

# List grades
def get_grade_letter(score):
    if score > 90:
        return "A"
    elif score > 80:
        return "B"
    elif score > 70:
        return "C"
    elif score > 60:
        return "D"
    elif score >= 50:
        return "E"
    else:
        return "F"

from collections import defaultdict
@login_required(login_url="/login/")
def index(request):
    search_item = request.GET.get("search_item", "")
    selected_class = request.GET.get("class", "")
    selected_subject = request.GET.get("subject", "")

    grades = Grade.objects.all()

    if search_item:
        grades = grades.filter(student__name__icontains=search_item)

    if selected_class:
        grades = grades.filter(student__class_assigned_id=selected_class)

    if selected_subject:
        grades = grades.filter(subject_id=selected_subject)

    classes = Class.objects.all()
    subjects = Subject.objects.all()

    # pagination
    paginator = Paginator(grades, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "pages/grades/index.html", {
        "grades": page_obj,
        "classes": classes,
        "subjects": subjects,
        "selected_class_id": selected_class,
        "selected_subject_id": selected_subject,
    })

@login_required(login_url="/login/")
def student_list(request):
    class_id = request.GET.get('class_id')   # from dropdown or sort
    if class_id:
        students = Student.objects.filter(class_id=class_id)
    else:
        students = Student.objects.all()

    classes = Class.objects.all()

    return render(request, 'students/index.html', {
        'students': students,
        'classes': classes,
        'selected_class': class_id,
    })

@login_required(login_url="/login/")
def grade_save(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("score_"):
                grade_id = key.split("_")[1]
                grade = Grade.objects.get(id=grade_id)
                grade.score = int(value)
                comment_key = f"comment_{grade_id}"
                grade.comment = request.POST.get(comment_key, "")
                grade.save()
        messages.success(request, "All grades updated successfully!")
    return redirect('grade_index')

from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def update(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            updates = data.get("updates", [])
            for item in updates:
                grade_id = item.get("grade_id")
                status = item.get("status")
                if grade_id and status:
                    Grade.objects.filter(id=grade_id).update(status=status)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})