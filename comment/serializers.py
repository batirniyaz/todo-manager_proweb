from rest_framework import serializers

from task.models import Task
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'user')

    def validate_user(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('User must be the same as the authenticated user.')
        return value

    def validate_task(self, value):
        tasks = Task.objects.filter(user=self.context['request'].user)
        print(f"user_{tasks=}")
        if value not in tasks:
            raise serializers.ValidationError('Task not found.')
        return value

    def create(self, validated_data):
        print(f"{validated_data=}")
        comment = Comment.objects.create(user=self.context['request'].user, **validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
