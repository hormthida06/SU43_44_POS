from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from school_app.models import User

@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        search_item = request.POST.get('search_item', '')
        users = User.objects.filter(
            Q(username__icontains=search_item) |
            Q(email__icontains=search_item)
        )
    else:
        users = User.objects.all()

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "pages/users/index.html", {"users": page_obj})

@login_required(login_url="/login/")
def show(request):
    return render(request, "pages/users/create.html")

@login_required(login_url="/login/")
def create(request):
    if request.method == "POST":
        try:
            users_obj = User()
            users_obj.username = request.POST.get('username')
            users_obj.password = make_password(request.POST.get('password'))  # hashed
            users_obj.email = request.POST.get('email')
            users_obj.role = request.POST.get('role')
            users_obj.status = request.POST.get('status')

            users_obj.full_clean()
            users_obj.save()
            messages.success(request, "User created successfully")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect("/users/show")

    return redirect("/users/index")


@login_required(login_url="/login/")
def delete(request, id):
    try:
        class_obj = User.objects.get(pk=id)
        class_obj.delete()
        messages.success(request, "Class deleted successfully")
    except ObjectDoesNotExist:
        messages.error(request, "Class not found")
    return redirect("/users/index")

@login_required(login_url="/login/")
def edit(request, id):
    try:
        user_obj = User.objects.get(pk=id)
        data = {"user": user_obj}
        return render(request, "pages/users/edit.html", data)
    except ObjectDoesNotExist:
        messages.error(request, "User not found")
        return redirect("/users/index")

@login_required(login_url="/login/")
def update(request, id):
    try:
        user_existing = User.objects.get(pk=id)
        user_existing.username = request.POST.get('username')
        password = request.POST.get('password')
        if password:
            user_existing.password = make_password(password)  # hash here
        user_existing.role = request.POST.get('role')
        user_existing.email = request.POST.get('email')
        user_existing.status = request.POST.get('status')
        user_existing.full_clean()
        user_existing.save()
        messages.success(request, "User updated successfully")
        return redirect(f"/users/edit/{id}")
    except ObjectDoesNotExist:
        messages.error(request, "User not found")
        return redirect("/users/index")

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def my_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  # <-- now works

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                # OPTIONAL: redirect by role
                if role == "admin":
                    return redirect("/")
                elif role == "teacher":
                    return redirect("/")
                elif role == "student":
                    return redirect("/")
                else:
                    return redirect("/")

    return render(request, "pages/auths/login.html")

def my_logout(request):
    logout(request)
    return redirect("/login/")