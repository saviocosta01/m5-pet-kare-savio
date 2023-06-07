from rest_framework.views import APIView, Response, Request, status
from .models import Pet
from groups.models import Group
from traits.models import Trait
from traits.serializers import TraitSerializer
from .serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.

# deve retirar a chave group e traits do request.data - utilizar .pop
# verificar se group e trais ja existe no banco de dados
# se existir relaciona existente se nao cria uma nova
# depois criar pet


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request):
        request_data = request.data
        serializer = PetSerializer(data=request_data)

        serializer.is_valid(raise_exception=True)
        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")

        group_obj = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()

        if not group_obj:
            group_obj = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data, group=group_obj)

        for traits_dict in traits_data:
            traits_obj = Trait.objects.filter(name__iexact=traits_dict["name"]).first()

            if not traits_obj:
                traits_obj = Trait.objects.create(**traits_dict)

            pet.traits.add(traits_obj)

        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request):
        pets = Pet.objects.all()

        page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(instance=page, many=True)
        return self.get_paginated_response(serializer.data)
