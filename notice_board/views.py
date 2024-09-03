from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Announcement
from .serializers import UserSerializer, AnnouncementSerializer

User = get_user_model()

#The view class for the landing page
class LandingPageView(APIView):
    announcement_list = Announcement.objects.order_by('created_at')[:2]
    context={
        "latest_announcements" : announcement_list
    }
    def get(self, request):
        return render(request, "notice_board/homePage.html", self.context)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request):
        registering_user = User.get(username=request.POST["username"], password=request.POST["password"])
        return HttpResponse("registering")

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=400)
    
class LoginPageView(APIView):
    def get(self,request):
        return render(request, "notice_board/login.html")

class AnnouncementCreateView(generics.CreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AnnouncementListView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnnouncementTypeListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        type = self.kwargs['type']
        return Announcement.objects.filter(type=type)

