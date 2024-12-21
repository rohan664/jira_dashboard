from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

AUTH_PARAMS = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Bearer token for authentication (e.g., Bearer <your_token>)",
)

USER_REQUEST_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username":openapi.Schema(type=openapi.TYPE_STRING, description="username of the user"),
        "password":openapi.Schema(type=openapi.TYPE_STRING, description="username of the user"),
    },
    required=["project_id", "members"],
)

CREATE_PROJECT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title":openapi.Schema(type=openapi.TYPE_STRING, description="title of the project"),
        "description":openapi.Schema(type=openapi.TYPE_STRING, description="description of the project"),
    },
    required=["title", "description"],
)

PROJECT_SCHEMA = openapi.Parameter(
    name="project_id",
    in_=openapi.IN_QUERY,  
    type=openapi.TYPE_INTEGER,  
    description="The ID of the project to be deleted",
)

PAGINATION_SCHEMA = openapi.Parameter(
    name="page_number",
    in_=openapi.IN_QUERY,  
    type=openapi.TYPE_INTEGER,  
    description="Page Number",
)

MEMBER_SCHEMA = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name of the member"),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the member"),
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the member"),
            "role": openapi.Schema(type=openapi.TYPE_STRING, description="Role of the member in the project"),
        },
        required=["first_name", "last_name", "id", "role"],
    )
)

ADD_MEMBER_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "project_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the project"),
        "members": MEMBER_SCHEMA,
    },
    required=["project_id", "members"],
)

DELETE_TASK_SCHEMA = openapi.Parameter(
    name="task_id",
    in_=openapi.IN_QUERY,  
    type=openapi.TYPE_INTEGER,  
    description="task id",
)

DELETE_USER_SCHEMA = openapi.Parameter(
    name="user_id",
    in_=openapi.IN_QUERY,  
    type=openapi.TYPE_INTEGER,  
    description="user id",
)

DELETE_COMMENT_SCHEMA = openapi.Parameter(
    name="comment_id",
    in_=openapi.IN_QUERY,  
    type=openapi.TYPE_INTEGER,  
    description="comment id",
)

ADD_COMMENT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "task_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the project"),
        "comment": MEMBER_SCHEMA,
    },
    required=["task_id", "comment"],
)

UPDATE_COMMENT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "comment_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the comment"),
        "comment": openapi.Schema(type=openapi.TYPE_STRING, description="comment"),
        "task_id":openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the task")
    },
    required=["comment_id", "comment","task_id"],
)

UPDATE_PROJECT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "project_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the project"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="title"),
        "description":openapi.Schema(type=openapi.TYPE_STRING, description="Description")
    },
    required=["project_id", "title","description"],
)