from django.contrib import admin

from .models import *

admin.site.register(Pass)
admin.site.register(TeacherPass)
admin.site.register(LocationPass)
admin.site.register(SRTPass)
admin.site.register(SpecialSRTPass)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(Location)
