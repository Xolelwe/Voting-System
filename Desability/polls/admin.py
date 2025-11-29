# polls/admin.py
from django.contrib import admin
from .models import Poll, Choice, SurveyResponse

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('title', 'pub_date')

@admin.register(SurveyResponse)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')
