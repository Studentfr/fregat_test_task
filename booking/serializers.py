from rest_framework import serializers

from booking.models import User, ParkingSpace, Reservation


class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class ParkingSpaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpace
        fields = '__all__'


class ReserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email',]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['reserved_by'] = ReserverSerializer(instance.reserved_by).data
        ret['parking_space'] = ParkingSpaceSerializer(instance.parking_space).data
        return ret