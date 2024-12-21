import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from jira_dashboard.serializers import UserSerializer
from jira_dashboard.models import customUsers
from jira_dashboard.utils.common_function import retrun_object_func
from rest_framework_simplejwt.tokens import RefreshToken
from jira_dashboard.utils.constants import SUCCESS,FAIL,SWAGGER_SUCCESS,SWAGGER_BAD_REQUEST,\
    SWAGGER_INTERNAL_SERVER_ERROR,USER_ID,USERNAME
from jira_dashboard.utils.messages import SOMETHING_WENT_WRONG,INVALID_REQUEST_OBJECT,\
    USERS_CREATED_SUCCESSFULLY,PASSWORD_DOES_NOT_MATCH,USER_NOT_PRESENT,USER_LOGGED_IN_SUCCESSFULLY,\
        DO_NOT_HAVE_NECCESSARY_PERMISSION,USER_IS_DELETED_ALREADY,USER_DELETED_SUCCESSFULLY
from drf_yasg.utils import swagger_auto_schema
from jira_dashboard.views.swagger_request_schema import USER_REQUEST_SCHEMA,AUTH_PARAMS,DELETE_USER_SCHEMA


@swagger_auto_schema(
    method='post',
    operation_description="Create a user",
    request_body=UserSerializer,
    responses={201: UserSerializer()}
)
@api_view(['POST'])
@csrf_exempt
def createUser(request):
    """This is used to create and update the user"""    
    try:
        request_body = json.loads(request.body)
        return_object = {}
        existing_data = customUsers.objects.filter(username = request_body.get(USERNAME)).first()
        if not existing_data:
            serializer = UserSerializer(data=request_body)
        else:
            update_request_body = {**model_to_dict(existing_data),**request_body}
            serializer = UserSerializer(existing_data,data=update_request_body)
        if not serializer.is_valid():
            return_object = retrun_object_func(FAIL,serializer.errors)
            return JsonResponse(return_object,safe=False,status=400)
        serializer.save()
        return_object = retrun_object_func(SUCCESS,USERS_CREATED_SUCCESSFULLY,serializer.data)

    except Exception as error:
        print(error)
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)


@swagger_auto_schema(
    method='post',
    operation_description="This is used to authenticate user",
    request_body = USER_REQUEST_SCHEMA,
    responses={200:SWAGGER_SUCCESS , 400: SWAGGER_BAD_REQUEST,500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(['POST'])
@csrf_exempt
def loginUsers(request):
    '''This is used to login purpose'''
    try:
        request_body = json.loads(request.body)
        return_object = {}
        if not ((request_body.get("username") or request_body.get("email")) and request_body.get("password")):
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        # validate user data
        user_data = customUsers.objects.filter(username = request_body.get("username")).first() or customUsers.objects.filter(email = request_body.get("email")).first()
        if not user_data:
            return_object = retrun_object_func(FAIL,USER_NOT_PRESENT)
            return JsonResponse(return_object,safe=False,status=401)
        # validate user password
        if not user_data.check_password(request_body.get("password")):
            return_object = retrun_object_func(FAIL,PASSWORD_DOES_NOT_MATCH)
            return JsonResponse(return_object,safe=False,status=401)
        token = RefreshToken.for_user(user_data)
        token['email'] = user_data.email
        token['first_name'] = user_data.first_name
        token['last_name'] = user_data.last_name
        token['is_superuser'] = user_data.is_superuser
        access_refresh_token = {
            "access":str(token.access_token),
            "refresh":str(token)
        }
        return_object = retrun_object_func(SUCCESS,USER_LOGGED_IN_SUCCESSFULLY,access_refresh_token)
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)

@swagger_auto_schema(
    method='delete',
    operation_description="This is used to offboard the user",
    manual_parameters = [AUTH_PARAMS,DELETE_USER_SCHEMA],
    responses={200:SWAGGER_SUCCESS, 400: SWAGGER_BAD_REQUEST, 500:SWAGGER_INTERNAL_SERVER_ERROR}
)
@api_view(["DELETE"])
@csrf_exempt
def offboard_user(request):
    try:
        return_object = {}
        request_body = json.loads(request.body)
        # check the user_id is present in the in parama or not
        user_id = request.GET.get(USER_ID)
        if not user_id:
            return_object = retrun_object_func(FAIL,INVALID_REQUEST_OBJECT)
            return JsonResponse(return_object,safe=False,status=400)
        if not request_body.get("is_superuser"):
            return_object = retrun_object_func(FAIL,DO_NOT_HAVE_NECCESSARY_PERMISSION)
            return JsonResponse(return_object,safe=False,status=401)
        user_details = customUsers.objects.get(id=user_id,is_active=True,is_superuser=False)
        print(user_details)
        if not user_details:
            return_object = retrun_object_func(FAIL,USER_IS_DELETED_ALREADY)
            return JsonResponse(return_object,safe=False,status=400)
        user_details.is_active = False
        user_details.save()
        return_object = retrun_object_func(SUCCESS,USER_DELETED_SUCCESSFULLY)
    except Exception as error:
        return_object = retrun_object_func(FAIL,SOMETHING_WENT_WRONG,{},str(error))
        return JsonResponse(return_object,safe=False,status=500)
    return JsonResponse(return_object,safe=False,status=200)