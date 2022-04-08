
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItem, ShippingAddress
from .serializer import ProductsSerializer
import stripe
import math
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from functools import reduce
from django.core.mail import send_mail, BadHeaderError

stripe.api_key = settings.STRIPE_PRIVATE_KEY


# For the reduce function
def prod(x, y):
    return x + y


@api_view(['GET'])
def getRoutes(request):

    routes = [
        '/api/products/',
        '/api/products/create',

        '/api/products/upload',

        '/api/products/<id>/reviews',

        '/api/products/top',
        '/api/products/<id>',

        '/api/products/<id>/delete',
        'api/products/<update>/<id>',
    ]

    return Response(routes)


@api_view(['GET'])
def getProductsCollection(request):
    products = Product.objects.filter(collection='true')
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


# Rings Product View
@api_view(['GET'])
def getProductsRing(request):
    products = Product.objects.filter(category="ring")
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

# Necklace Product view


@api_view(['GET'])
def getProductsNecklace(request):
    products = Product.objects.filter(category='necklace')
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

# Earring Product View


@api_view(['GET'])
def getProductsEarring(request):
    products = Product.objects.filter(category='earring')
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

# Bangle Product View


@api_view(['GET'])
def getProductsBangle(request):
    products = Product.objects.filter(category='bangle')
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

# Bracelet Product View


@api_view(['GET'])
def getProductsBracelet(request):
    products = Product.objects.filter(category='bracelet')
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

# Chain Product View


@api_view(['GET'])
def getProductsChain(request):
    products = Product.objects.filter(category='chain')
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductsSerializer(product, many=False)
    return Response(serializer.data)


# Global Variable used for addOrderItems and updated by getclientSecret
productTotal = 0  # Stripe issues paymetns in Cents/ Pennies


# Adding Succesful Order to backend Model
@api_view(['POST'])
def addOrderItems(request):

    data = request.data
    shippingPrice = data['delivery']
    if data and len(data) == 0:
        return Response({'Detail: No Items in the Cart'}, HttpResponse(status=400))
    else:
        if shippingPrice != 'Standard':
            shippingPrice = 5.99
        else:
            shippingPrice = 0
        totalPrice = shippingPrice + productTotal
        totalPrice = round(totalPrice, 2)
        # Order.objects.all().delete()
        # ShippingAddress.objects.all().delete()
        order = Order.objects.create(
            shippingPrice=shippingPrice,
            totalPrice=totalPrice,
        )

        shipping = ShippingAddress.objects.create(
            order=order,
            addressLine1=data['deliveryDetails']['addressLine1'],
            addressLine2=data['deliveryDetails']['addressLine2'],
            city=data['deliveryDetails']['city'],
            postcode=data['deliveryDetails']['postcode'],
            shippingPrice=shippingPrice,
            phone=data['deliveryDetails']['phone']
        )

        for i in data['cartStorage']:
            product = Product.objects.get(sku=i['sku'])

            OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
            )

            product.countInStock -= 1
            product.save()

    print(data['deliveryDetails']['addressLine1'])

    return HttpResponse(status=200)


@api_view(['POST'])
def getClientSecret(request):

    productPriceList = []
    data = request.data
    for i in data:
        product = Product.objects.get(_id=i['_id'])
        productPriceList.append(product.price)
    productTotal = reduce(prod, productPriceList)
    divideBy100 = productTotal / 100
    multiplyByDiscount = divideBy100 * 80
    mathFloorPrice = math.floor(multiplyByDiscount)
    totalPrice = mathFloorPrice * 10

    try:
        intent = stripe.PaymentIntent.create(
            amount=totalPrice,
            currency='gbp',
            metadata={'integration_check': 'accept_a_payment'},
        )
        return JsonResponse({
            'client_secret': intent.client_secret
        })

    except:
        return Response({'Details': 'Server Error....'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        print(session)

    return HttpResponse(status=200)


@api_view(["POST"])
def sendEmail(request):
    # Convert List to String to comply with django Send_mail module
    s = [
        request.data["firstName"],
        request.data["sureName"],
        request.data["phone"],
        request.data["email"],
        request.data["message"],
    ]
    listToString = " ".join(map(str, s))
    # print(listToString)

    try:
        send_mail(
            "Contact Enquiry",
            listToString,
            "contact@kylemitt.com",
            ["contact@kylemitt.com"],
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    return Response("Success")
