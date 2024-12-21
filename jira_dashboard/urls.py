"""
URL configuration for jira_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from jira_dashboard.views import users,project,tasks
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Jira Dashboard",
      default_version='v1',
      description="In this project I implemnet rest_freamework",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="rohandesai664@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('create-user',users.createUser),
    path('login',users.loginUsers),
    path('offboard-user',users.offboard_user),
    path('create-project',project.create_project),
    path('update-project',project.update_project),
    path('delete-project',project.delete_project),
    path('get-project-details',project.get_project_details),
    path('add-members',project.add_members),
    path('create-task',tasks.create_task),
    path('delete-task',tasks.delete_task),
    path('get-task-details',tasks.get_task_details),
    path('post-comment',tasks.post_comment),
    path('delete-comment',tasks.delete_comment),
    path('update-comment',tasks.update_comment),
    path('get-comment-details',tasks.get_comment_details),

]
