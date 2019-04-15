

# Register your models here.
from django.contrib import admin
from .models import *

# university = models.CharField(verbose_name='毕业院校', max_length=200, default='略')
# major = models.CharField(verbose_name='专业', max_length=50, default='略')
# edu = models.CharField(verbose_name='学历', max_length=20, default='本科')
# honortitle = models.CharField(verbose_name='荣誉', max_length=100, default='无')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'sex', 'email', 'phone', 'birth_time', 'address', 'aboutme')

    list_editable = ('name', 'email', 'phone', 'birth_time', 'address', 'aboutme')
    fieldsets = (
        (
            "基本选项",{
                "fields": ('username', 'email','photo', 'phone', 'birth_time', 'address', 'aboutme', 'university','major','edu', 'honortitle')
            }),
    )

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('worktime', 'company', 'position', 'responsibility', 'user')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pro_name', 'pro_environment', 'pro_brief', 'pro_responsibility')



class ContactAdmin(admin.ModelAdmin):
    list_display = ('con_name', 'con_email', 'con_number', 'con_message', 'con_time')

class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skillinfo')
    list_editable = ('skillinfo',)


    # sillinfo = models.TextField(verbose_name='专业技能')
    #
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

admin.site.register(User, AuthorAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Projects, ProjectAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Skill, SkillAdmin)
