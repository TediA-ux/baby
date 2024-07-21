"""
URL configuration for daystar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import Login
from user.views import register
from user.forms import UserRegisterForm
from user import views as user_view
from django.contrib.auth import views as auth

from baby_sitting.views import (
    babies_baby_sitting_check_in,
    babies_create_view,
    babies_list_and_detail_view,
    babies_outstandings,
    babies_pay_view,
    baby_sitters_create_and_edit_view,
    baby_sitters_list_and_detail_view,
    baby_sitting_check_out,
    baby_sittings_list,
    payments_list,
)

urlpatterns = [
    path("", babies_list_and_detail_view),
    path("baby-sitters/", baby_sitters_list_and_detail_view),
    path("baby-sitters/<uuid:pk>/", baby_sitters_list_and_detail_view),
    path("baby-sitters/add/", baby_sitters_create_and_edit_view),
    path("baby-sitters/<uuid:pk>/edit/", baby_sitters_create_and_edit_view),
    path("babies/", babies_list_and_detail_view),
    path("babies/<uuid:pk>/", babies_list_and_detail_view),
    path("babies/<uuid:pk>/outstandings/", babies_outstandings),
    path("babies/<uuid:pk>/pay/", babies_pay_view),
    path("babies/<uuid:pk>/check-in/", babies_baby_sitting_check_in),
    path("babies/add/", babies_create_view),
    path("baby-sittings/", baby_sittings_list),
    path("baby-sittings/<uuid:pk>/check-out/", baby_sitting_check_out),
    path("payments/", payments_list),
    path("admin/", admin.site.urls),
   
    path('', include('user.urls')),
    path('login/', Login, name ='login'),
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    path('register/', register, name ='register'),
 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
