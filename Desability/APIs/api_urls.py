"""
api_urls.py

URL patterns for all API endpoints.
Include this in your Django project's urls.py:

    from django.urls import path, include
    import api_urls
    
    urlpatterns = [
        path('api/', include((api_urls.api_urlpatterns, 'api'))),
    ]
"""

from django.urls import path
from api_views import (
    api_auth_login,
    api_chat,
    api_candidates,
    api_cast_vote,
    api_results,
    api_survey_questions,
    api_submit_survey,
    api_survey_results,
)

api_urlpatterns = [
    # Authentication
    path('auth/login/', api_auth_login, name='auth_login'),
    
    # Chat / Helper
    path('chat/', api_chat, name='chat'),
    
    # Candidates & Voting
    path('candidates/', api_candidates, name='candidates'),
    path('vote/', api_cast_vote, name='cast_vote'),
    path('results/', api_results, name='results'),
    
    # Survey
    path('survey/questions/', api_survey_questions, name='survey_questions'),
    path('survey/submit/', api_submit_survey, name='survey_submit'),
    path('survey/results/', api_survey_results, name='survey_results'),
]
