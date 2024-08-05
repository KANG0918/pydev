# windows不能用

.PHONY:server
server:
	python manage.py runserver

migration:
	python manage.py makemigrations