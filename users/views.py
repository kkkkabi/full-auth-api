from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# import library for goolge Auth view
from djoser.social.views import ProviderAuthView

#--------------------------User Authentication view----------------------------------#

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    # set the access and refresh token in the cookies.
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs) #super method posts passing in request

        if response.status_code == 200: # if the response is succesful, get the access and refresh token
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            # set the cookies
            response.set_cookie(
                'access', #name of my cookies
                access_token,
                max_age = settings.AUTH_COOKIES_ACCESS_MAX_AGE,  #5mins
                path = settings.AUTH_COOKIES_PATH,
                secure = settings.AUTH_COOKIES_SECURE,
                httponly = settings.AUTH_COOKIES_HTTP_ONLY,
                samesite = settings.AUTH_COOKIES_SAMESITE
            )

            response.set_cookie(
                'refresh', #name of my cookies
                refresh_token,
                max_age = settings.AUTH_COOKIES_REFRESH_MAX_AGE, #24 hours
                path = settings.AUTH_COOKIES_PATH,
                secure = settings.AUTH_COOKIES_SECURE,
                httponly = settings.AUTH_COOKIES_HTTP_ONLY,
                samesite = settings.AUTH_COOKIES_SAMESITE
            )

        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    '''Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.'''
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token: 
            #if we have refresh token, set request.data, call the token, fresh views, post request and have this inside of the data
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access', #name of my cookies
                access_token,
                max_age = settings.AUTH_COOKIES_ACCESS_MAX_AGE,  #5mins
                path = settings.AUTH_COOKIES_PATH,
                secure = settings.AUTH_COOKIES_SECURE,
                httponly = settings.AUTH_COOKIES_HTTP_ONLY,
                samesite = settings.AUTH_COOKIES_SAMESITE                
            )

        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    def post(self, request, *args, **kwargs):
        # send this request to the token, verify view with that token.
        # the response should be 204 No Content.
        # 204 No Content means the request is successful and user is still logged in and doesn't need to refresh
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)
    
    
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
    

#--------------------------Social OAuth2 view----------------------------------#

class CustomProviderAuthView(ProviderAuthView):
    def post (self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201: # 201 Created  indicates that the request has succeeded and has led to the creation of a resource.
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access', #name of my cookies
                access_token,
                max_age = settings.AUTH_COOKIES_ACCESS_MAX_AGE,  #5mins
                path = settings.AUTH_COOKIES_PATH,
                secure = settings.AUTH_COOKIES_SECURE,
                httponly = settings.AUTH_COOKIES_HTTP_ONLY,
                samesite = settings.AUTH_COOKIES_SAMESITE
            )

            response.set_cookie(
                'refresh', #name of my cookies
                refresh_token,
                max_age = settings.AUTH_COOKIES_REFRESH_MAX_AGE, #24 hours
                path = settings.AUTH_COOKIES_PATH,
                secure = settings.AUTH_COOKIES_SECURE,
                httponly = settings.AUTH_COOKIES_HTTP_ONLY,
                samesite = settings.AUTH_COOKIES_SAMESITE
            )
            
        return response