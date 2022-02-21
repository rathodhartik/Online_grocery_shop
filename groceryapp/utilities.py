from copy import error
from rest_framework import status









OK = status.HTTP_200_OK
CREATED = status.HTTP_201_CREATED
BAD_REQUEST =status.HTTP_400_BAD_REQUEST
NO_CONTENT =status.HTTP_204_NO_CONTENT



def logout_success(message):
   
    msg={"code":CREATED,
        "message":message}
    return msg


def success_added(message,data):
   
    msg={"code":CREATED,
        "message":message,
        "data":data}
    return msg

def login_success(message,data,access,refresh):
     user_data={
        "user":data,
        "access_token":access,
        "refresh_token":refresh}
     msg={"code":CREATED,"message":message,"data":user_data}
     return msg

def data_fail(message,data):
    msg={"code":BAD_REQUEST,
         "message":message,
         "data":data}
    return msg

def fail(message):
    fail = {"code":BAD_REQUEST,
            "message":message}
    return fail

def update_data(message,data):
    msg={"code":OK,
             "message":message,
             "data":data}
    return msg

def deleted_data(message):
    msg={"code":NO_CONTENT,
             "message":message,}
    return msg


def success_mount(message,data,amount,quantity):
     user_data={
        "user":data,
        "total_amount":amount,
        "total_quantity":quantity,}
     msg={"code":CREATED,"message":message,"data":user_data}
     return msg
