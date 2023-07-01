from django.urls import re_path as url
from ModelApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   url('predict/',views.predict),
   url('updateReviewState/', views.UpdateReviewStateAPI)
]

