from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import LevelSerializer, SavingsGoalSerializer, UserSerializer
from apps.core.models import Level , SavingsGoal, SavingsModeChoices
from django.contrib.auth.models import User

@extend_schema(
    tags=["Usuarios"],
    summary="Gestión de Usuarios",
    description="API para gestionar usuarios. Permite listar, buscar y crear usuarios. "
                "Los administradores pueden listar todos los usuarios, mientras que "
                "un usuario estándar solo puede ver su propio perfil.",
)
class UserViewSet(viewsets.ModelViewSet):
    """
    API para gestionar usuarios.
    - Listar, buscar y crear usuarios
    - Solo admins pueden listar todos los usuarios
    - Un usuario solo puede ver su propio perfil
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username", "email"]
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Si el usuario no es admin, solo puede ver su propio perfil."""
        # if not self.request.user.is_staff:
        #     return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    @extend_schema(
        tags=["Usuarios"],
        summary="Listar usuarios",
        description="Lista los usuarios disponibles. Si el usuario no es admin, solo verá su propio perfil.",
        parameters=[
            OpenApiParameter(name="search", type=str, description="Buscar por username o email"),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
@extend_schema(
    tags=["Ahorros"],
    summary="Obtener, crear y administrar metas de ahorro",
    description="API para manejar las metas de ahorro de los usuarios.",
    parameters=[
        OpenApiParameter(
            name="savings_mode",
            description="Filtrar por modo de ahorro (percentage, fixed, rounding, range)",
            required=False,
            type=str,
            enum=[choice.value for choice in SavingsModeChoices]
        ),
        OpenApiParameter(
            name="is_active",
            description="Filtrar por estado activo/inactivo",
            required=False,
            type=bool
        ),
        OpenApiParameter(
            name="min_amount",
            description="Filtrar metas con un monto mínimo",
            required=False,
            type=float
        ),
        OpenApiParameter(
            name="max_amount",
            description="Filtrar metas con un monto máximo",
            required=False,
            type=float
        ),
    ]
)
class SavingsGoalViewSet(viewsets.ModelViewSet):
    queryset = SavingsGoal.objects.all()
    serializer_class = SavingsGoalSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get_queryset(self):
        """Filtra las metas de ahorro para mostrar solo las del usuario autenticado"""
        queryset = self.queryset.filter(user=self.request.user)

        savings_mode = self.request.query_params.get("savings_mode")
        if savings_mode:
            queryset = queryset.filter(savings_mode=savings_mode)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        min_amount = self.request.query_params.get("min_amount")
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        max_amount = self.request.query_params.get("max_amount")
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        return queryset
    
# @extend_schema(
#     tags=["Ahorros"],
#     summary="Obtener, crear y administrar metas de ahorro",
#     description="API para manejar las metas de ahorro de los usuarios.",
# )
# class SavingsGoalViewSet(viewsets.ModelViewSet):
#     queryset = SavingsGoal.objects.all()
#     serializer_class = SavingsGoalSerializer
#     permission_classes = [IsAuthenticated]  # Requiere autenticación

#     def get_queryset(self):
#         """Filtra las metas de ahorro para mostrar solo las del usuario autenticado"""
#         return self.queryset.filter(user=self.request.user)
    

class LevelListView(APIView):
    serializer_class = LevelSerializer 
    
    def get(self, request):
        levels = Level.objects.all()
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
