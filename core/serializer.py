from rest_framework import serializers
from post.models import Post
from .models import GlobalPID

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['po_content', 'community']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # Crear el GeneralPID
        global_pid = GlobalPID.objects.create()

        # Crear el post con el autor y el GeneralPID
        return Post.objects.create(author=user, global_pid=global_pid, **validated_data)
