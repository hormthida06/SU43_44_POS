
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from school_app.models import Schedule, Class, Subject

@login_required(login_url="/login/")
def index(request):
    schedules = Schedule.objects.select_related("class_assigned", "subject").all()

    return render(request, "pages/schedules/index.html", {
        "schedules": schedules
    })

@login_required(login_url="/login/")
def create(request):
    if request.method == 'POST':
        try:
            schedule = Schedule()

            class_id = request.POST.get('class_assigned')
            schedule.class_assigned = Class.objects.get(pk=class_id) if class_id else None

            subject_id = request.POST.get('subject_name')
            schedule.subject_name = Subject.objects.get(pk=subject_id) if subject_id else None

            schedule.day = request.POST['day']
            schedule.time_slot = request.POST['time_slot']

            schedule.full_clean()
            schedule.save()
            messages.success(request, 'Schedule successfully created!')
            return redirect('show')

        except Exception as e:
            messages.error(request, f"Error: {e}")
            classes = Class.objects.all()
            subjects = Subject.objects.all()
            return render(request, "pages/schedules/create.html", {"classes": classes, "subjects": subjects})

    else:
        classes = Class.objects.all()
        subjects = Subject.objects.all()
        return render(request, "pages/schedules/create.html", {"classes": classes, "subjects": subjects})

def show(request):
    return render(request, "pages/schedules/create.html")

@login_required(login_url="/login/")
def delete(request, id):
    try:
        schedule_obj = Schedule.objects.get(pk=id)
        schedule_obj.delete()
        messages.success(request, "Schedule deleted successfully")
    except ObjectDoesNotExist:
        messages.error(request, "Schedule not found")
    return redirect("/schedules/index")

@login_required(login_url="/login/")
def edit(request, id):
    try:
        schedule_obj = Schedule.objects.get(pk=id)
        data = {"schedule": schedule_obj}
        return render(request, "pages/schedules/edit.html", data)
    except ObjectDoesNotExist:
        messages.error(request, "Schedule not found")
        return redirect("/schedules/index")

@login_required(login_url="/login/")
def update(request, id):
    try:
        schedule_existing = Schedule.objects.get(pk=id)
        schedule_existing.schedule_name = request.POST.get('schedule_name')
        schedule_existing.full_clean()
        schedule_existing.save()
        messages.success(request, "Schedule updated successfully")
        return redirect(f"/schedules/edit/{id}")
    except ObjectDoesNotExist:
        messages.error(request, "Schedule not found")
        return redirect("/schedules/index")
