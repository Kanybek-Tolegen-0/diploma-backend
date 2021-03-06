from datetime import date, datetime

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import pagination
from rest_framework import status
from rest_framework import permissions

from rest_framework.response import Response


from . import serializers
from . import models
from . import paginators
from .validators import (
    validate_reserve_datetime,
    validate_passed_datetime,
    validated_by_cafe_working_hours
)

class UserViewSet(generics.RetrieveAPIView,
                  generics.UpdateAPIView,
                  generics.DestroyAPIView):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserModelSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_current_user(self, request):
        return self.get_queryset().get(id=request.user.id)

    def get(self, request, *args, **kwargs):
        user = self.get_current_user(request)
        user_serialized = self.get_serializer(user)
        return Response(data=user_serialized.data)

    def patch(self, request, *args, **kwargs):
        user = self.get_current_user(request)
        user_serialized = self.get_serializer(user)
        try:
            user_serialized.update(user, request.data)
        except Exception as exc:
            return Response(data={"error": "Cannot update fields", "message": str(exc)})
        return Response(data=user_serialized.data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_current_user(request)
        user_serialized = self.get_serializer(user)
        deleted = user_serialized.delete(user)
        if deleted:
            return Response(data={"status": "deleted"})
        return Response(data={"status": "error"})


class CafeListView(generics.ListAPIView):
    queryset = models.Cafe.objects.all().prefetch_related(
                                        'cafephonenumber_set',
                                        'cafecuisine_set',
                                        )
    serializer_class = serializers.CafeModelSerializer

    def list(self, request, *args, **kwargs):
        pg = paginators.CustomLimitOffsetPaginator()
        cafes = pg.paginate_queryset(queryset=self.get_queryset(), request=request)
        cafes_serializered = self.get_serializer(cafes, many=True)
        return Response(data=cafes_serializered.data)


class CafeRetriveView(generics.RetrieveAPIView):
    queryset = models.Cafe.objects.all()
    serializer_class = serializers.CafeModelSerializer
    lookup_field = 'id'


class CafePlacesListView(generics.ListAPIView):
    queryset = models.Place.objects.select_related('cafe').all()

    def list(self, request, *args, **kwargs):
        queryset = models.Place.objects.select_related('cafe').filter(cafe__id=kwargs.get('id')).values()
        serialized_data = serializers.PlaceModelSerializer(data=queryset, many=True)
        return Response(data=serialized_data.initial_data)


class CafeReservesListView(generics.ListAPIView):
    queryset = models.Reserve.objects.select_related('place').all()

    def list(self, request, *args, **kwargs):
        if request.GET.get('day', None):
            day, month, year = request.GET.get('day').split('-')
            current_date = date(int(year), int(month), int(day))
        else:
            current_date = date.today()
        cafe_reserves = self.get_queryset().filter(
            place__cafe__id=kwargs.get('id'),
            reserve_start_time__date=current_date,
            reserve_start_time__date__gte=date.today()
        )
        cafe_reserves_serialized = serializers.ReserveModelSerializer(cafe_reserves, many=True)
        return Response(data=cafe_reserves_serialized.data)


class UserReservesView(generics.ListCreateAPIView):
    serializer_class = serializers.ReserveModelSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return models.Reserve.objects.filter(user=user, reserve_start_time__date__gte=date.today()).select_related('place')

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            validate_passed_datetime(serializer.validated_data.get('reserve_start_time'))
            validated_by_cafe_working_hours(
                serializer.validated_data.get('reserve_start_time'),
                serializer.validated_data.get('reserve_duration'),
                serializer.validated_data.get('place').cafe.workday_start_time,
                serializer.validated_data.get('place').cafe.workday_end_time,
            )
            for reserve in models.Reserve.objects.filter(place__id=data.get('place')):
                valid = validate_reserve_datetime(
                    serializer.validated_data.get('reserve_start_time'),
                    serializer.validated_data.get('reserve_duration'),
                    reserve.reserve_start_time,
                    reserve.reserve_duration
                )
            serializer.save()
            return Response(data={"status": "1"})
        except Exception as e:
            print("EXCEPTION", e)

        return Response(data={"status":"0"}, status=status.HTTP_404_NOT_FOUND)

class ExactReserveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Reserve.objects.select_related('place').all()
    serializer_class = serializers.ReserveModelSerializer

    permission_classes = [permissions.AllowAny,]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        reserve_instance = models.Reserve.objects.get(id=kwargs.get('id', None))

        data = request.data
        data['user'] = request.user.id
        data['id'] = kwargs.get('id', None)
        data['place'] = reserve_instance.place.id
        
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)

            validate_passed_datetime(serializer.validated_data.get('reserve_start_time'))
            validated_by_cafe_working_hours(
                serializer.validated_data.get('reserve_start_time'),
                serializer.validated_data.get('reserve_duration'),
                serializer.validated_data.get('place').cafe.workday_start_time,
                serializer.validated_data.get('place').cafe.workday_end_time,
            )
            for reserve in models.Reserve.objects.filter(place__id=data.get('place')):
                valid = validate_reserve_datetime(
                    serializer.validated_data.get('reserve_start_time'),
                    serializer.validated_data.get('reserve_duration'),
                    reserve.reserve_start_time,
                    reserve.reserve_duration
                )
            serializer.update(reserve_instance, serializer.validated_data)
            return Response(data={"status": "1"})
        except Exception as e:
            print("Exception", e)
        return Response(data={"status": "0"})
