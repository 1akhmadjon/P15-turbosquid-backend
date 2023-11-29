from django.contrib.auth.views import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from accounts.serializers import UserSerializer, UserRegisterSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterAPIView(GenericAPIView):
    serializer_class = (UserRegisterSerializer)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        balance = request.POST.get('balance')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return Response({'success': False, 'error': 'Username already exists!'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'error': 'Email already exists!'}, status=400)
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password1,
                    balance=balance
                )
                user_serializer = UserSerializer(user)
                return Response({'success': True, 'data': user_serializer.data})
        else:
            return Response({'success': False, 'error': "Passwords are not same!"})


# class LogoutAPIView(GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = (LogoutSerializer,)
#
#     def post(self, request):
#         refresh_token = request.data.get('refresh')
#         token = RefreshToken(refresh_token)
#         token.blacklist()
#         return Response(status=204)


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']
        token = RefreshToken(refresh_token)

        # Blacklist the refresh token using OutstandingToken model
        OutstandingToken.objects.filter(token=token).delete()

        return Response(status=204)


class UserInfoAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({'success': True, 'data': user_serializer.data})
