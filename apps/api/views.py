# apps/api/views.py
from django.http import JsonResponse

def test_api(request):
    return JsonResponse({"message": "Authorized!"})