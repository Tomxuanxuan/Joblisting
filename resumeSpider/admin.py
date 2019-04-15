from django.contrib import admin

# Register your models here.
from .models import *
class PosbriefAdmin(admin.ModelAdmin):
    list_display = ('jobName', 'salary', 'businessArea', 'updateDate', 'createDate')

class PositionsAdmin(admin.ModelAdmin):
    list_display = ('pos_title', 'pos_salary', 'pos_company', 'pos_address', 'pos_bright')

admin.site.register(Posbrief, PosbriefAdmin)
admin.site.register(Positions, PositionsAdmin)
