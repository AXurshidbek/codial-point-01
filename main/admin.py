from django.contrib import admin
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'point_limit')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mentor', 'active')
    list_display_links = ('id', 'name')
    list_filter = ('mentor', 'active')
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user__first_name', 'user__last_name', 'point', 'group')
    list_display_links = ('id', 'user')
    list_filter = ('group',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    ordering = ('-point',)
    list_editable = ('point',)


@admin.register(PointType)
class PointTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'max_point')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(GivePoint)
class GivePointAdmin(admin.ModelAdmin):
    list_display = ('id', 'mentor', 'student__user__username', 'amount', 'point_type', 'description', 'date')
    list_display_links = ('id', 'mentor', 'student__user__username')
    list_filter = ('mentor', 'student', 'point_type', 'date')
    search_fields = (
        'student__user__username', 'student__user__first_name', 'student__user__last_name',
        'mentor__user__username', 'mentor__user__first_name', 'mentor__user__last_name'
    )


@admin.register(New)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at','seminary')
    list_display_links = ('id', 'title')
    search_fields = ('title','description')
    list_filter = ('created_at',)


