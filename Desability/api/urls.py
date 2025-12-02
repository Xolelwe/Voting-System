from django.urls import path
from .views import test_api
from .views import accessibility_instructions 

urlpatterns = [
    path('test/', test_api),
    path('instructions/', accessibility_instructions),
]
