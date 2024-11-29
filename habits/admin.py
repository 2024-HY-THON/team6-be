from django.contrib import admin
from .models import Category, Habit, Action

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'user', 'category', 'choose')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('habit_id', 'category', 'user', 'content')

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'do_or_not', 'created')