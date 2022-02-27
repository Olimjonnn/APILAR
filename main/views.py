from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from main.serializer import *
from main.models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated



class ClientView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

class ProductionView(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

class ShopView(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

class ShopItemView(viewsets.ModelViewSet):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    def create(self, request):
        try:
            product_id = request.data['product']
            shop_id = request.data['shop']
            price = int(request.data['price'])
            quantity = int(request.data['quantity'])
            ShopItem.objects.create(product_id=product_id,shop_id=shop_id,price=price, quantity=quantity)
            product = Product.objects.get(id=product_id)
            product.quantity -= quantity
            product.save()
            shop = Shop.objects.get(id=shop_id)
            shop.price += price*quantity
            shop.save()
            client = Client.objects.get(id=shop.client.id)
            client.debt += price*quantity
            client.save()
            cash = Cash.objects.first()
            cash.cash += price*quantity
            cash.save()

            return Response({'message:':'Alhamdulillah'})
        except Exception as arr:
            data = {
                'status': False,
                'error': f"{arr}"
            }
            return Response(data)
    @action(['POST'], detail=False)
    def delete(self, request):
        shop = request.data['shop']
        s = ShopItem.objects.get(id=shop)
        product = Product.objects.get(id=s.product.id)
        product.quantity += s.quantity
        product.save()
        shop = Shop.objects.get(id=s.shop)
        shop.price -= s.price*s.quantity
        shop.save()
        client = Client.objects.get(id=shop.client.id)
        client.debt -= s.price*s.quantity
        client.save()
        cash = Cash.objects.first()
        cash.cash -= s.price*s.quantity
        cash.save()
        return Response({'message':'deleted'})




class CashView(viewsets.ModelViewSet):
    queryset = Cash.objects.all()
    serializer_class = CashSerializer

 
