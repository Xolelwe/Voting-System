from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('menu/', views.menu, name='menu'),
    path('vote/', views.vote_page, name='vote'),
    path('vote/submit/<int:choice_id>/', views.submit_vote, name='submit_vote'),
    path('survey/', views.survey_page, name='survey'),
    path('survey/submit/', views.submit_survey, name='submit_survey'),
    path('results/', views.results, name='results'),
]



