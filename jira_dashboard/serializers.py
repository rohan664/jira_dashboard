from rest_framework import serializers
from jira_dashboard.models import customUsers,Project,Membership,Task,TaskComment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = customUsers
        fields = ['id','username','first_name','last_name','email','phone','profile_url','bio','password','is_active']

    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must include at least one numeric character.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must include at least one alphabetic character.")
        if value.lower() == value or value.upper() == value:
            raise serializers.ValidationError("Password must include both uppercase and lowercase characters.")
        return value
    
    def create(self, validated_data):
        user = customUsers(
            username=validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            profile_url=validated_data.get('profile_url'),
            bio = validated_data.get('bio')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)
        instance.profile_url = validated_data.get('profile',instance.profile_url)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.is_active = validated_data.get('is_active',instance.is_active)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
# project 
class ProjectSerializers(serializers.ModelSerializer):
    createdBy = UserSerializer(read_only=True)
    class Meta:
        model= Project
        fields = ['title','description','createdBy','createdAt','updatedAt','is_deleted']

    def create(self, validated_data):
        created_by_user = self.context.get('createdBy')
        project = Project(
            title = validated_data['title'],
            description = validated_data['description'],
            createdBy = created_by_user
        )
        project.save()

        membership = Membership(
            role = "admin",
            user = created_by_user,
            project = project
        )
        membership.save()
        
        return project
        

class MembershipSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Membership
        fields = ["id","role"]

    def create(self, validated_data):
        project = self.context.get('project')
        user = customUsers.objects.get(id=validated_data['id'])
        membership, created = Membership.objects.update_or_create(
            project=project,
            user=user,
            defaults={'role': validated_data['role']}
        )
        return membership

class AddMembersSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    members = MembershipSerializers(many=True)

    def create(self, validated_data):
        project = Project.objects.get(id=validated_data['project_id'])
        members_data = validated_data['members']
        memberships = []
        for member_data in members_data:
            serializer = MembershipSerializers(data=member_data, context={'project': project})
            serializer.is_valid(raise_exception=True)
            memberships.append(serializer.save())
        return memberships
    
class TaskSerializer(serializers.Serializer):
    project_id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    storyPoint = serializers.IntegerField()
    createdBy = serializers.IntegerField()

    def create(self, validated_data):
        project = self.context.get("project")
        # get assignee
        user = customUsers.objects.get(id=validated_data.get("createdBy"))
        if not user:
            raise serializers.ValidationError({"error":"User not found with the given ID."})
        print(user)
        task = Task(
            title = validated_data.get("title"),
            description = validated_data.get("description"),
            project = project,
            storyPoint = validated_data.get("storyPoint"),
            assignee = user
        )
        task.save()
        return task
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.description = validated_data.get("description")
        instance.storyPoint = validated_data.get("storyPoint")
        instance.save()
        return instance
    
class TaskModelSeriliazers(serializers.ModelSerializer):
    project = ProjectSerializers()
    class Meta:
        model = Task
        fields = ['id','title','description','project','deassignee','assignee','createdAt','updatedAt','is_deleted']

class TaskCommentSeriliazers(serializers.ModelSerializer):
    task_id = TaskModelSeriliazers(read_only=True)
    class Meta:
        model = TaskComment
        fields = ['id','comment','task_id','createdBy','createdAt','updatedAt','is_deleted']
