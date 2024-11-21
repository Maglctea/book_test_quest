from django.urls import path
from rest_framework import routers

from book.views import get_file, create_task, get_task_status

router = routers.DefaultRouter()
urlpatterns = [
    path('books_export_tasks/<int:task_id>/file', get_file, name='list_export_books_task'),
    path('books_export_tasks/<int:task_id>', get_task_status, name='list_export_books_task'),
    path('books_export_tasks/', create_task, name='detail_export_books_task'),
]
