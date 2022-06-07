from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(r'cafes/', views.CafeListView.as_view()),
    path(r'cafes/<int:id>/', views.CafeRetriveView.as_view()),
    path(r'cafes/<int:id>/places/', views.CafePlacesListView.as_view()),
    path(r'reserves/', views.UserReservesListView.as_view()),

]
