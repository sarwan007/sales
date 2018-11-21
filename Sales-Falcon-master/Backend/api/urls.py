from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('user/register', views.UserRegistration.as_view()),
    path('user/login', views.Login.as_view()),
    path('user/logout', views.Logout.as_view()),
    path('user/profile', views.UserDetails.as_view()),
    re_path(r'^user/upload/(?P<filename>[^/]+)$', views.FileUpload.as_view()),
    path('user/customers', views.CustomerDetails.as_view()),
    path('user/email', views.SendEmail.as_view()),
    path('notes', views.MeetingNotesView.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)

