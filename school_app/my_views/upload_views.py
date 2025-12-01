from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from school_app.models import UploadedFile

@login_required(login_url="/login/")
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')
        for f in files:
            UploadedFile.objects.create(
                file=f,
                name=f.name,
                size=f.size
            )
        messages.success(request, f'{len(files)} file(s) uploaded successfully!')
        return redirect('upload_page')

    return render(request, 'upload_page.html')
