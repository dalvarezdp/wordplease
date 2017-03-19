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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from blogs.api import BlogViewSet, PostViewSet, BlogUserViewSet
from blogs.views import posts_list, blogs_list, blog_detail, post_detail, NewPostView
from users.api import UserViewSet
from users.views import LoginView, logout, SignupView
from wordplease import settings

router = DefaultRouter()
router.register("users", UserViewSet, base_name="users_api")
router.register("blog/(?P<username>\w+)", BlogViewSet)
router.register("posts", PostViewSet, base_name="posts_api")
router.register("blogs", BlogUserViewSet, base_name="blogs_api")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', posts_list, name="posts_list"), # si la URL es / , ejecutar función posts_list
    url(r'^blogs$', blogs_list, name="blogs_list"),
    url(r'^blog/(?P<username>\w+)$', blog_detail, name="blog_detail"),
    url(r'^blog/(?P<username>\w+)/(?P<post_id>\w+)', post_detail, name="post_detail"),
    url(r'^new-post$', NewPostView.as_view(), name="new_post"),
    url(r'^login', LoginView.as_view(), name="login"),
    url(r'^signup', SignupView.as_view(), name="signup"),
    url(r'^logout$', logout, name="logout"),

    # API Users & Posts
    url(r'^api/1.0/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
