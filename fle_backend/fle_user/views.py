from django.shortcuts import render
from rest_framework.response import Response #type:ignore
from rest_framework import status #type:ignore
from .sendmails import send_email_verify
import uuid
from .models import Account
from rest_framework.views import APIView #type:ignore
from .serializers import RegisterSerializer,UserViewSerializer
from rest_framework.exceptions import AuthenticationFailed #type:ignore
from django.utils import timezone
from .token import get_tokens
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated #type:ignore
import requests #type:ignore
from django.core.files.base import ContentFile
from .permission import IsUser
from rest_framework.permissions import IsAuthenticated #type:ignore
from rest_framework_simplejwt.authentication import JWTAuthentication #type:ignore
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore
from rest_framework.generics import UpdateAPIView #type:ignore

# Create your views here.


class RegisterView(APIView):
    def post(self, request):

        if not request.data:
            return Response({'error': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(request.data)

        serializer = RegisterSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        token = str(uuid.uuid4())

        user_profile = serializer.save()
        user_profile.email_token = token
        user_profile.save()
        send_email_verify(serializer.data['email'], token)
        response = Response()
        response.data = {
            'message': f"Account successfully created for {serializer.data['first_name']}",
            'message_email': f"Email verification required",
            'Userinfo': serializer.data
        }
        return response

    def get(self, request, token):
        print('hello  get functions')
        # User = get_user_model()
        print(token)
        try:
            user = Account.objects.get(email_token=token)
            print('user found')
            if user.is_emailverified == True:
                verify_response = {
                    'message': 'Account already verified',
                }
                return Response(verify_response)
            else:
                user.is_emailverified = True
                user.save()
                print(user, '........................................')
                response_data = {
                    'message': 'Email verified successfully.',
                }
                return Response(response_data)
        except:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
        


class LoginView(APIView):
    def post(self, request):
        if not request.data:
            return Response({'error': 'No data provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            email = request.data.get('email')
            password = request.data.get('password')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        if not user.is_active:
            raise AuthenticationFailed('Your account is blocked')
        
        if not user.is_emailverified:
            token = user.email_token
            if token is None:
                token = str(uuid.uuid4())
                user.email_token = token
                user.save()
            send_email_verify(user.email, token)
            raise AuthenticationFailed(f'Your Email is not Verified \n Verify Link is send to {user.email}')
        
        authenticate(email=email, password=password)
        user.last_login = timezone.now()
        print(timezone.now())
        user.save()
        pictureurl = '' 
        if user.picture:
            pictureurl = user.picture.url
        print(pictureurl)
        print(user.last_login)
        Serialized_data = UserViewSerializer(user)
        token = get_tokens(user)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'userInfo': Serialized_data.data,
            'token': token,
            'message': 'successfully loged',
            'status': 200,
            'picture_url': pictureurl
        }
        return response
    
    
class CheckAuthView(APIView):
    def get(self, request):
        print('frfggggggggg')
        return Response({'message': 'You are authenticated'})
    


class GoogleLoginView(APIView):
    def post(self, request):
        if not request.data:
            return Response({'error': 'No data provided.'}, status=status.HTTP_400_BAD_REQUEST)  
        try:
            email = request.data.get('email')
            is_emailverified = request.data.get('is_emailverified')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            google_image_url = request.data.get('picture')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        user, created = Account.objects.get_or_create(email=email, defaults={'is_active': True})
        if created:
            response = requests.get(google_image_url)
            if response.status_code == 200:
                user.picture.save(
                    'google_profile_image.jpg',
                    ContentFile(response.content),
                )
            user.first_name = first_name
            user.last_name = last_name
            user.is_emailverified = is_emailverified
        user.last_login = timezone.now()
        user.save()
        pictureurl = ''
        if user.picture:
            pictureurl = user.picture.url
        print(pictureurl)
        print(user.first_name)
        print(user.is_active)
        if not user.is_active:
            raise AuthenticationFailed('Your account is blocked')
        
        if not user.is_emailverified:
            token = user.email_token
            if token is None:
                token = str(uuid.uuid4())
                user.email_token = token
                user.save()
            send_email_verify(user.email, token)
            raise AuthenticationFailed(f'Your Email is not Verified \n Verify Link is send to {user.email}')
        
        serialized_data = UserViewSerializer(user)
        token = get_tokens(user)
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'userInfo': serialized_data.data,
            'token': token,
            'message': 'Successfully logged in or registered',
            'status': 200,
            'picture_url': pictureurl
        }
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

        try:
            token = RefreshToken(token)
            token.blacklist()
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        return Response({'detail': 'Logout successful'})
    



class UserHomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        user = request.user
        print(user,'userrrrrrrrrrrrrrrrrrrrrr')

        try:
            user_profile = Account.objects.get(email=user)
            print('user profile found')
        except Account.DoesNotExist:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = UserViewSerializer(user_profile)

        return Response({'data': serialized_data.data,
                         'message': 'success'}, status=status.HTTP_200_OK)
    
    def patch(self, request):
        if not request.data:
            return Response({'detail': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            try:
    
                email = request.data.get('email', None)
                mobile = request.data.get('mobile', None)
                
                if email:
                    try:
                        existing_user = Account.objects.get(email=email)
                        if existing_user != request.user:
                            error_message = "Email is already in use by another user."
                            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                    except Account.DoesNotExist:
                        pass

                if mobile:
                    
                    try:
                        existing_user = Account.objects.get(mobile=mobile)
                        if existing_user != request.user:
                            error_message = "Mobile number is already in use by another user."
                            print('print mobile')
                            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                    except Account.DoesNotExist:
                        pass
            except:
                pass
            serialized_data = UserViewSerializer(request.user,data = request.data, partial=True)

            if serialized_data.is_valid():
                serialized_data.save(raise_exception=True)
                return Response({'data': serialized_data.data,
                                    'message': 'updated successfully'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)






    
