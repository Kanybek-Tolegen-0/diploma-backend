from django.db.models import F
from django.db.models import Q

from rest_framework import serializers

from . import models


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = '__all__'


class CafePhoneNumberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CafePhoneNumber
        fields = '__all__'


class CafeCuisineModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CafeCuisine
        fields = '__all__'


class CafeModelSerializer(serializers.ModelSerializer):
    phones = CafePhoneNumberModelSerializer(source='cafephonenumber_set', many=True)
    cuisines = CafeCuisineModelSerializer(source='cafecuisine_set', many=True)

    class Meta:
        model = models.Cafe
        fields = [
            'name',
            'photo',
            'address',
            'phones',
            'cuisines'
        ]


class CuisineModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cuisine
        fields = '__all__'


class PlaceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Place
        fields = '__all__'


class ReserveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reserve
        fields = '__all__'

    def create(self, validated_data):
        start_time = validated_data.get('reserve_start_time')
        duration = validated_data.get('reserve_duration')
        end_time = start_time + duration
        place = validated_data.get('place')

        # Check if place is already reserved

        # If end_time of new reserve between start_time and end_time
        # OR
        # If end_time of existing reserve between start_time and end_time
        # THEN True, ELSE False
        # already_reserved = models.Reserve.objects.filter(
        #     (
        #         (
        #             Q(reserve_start_time__gte=start_time) &
        #             Q(reserve_start_time__lte=end_time)
        #         ) |
        #         (
        #             Q(F('reserve_start_time') + F('reserve_duration') >= start_time) &
        #             Q(F('reserve_start_time') + F('reserve_duration') <= end_time )
        #         )
        #     ),
        #     place=place).exists()
        already_reserved = models.Reserve.objects.filter(
            (
                Q(reserve_start_time__gte=start_time) &
                Q(reserve_start_time__lte=end_time)
            ),
            place=place).exists()

        if not already_reserved:
            return models.Reserve.objects.create(**validated_data)
        return None
