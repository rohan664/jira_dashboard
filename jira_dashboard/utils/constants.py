# Status
SUCCESS = 0
FAIL    = 1
SWAGGER_SUCCESS = "Success"
SWAGGER_BAD_REQUEST = "Bad Request"
SWAGGER_INTERNAL_SERVER_ERROR = 'Internal Server Error'

# paginations
PAGE_SIZE = 10

# mandatory fields
CREATE_PROJECT_FIELDS = ["title"]
CREATE_MEMBERS        = ["project_id","members"]
CREATE_TASK           = ["title"] 
POST_COMMENT          = ["task_id","comment"]
UPDATE_PROJECT        = ["project_id","title","description"]
UPDATE_COMMENT        = ["comment_id","comment","task_id"]

# 
USER_ID  = 'user_id'
USERNAME = 'username'