import urllib
import base64
from ast import literal_eval
from django.shortcuts import render
from rest_framework import generics as g
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import  (EmployeeDeptSerializer, EmployeeSerializer, 
    DepartmentSerializer,EmployeeDeptSerializer,EmployeeDetail,DepartEmployeeDetail,
     EmployeeInfoSerializer,EmployeeUpdateSerializer)
from .models import Employee, Department, EmployeeDepartment
from django.db.models import Q


class EmployeeCreate(g.CreateAPIView):
    queryset = Employee.objects.filter(active=2).order_by('-id') # this is reverse order
    serializer_class = EmployeeSerializer
    
class EmployeeList(APIView):

    def get(self, request, format=None):
        # to ge the list of employees entered
        try:
            objects = Employee.objects.filter(active=2).order_by('id')
            details = EmployeeInfoSerializer(objects,many=True).data
            response = {'status':2,'message': 'successfully retreived','data':details}
        except Exception as e:
            response = {'status':0,'message': str(e)}
        return Response(response)


class EmployeeUpdate(g.UpdateAPIView):

    serializer_class = EmployeeUpdateSerializer

    def put(self, request, pk, format=None):
        # update the particular employee details using employee primary cake
        try:
            employee = Employee.objects.get(id=pk)
            serializer = EmployeeUpdateSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'status':2,'message':'Successfully updated'})
        except Exception as e:
            return Response({'status':0,'message': str(e)})
        return Response({'mesaage':serializer.errors, 'status':0})

class EmployeeInfo(g.CreateAPIView):

    serializer_class = EmployeeDetail

    def post(self,request,format=None):
        """
        To get the info of the employee using employee refernece id
        ---
        """
        try:
            data = request.data
            ref_id = data.get('emp_id')
            serializer = EmployeeDetail(data=request.data)
            if serializer.is_valid():
                obj = Employee.objects.get(employee_ref_id=ref_id)
                details = {'id': obj.id,'first_name':obj.first_name,
                    'last_name':obj.last_name if obj.last_name else '',
                    'gender': obj.get_gender_display(),
                    'salary': obj.salary if obj.salary else '',
                    'employee_ref_id': obj.employee_ref_id ,
                    'date_of_birth': obj.birth_date.strftime('%Y-%m-%d'),
                    'created_on': obj.created.strftime('%Y-%m-%d')
                    }
                response = {'status':2,'message': 'successfully retreived','data':details}
            else:
                response={'status':0,'message':serializer.errors}
        except Exception as e:
            response = {'status':0,'message': str(e)}
        return Response(response)
    
class Employeedetails(g.CreateAPIView):

    serializer_class = DepartEmployeeDetail

    def post(self,request,format=None):
        """
        get details of all the employees of a particular department(query param) having salary range between two given numbers.
        ---
        """
        try:
            serializer = DepartEmployeeDetail(data=request.data)
            if serializer.is_valid():
                data = request.data
                depart_no = data.get('depart_num')
                salary_from = data.get('salary_from',0)
                salary_to = data.get('salary_to',0)
                # get the objects of EmployeeDepartment table using the department number
                emp_objs= EmployeeDepartment.objects.filter(department__department_no = int(depart_no),active=2).values_list('employee',flat=True)
                # from employeedepartment objects get the Employee objetcs and query for the salary in beteween from and to values requested using Q models
                empl_details = Employee.objects.filter(Q(salary__gte=int(salary_from)),Q(salary__lte=int(salary_to)),id__in=emp_objs,active=2).order_by('-id')
                # get the details of the Employee to display
                details = EmployeeInfoSerializer(empl_details,many=True).data
                response = {'status':2,'message':'successfully retrieved','data':details}
            else:
                    response = {'status':0,'message': serializer.errors}
        except Exception as e:
            response = {'status':0,'message': str(e)}
        return Response(response)

    

class DepartmentList(g.ListAPIView):
    queryset = Department.objects.filter(active=2).order_by('-id') # this is reverse order
    serializer_class = DepartmentSerializer

class EmployeeDepList(g.ListAPIView):
    queryset = EmployeeDepartment.objects.filter(active=2).order_by('-id')
    serializer_class=EmployeeDeptSerializer

class DepartmentCreate(g.CreateAPIView):

    serializer_class = DepartmentSerializer
    def post(self, request, format=None):
        """
        API to create Departments Objects.
        ---
        """
        serializer =DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            response = {'status': 2, 'message': "Created Successfully", 'data':serializer.data}
        else:
            response = {'status': 0, 'message': serializer.errors}
        return Response(response)

class EmployeeRelation(g.CreateAPIView):

    serializer_class = EmployeeDeptSerializer
    def post(self, request, format=None):
        """
        API to create Departments Objects.
        ---
        """
        serializer = EmployeeDeptSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            response = {'status': 2, 'message': "Created Successfully", 'data':serializer.data}
        else:
            response = {'status': 0, 'message': serializer.errors}
        return Response(response)






