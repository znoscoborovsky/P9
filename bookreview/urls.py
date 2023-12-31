"""
URL configuration for bookreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import authentication.views
import review.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", review.views.home, name="home"), 
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path("ticket/", review.views.create_ticket, name='ticket'),
    path("ticket/<int:ticket_id>/review/", review.views.create_review, name='review'),
    path("no_more_review/", review.views.no_more_critic, name='no_more_review'),
    path('ticket/<int:ticket_id>/edit/', review.views.edit_ticket, name='edit_ticket'),
    path('review/<int:review_id>/edit/', review.views.edit_review, name='edit_review'),
    path('ticket_and_review/', review.views.create_ticket_and_review, name='ticket_review'),
    path('follow-users/', review.views.follow_users, name='follow_users'),
    path('<int:follow_id>/', review.views.del_follower, name='del_follower')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# handling the 404 and 500 errors
handler404 = review.views.handler404
handler500 = review.views.handler500