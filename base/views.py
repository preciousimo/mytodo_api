from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from .models import Todo

#   ---- FUNCTION BASED VIEW (View the API list endpoint) ----
@api_view(['GET'])
def endpoints(request):
    data = ['/todos', '/create', '/todo/pk', '/todo/pk/complete']
    return Response(data)

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
        
    def perform_update(self,serializer):
        serializer.instance.completed=not(serializer.instance.completed)
        serializer.save()

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # data is a dictionary
            user = User.objects.create_user(
                username=data['username'], password=data['password']
            )
            user.save()
            
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {'error':'username taken. choose another username'}, status=400
            )