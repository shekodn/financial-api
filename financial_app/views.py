from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Transaction
from .serializers import (
    AuxGetUserSummaryByCategorySerializer,
    TransactionSerializer,
    UserAccountSummarySerializer,
    UserSerializer,
)

# User views
@api_view(["GET", "DELETE", "PUT"])
def get_delete_put_user(request, pk):
    # Checks if user exists
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single user
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    # delete a single user
    elif request.method == "DELETE":
        return Response({})
    # update details of a single user
    elif request.method == "PUT":
        return Response({})


@api_view(["GET", "POST"])
def get_post_users(request):
    # get all users
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    # insert a new record for a user
    elif request.method == "POST":

        data = {
            "name": request.data.get("name"),
            "age": int(request.data.get("age")),
            "email": request.data.get("email"),
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Transaction views
@api_view(["GET", "DELETE", "PUT"])
def get_delete_put_transaction(request, pk):
    # Checks if user exists
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # get details of a single transaction
    if request.method == "GET":
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def get_post_transactions(request):
    # get all transactions
    if request.method == "GET":
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    # insert a new record for a transaction
    elif request.method == "POST":
        # Checks if it is receiving an array or a single transaction
        has_many = True if isinstance(request.data, list) else False

        serializer = TransactionSerializer(data=request.data, many=has_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Summary views
@api_view()
def get_user_account_summary(request, pk):
    # Checks if user exists
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")
        serializer = UserAccountSummarySerializer(
            user, context={"start_date": start_date, "end_date": end_date}
        )
        return Response(serializer.data)


@api_view()
def get_user_summary_by_category(request, pk):
    # Checks if user exists
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AuxGetUserSummaryByCategorySerializer(user)
        return Response(serializer.data)
