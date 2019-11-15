from rest_framework.serializers import ModelSerializer
from django.core.exceptions import ValidationError
from .models import Parking
import re

class ParkingSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = ('id','plate' ,'time', 'paid','left')
        read_only_fields = ('id', 'time', 'paid','left')

    def validate_plate(self, data):
        if re.match(r'[a-zA-Z]{3}-[0-9]{4}', data) == None:
            raise ValidationError('Placa invalida.')
        return data
