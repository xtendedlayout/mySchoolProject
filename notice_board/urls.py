from django.urls import path
from .views import RegisterView, LoginView, AnnouncementCreateView, AnnouncementListView, AnnouncementTypeListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('announcements/', AnnouncementCreateView.as_view(), name='create_announcement'),
    path('announcements/all/', AnnouncementListView.as_view(), name='list_announcements'),
    path('announcements/<str:type>/', AnnouncementTypeListView.as_view(), name='list_announcements_by_type'),
]
