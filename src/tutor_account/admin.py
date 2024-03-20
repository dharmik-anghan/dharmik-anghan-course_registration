from django.contrib import admin

from tutor_account.models import Tutor

# Register your models here.

class TutorAdmin(admin.ModelAdmin):
    list_display = ['id', 'qualification', 'course_count', 'application_accepted', 'application_accepted_by']

admin.site.register(Tutor, TutorAdmin)
