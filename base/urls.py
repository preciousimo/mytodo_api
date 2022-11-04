from django.urls import path
from . import views

urlpatterns = [
    # path('', views.todo_list, name='todos'),
    path('', views.TodoList.as_view()),
]