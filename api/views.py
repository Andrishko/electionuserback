from django.shortcuts import render
import random
import string
from datetime import datetime, timedelta
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from api.models import *
from rest_framework.decorators import api_view
from rest_framework.request import Request
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import json

keyVote = 'hkldhlkdjsahfdjk'


def sign(data_to_sign):
    # Генерація закритого та відкритого ключів
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    # Конвертування словника даних у формат JSON
    data_json = json.dumps(data_to_sign).encode()
    # Підписування даних закритим ключем
    signature = private_key.sign(
        data_json,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    # Конвертування відкритого ключа у PEM формат
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return {'signature': signature.hex(),
            'public_key': pem_public_key.decode()}

def generate_unique_string():
    # Define the characters to use for generating the string
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random string of length 50
        random_string = ''.join(random.choices(characters, k=255))

        # Check if the string exists in the `uniq` table
        if not codeVote.objects.filter(code=random_string).exists():
            return random_string


@api_view(["GET"])
def main(request: Request):

    return render(request, 'index.html')


@api_view(["PUT"])
def check(request: Request):
    req = request.data
    user = codeVote.objects.get(name=req['name'])
    if user.is_voted == 1:
      return JsonResponse({'value': 'you voted'})
    user.is_voted == 1
    user.save()
    return JsonResponse({'value': 'aproved', 'code': user.code})


@api_view(["PUT"])
def counter(request: Request):

    data = json.loads(request.body)
    # Розпакування даних
    data_to_sign = data.get('data')
    signature = data.get('signature')
    pem_public_key = data.get('public_key')
    # Завантаження відкритого ключа з PEM формату
    public_key = serialization.load_pem_public_key(
        pem_public_key.encode(),
        backend=default_backend()
    )

    # Конвертування даних у формат JSON
    data_json = json.dumps(data_to_sign).encode()

    # Перевірка цифрового підпису
    public_key.verify(
        bytes.fromhex(signature),
        data_json,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return JsonResponse({'valid': True, 'data': data_to_sign, 'key': keyVote})

    # Підпис є недійсним
    # return JsonResponse({'valid': False, 'error': str(e)})
    # voting_name = data["voting"]
    # voting = Counter.objects.filter(voting_name=voting_name).first()
    # if voting:
    #     # Якщо голосування існує в базі даних, збільшуємо число на 1
    #     voting.count += 1
    #     voting.save()

    # else:
    #     # Якщо голосування немає в базі даних, створюємо новий об'єкт
    #     new_voting = Counter(name=voting_name, number=1)
    #     new_voting.save()

    # return ''

@api_view(["GET"])
def get_key(request: Request):
    return JsonResponse({'key': keyVote})
