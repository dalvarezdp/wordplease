"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from blogs.views import posts_list, blogs_list, blog_detail
from users.views import LoginView, logout, SignupView
from wordplease import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', posts_list, name="posts_list"), # si la URL es / , ejecutar función posts_list
    url(r'^blogs', blogs_list, name="blogs_list"),
    url(r'^blog/(?P<username>\w+)', blog_detail, name="blog_detail"),
    url(r'^login', LoginView.as_view(), name="login"),
    url(r'^signup', SignupView.as_view(), name="signup"),
    url(r'^logout$', logout, name="logout")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
