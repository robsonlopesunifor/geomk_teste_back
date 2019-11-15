from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from .viewsets import ParkingViewSet
import json
# Create your tests here.

class ParkingAPITestCase(APITestCase):

    def test_cliente(self):
        factory = APIRequestFactory()
        request = factory.get('/parking/')
        view = ParkingViewSet.as_view({'get':'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_entrar_placa(self):
        factory = APIRequestFactory()
        view = ParkingViewSet.as_view({'post':'create'})
        request = factory.post('/parking/', {'plate':'AAA-7777'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['plate'], 'AAA-7777')
        self.assertEqual(response.data['paid'], False)
        self.assertEqual(response.data['left'], False)

        request = factory.post('/parking/', {'plate':'777-AAAA'})
        response = view(request)
        self.assertEqual(response.status_code, 400)

        request = factory.post('/parking/', {'plate':'AAA7777'})
        response = view(request)
        self.assertEqual(response.status_code, 400)

        request = factory.post('/parking/', {'plate':'AA-7777'})
        response = view(request)
        self.assertEqual(response.status_code, 400)

        request = factory.post('/parking/', {'plate':'AAA-777'})
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_historico(self):

        factory = APIRequestFactory()

        view = ParkingViewSet.as_view({'post':'create'})
        request = factory.post('/parking/', {'plate':'AAA-8888'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        view = ParkingViewSet.as_view({'post':'create'})
        request = factory.post('/parking/', {'plate':'AAA-7777'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        view = ParkingViewSet.as_view({'post':'create'})
        request = factory.post('/parking/', {'plate':'AAA-7777'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        request = factory.get('/parking/')
        view = ParkingViewSet.as_view({'get':'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['plate'], 'AAA-8888')
        self.assertEqual(response.data[1]['plate'], 'AAA-7777')
        self.assertEqual(response.data[2]['plate'], 'AAA-7777')
        
        request = factory.get('/parking/AAA-7777')
        view = ParkingViewSet.as_view({'get':'list'})
        response = view(request,plate='AAA-7777')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['plate'], 'AAA-7777')
        self.assertEqual(response.data[1]['plate'], 'AAA-7777')

    def test_pagamento(self):
        factory = APIRequestFactory()
        
        view = ParkingViewSet.as_view({'post':'create'})
        request = factory.post('/parking/', {'plate':'AAA-7777'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['paid'], False)

        request = factory.put('/parking/')
        view = ParkingViewSet.as_view({'put':'pay'})
        response = view(request,response.data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['paid'], True)

    def test_saida(self):
        factory = APIRequestFactory()
        
        view = ParkingViewSet.as_view({'post':'create'})
        request = factory.post('/parking/', {'plate':'AAA-7777'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['paid'], False)

        id_placa_registrada = response.data['id']

        request = factory.put('/parking/')
        view = ParkingViewSet.as_view({'put':'out'})
        response = view(request,id_placa_registrada)
        self.assertEqual(response.status_code, 400)

        request = factory.put('/parking/')
        view = ParkingViewSet.as_view({'put':'pay'})
        response = view(request,id_placa_registrada)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['paid'], True)

        request = factory.put('/parking/')
        view = ParkingViewSet.as_view({'put':'out'})
        response = view(request,id_placa_registrada)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['left'], True)


        