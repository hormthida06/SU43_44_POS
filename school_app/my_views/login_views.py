from django.shortcuts import render, redirect
from django.contrib import messages
from school_app.models import User

def my_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        try:
            user = User.objects.get(username=username, password=password, role=role)
        except User.DoesNotExist:
            messages.error(request, "Invalid username, password, or role")
            return redirect("/login/")

        request.session["user_id"] = user.id
        request.session["role"] = user.role

        if user.role == "admin":
            return redirect("/dashboard/")
        elif user.role == "teacher":
            return redirect("/T_dashboard/")
        elif user.role == "student":
            return redirect("/ST_dashboard/")
        elif user.role == "parent":
            return redirect("/P_dashboard/")

    return render(request, "login.html")


def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            role = request.session.get("role")
            if role != required_role:
                return redirect("/login/")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def logout(request):
    request.session.flush()
    return redirect("/login/")
