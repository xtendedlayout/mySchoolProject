from django.urls import path
from .views import LandingPageView,RegisterView, ValidateSigupView, LoginPageView, LogoutView,StudentPanelView, AdminPanelView,LoginView, AnnouncementCreateView, AnnouncementListView, AnnouncementTypeListView

app_name = "notice_board"
urlpatterns = [
    path('home/', LandingPageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/val/', ValidateSigupView.as_view(), name='signupval'),
    path('auth/', LoginPageView.as_view(), name='loginpage'),
    path('auth/val/', LoginView.as_view(), name='loginval'),
    path('admin/', AdminPanelView.as_view(), name='admin'),
    path('dashboard/', StudentPanelView.as_view(), name='dashboard'),
    path('dashboard/logout/', LogoutView.as_view(), name='logout'),
    path('admin/create/', AnnouncementCreateView.as_view(), name='create_announcement'),
    path('announcements/all/', AnnouncementListView.as_view(), name='list_announcements'),
    path('announcements/<str:type>/', AnnouncementTypeListView.as_view(), name='list_announcements_by_type'),
]
