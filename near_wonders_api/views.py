from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from near_wonders_api.models import Todo
from near_wonders_api.serializers import TodoSerializer


class TodoCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
