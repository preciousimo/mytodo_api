from django.urls import path
from . import views

urlpatterns = [
    # path('', views.todo_list, name='todos'),
    path('', views.TodoList.as_view()),
    path('create/', views.TodoListCreate.as_view()),
    path('todo/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()),
]