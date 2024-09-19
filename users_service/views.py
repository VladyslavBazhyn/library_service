from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, mixins, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users_service.permissions import UserIsOwnerOrReadOnly
from users_service.serializers import UserRegisterSerializer, UserProfileSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)


class UserProfileView(
    generics.RetrieveAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin
):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        pk = self.request.user.pk
        obj = get_object_or_404(get_user_model(), id=pk)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
