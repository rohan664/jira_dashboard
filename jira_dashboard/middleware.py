from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
import time,json
from jira_dashboard.utils.messages import SOMETHING_WENT_WRONG_IN_MIDDLEWARE

class UserAuthentication:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):

        bypass_url = ['/create-user','/login','/swagger/']
        if request.path in bypass_url:
            return self.get_response(request)
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return JsonResponse({"error":"Token is not present in request"},status=401)
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error':'Inavalid authorization header format'})
        
        token_str = auth_header.split(' ')[1]
        if token_str:
            try:
                token = AccessToken(token_str)
                user_id = token['user_id']
                if request.method in ['POST','PUT','PATCH']:
                    request_body = json.loads(request.body)
                    request_body["createdBy"] = user_id
                    request_body["is_superuser"] = token["is_superuser"]
                    request._body = json.dumps(request_body).encode('utf-8')
                if request.method in ['DELETE','GET']:
                    request_body = {
                        "createdBy":user_id,
                        "is_superuser":token["is_superuser"]
                    }
                    request._body = json.dumps(request_body).encode('utf-8')
            except Exception as error:
                return JsonResponse({'message': SOMETHING_WENT_WRONG_IN_MIDDLEWARE,"error":str(error)}, status=401)
        return self.get_response(request)
        