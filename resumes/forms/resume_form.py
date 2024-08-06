from django.forms import ModelForm
from resumes.models import Resume
from django.forms.widgets import TextInput, Textarea, CheckboxInput, EmailInput


# 建立表單
class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = [
            "name",
            "email",
            "introduce",
            "profile",
            "online",
        ]  # 只開放這些丟過來，其他都會被濾掉

        widgets = {
            "name": TextInput(attrs={"class": "input"}),
            "email": EmailInput(attrs={"class": "input"}),
            "introduce": TextInput(attrs={"class": "input"}),
            "profile": Textarea(attrs={"rows": "5", "class": "textarea"}),
            "online": CheckboxInput(attrs={"class": "input"}),
        }
        labels = {
            "name": "姓名",
            "email": "Email",
            "introduce": "簡介",
            "profile": "個人檔案",
            "online": "是否上線",
        }
