from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import sessions
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, permissions # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
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
    def get(self, request):
        return render(request, "notice_board/signup.html")

class ValidateSigupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request):
        name = request.data.get('fullname')
        email = request.data.get('email')
        password = request.data.get('password')
        tempuser = User.objects.filter(email=email).first()
        if tempuser:
            return render(request, "notice_board/signup.html",{'error': 'This email is already Registered'})
        newUser = User(first_name=name, email= email, password=password, role="student")
        newUser.save()
        request.session["name"]= newUser.first_name
        request.session["role"]= newUser.role
        return HttpResponseRedirect(reverse("notice_board:dashboard"))
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.password == password:
            #refresh = RefreshToken.for_user(user)
            #return Response({
             #   'refresh': str(refresh),
            #    'access': str(refresh.access_token),
            #})
            request.session["name"]= user.username
            request.session["role"]= user.role
            if user.role == "admin":
                return HttpResponseRedirect(reverse("notice_board:admin"))
            return HttpResponseRedirect(reverse("notice_board:dashboard"))
        return Response({'error': 'Invalid Credentials'}, status=400)
    
class LoginPageView(APIView):
    def get(self,request):
        return render(request, "notice_board/login.html")

class StudentPanelView(APIView):
    announcement_list = Announcement.objects.order_by('created_at')[:2]
    context={
        "latest_announcements" : announcement_list
    }

    def get(self, request):
        return render(request, "notice_board/studentPanel.html", self.context)

class AdminPanelView(APIView):
    announcement_list = Announcement.objects.order_by('created_at')[:2]
    context={
        "latest_announcements" : announcement_list
    }

    def get(self, request):
        return render(request, "notice_board/adminPanel.html", self.context)

 #currently of no use   
class LoginValidateView(APIView):
    def post(self,request):
        if request.method =="POST":
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                return HttpResponse("You are logged in")
            else:
                return HttpResponse("enable cookies and try again")
        request.session.set_test_cookie()
        return render(request, "notice_board/login.html")
    

class LogoutView(APIView):
    def get(self, request):
        uzer =request.session["name"]
        if uzer:
            del request.session["name"]
            return HttpResponseRedirect(reverse("notice_board:home"))

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

