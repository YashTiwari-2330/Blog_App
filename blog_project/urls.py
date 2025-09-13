"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog_app import views
from django.contrib.auth.views import LoginView, LogoutView 
urlpatterns = [
    # path('' , views.index , name='index'),
    path('' , views.post_list , name='post_list'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('posts/create/' , views.post_create , name='post_create'),
    path('posts/<int:id>/edit/' , views.post_edit , name='post_edit'),
    path('posts/<int:id>/delete/', views.post_delete, name='post_delete'),
    path('posts/drafts/', views.post_draft_list, name='post_draft_list'),
    path('posts/<int:id>/publish/', views.post_publish, name='post_publish'),
    path('register/', views.register, name='register'),  # type: ignore
    path("search/", views.search_post, name="search_post"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)