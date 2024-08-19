import os


# 判斷是開發環境還是線上部屬
def is_dev():
    return os.getenv("DJANGO_ENV", "development") == "development"


def is_prod():
    return os.getenv("DJANGO_ENV") == "production"
