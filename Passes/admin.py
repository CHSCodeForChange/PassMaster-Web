from django.contrib import admin
from .models import Pass, TeacherPass, LocationPass, SRTPass

admin.site.register(Pass)
admin.site.register(TeacherPass)
admin.site.register(LocationPass)
admin.site.register(SRTPass)
