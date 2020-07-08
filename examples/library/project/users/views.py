from rest_framework import viewsets

from drf_psq import PsqMixin, Rule, psq

from .models import User
from .serializers import UserBasicSerializer, UserFullSerializer
from .permissions import IsAuthenticated, IsAdminUser, IsSelf


class UserViewSet(PsqMixin, viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserFullSerializer
    permission_classes = [IsAdminUser]

    psq_rules = {
        'list': [
            Rule([IsAdminUser]),
            Rule(
                [IsAuthenticated],
                UserBasicSerializer,
                lambda self: User.objects.filter(is_superuser=False, is_staff=False)
            )
        ],

        'create': [Rule([IsAdminUser], UserFullSerializer)],

        ('retrieve', 'update', 'partial_update'): [
            Rule([IsAdminUser], UserFullSerializer),
            Rule([IsAuthenticated & IsSelf], UserBasicSerializer)
        ],

        # 'destroy': [Rule([IsAdminUser])],
    }


    def get_object(self):
        if self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()


    @psq([Rule([IsAdminUser])])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
