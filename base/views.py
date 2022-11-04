from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TodoSerializer
from .models import Todo

#   ---- FUNCTION BASED VIEW (View the API list endpoint) ----
# @api_view(['GET', 'POST'])
# def todo_list(request): 
    
#     if request.method == 'GET':
#         query = request.GET.get('query')
        
#         if query == None:
#             query = ''
        
#         todos = Todo.objects.filter(Q(title__icontains=query) | Q(memo__icontains=query))
#         serializer = TodoSerializer(todos, many=True)

#         return Response(serializer.data)

#     if request.method == 'POST':
#         todo = Todo.objects.create(
#             title=request.data['title'],
#             memo=request.data['memo']
#         )
#         serializer = TodoSerializer(todo, many=False)
        
#         return Response(serializer.data)

#   ---- CLASS BASED VIEW (View the API list endpoint) ----
class TodoList(generics.ListAPIView):
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        return Todo.objects.filter(user=user).order_by('-created')

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)