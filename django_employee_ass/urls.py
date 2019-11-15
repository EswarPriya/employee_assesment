from django.contrib import admin
from django.conf.urls import include,url
from employee.views import (EmployeeList,DepartmentList,DepartmentCreate,
    EmployeeCreate,EmployeeDepList,EmployeeRelation,Employeedetails,EmployeeUpdate,
    EmployeeInfo)

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^employee/list/$',EmployeeList.as_view()),
    url(r'^employee/create/$',EmployeeCreate.as_view()),
    url(r'^employee/update/(?P<pk>\d+)/$',EmployeeUpdate.as_view()),
    url(r'^employee/info/$',EmployeeInfo.as_view()),
    url(r'^department/list/$',DepartmentList.as_view()),
    url(r'^department/employee/list/$', EmployeeDepList.as_view()),
    url(r'^department/create/$',DepartmentCreate.as_view()),
    url(r'^employee/relation/$',EmployeeRelation.as_view()),
    url(r'^employee/details/$',Employeedetails.as_view())

    # Here add your URL's
]
