from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
def login(request):
    username = request.data['']