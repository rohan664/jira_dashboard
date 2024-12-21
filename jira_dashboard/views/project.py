import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from jira_dashboard.utils.common_function import retrun_object_func,get_pagination_data
from jira_dashboard.utils.constants import SUCCESS,FAIL,CREATE_PROJECT_FIELDS,CREATE_MEMBERS,SWAGGER_BAD_REQUEST,SWAGGER_INTERNAL_SERVER_ERROR,SWAGGER_SUCCESS,UPDATE_PROJECT
from jira_dashboard.utils.messages import SOMETHING_WENT_WRONG,INVALID_REQUEST_OBJECT,\
    PROJECT_CREATED_SUCCESSFULLY,USER_ID_IS_NOT_PRESENT,PROJECT_DETAILS_NOT_FOUND, \
        DO_NOT_HAVE_NECCESSARY_PERMISSION,PROJECT_DELETED_SUCCESSFULLY,FAIL_TO_DELETE_PROJECT,DATA_RETRIVE_SUCCESSFULLY,MEMBERS_ADDED_SUCCESSFULLY,PROJECT_UPDATE_SUCCESSFULLY,INVALID_PAGE_NUMBER
from jira_dashboard.serializers import ProjectSerializers,AddMembersSerializer
from jira_dashboard.models import Project,customUsers,Membership
from drf_yasg.utils import swagger_auto_schema
from jira_dashboard.views.swagger_request_schema import AUTH_PARAMS,CREATE_PROJECT_SCHEMA,PROJECT_SCHEMA,PAGINATION_SCHEMA,ADD_MEMBER_SCHEMA,UPDATE_PROJECT_SCHEMA

@swagger_auto_schema(
    method="post",
    operation_description="This function is used to create project",
    request_body=CREATE_PROJECT_SCHEMA,
    manual_parameters=[AUTH_PARAMS], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["POST"])
@csrf_exempt
def create_project(request):
    '''This function is used to create project'''
    try:
        request_body = json.loads(request.body)
        return_object = {}
        if not all([keys in request_body for keys in CREATE_PROJECT_FIELDS]):
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        user_data = customUsers.objects.get(id=request_body.get("createdBy"))
        serializers = ProjectSerializers(data=request_body,context={"createdBy":user_data})
        if not serializers.is_valid():
            return_object = retrun_object_func(FAIL,str(serializers.errors))     
            return JsonResponse(return_object,safe=False,status=400)
        serializers.save()
        return_object = retrun_object_func(SUCCESS,PROJECT_CREATED_SUCCESSFULLY,serializers.data)

    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="patch",
    operation_description="This function is used to update the project details",
    request_body=UPDATE_PROJECT_SCHEMA,
    manual_parameters=[AUTH_PARAMS], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["PATCH"])
@csrf_exempt
def update_project(request):
    try:
        request_body = json.loads(request.body)
        return_object = {}
        if not all([key in request_body for key in UPDATE_PROJECT]):
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        project_owner = Project.objects.filter(id=request_body.get("project_id"),createdBy=request_body.get("createdBy")).first()
        if not project_owner:
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=400)
        project_owner.title = request_body.get("title")
        project_owner.description = request_body.get("description")
        project_owner.save()
        return_object = retrun_object_func(SUCCESS,PROJECT_UPDATE_SUCCESSFULLY)
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="delete",
    operation_description="This function is used to delete project base on project ID",
    request_body=None,
    manual_parameters=[AUTH_PARAMS,PROJECT_SCHEMA], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(['DELETE'])
@csrf_exempt
def delete_project(request):
    '''This function is used to delete project base on project ID'''
    try:
        project_id = request.GET.get("project_id","")
        request_body = json.loads(request.body)
        return_object = {}
        if not project_id:
            return_object = retrun_object_func(FAIL,USER_ID_IS_NOT_PRESENT)
            return JsonResponse(return_object,safe=False,status=400)
        project_details = Project.objects.filter(id=project_id).first()
        if not project_details:
            return_object = retrun_object_func(FAIL,PROJECT_DETAILS_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        user_details = customUsers.objects.get(id=request_body.get("createdBy"))
        if project_details.createdBy != user_details:
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=401)
        project_details = Project.objects.filter(id=project_id).update(is_deleted = True)
        if not project_details > 0: 
            return_object = retrun_object_func(FAIL,FAIL_TO_DELETE_PROJECT)
            return JsonResponse(return_object,safe=False,status=400)
        return_object = retrun_object_func(SUCCESS,PROJECT_DELETED_SUCCESSFULLY)

    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="get",
    operation_description="This function is used to get project base on created by",
    request_body=None,
    manual_parameters=[AUTH_PARAMS,PAGINATION_SCHEMA], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["GET"])
@csrf_exempt
def get_project_details(request):
    '''This function is used to get project base on created by'''
    try:
        request_body = json.loads(request.body)
        # get page number from params
        page_number = request.GET.get("page_number")
        return_object = {}
        project_details = Project.objects.filter(is_deleted=False,createdBy=request_body.get("createdBy"))
        if not project_details:
            return_object = retrun_object_func(FAIL,PROJECT_DETAILS_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        if not (page_number and int(page_number) > 0):
            return_object = retrun_object_func(FAIL,INVALID_PAGE_NUMBER)
            return JsonResponse(return_object,safe=False,status=400) 
        paginated_data,error = get_pagination_data(project_details,page_number,ProjectSerializers)
        if error:
            return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},error)
            return JsonResponse(return_object,safe=False,status=500) 
        return_object = retrun_object_func(SUCCESS,DATA_RETRIVE_SUCCESSFULLY,paginated_data)
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method="post",
    operation_description="This function is used to add members in project",
    request_body=ADD_MEMBER_SCHEMA,
    manual_parameters=[AUTH_PARAMS], 
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["POST"])
@csrf_exempt
def add_members(request):
    try:
        request_body = json.loads(request.body)
        return_object = {}
        if not ([value in request_body for value in CREATE_MEMBERS] and request_body.get("members") and isinstance(request_body.get("members"),list)):
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        project_details = Project.objects.get(id=request_body.get("project_id"))
        if not project_details:
            return_object = retrun_object_func(FAIL,PROJECT_DETAILS_NOT_FOUND)
            return JsonResponse(return_object,safe=False,status=400)
        if project_details.createdBy_id != request_body.get("createdBy"):
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=400)
        admin_user = list(Membership.objects.filter(role="Admin",project=request_body.get("project_id")).values())
        if admin_user:
            admin_object = {value.get("id"):value for value in admin_user}
            for value in request_body.get("members"):
                if value.get("id") in admin_object:
                    value["role"] = "Admin"
        serializers = AddMembersSerializer(data=request_body)
        if not serializers.is_valid():
            return_object = retrun_object_func(FAIL,str(serializers.errors))
            return JsonResponse(return_object,safe=False,status=400)
        serializers.save()
        return_object = retrun_object_func(SUCCESS,MEMBERS_ADDED_SUCCESSFULLY)

    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)
        





