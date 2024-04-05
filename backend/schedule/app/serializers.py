from rest_framework import serializers

from .models import Trainer, Record, User, Schedule


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class RecordSerializer(serializers.ModelSerializer):
    client = UserSerializer()
    trainer = TrainerSerializer()
    schedule = ScheduleSerializer()
    class Meta:
        model = Record
        fields = "__all__"
