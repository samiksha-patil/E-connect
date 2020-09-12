"""my_classroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from classroom import views as room
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html') ,name='logout'),
    path('item/upload',room.create_classroom,name='create_room'),
    path('item/detail/<int:pk>',room.ClassroomDetailView.as_view(), name='product'),
    path('add_to_cart/<int:pk>/',room.add_to_cart,name='add_to_cart'),
    path('add/',room.StudentJoint,name='add'),
    path('',room.ClassroomSummaryView.as_view(),name='order-summary'),
    path('item/room_detail/<int:pk>',room.RoomDetailView.as_view(), name='detail'),
    path('item/<int:pk>/comment/',room.add_comment_to_room, name='add_comment_to_room'),
    path('comment/<int:pk>/',room.CommentDetailView.as_view(),name='comment_detail'),
    path('comment/<int:pk>/answer/',room.add_answer_to_comment, name='add_answer_to_comment'),
    path('item/detail/<int:pk>/quiz/ad/',room.QuizCreateView.as_view(),name='quiz_add'),
    path('quiz/<int:pk>/', room.QuizUpdateView.as_view(), name='quiz_change'),
    path('quiz/<int:pk>/question/add/', room.question_add, name='question_add'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/', room.question_change, name='question_change'),
    path('student/quiz/<int:pk>/', room.take_quiz, name='take_quiz'),
    path('student/quiz/<int:pk>/result', room.result, name='result'),
    path('student/quiz/<int:pk>/dashboard', room.TakenQuizListView, name='dashboard'),
    path('item/room_detail/<int:pk>/quiz',room.RoomDetailQuizView.as_view(), name='detail_Quiz'),
    path('item/detail/<int:pk>/assignment/ad/',room.AssignmentCreateView.as_view(),name='assignment_add'),
    path('student/assignment/<int:pk>/', room.solution_assignment, name='sol_ass'),
    path('item/room_detail/<int:pk>/assignment/',room.RoomDetailAssignmentView.as_view(), name='detail_assignment'),
    path('student/assignment/<int:pk>/dashboard/', room.TakenAssignmentListView, name='ass_dashboard'),
    path('student/assignment/grade/<int:pk>/', room.GradeAssignment, name='ass_grade'),
    path('item/<int:pk>/classmates/',room.classmates, name='classmates'),
    path('profile/', user_views.profile, name='profile'),
    path('remove_from_cart/<int:pk>/',room.remove_from_cart,name='remove_from_cart'),
    path('item/<int:pk>/delete/',room.RoomDeleteView.as_view(template_name='classroom/item_confirm_delete.html'),name='room-delete'),
    path('quiz/<int:pk>/delete/', room.QuizDeleteView.as_view(), name='quiz_delete'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', room.QuestionDeleteView.as_view(), name='question_delete'),
    path('item/detail/<int:pk>/announcement/add/',room.AnnouncementCreateView.as_view(),name='announcement_add'),
    path('item/room_detail/<int:pk>/announcement/',room.RoomDetailAnnouncementView.as_view(), name='detail_announcement'),
    
    
]
if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   