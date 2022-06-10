from django.urls import path, include

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path(r'cafes/', views.CafeListView.as_view()),
    path(r'cafes/<int:id>/', views.CafeRetriveView.as_view()),
    path(r'cafes/<int:id>/places/', views.CafePlacesListView.as_view()),
    path(r'reserves/<int:id>/', views.CafeReservesListView.as_view()),
    path(r'reserves/', views.UserReservesView.as_view()),
    path(r'user/', views.UserViewSet.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
