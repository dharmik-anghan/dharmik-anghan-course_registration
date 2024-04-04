"""
URL configuration for filomather project.

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
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("account.urls")),
    path("api/admin/", include("custom_admin.urls")),
    path("api/instructor/", include("instructor.urls")),
    path("api/course/", include("course.urls")),
    path("api/student/", include("student.urls")),
    path("api/review/", include("review.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Course API Portal Admin"
admin.site.site_title = "Course App Admin Portal"
admin.site.index_title = "Welcome to Course Admin Portal"
