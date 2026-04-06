from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

import random

from django.http import HttpResponse

def index(request):
    return HttpResponse("거시경제 자산 관리 서비스 'Tide' 백엔드 시작!")