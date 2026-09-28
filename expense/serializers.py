from rest_framework import serializers
from django.contrib.auth.models import User
from expense.models import Expense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","password","email"]
        read_only_fields=["id"]
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)

    
class ExpenceSerializer(serializers.ModelSerializer):
    owner=serializers.SerializerMethodField()
    
    class Meta:
        model=Expense
        fields="__all__"
        read_only_fields=["id","created_at"]
    def get_greeting(selg,obj):
        return "Hi,Welcome to Expense Tracker!"
    def get_owner(self,obj):
        return obj.owner.username

