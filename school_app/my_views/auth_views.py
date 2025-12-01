from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from school_app.models import User


def my_login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Get user from YOUR user table
            user = User.objects.get(username=username)

            # Check hashed password
            if check_password(password, user.password):

                # Log in user manually
                login(request, user)

                # Redirect by role (from user.role)
                if user.role == "admin":
                    return redirect("/dashboard/")
                elif user.role == "teacher":
                    return redirect("/T_dashboard/")
                elif user.role == "student":
                    return redirect("/ST_dashboard/")
                else:
                    return redirect("/")

            else:
                messages.error(request, "Invalid password")
                return redirect("/login/")

        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("/login/")

    return render(request, "pages/auths/login.html")

def my_logout(request):
    logout(request)
    return redirect("/login/")