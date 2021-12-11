from datetime import datetime

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from booking.models import User, ParkingSpace, Reservation
from booking.serializers import UserRegistrationSerializer, UserSerializer, ParkingSpaceSerializer, \
    ReservationSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        reg_serializer = UserRegistrationSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response({
                    "token": new_user.token
                },
                    status=status.HTTP_201_CREATED)
            return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Such email is already taken"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ParkingSpaceView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSpaceSerializer


class ParkingSpaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSpaceSerializer


class ReservationView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request, *args, **kwargs):
        queryset = Reservation.objects.filter(start__lte=request.data['start'], end__gte=request.data['start'], parking_space=request.data['parking_space'])
        print(queryset)
        if queryset.exists():
            return Response({
            'success': 'False',
            'status code': status.HTTP_306_RESERVED,
            'message': 'The parking space is already reserved at this time',
        })
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JWTAuthentication
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer