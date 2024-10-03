from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import sessions
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, permissions # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from django.contrib.auth import get_user_model
from .models import Announcement, Comments
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
            request.session["id"] = user.id
            if user.role == "admin":
                return HttpResponseRedirect(reverse("notice_board:admin"))
            return HttpResponseRedirect(reverse("notice_board:dashboard"))
        return Response({'error': 'Invalid Credentials'}, status=400)
    
class LoginPageView(APIView):
    def get(self,request):
        return render(request, "notice_board/login.html")

class StudentPanelView(APIView):
    announcement_list = Announcement.objects.order_by('created_at')[:5]
    #general_announcements = Announcement.objects.filter("Genral").order_by('created_at')[:10]
    context={
        "latest_announcements" : announcement_list
    }

    def get(self, request):
        return render(request, "notice_board/studentPanel.html", self.context)

class AdminPanelView(APIView):

    def get(self, request):
        return render(request, "notice_board/adminPanel.html")

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
    #permission_classes = [permissions.IsAuthenticated]

    #def perform_create(self, serializer):
    #    serializer.save(created_by=self.request.user)
    def post(self, request):
        choiceCounter = 0
        typeList = ["General", "Intake", "Class", "Course"]
        choices = [request.data.get('General'), request.data.get('Intake'), request.data.get('Class'), request.data.get('Course')]
        for choice in choices:
            if(choice):
                choiceCounter += 1
                category = typeList[choices.index(choice)]
        if(choiceCounter != 1):
            return  HttpResponseRedirect(reverse("notice_board:admin", errorMessage = {'msg': "Select one category only"}))
        title = request.data.get('title')
        content = request.data.get('content')
        userId = request.session["id"]
        if(title=="" or content==""):
            errorMessage = {
                "msg": "Post should have both a title and content"
            }
            return  HttpResponseRedirect(reverse("notice_board:admin"), errorMessage)
        newAnnouncement = Announcement(title=title, content=content, type=category,created_by_id=userId)
        newAnnouncement.save()
        return HttpResponseRedirect(reverse("notice_board:admin"))


class AnnouncementCommentView(APIView):
    def post(self, request):
        comment = request.data.get('comment')
        announcement_id = request.data.get('announcement_id')
        user_id = request.session["id"]
        if comment:
            newComment = Comments(comment=comment, created_by=user_id,comment_for=announcement_id)
            newComment.save()
            return HttpResponseRedirect(reverse("notice_board:dashboard"))
        

        

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

