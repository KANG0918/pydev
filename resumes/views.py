from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
            resume = form.save(commit=False)  # 先抓但不要存
            resume.user = req.user  # 履歷使用者跟當前登入者相同
            resume.save()  # 存檔
            messages.success(req, "新增成功")
            return redirect(reverse("resume:index"))  # reverse 把字串換成url_for
        else:
            messages.error(req, "新增失敗")
            return render(req, "resumes/new.html", {"form": form})

    resumes = Resume.objects.order_by("-id")  # 拿取所有資料
    return render(
        req,
        "resumes/index.html",
        {"resumes": resumes},
    )  # 將資料傳到index.html


@login_required
def new(req):
    form = ResumeForm()
    return render(req, "resumes/new.html", {"form": form})


def show(req, id):
    if req.method == "POST":
        resume = get_object_or_404(Resume, pk=id, user=req.user)
        # form元件(去forms找)
        form = ResumeForm(req.POST, instance=resume)
        if form.is_valid():
            form.save()  # 叫表單存檔
            messages.success(req, "更新成功")
            return redirect("resume:show", resume.id)  # reverse 把字串換成url_for
        else:
            messages.error(req, "更新失敗")
            return render(
                req,
                "resumes/edit.html",
                {
                    "form": form,
                    "resume": resume,
                    "bookmarked": resume.bookmarked_by(req.user),
                },
            )
    resume = get_object_or_404(Resume, pk=id)
    # comments = resume.comment_set.filter(deleted_at=None).order_by("-id")  # 拿出留言+軟刪除(假刪除)
    comments = resume.comment_set.order_by("-id")  # 把上行改寫在model中
    return render(
        req,
        "resumes/show.html",
        {
            "resume": resume,
            "comments": comments,
            "bookmarked": resume.bookmarked_by(req.user),
        },
    )


@login_required
def edit(req, id):
    resume = get_object_or_404(Resume, pk=id, user=req.user)
    form = ResumeForm(instance=resume)  # 把resume餵給ResumeForm
    return render(req, "resumes/edit.html", {"form": form, "resume": resume})


@login_required
def delete(req, id):
    resume = get_object_or_404(Resume, pk=id, user=req.user)
    resume.delete()
    messages.success(req, "刪除成功")
    return redirect("resume:index")


@login_required
def comment(req, id):
    if req.method == "POST":
        resume = get_object_or_404(Resume, pk=id)
        comment = resume.comment_set.create(content=req.POST["content"], user=req.user)
        # 特定的resume產生的留言 #_set 是 django的外鍵給的方法 # 是物件對物件
        return render(req, "resumes/_comment.html", {"comment": comment})


@login_required
def delete_comment(req, id):
    if req.method == "DELETE":
        comment = get_object_or_404(Comment, pk=id, user=req.user)  # 其他user不能刪除
        # comment.deleted_at = timezone.now()
        # comment.save()
        comment.delete()  # 把上行改寫在model中
        return HttpResponse("")  # 因為是htmx所以用這方式，把標的物(最近的li)換成''


@login_required
def bookmark(req, id):
    # 判斷是否收藏過
    if req.method == "POST":
        resume = get_object_or_404(Resume, pk=id)
        if resume.bookmarked_by(req.user):
            resume.bookmark.remove(req.user)
            return render(
                req, "resumes/_bookmark.html", {"resume": resume, "bookmarked": False}
            )
        else:
            resume.bookmark.add(req.user)
            return render(
                req, "resumes/_bookmark.html", {"resume": resume, "bookmarked": True}
            )
