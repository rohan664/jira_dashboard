from pydantic import BaseModel
from jira_dashboard.utils.constants import PAGE_SIZE
from django.core.paginator import Paginator


class ReturnCommonFunc(BaseModel):
    status:int
    message:str

def retrun_object_func(status:int,message:str,data:object={},error:str = {}) -> object:
    '''It is used to retrun response using commom pattern '''
    try:
        validate_data = ReturnCommonFunc(status=status,message=message)
        return_object = {
            "status":validate_data.status,
            "message":validate_data.message
        }       
        if error:
            return_object["errors"] = error
        if data:
            return_object["result"] = data
    except Exception as error:
        print("retrun_object_func",error)
        return_object = {"errors":error.errors() if error.errors() else error}
    return return_object

def get_pagination_data(object,page_number,serializers):
    '''get pagination object'''
    try:
        paginator_object = {}
        paginator_obj = Paginator(object,PAGE_SIZE)
        page_obj = paginator_obj.get_page(page_number)
        serializer = serializers(page_obj.object_list, many=True)
        pagination_obj = {
            "total_pages" : paginator_obj.num_pages,
            "current_page" : page_obj.number,
            "has_next":page_obj.has_next(),
            "has_previous":page_obj.has_previous(),
            "data":serializer.data
        }
    except Exception as error:
        print("get_pagination_data error:",error)
        return None,str(error)
    return pagination_obj,False


