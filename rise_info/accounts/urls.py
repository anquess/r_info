from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.account_list, name="account_list"),
    path('new/', views.account_new, name="account_new"),
    path('<int:pk>/del/', views.account_delete, name="account_delete"),
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='accounts/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='accounts/logout.html'
    ), name='logout'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),  
]
