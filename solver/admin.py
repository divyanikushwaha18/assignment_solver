from django.contrib import admin
from .models import Assignment, Solution

# Explicitly register models
admin.site.register(Assignment)
admin.site.register(Solution)


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignment_type', 'status', 'created_by', 'created_at')
    list_filter = ('assignment_type', 'status')
    search_fields = ('title', 'description')


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'created_by', 'created_at')
    list_filter = ('assignment__assignment_type',)
    search_fields = ('content', 'assignment__title')
