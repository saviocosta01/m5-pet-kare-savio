from rest_framework import serializers
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=("Male", "Female", "Not Informed"), default="Not Informed"
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
