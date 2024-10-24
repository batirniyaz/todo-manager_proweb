from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer

from rest_framework import status


class TaskListAPIView(APIView):

    @extend_schema(
        tags=['Tasks'],
        summary="Retrieve a list of tasks",
        description="This endpoint retrieves tasks filtered by status, due date, or specific year, month, and day.",
        parameters=[
            OpenApiParameter(name='status', description="Filter by task status ('P', 'IP', 'C')", required=False,
                             type=str, examples=[
                                OpenApiExample('Pending', value='P'),
                                OpenApiExample('In Progress', value='IP'),
                                OpenApiExample('Completed', value='C')
                                ]),
            OpenApiParameter(name='year', description="Filter by year of due date", required=False, type=int),
            OpenApiParameter(name='month', description="Filter by month of due date", required=False, type=int),
            OpenApiParameter(name='day', description="Filter by day of due date", required=False, type=int),
            OpenApiParameter(name='page', description="Page number", required=False, type=int),
            OpenApiParameter(name='page_size', description="Number of items per page", required=False, type=int)
        ],
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description='A successful response returns a list of tasks.',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={
                            "status": "success",
                            "length": 2,
                            "data": [
                                {
                                    "id": 1,
                                    "title": "Task 1",
                                    "description": "Task 1 description",
                                    "status": "P",
                                    "due_date": "2024-10-23T12:00:00Z",
                                    "created_at": "2024-10-20T09:00:00Z",
                                    "updated_at": "2024-10-21T10:00:00Z"
                                },
                                {
                                    "id": 2,
                                    "title": "Task 2",
                                    "description": "Task 2 description",
                                    "status": "IP",
                                    "due_date": "2024-10-24T12:00:00Z",
                                    "created_at": "2024-10-21T09:00:00Z",
                                    "updated_at": "2024-10-22T10:00:00Z"
                                }
                            ]
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='Bad request, invalid input',
                examples=[
                    OpenApiExample(
                        'Invalid Status',
                        value={"msg": "Invalid status filter"}
                    ),
                    OpenApiExample(
                        'Invalid Date',
                        value={"msg": "Invalid date format"}
                    )
                ]
            ),
            404: OpenApiResponse(
                description='No tasks found',
                examples=[
                    OpenApiExample(
                        'No Tasks Found',
                        value={"status": "error", "msg": "No tasks found"}
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Server error',
                examples=[
                    OpenApiExample(
                        'Server Error',
                        value={"status": "error", "msg": "An error occurred"}
                    )
                ]
            )
        }
    )
    def get(self, request):  # noqa
        try:
            tasks = Task.objects.filter(user=request.user)

            status_filter = request.query_params.get('status', None)
            if status_filter:
                if status_filter not in ['P', 'IP', 'C']:
                    return Response({"msg": "Invalid status filter"}, status=status.HTTP_400_BAD_REQUEST)
                tasks = tasks.filter(status=status_filter)

            year = request.query_params.get('year', None)
            month = request.query_params.get('month', None)
            day = request.query_params.get('day', None)

            if year:
                try:
                    tasks = tasks.filter(due_date__year=int(year))
                except ValueError:
                    return Response({"msg": "Invalid year format"}, status=status.HTTP_400_BAD_REQUEST)

            if month:
                if not year:
                    return Response({"msg": "Year is required when filtering by month"},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    tasks = tasks.filter(due_date__month=int(month))
                except ValueError:
                    return Response({"msg": "Invalid month format"}, status=status.HTTP_400_BAD_REQUEST)

            if day:
                if not year and not month:
                    return Response({"msg": "Year and month are required when filtering by day"},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    tasks = tasks.filter(due_date__day=int(day))
                except ValueError:
                    return Response({"msg": "Invalid day format"}, status=status.HTTP_400_BAD_REQUEST)

            paginator = PageNumberPagination()
            page_size = request.query_params.get('page_size', paginator.page_size)
            paginator.page_size = page_size if page_size else paginator.page_size
            page = paginator.paginate_queryset(tasks, request)

            if page is not None:
                serializer = TaskSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = TaskSerializer(tasks, many=True)

            data = {
                "status": "success",
                "length": tasks.count(),
                "data": serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({"status": "error", "msg": "No tasks found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        tags=['Tasks'],
        summary="Create a new task",
        description="This endpoint allows you to create a new task. ",
        request=TaskSerializer,
        responses={
            201: OpenApiResponse(
                response=TaskSerializer,
                description='Task created successfully',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={
                            "status": "success",
                            "msg": "Task created successfully",
                            "data": {
                                "id": 1,
                                "title": "New Task",
                                "description": "Description of the task",
                                "status": "P",
                                "due_date": "2024-10-25T12:00:00Z",
                                "created_at": "2024-10-23T09:00:00Z",
                                "updated_at": "2024-10-23T09:00:00Z"
                            }
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
                            "title": ["This field is required."],
                            "due_date": ["Enter a valid date and time."]
                        }
                    ),
                    OpenApiExample(
                        'Invalid Status',
                        value={"status": ["Invalid value for status, choose from ['P', 'IP', 'C']"]}
                    )
                ]
            ),
            500: OpenApiResponse(
                description='Server error',
                examples=[
                    OpenApiExample(
                        'Server Error',
                        value={"status": "error", "msg": "An internal server error occurred"}
                    )
                ]
            )
        }
    )
    def post(self, request):  # noqa
        data = request.data
        serializer = TaskSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "msg": "Task created successfully",
                "data": serializer.data
            }

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):

    @extend_schema(
        tags=['Tasks'],
        summary="Retrieve a task by ID",
        description="This endpoint retrieves a task by its ID.",
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description='A successful response returns the task details.',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={
                            "status": "success",
                            "data": {
                                "id": 1,
                                "title": "Task 1",
                                "description": "Task 1 description",
                                "status": "P",
                                "due_date": "2024-10-23T12:00:00Z",
                                "created_at": "2024-10-20T09:00:00Z",
                                "updated_at": "2024-10-21T10:00:00Z"
                            }
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Task not found',
                examples=[
                    OpenApiExample(
                        'Task Not Found',
                        value={"status": "error", "msg": "Task not found"}
                    )
                ]
            )
        }
    )
    def get(self, request, pk):  # noqa
        try:
            task = Task.objects.get(id=pk, user=request.user)
            serializer = TaskSerializer(task)
            data = {
                "status": "success",
                "data": serializer.data
            }
            return Response(data)
        except Task.DoesNotExist:
            return Response({"status": "error", "msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        tags=['Tasks'],
        summary="Update a task by ID",
        description="This endpoint allows you to update a task by its ID.",
        request=TaskSerializer,
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description='Task updated successfully',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={
                            "status": "success",
                            "msg": "Task updated successfully",
                            "data": {
                                "id": 1,
                                "title": "Updated Task",
                                "description": "Updated description",
                                "status": "IP",
                                "due_date": "2024-10-25T12:00:00Z",
                                "created_at": "2024-10-20T09:00:00Z",
                                "updated_at": "2024-10-23T10:00:00Z"
                            }
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
                            "title": ["This field is required."],
                            "due_date": ["Enter a valid date and time."]
                        }
                    ),
                    OpenApiExample(
                        'Invalid Status',
                        value={"status": ["Invalid value for status, choose from ['P', 'IP', 'C']"]}
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Task not found',
                examples=[
                    OpenApiExample(
                        'Task Not Found',
                        value={"status": "error", "msg": "Task not found"}
                    )
                ]
            )
        }
    )
    def put(self, request, pk):
        try:
            task = Task.objects.get(id=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({"status": "error", "msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "msg": "Task updated successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Tasks'],
        summary="Update a task by ID",
        description="This endpoint allows you to update a task by its ID.",
        request=TaskSerializer,
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description='Task updated successfully',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={
                            "status": "success",
                            "msg": "Task updated successfully",
                            "data": {
                                "id": 1,
                                "title": "Updated Task",
                                "description": "Updated description",
                                "status": "IP",
                                "due_date": "2024-10-25T12:00:00Z",
                                "created_at": "2024-10-20T09:00:00Z",
                                "updated_at": "2024-10-23T10:00:00Z"
                            }
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
                            "title": ["This field is required."],
                            "due_date": ["Enter a valid date and time."]
                        }
                    ),
                    OpenApiExample(
                        'Invalid Status',
                        value={"status": ["Invalid value for status, choose from ['P', 'IP', 'C']"]}
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Task not found',
                examples=[
                    OpenApiExample(
                        'Task Not Found',
                        value={"status": "error", "msg": "Task not found"}
                    )
                ]
            )
        }
    )
    def patch(self, request, pk):
        try:
            task = Task.objects.get(id=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({"status": "error", "msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "msg": "Task updated successfully",
                "data": serializer.data
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Tasks'],
        summary="Delete a task by ID",
        description="This endpoint allows you to delete a task by its ID.",
        responses={
            200: OpenApiResponse(
                description='Task deleted successfully',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={"status": "success", "msg": "Task deleted successfully"}
                    )
                ]
            ),
            404: OpenApiResponse(
                description='Task not found',
                examples=[
                    OpenApiExample(
                        'Task Not Found',
                        value={"status": "error", "msg": "Task not found"}
                    )
                ]
            )
        }
    )
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response({"status": "error", "msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        task.delete()
        data = {
            "status": "success",
            "msg": "Task deleted successfully"
        }
        return Response(data, status=status.HTTP_200_OK)
