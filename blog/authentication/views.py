from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import SignupSerializer, LoginSerializer, RefreshTokenSerializer


class SignUpAPIView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        email = request.POST['email']
        user = User.objects.get(email=email)

        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Login Successful.',
                         'data': serializer.data}, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    def post(self,request):
        if request.method == "POST":
            serializer = RefreshTokenSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': True, 'message': 'You Have Logged Out..!!'}, status=status.HTTP_204_NO_CONTENT)

