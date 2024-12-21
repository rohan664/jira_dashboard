from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator



class Project(models.Model):
    '''Model define Project'''
    title = models.CharField(max_length=256,blank=False,null=False,unique=True)
    description = models.TextField(null=False,blank=False)
    is_deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdBy = models.ForeignKey('customUsers',on_delete=models.CASCADE,related_name='created_projects')

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'jira_dashboard'
        ordering = ['-createdAt']
        db_table = 'projects'


class customUsers(AbstractUser):
    phone = models.CharField(max_length=15, null=False,blank=False,unique=True)
    bio = models.TextField(null=True)
    profile_url = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    username  = models.CharField(max_length=256,null=False,unique=True,blank=False)
    email  = models.EmailField(max_length=256,null=False,unique=True,blank=False)

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ('phone', 'email','username') 
        app_label = 'jira_dashboard'
        ordering = ['-createdAt']
        db_table  = 'users'

class Membership(models.Model):
    """Model to represent membership of users in projects with roles"""
    user = models.ForeignKey('customUsers', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50, 
        choices=[
            ('Admin', 'Admin'), 
            ('Member', 'Member'),
        ],
        default='Member'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        app_label = 'jira_dashboard'
        db_table = 'memberships'

class Task(models.Model):
    """Model represent the task associated with project"""
    title = models.CharField(max_length=256,blank=False,null=False)
    description = models.TextField(null=True)
    project = models.ForeignKey("Project",on_delete=models.CASCADE)
    deassignee = models.BooleanField(default=False)
    storyPoint = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    assignee = models.ForeignKey("customUsers",on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'jira_dashboard'
        db_table = 'task'

class TaskComment(models.Model):
    '''Model represent comment associated with task'''
    comment = models.TextField()
    task_id = models.ForeignKey("task",on_delete=models.CASCADE)
    createdBy = models.ForeignKey("customUsers",on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'jira_dashboard'
        db_table = 'comment'

