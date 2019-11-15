from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Parking
from .serializers import ParkingSerializer
from datetime import datetime, timezone
from rest_framework import status
import re

class ParkingViewSet(ModelViewSet):

    serializer_class = ParkingSerializer

    def get_queryset(self):
        queryset = Parking.objects.all()
        for registro in queryset:
            if registro.paid == False:
                agora = datetime.now(timezone.utc)
                tempo_corrido = agora - registro.start
                tempo_hora_minuto = ("%s horas e %s minutos" % (tempo_corrido.seconds//3600, (tempo_corrido.seconds//60)%60))
                registro.time = tempo_hora_minuto
                registro.save()
        return queryset

    def list(self, request, *args, **kwargs): #GET
        queryset = self.get_queryset()
        if 'plate' in self.kwargs:
            queryset = queryset.filter(plate=self.kwargs['plate'])
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    # pontoturistico/1/denunciar
    @action(methods=['put'],detail=True)  # detail=True passa a Primare Key
    def out(self,request, pk=None): # pegar a PrimareKey
        queryset = self.get_queryset()
        queryset = queryset.filter(pk=pk)[0]
        if queryset.paid == True:
            queryset.left = True
            queryset.save()
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        else:
            return Response({"Erro":"Pagamento pendente"},status=status.HTTP_400_BAD_REQUEST)
        

    # pontoturistico/1/denunciar
    @action(methods=['put'],detail=True)  # detail=True passa a Primare Key
    def pay(self,request, pk=None): # pegar a PrimareKey
        queryset = self.get_queryset()
        queryset = queryset.filter(pk=pk)[0]
        queryset.paid = True
        queryset.save()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
