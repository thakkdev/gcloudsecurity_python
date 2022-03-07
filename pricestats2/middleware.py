from functools import wraps
from typing import Any, Callable
from flask import request, Response, session


# [START cloudrun_user_validatetoken]
def validatetoken(func: Callable[..., int]) -> Callable[..., int]:
    @wraps(func)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        ipaddr = request.remote_addr
        tokenvalue = request.cookies.get('access_token')
               
        ###***PROD consideration***### - in production deny access for ipaddr with localhost address or IP's in a given range
        
        # below code uses flask session to store and validate token
        useridsession = session.get(ipaddr)
        if useridsession == None:
            return Response('Access denied', status=401)
        
        accesstokensession = session.get(useridsession)
        if tokenvalue != accesstokensession:
            return Response('Access denied', status=401)

        ###***PROD consideration***### - in production validate user using database session management 
        ###***PROD consideration***### - refresh access token token in db/Flask session after every call 
        ###***PROD consideration***### - create mechanism to expire access token due to inactvity after few minutes
        
        return func(*args, **kwargs)

    return decorated_function

# [END cloudrun_user_validatetoken]

