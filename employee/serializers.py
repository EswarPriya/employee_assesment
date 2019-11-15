from django.contrib.auth.models import User, Group
from rest_framework import serializers
from employee.models import Employee,EmployeeDepartment,Department
import re

GENDER_CHOICES = ((1,'Male'),(2,'Female'),)

class  EmployeeInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, max_length=15)
    last_name = serializers.CharField(required=True, max_length=15)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES,required=True)
    address = serializers.CharField(required=False,max_length=50)
    employee_ref_id = serializers.CharField(required=True, max_length=15)
    birth_date = serializers.DateField(required=True)
    
    class Meta:
        model = Employee
        fields = ('id','active','first_name','last_name', 'gender','address','salary','employee_ref_id','birth_date','created','modified')

    def get_active(self,obj):
        return obj.active

    def get_id(self,obj):
        return str(obj.id)

class EmployeeSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(required=False,max_length=15)
    last_name = serializers.CharField(required=False,max_length=15)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES,required=False,)
    address = serializers.CharField(required=False,max_length=50)
    employee_ref_id = serializers.CharField(required=False, max_length=15)
    birth_date = serializers.DateField(required=False)
    
    class Meta:
        model = Employee
        fields = ('first_name','last_name', 'gender','address','salary','employee_ref_id','birth_date')
    
    def validate(self,data):
        if self.instance:
            if (self.Meta.model).objects.exclude(id=self.instance.id).filter(employee_ref_id=data['employee_ref_id']).exists():
                raise serializers.ValidationError('EMployee reference id already exists')
        else:
            if (self.Meta.model).objects.filter(employee_ref_id=data['employee_ref_id']).exists():
                raise serializers.ValidationError('EMployee reference id already exists')
        return data

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True, max_length=15)
    last_name = serializers.CharField(required=True, max_length=15)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES,required=True)
    address = serializers.CharField(required=False,max_length=50)
    employee_ref_id = serializers.CharField(required=True, max_length=15)
    birth_date = serializers.DateField(required=True)
    
    class Meta:
        model = Employee
        fields = ('first_name','last_name', 'gender','address','salary','employee_ref_id','birth_date','created','modified')

    def validate(self,data):
        if self.instance:
            if (self.Meta.model).objects.exclude(id=self.instance.id).filter(employee_ref_id=data['employee_ref_id']).exists():
                raise serializers.ValidationError('EMployee reference id already exists')
        else:
            if (self.Meta.model).objects.filter(employee_ref_id=data['employee_ref_id']).exists():
                raise serializers.ValidationError('EMployee reference id already exists')
        return data
    

class EmployeeDetail(serializers.Serializer):
    emp_id = serializers.CharField(required=True,max_length=15)

class DepartmentSerializer(serializers.ModelSerializer):
    department_no = serializers.IntegerField(required=True)
    department_name = serializers.CharField(required=True)

    class Meta:
        model = Department
        fields = ('department_no','department_name')
    
    def validate(self,data):
        if self.instance:
            if (self.Meta.model).objects.exclude(id=self.instance.id).filter(department_name=data['department_name']).exists():
                raise serializers.ValidationError('Department Name already exists')
        else:
            if (self.Meta.model).objects.filter(department_name=data['department_name']).exists():
                raise serializers.ValidationError('Department Name already exists')
        return data

class EmployeeDeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDepartment
        fields = ('employee','department','employee_role','hire_date')

    def validate(self,data):
        if self.instance:
            if (self.Meta.model).objects.exclude(id=self.instance.id).filter(department__id=int(data['department']),employee__id=int(data['employee'])).exists():
                raise serializers.ValidationError('This Employee has been already attached to the department')
        else:
            if (self.Meta.model).objects.filter(department__id=int(data['department']),employee__id=int(data['employee'])).exists():
                raise serializers.ValidationError('This Employee has been already attached to the department')
        return data

class DepartEmployeeDetail(serializers.Serializer):
    depart_num = serializers.IntegerField(required=True)
    salary_from = serializers.CharField(required=False,max_length=10)
    salary_to = serializers.CharField(required=False,max_length=10)

    def validate(self,data):
        salary_from = data.get('salary_from')
        salary_to = data.get('salary_to')
        if salary_from and not salary_to:
            raise serializers.ValidationError({'salary_to':'Please enter salary_to'})
        if (salary_from and salary_to) and (int(salary_from) >= int(salary_to)):
            raise serializers.ValidationError({'salary_to':'salary_from should be lesser than salary_to to compare the range'})
        return data
