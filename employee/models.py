from django.template.defaultfilters import slugify
import six
from django.contrib import admin
from django.views import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import models
from import_export.admin import ImportExportModelAdmin
# from django.utils.encoding import smart_str, smart_unicode



class BaseContentBase(models.base.ModelBase):
    
    def __iter__(self):
        return self.objects.all().__iter__()

    @staticmethod
    def register(mdl):
        if (not hasattr(mdl, 'Meta')) or getattr(
                getattr(mdl, '_meta', None),
                'abstract', True
        ):
            return mdl

        class MdlAdmin(ImportExportModelAdmin):
            list_display = ['__str__'] + getattr(mdl, 'admin_method', []) + [i.name for i in mdl._meta.fields]
            filter_horizontal = [i.name for i in mdl._meta.many_to_many]

        if hasattr(mdl, 'Admin'):
            class NewMdlAdmin(mdl.Admin, MdlAdmin):
                pass
            admin.site.register(mdl, NewMdlAdmin)

        else:
            admin.site.register(mdl, MdlAdmin)

    def __new__(cls, name, bases, attrs):
        mdl = super(BaseContentBase, cls).__new__(cls, name, bases, attrs)
        BaseContentBase.register(mdl)
        return mdl


class BaseContent(six.with_metaclass(BaseContentBase, models.Model)):
    # ---------comments-----------------------------------------------------#
    # BaseContent is the abstract base model for all
    # the models in the project
    # This contains created and modified to track the
    # history of a row in any table
    # This also contains switch method to deactivate one row if it is active
    # and vice versa
    # ------------------------ends here---------------------------------------------#

    ACTIVE_CHOICES = ((0, 'Inactive'), (2, 'Active'),)
    active = models.PositiveIntegerField(choices=ACTIVE_CHOICES,
                                         default=2, db_index=True,)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    #                                        BaseContent
    class Meta:
        #-----------------------------------------#
        # Don't create a table in database
        # This table is abstract
        #--------------------ends here--------------------#
        abstract = True

    # BaseContent
    def switch(self):
        # Deactivate a model if it is active
        # Activate a model if it is inactive
        self.active = {2: 0, 0: 2}[self.active]
        self.save()

    #  BaseContent
    def copy(self, commit=True):
        # Create a copy of given item and save in database
        obj = self
        obj.pk = None
        if commit:
            obj.save()
        return obj

    # BaseContent
    def __unicode__(self):
        for i in ['name', 'text']:
            if hasattr(self, i):
                return getattr(self, i, 'Un%sed' % i)
        if hasattr(self, '__str__'):
            return self.__str__()
        return super(BaseContent, self).__unicode__()

GENDER_CHOICES = ((1,'Male'),(2,'Female'),)

class Employee(BaseContent):
    first_name = models.CharField(max_length=25,blank=True,null=True)
    last_name = models.CharField(max_length=20,blank=True,null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    address = models.TextField()
    salary = models.IntegerField(default=0)
    employee_ref_id = models.CharField(max_length=15)
    birth_date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return str(self.first_name) +'_'+ str(self.last_name)

    class Meta:
        ordering = ['-id']

class Department(BaseContent):
    department_no = models.IntegerField(default=0)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.department_name)

class EmployeeDepartment(BaseContent):
    employee = models.ForeignKey('Employee',blank=True,null=True,on_delete=models.CASCADE)
    department = models.ForeignKey('Department',blank=True,null=True,on_delete=models.CASCADE)
    employee_role = models.CharField(max_length=50)
    hire_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
