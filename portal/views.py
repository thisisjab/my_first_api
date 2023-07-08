from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers


class JobsListView(ListCreateAPIView):
    queryset = models.Job.objects.prefetch_related('category').all()
    serializer_class = serializers.JobSerializer


class JobDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer


class CategoryListView(ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CompanyListView(APIView):
    def get(self, request):
        companies = models.Company.objects.all()
        serializer = serializers.CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CompanyDetailView(APIView):
    def get(self, request, id):
        company = get_object_or_404(models.Company, id=id)
        serializer = serializers.CompanySerializer(company)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, id):
        company = get_object_or_404(models.Company, id=id)
        serializer = serializers.CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        company = get_object_or_404(models.Company, id=id)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
