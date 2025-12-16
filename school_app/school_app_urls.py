from django.contrib import admin
from django.contrib.auth import authenticate
from django.urls import path

from school_app import views
from school_app.my_views import student_views, subject_views, teacher_views, class_views, user_views, grade_views, \
    attendances_views, schedule_views, fee_views, parent_views, result_views, auth_views

urlpatterns = [
path("ST_dashboard/", views.st_dashboard),
path("T_dashboard/", views.leactur_dashboard),
path("dashboard/", views.dashboard),

    path("login/", auth_views.my_login, name="login"),
    path("logout/", auth_views.my_logout, name="logout"),
    # path("login", auth_views.my_login),
    # path("logout", auth_views.my_logout),
    path("", views.home, name="home"),

    path("find_by_id/<id>", views.find_by_id, name="find_by_id"),

    path("content", views.content),
    path("report", views.report),
    path("teacher_report", views.teacher_report),
    path("dashboard", views.dashboard),

    path("academic", views.academic),
    path("internship", views.internship),
    path("about_us", views.about_us),
    path("contact_us", views.contact_us),
    path("ST_dashboard", views.st_dashboard),
    path("T_dashboard", views.leactur_dashboard),
    path("ST_Video", views.video_for_st),
    path("CFT", views.teacher_class),
    path("Upload", views.teacher_upload),
# path('upload/', views.upload_files, name='upload_page'),
#Student
    path("students/index",student_views.index),

    path('students/show', student_views.show, name='show'),

    path("students/create",student_views.create),

     # path("students/delete/<id>", student_views.delete),
    #
    # path("students/edit/<id>", student_views.edit),

    # path("students/update/<id>", student_views.update),

path('students/update/<int:student_id>', student_views.update, name='update'),

    path("students/delete_by_id/<id>", student_views.delete_by_id),

    path("students/edit_by_id/<id>", student_views.edit_by_id),

#Subject
    path("subjects/index",subject_views.index),

    path("subjects/show",subject_views.show),

    path("subjects/create",subject_views.create),

    path("subjects/delete/<id>", subject_views.delete),

    path("subjects/edit/<id>", subject_views.edit),

    path("subjects/update/<id>", subject_views.update),

#Class
    path("classes/index",class_views.index),
    path("classes/show",class_views.show),

    path("classes/create",class_views.create),

    path("classes/delete/<id>", class_views.delete),

    path("classes/edit/<id>", class_views.edit),

    path("classes/update/<id>", class_views.update),

#User
    path("users/index",user_views.index),

    path("users/show",user_views.show),

    path("users/create",user_views.create),

    path("users/delete/<id>", user_views.delete),

    path("users/edit/<id>", user_views.edit),

    path("users/update/<id>", user_views.update),

#-------------------------------------Grade
    path("grades/update_status/", grade_views.update, name="update_status"),
    path("grades/save", grade_views.grade_save, name="grade_save"),
    path('grades/index', grade_views.index, name='grade_index'),

    # path("grades/create", grade_views.create),
    #
    # path("grades/delete/<id>", grade_views.delete),
    #
    # path("grades/edit/<id>", grade_views.edit),
    #
    # path("grades/update/<id>", grade_views.update),
#Attendances
    # Attendances
    path("attendances/index/", attendances_views.index, name="attendance_index"),
    path("attendances/update_status/", attendances_views.update_status, name="update_status"),
    path("attendances/save", student_views.save_attendance, name="attendance_save"),

    # path("attendances/edit/<int:id>/", attendances_views.edit, name="attendance_edit"),
    # path("attendances/delete/<int:id>/", attendances_views.delete, name="attendance_delete"),

#Schedule
    path("schedules/index",schedule_views.index),

    path("schedules/show",schedule_views.show),

    path("schedules/create",schedule_views.create),

    path("schedules/delete/<id>", schedule_views.delete),

    path("schedules/edit/<id>", schedule_views.edit),

    path("schedules/update/<id>", schedule_views.update),

#Fee
    path("fees/index",fee_views.index),

    path("fees/show",fee_views.show),

    path("fees/create",fee_views.create),

    path("fees/delete/<id>", fee_views.delete),

    path("fees/edit/<id>", fee_views.edit),

    path("fees/update/<id>", fee_views.update),

#Parent
    path("parents/index",parent_views.index),

    path("parents/show",parent_views.show),

    path("parents/create",parent_views.create),

    path("parents/delete/<id>", parent_views.delete),

    path("parents/edit/<id>", parent_views.edit),

    path("parents/update/<id>", parent_views.update),

#Teacher
    path("teachers/index", teacher_views.index),

    path('teachers/show', teacher_views.show, name='show'),

    path("teachers/create", teacher_views.create),

    path('teachers/update/<int:teacher_id>', teacher_views.update_by_id, name='update'),
    path('teachers/edit_by_id/<int:id>', teacher_views.edit_by_id, name='edit_teacher'),

#Result
    path("results/index", result_views.index)

]

