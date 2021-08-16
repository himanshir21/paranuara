from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PeopleListView, PeopleRetrieveView, CommonFriendView

urlpatterns = [
    path('company/<int:company_index>/peoples', PeopleListView.as_view()),
    path('people/<int:index>', PeopleRetrieveView.as_view()),
    path('common_friends/<int:p1_index>/<int:p2_index>',
         CommonFriendView.as_view()),
]
