from rest_framework import serializers
from post.models import Post
from comments.models import Comment
from reports.models import Report
from .models import GlobalPID
from django.contrib.contenttypes.models import ContentType

#serializer de posts

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['po_content', 'community', 'anon']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # Crear el GeneralPID
        global_pid = GlobalPID.objects.create()

        # Crear el post con el autor y el GeneralPID
        return Post.objects.create(author=user, global_pid=global_pid, **validated_data)

#Serializer de comentarios

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['global_pid', 'co_content', 'post', 'author', 'parent', 'is_reply', 'creat_date',]
        extra_kwargs = {
            'author': {'read_only': True},
            'is_reply': {'read_only': True},
            'global_pid': {'read_only': True},
        }

    def get_replies(self, obj):
        if obj.is_reply:
            return None
        replies_qs = obj.replies.all().order_by('creat_date')
        return CommentSerializer(replies_qs, many=True, context=self.context).data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        parent = validated_data.get('parent', None)
        is_reply = parent is not None

        global_pid = GlobalPID.objects.create()

        return Comment.objects.create(
            author=user,
            global_pid=global_pid,
            is_reply=is_reply,
            **validated_data
        )

    #Report Serializers

class ReportSerializer(serializers.ModelSerializer):
    # Mostramos solo lectura para el contenido real
    content_object = serializers.SerializerMethodField()
    content_type = serializers.CharField(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'reporter', 'global_pid', 'reason', 'timestamp', 'content_object', 'content_type']
        read_only_fields = ['timestamp', 'content_object', 'content_type']

    def get_content_object(self, obj):
        if obj.content:
            return str(obj.content)  # Podés devolver un serializer si querés
        return None

    def create(self, validated_data):
        global_pid = validated_data.get('global_pid')
        reporter = validated_data.get('reporter')
        reason = validated_data.get('reason')

            # Buscamos a qué modelo pertenece el global_pid
        post = Post.objects.filter(global_pid=global_pid).first()
        comment = Comment.objects.filter(global_pid=global_pid).first()

        if post:
            content_type = ContentType.objects.get_for_model(Post)
            object_id = post.pk
        elif comment:
            content_type = ContentType.objects.get_for_model(Comment)
            object_id = comment.pk
        else:
            raise serializers.ValidationError("GlobalPID no está vinculado ni a un Post ni a un Comment.")

        report = Report.objects.create(
            global_pid=global_pid,
            reporter=reporter,
            reason=reason,
            content_type=content_type,
            object_id=object_id
        )

        return report