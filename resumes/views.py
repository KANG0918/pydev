from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import ResumeForm
from .models import Comment, Resume

# from turbo_helper import TurboStreamResponse

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

    # comments = resume.comment_set.filter(deleted_at=None).order_by("-id")  # 拿出留言+軟刪除(假刪除)
    comments = resume.comment_set.order_by("-id")  # 把上行改寫在model中
    return render(req, "resumes/show.html", {"resume": resume, "comments": comments})


def edit(req, id):
    resume = get_object_or_404(Resume, pk=id)
    form = ResumeForm(instance=resume)  # 把resume餵給ResumeForm
    return render(req, "resumes/edit.html", {"form": form, "resume": resume})


def delete(req, id):
    resume = get_object_or_404(Resume, pk=id)
    resume.delete()
    messages.success(req, "刪除成功")
    return redirect("resume:index")


def comment(req, id):
    if req.method == "POST":
        resume = get_object_or_404(Resume, pk=id)
        comment = resume.comment_set.create(content=req.POST["content"])
        return render(req, "resumes/_comment.html", {"comment": comment})


def delete_comment(req, id):
    if req.method == "DELETE":
        comment = get_object_or_404(Comment, pk=id)
        # comment.deleted_at = timezone.now()
        # comment.save()
        comment.delete()  # 把上行改寫在model中
        return HttpResponse("")  # 因為是htmx所以用這方式，把標的物(最近的li)換成''
