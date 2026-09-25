from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from expense.serializers import UserSerializer,ExpenceSerializer
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from expense.models import Expense
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone
# Create your views here.

class RegisterView(ViewSet):
    def create(self,request):
        dser=UserSerializer(data=request.data)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)


class ExpenseView(ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        dser=ExpenceSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        expense_list=Expense.objects.filter(owner=request.user)
        dser=ExpenceSerializer(expense_list,many=True)
        return Response(data=dser.data,status=status.HTTP_200_OK)
    def destroy(self,request,pk=0):
        Expense.objects.get(id=pk).delete()
        return Response(data={"msg":"Deleted!!!"})
    def update(self,request,pk=0):
        expence_obj=Expense.objects.get(id=pk)
        dser=ExpenceSerializer(data=request.data,instance=expence_obj)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self,request,pk=0):
        expense_obj=Expense.objects.get(id=pk)
        dser=ExpenceSerializer(data=request.data,instance=expense_obj,partial=True)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

class ExpenseSummeryView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cur_date=timezone.now()
        cur_month=cur_date.month
        cur_year=cur_date.year
        # print(cur_month,cur_year)
        data=Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        category_summery=data.values('category').annotate(Sum('amount'))
        cat_summery=[summery for summery in category_summery]
        #print(cat_summery)
        for i in category_summery:
            print(i)
        total_expense=data.values('amount').aggregate(Sum('amount'))
        print(total_expense)
        # ser=ExpenceSerializer(qs,many=True)
        context={
            "total_expense":total_expense,
            "category_summery":cat_summery
        }

        return Response(data=context)





