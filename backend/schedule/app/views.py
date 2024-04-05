from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trainer, User
from .serializers import TrainerSerializer, RecordSerializer, UserSerializer
from .forms import RecordForm


class TrainerAPIView(APIView):
    def get(self, request):
        trainers = Trainer.objects.all()
        serializer = TrainerSerializer(trainers, many=True)
        return Response(serializer.data)


class UserAPIView(APIView):
    def get(self, request):
        trainers = User.objects.all()
        serializer = UserSerializer(trainers, many=True)
        return Response(serializer.data)


class RecordAPIView(APIView):
    def post(self, request):
        form = RecordForm(request.data)
        if form.is_valid():
            record = form.save()
            serializer = RecordSerializer(record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
