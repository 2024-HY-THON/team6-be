from django.contrib import admin
from .models import Category, Habit

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'user', 'category', 'choose')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('habit_id', 'category', 'user', 'content')
