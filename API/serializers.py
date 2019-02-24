from rest_framework import serializers
from .models import Registro

class DoorCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ("code")