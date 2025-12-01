from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from school_app.models import Attendance, Student, Class
from datetime import date

@login_required(login_url="/login/")
def index(request):
    classes = Class.objects.all()
    attendances = []
    selected_class_id = request.POST.get('class')
    selected_date = request.POST.get('dob')

    if selected_class_id and selected_date:
        # Get all students in the selected class
        students = Student.objects.filter(class_assigned_id=selected_class_id)

        # For each student, make sure there's an attendance record for the date
        for student in students:
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=selected_date,
                defaults={'status': None}
            )
            # ✅ Add to the list (existing or new)
            attendances.append(attendance)
    else:
        attendances = Attendance.objects.all().order_by('-date')

    # Pagination
    paginator = Paginator(attendances, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "attendances": page_obj,
        "classes": classes,
        "selected_class_id": selected_class_id,
        "selected_date": selected_date,
        "count_item": len(attendances),
    }
    return render(request, "pages/attendances/index.html", context)


# def update_status(request):
#     if request.method == "POST":
#         attendance_id = request.POST.get("attendance_id")
#         status = request.POST.get("status")
#         try:
#             attendance = Attendance.objects.get(id=attendance_id)
#             attendance.status = status
#             attendance.save()
#             return JsonResponse({"success": True})
#         except ObjectDoesNotExist:
#             return JsonResponse({"success": False, "error": "Attendance not found"})
#     return JsonResponse({"success": False, "error": "Invalid request"})

from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def update_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            updates = data.get("updates", [])
            for item in updates:
                attendance_id = item.get("attendance_id")
                status = item.get("status")
                if attendance_id and status:
                    Attendance.objects.filter(id=attendance_id).update(status=status)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})
