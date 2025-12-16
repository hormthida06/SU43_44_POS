from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from school_app.models import User
from functools import wraps


def my_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # basic validation
        if not username or not password or not role:
            messages.error(request, "All fields are required.")
            return redirect("/login/")

        try:
            # user must exist
            user = User.objects.get(username=username, role=role)

            # user must be active
            if not user.is_active:
                messages.error(request, "Account is inactive. Contact admin.")
                return redirect("/login/")

            # secure password check
            if not check_password(password, user.password):
                messages.error(request, "Invalid username or password.")
                return redirect("/login/")

            # login success
            request.session["user_id"] = user.id
            request.session["role"] = user.role

            messages.success(request, "Login successful!")

            # role-based redirect
            if user.role == "admin":
                return redirect("/dashboard/")
            elif user.role == "teacher":
                return redirect("/T_dashboard/")
            elif user.role == "student":
                return redirect("/ST_dashboard/")
            elif user.role == "parent":
                return redirect("/P_dashboard/")

        except User.DoesNotExist:
            messages.error(request, "Login failed! User does not exist.")
            return redirect("/login/")

    return render(request, "login.html")
