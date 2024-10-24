from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter

from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(APIView):
    @extend_schema(
        request=CommentSerializer,
        responses={
            201: OpenApiResponse(
                description='Comment created',
                examples=[
                    OpenApiExample(
                        'Comment created',
                        value={
                            'id': 1,
                            'task': 1,
                            'user': 1,
                            'text': 'This is a comment',
                            'created_at': '2021-01-01T00:00:00Z'
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='Bad request, invalid input',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'task': [
                                'Task not found.'
                            ]
                        }
                    ),
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'user': [
                                'User must be the same as the authenticated user.'
                            ]
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Internal server error',
                examples=[
                    OpenApiExample(
                        'Internal server error',
                        value={
                            'error': 'Internal server error'
                        }
                    )
                ]
            )
        },
    )
    def post(self, request):
        print(f"{request.data=}")
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "msg": "Comment created",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task',
                type=int,
                required=False,
                description='Filter comments by task id',
                location='query',
                examples=[OpenApiExample('Filter by task', value=1)]
            )
        ],
        responses={
            201: OpenApiResponse(
                response=CommentSerializer,
                description='List of comments',
                examples=[
                    OpenApiExample(
                        'List of comments',
                        value=[
                            {
                                'id': 1,
                                'task': 1,
                                'user': 1,
                                'text': 'This is a comment',
                                'created_at': '2021-01-01T00:00:00Z'
                            }
                        ]
                    )
                ]
            ),
            400: OpenApiResponse(
                description='Bad request, invalid input',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'task': [
                                'Task not found.'
                            ]
                        }
                    ),
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'user': [
                                'User must be the same as the authenticated user.'
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description='No comments found',
                examples=[
                    OpenApiExample(
                        'No comments found',
                        value={
                            'error': 'No comments found'
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Internal server error',
                examples=[
                    OpenApiExample(
                        'Internal server error',
                        value={
                            'error': 'Internal server error'
                        }
                    )
                ]
            )
        },
    )
    def get(self, request):
        try:
            comments = Comment.objects.filter(user=request.user)

            task = request.query_params.get('task', None)
            if task:
                try:
                    comments = comments.filter(task=task)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            serializer = CommentSerializer(comments, many=True)

            data = {
                "status": "success",
                "msg": "Comments retrieved",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"error": "No comments found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailView(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=CommentSerializer,
                description='Comment details',
                examples=[
                    OpenApiExample(
                        'Comment details',
                        value={
                            'id': 1,
                            'task': 1,
                            'user': 1,
                            'text': 'This is a comment',
                            'created_at': '2021-01-01T00:00:00Z'
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Comment not found',
                examples=[
                    OpenApiExample(
                        'Comment not found',
                        value={
                            'error': 'Comment not found'
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Internal server error',
                examples=[
                    OpenApiExample(
                        'Internal server error',
                        value={
                            'error': 'Internal server error'
                        }
                    )
                ]
            )
        },
    )
    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)

            serializer = CommentSerializer(comment)

            data = {
                "status": "success",
                "msg": "Comment retrieved",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(
                response=CommentSerializer,
                description='Comment updated',
                examples=[
                    OpenApiExample(
                        'Comment updated',
                        value={
                            'id': 1,
                            'task': 1,
                            'user': 1,
                            'text': 'This is a comment',
                            'created_at': '2021-01-01T00:00:00Z'
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='Bad request, invalid input',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'task': [
                                'Task not found.'
                            ]
                        }
                    ),
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'user': [
                                'User must be the same as the authenticated user.'
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Comment not found',
                examples=[
                    OpenApiExample(
                        'Comment not found',
                        value={
                            'error': 'Comment not found'
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Internal server error',
                examples=[
                    OpenApiExample(
                        'Internal server error',
                        value={
                            'error': 'Internal server error'
                        }
                    )
                ]
            )
        },
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "msg": "Comment updated",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CommentSerializer,
        responses={
            200: OpenApiResponse(
                response=CommentSerializer,
                description='Comment updated',
                examples=[
                    OpenApiExample(
                        'Comment updated',
                        value={
                            'id': 1,
                            'task': 1,
                            'user': 1,
                            'text': 'This is a comment',
                            'created_at': '2021-01-01T00:00:00Z'
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='Bad request, invalid input',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'task': [
                                'Task not found.'
                            ]
                        }
                    ),
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'user': [
                                'User must be the same as the authenticated user.'
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Comment not found',
                examples=[
                    OpenApiExample(
                        'Comment not found',
                        value={
                            'error': 'Comment not found'
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Internal server error',
                examples=[
                    OpenApiExample(
                        'Internal server error',
                        value={
                            'error': 'Internal server error'
                        }
                    )
                ]
            )
        },
    )
    def patch(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "msg": "Comment updated",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='Comment deleted',
                examples=[
                    OpenApiExample(
                        'Comment deleted',
                        value={
                            'status': 'success',
                            'msg': 'Comment deleted'
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Comment not found',
                examples=[
                    OpenApiExample(
                        'Comment not found',
                        value={
                            'error': 'Comment not found'
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Internal server error',
                examples=[
                    OpenApiExample(
                        'Internal server error',
                        value={
                            'error': 'Internal server error'
                        }
                    )
                ]
            )
        },
    )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        comment.delete()
        data = {
            "status": "success",
            "msg": "Comment deleted"
        }
        return Response(data, status=status.HTTP_200_OK)

