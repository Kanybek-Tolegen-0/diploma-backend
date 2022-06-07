from rest_framework import viewsets
from rest_framework import generics
from rest_framework import pagination
from rest_framework import status

from rest_framework.response import Response


from . import serializers
from . import models
from . import paginators


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserModelSerializer


class CafeListView(generics.ListAPIView):
    queryset = models.Cafe.objects.all().prefetch_related(
                                        'cafephonenumber_set',
                                        'cafecuisine_set'
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
    queryset = models.Place.objects.all().select_related('cafe')
    serializer_class = serializers.PlaceModelSerializer


class UserReservesListView(generics.ListCreateAPIView):
    serializer_class = serializers.ReserveModelSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Reserve.objects.filter(user=user).select_related('place')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
            except AssertionError:
                instance = None
        else:
            instance = None

        if instance:
            return Response(data=serializer.data)
        return Response(data={"error":"already_reserved"}, status=status.HTTP_404_NOT_FOUND)
