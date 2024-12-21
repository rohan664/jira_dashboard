import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from jira_dashboard.utils.messages import SOMETHING_WENT_WRONG,INVALID_REQUEST_OBJECT,PROJECT_DETAILS_NOT_FOUND, \
    DO_NOT_HAVE_NECCESSARY_PERMISSION,TASK_CREATED_SUCCESSFULLY,TASK_DELETED_SUCCESSFULLY,TASK_DETAILS_NOT_FOUND,DATA_RETRIVE_SUCCESSFULLY,\
        COMMENT_CREATED_SUCCESSFULLY,COMMENT_NOT_FOUND,COMMENT_DELETED_SUCCESSFULLY,COMMENT_UPDATE_SUCCESSFULLY,INVALID_PAGE_NUMBER
from jira_dashboard.utils.constants import SUCCESS,FAIL,CREATE_TASK,POST_COMMENT,SWAGGER_BAD_REQUEST,SWAGGER_INTERNAL_SERVER_ERROR,SWAGGER_SUCCESS,UPDATE_COMMENT
from jira_dashboard.utils.common_function import retrun_object_func,get_pagination_data
from jira_dashboard.models import Project,customUsers,Membership,Task,TaskComment
from jira_dashboard.serializers import TaskSerializer,TaskModelSeriliazers,TaskCommentSeriliazers
from drf_yasg.utils import swagger_auto_schema
from  jira_dashboard.views.swagger_request_schema import AUTH_PARAMS,DELETE_TASK_SCHEMA,PAGINATION_SCHEMA,PROJECT_SCHEMA,ADD_COMMENT_SCHEMA,DELETE_COMMENT_SCHEMA,UPDATE_COMMENT_SCHEMA

@swagger_auto_schema(
    method="post",
    operation_description="This function is used to create task",
    request_body=TaskSerializer,
    manual_parameters=[AUTH_PARAMS], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["POST","PATCH"])
@csrf_exempt
def create_task(request):
    '''This function is used to create task'''
    try:
        request_body = json.loads(request.body)
        return_object = {}
        # get project details base on name
        if not all([value in request_body for value in CREATE_TASK]):
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        project = Project.objects.get(id=request_body.get("project_id"))
        if not project:
            return_object = retrun_object_func(FAIL,PROJECT_DETAILS_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        isMember = Membership.objects.filter(user=request_body.get("createdBy"),project=project.id)
        if not isMember:
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=400)
        if request_body.get("task_id"):
            task_details = Task.objects.filter(id=request_body.get("task_id")).first()
            if not task_details:
                return_object = retrun_object_func(FAIL,TASK_DETAILS_NOT_FOUND)
                return JsonResponse(return_object,safe=False,status=400)
            serializers = TaskSerializer(task_details,data=request_body)
        else:
            serializers = TaskSerializer(data=request_body,context={"project":project})
        if not serializers.is_valid():
            return_object = retrun_object_func(FAIL,serializers.errors)
            return JsonResponse(return_object,safe=False,status=400)
        serializers.save()
        return_object = retrun_object_func(SUCCESS,TASK_CREATED_SUCCESSFULLY)

    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)


@swagger_auto_schema(
    method="delete",
    operation_description="This function is used to delete task",
    manual_parameters=[AUTH_PARAMS,DELETE_TASK_SCHEMA], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["DELETE"])
@csrf_exempt
def delete_task(request):
    try:
        return_object = {}
        request_body = json.loads(request.body)
        # check task_id is present or not in params
        task_id = request.GET.get("task_id")
        if not task_id:
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return_object = retrun_object_func(FAIL,TASK_DELETED_SUCCESSFULLY)
            return JsonResponse(return_object,safe=False,status=400)
        isMember = Membership.objects.filter(user=request_body.get("createdBy"),project=task.project,role="admin")
        if not isMember:
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=400)
        task.is_deleted = True
        task.save()
        return_object = retrun_object_func(SUCCESS,TASK_DELETED_SUCCESSFULLY)

    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="get",
    operation_description="This function is used to get task details",
    manual_parameters=[AUTH_PARAMS,PAGINATION_SCHEMA,PROJECT_SCHEMA], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)       
