from django.utils import timezone

from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_due_date(self, value): # noqa
        if value and value < timezone.now():
            raise serializers.ValidationError('Due date cannot be in the past.')
        return value

    def validate_status(self, value): # noqa
        if value not in [Task.PENDING, Task.IN_PROGRESS, Task.COMPLETED]:
            raise serializers.ValidationError('Status cannot be set to completed.')
        return value

    def create(self, validated_data):
        task = Task.objects.create(user=self.context['request'].user, **validated_data)
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()
        return instance
