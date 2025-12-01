

# USER MODEL
# --------------------------
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes role and status fields for role-based access control.
    """

    # Role choices
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    # Status choices
    STATUS_CHOICES = [
        ('1', 'Active'),
        ('0', 'Inactive'),
    ]

    # Custom fields
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    # Optional extra fields (uncomment if needed)
    # phone = models.CharField(max_length=20, blank=True, null=True)
    # class_name = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

# CLASS MODEL
# --------------------------
class Class(models.Model):
    class_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.class_name


# SUBJECT MODEL
# --------------------------
class Subject(models.Model):
    subject_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.subject_name


# UPDATED TEACHER MODEL
# --------------------------
class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='students/', null=True, blank=True)
    class_assigned = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.name

# PARENT MODEL
# --------------------------
class Parent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_profile')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name


# PARENT-STUDENT RELATION MODEL
# --------------------------
class ParentStudent(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')

    def __str__(self):
        return f"{self.parent.full_name} - {self.student.name}"



# ATTENDANCE MODEL
# --------------------------
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.status} on {self.date}"


# FEE MODEL
# --------------------------
class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.status}"


# GRADE MODEL
# --------------------------
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='grades')
    score = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} ({self.score})"


# SCHEDULE MODEL
# --------------------------
class Schedule(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateTimeField(null=True, blank=True)
    time_slot = models.TimeField()

    def __str__(self):
        return f"{self.class_assigned} - {self.subject}"

#teacher upload
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # files stored in MEDIA_ROOT/uploads/
    name = models.CharField(max_length=255, null=True, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.file.name
