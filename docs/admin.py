from django.contrib import admin
from .models import *


@admin.register(Doc)
class AdminDoc(admin.ModelAdmin):
    list_display = ['title', 'user', 'status']

@admin.register(Person)
class AdminPerson(admin.ModelAdmin):
    list_display = ['name', 'institution']

@admin.register(Institution)
class AdminInstitution(admin.ModelAdmin):
    list_display = ['title',]
