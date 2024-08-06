from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Resume
from django.http import HttpResponse
from .forms import ResumeForm
from django.urls import reverse

# Create your views here.


def index(req):
    if req.method == "POST":
        # form元件(去forms找)
        form = ResumeForm(req.POST)
        if form.is_valid():
            form.save()  # 叫表單存檔
            messages.success(req, "新增成功")
            return redirect(reverse("resume:index"))  # reverse 把字串換成url_for
        else:
            messages.error(req, "新增失敗")
            return render(req, "resumes/new.html", {"form": form})

    resumes = Resume.objects.all()  # 拿取所有資料
    return render(
        req,
        "resumes/index.html",
        {"resumes": resumes},
    )  # 將資料傳到index.html


def new(req):
    form = ResumeForm()
    return render(req, "resumes/new.html", {"form": form})


def show(req, id):
    resume = get_object_or_404(Resume, pk=id)
    if req.method == "POST":
        # form元件(去forms找)
        form = ResumeForm(req.POST, instance=resume)
        if form.is_valid():
            form.save()  # 叫表單存檔
            messages.success(req, "更新成功")
            return redirect("resume:show", resume.id)  # reverse 把字串換成url_for
        else:
            messages.error(req, "更新失敗")
            return render(req, "resumes/edit.html", {"form": form, "resume": resume})
    resume = get_object_or_404(Resume, pk=id)
    return render(req, "resumes/show.html", {"resume": resume})


def edit(req, id):
    resume = get_object_or_404(Resume, pk=id)
    form = ResumeForm(instance=resume)  # 把resume餵給ResumeForm
    return render(req, "resumes/edit.html", {"form": form, "resume": resume})


def delete(req, id):
    resume = get_object_or_404(Resume, pk=id)
    resume.delete()
    messages.success(req, "刪除成功")
    return redirect("resume:index")
