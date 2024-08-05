from django.shortcuts import render, get_object_or_404
from .models import Resume
from django.http import HttpResponse

# Create your views here.


def index(req):
    resumes = Resume.objects.all()  # 拿取所有資料
    return render(
        req, "resumes/index.html", {"resumes": resumes}
    )  # 將資料傳到index.html


def show(req, id):
    resume = get_object_or_404(Resume, pk=id)
    return HttpResponse(resume.email)
