from django.contrib import admin
from .models import Career, StudentQuery

admin.site.site_header = 'Student Guidance Portal — Admin'
admin.site.site_title = 'Student Guidance Portal Admin'
admin.site.index_title = 'Manage Student Queries & Career Guidance'


@admin.register(StudentQuery)
class StudentQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'short_question', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'question', 'answer')
    readonly_fields = ('created_at',)
    fields = ('user', 'category', 'question', 'answer', 'status', 'created_at')

    @admin.display(description='Question')
    def short_question(self, obj):
        return obj.question[:60] + ('...' if len(obj.question) > 60 else '')


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'description', 'skills', 'job_roles')
    prepopulated_fields = {'slug': ('title',)}
