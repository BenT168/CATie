from django.contrib import admin

# Register your models here.
from courses.models import Course, Year, Session

admin.site.register(Course)
admin.site.register(Year)
admin.site.register(Session)    