@api_view(["GET"])        
@csrf_exempt
def get_task_details(request):
    try:
        request_body = json.loads(request.body)
        return_object = {}
        # check the project_id is present or not
        page_number = request.GET.get("page_number")
        project_details = Project.objects.filter(is_deleted=False,createdBy=request_body.get("createdBy"))
        if not project_details:
            return_object = retrun_object_func(FAIL,PROJECT_DETAILS_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        task_details = Task.objects.filter(project__in=project_details,is_deleted=False)
        if not task_details:
            return_object = retrun_object_func(FAIL,TASK_DETAILS_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        if page_number:
            paginated_data,error = get_pagination_data(task_details,page_number,TaskModelSeriliazers)
            if error:
                return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},error)
                return JsonResponse(return_object,safe=False,status=500) 
            return_object = retrun_object_func(SUCCESS,DATA_RETRIVE_SUCCESSFULLY,paginated_data)
            return JsonResponse(return_object,safe=False,status=200)
        paginated_data = TaskModelSeriliazers(data=task_details)
        return_object = retrun_object_func(SUCCESS,DATA_RETRIVE_SUCCESSFULLY,paginated_data.data)

    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="post",
    operation_description="This function is used to post comment on task",
    request_body=ADD_COMMENT_SCHEMA,
    manual_parameters=[AUTH_PARAMS], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["POST"])
@csrf_exempt
def post_comment(request):
    try:
        request_body = json.loads(request.body)
        return_object = {}
        if not all([key in request_body for key in POST_COMMENT]):
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        task = Task.objects.filter(id=request_body.get("task_id"),is_deleted=False).first()
        if not task:
            return_object = retrun_object_func(FAIL,TASK_DETAILS_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        is_member = Membership.objects.filter(project=task.project,user=request_body.get("createdBy"))
        if not is_member:
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=400)
        serializer = TaskCommentSeriliazers(data=request_body)
        if not serializer.is_valid():
            return_object = retrun_object_func(FAIL,serializer.errors)
            return JsonResponse(return_object,safe=False,status=400)
        serializer.save()
        return_object = retrun_object_func(SUCCESS,COMMENT_CREATED_SUCCESSFULLY)
        
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="delete",
    operation_description="This function is used to delete comments",
    request_body=None,
    manual_parameters=[AUTH_PARAMS,DELETE_COMMENT_SCHEMA], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(['DELETE'])
@csrf_exempt
def delete_comment(request):
    try:
        request_body = json.loads(request.body)
        return_object = {}
        comment_id = request.GET.get("comment_id")
        if not comment_id:
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        comment_details = TaskComment.objects.filter(is_deleted=False,createdBy=request_body.get("createdBy"),id=comment_id).first()
        if not comment_details:
            return_object = retrun_object_func(FAIL,COMMENT_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        comment_details.is_deleted = True
        comment_details.save()
        return_object = retrun_object_func(SUCCESS,COMMENT_DELETED_SUCCESSFULLY)
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)
        

@swagger_auto_schema(
    method="patch",
    operation_description="This function is used to update the comment",
    request_body=UPDATE_COMMENT_SCHEMA,
    manual_parameters=[AUTH_PARAMS], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(['PATCH'])
@csrf_exempt
def update_comment(request):
    try:
        request_body = json.loads(request.body)
        return_object = {}
        if not all([key in request_body for key in UPDATE_COMMENT]):
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        comment_details = TaskComment.objects.filter(is_deleted=False,id=request_body.get("comment_id"),task_id=request_body.get("task_id")).first()
        if not comment_details:
            return_object = retrun_object_func(FAIL,COMMENT_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        if not comment_details.createdBy != request_body.get("createdBy"):
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=400)
        comment_details.comment = request_body.get("comment")
        comment_details.save()
        return_object = retrun_object_func(SUCCESS,COMMENT_UPDATE_SUCCESSFULLY)
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="get",
    operation_description="This function is used to get comments",
    request_body=None,
    manual_parameters=[AUTH_PARAMS,PAGINATION_SCHEMA,DELETE_TASK_SCHEMA], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(['GET'])
@csrf_exempt
def get_comment_details(request):
    try:
        return_object = {}
        page_number = request.GET.get("page_number")
        task_id = request.GET.get("task_id")
        comment_details = TaskComment.objects.filter(is_deleted=False,task_id = task_id)
        if not comment_details:
            return_object = retrun_object_func(FAIL,COMMENT_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        if not (page_number and int(page_number) > 0):
            return_object = retrun_object_func(FAIL,INVALID_PAGE_NUMBER)
            return JsonResponse(return_object,safe=False,status=400)  
        paginated_data,error = get_pagination_data(comment_details,page_number,TaskCommentSeriliazers)
        if error:
            return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},error)
            return JsonResponse(return_object,safe=False,status=500) 
        return_object = retrun_object_func(SUCCESS,DATA_RETRIVE_SUCCESSFULLY,paginated_data)
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)