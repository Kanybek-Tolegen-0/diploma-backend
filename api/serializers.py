from rest_framework import serializers

from . import models


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = '__all__'


class CafeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cafe
        fields = '__all__'


class CafePhoneNumberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CafePhoneNumber
        fields = '__all__'


class CuisineModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cuisine
        fields = '__all__'


class CafeCuisineModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CafeCuisine
        fields = '__all__'


class PlaceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Place
        fields = '__all__'


class ReserveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reserve
        fields = '__all__'
