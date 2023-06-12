from rest_framework.views import APIView, Response, Request, status
from .models import Pet
from groups.models import Group
from traits.models import Trait
from .serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

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
        trait_value = request.query_params.get("trait", None)
        pets = Pet.objects.all()

        if trait_value:
            pets = Pet.objects.filter(traits__name__iexact=trait_value)

        page = self.paginate_queryset(pets, request)

        serializer = PetSerializer(instance=page, many=True)
        return self.get_paginated_response(serializer.data)


class PetDetailsViwes(APIView):
    def get(self, request: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        if group_data:
            try:
                group_obj = Group.objects.get(
                    scientific_name__iexact=group_data["scientific_name"]
                )

            except Group.DoesNotExist:
                group_obj = Group.objects.create(**group_data)
            pet.group = group_obj

        if traits_data:
            traits_instancias = []
            for trait in traits_data:
                traits_obj = Trait.objects.filter(name__iexact=trait["name"]).first()
                if not traits_obj:
                    traits_obj = Trait.objects.create(**trait)

                traits_instancias.append(traits_obj)

            pet.traits.set(traits_instancias)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()

        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
