from django.urls import path
from .views import LandingPageView,RegisterView, LoginPageView, LoginView, AnnouncementCreateView, AnnouncementListView, AnnouncementTypeListView

urlpatterns = [
    path('home/', LandingPageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('loginPage/', LoginPageView.as_view(), name='loginpage'),
    path('login/', LoginView.as_view(), name='login'),
    path('announcements/', AnnouncementCreateView.as_view(), name='create_announcement'),
    path('announcements/all/', AnnouncementListView.as_view(), name='list_announcements'),
    path('announcements/<str:type>/', AnnouncementTypeListView.as_view(), name='list_announcements_by_type'),
]
