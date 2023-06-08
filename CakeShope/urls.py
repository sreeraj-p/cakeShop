"""CakeShope URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from cakes import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cakes/add/',views.CakeCreateView.as_view(),name='cake-add'),
    path('cakes/list/',views.CakeListView.as_view(),name='cake-list'),
    path('cake/<int:j>/details/',views.CakeDetailsView.as_view(),name='cake-detail'),
    path('cake/<int:j>/change',views.CakeEditView.as_view(),name='cake-edit'),
    path('cake/<int:j>/remove',views.CakeDeleteView.as_view(),name='cake-delete'),
    path('register/',views.SignUpView.as_view(),name='register'),
    path('',views.SignInView.as_view(),name='signin'),
    path('signout/',views.sign_out_view,name='logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
