from rest_framework import serializers
from .models import User, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "name", "email", "age"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["reference", "account", "date", "amount", "type", "category", "user"]


class UserAccountSummarySerializer(serializers.ModelSerializer):
    """
    Description:
        This serializer calls the get_user_account_summary method and displays
        data per accoount and according to the business logic.
    Example:
        {"account": "C00099", "balance": "1738.87", "total_inflow": "2500.72", "total_outflow": "-761.85"},
        {"account": "S00012", "balance": "150.72", "total_inflow": "150.72", "total_outflow": "0.00"},
    """

    user_account_summary = serializers.SerializerMethodField()

    def get_user_account_summary(self, instance):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")
        return instance.get_user_account_summary(start_date, end_date)

    class Meta:
        model = User
        fields = ["user_account_summary"]


class AuxGetUserSummaryByCategorySerializer(serializers.ModelSerializer):
    """
    Description:
        This serializer is a sidekick. What we do here is get the inflow and
        outflow of user's transactions. After we get them, we call the
        GetUserSummaryByCategorySerializer in order to display the data
        according to the business logic.
    """

    inflow = serializers.SerializerMethodField()
    outflow = serializers.SerializerMethodField()

    def get_inflow(self, instance):
        return GetUserSummaryByCategorySerializer(
            instance.get_user_summary_by_inflow(), many=True
        ).data

    def get_outflow(self, instance):
        return GetUserSummaryByCategorySerializer(
            instance.get_user_summary_by_outflow(), many=True
        ).data

    class Meta:
        model = User
        fields = ["inflow", "outflow"]


class GetUserSummaryByCategorySerializer(serializers.ModelSerializer):
    """
    Description:
        This serializer only returns a simple representation in order to comply
        with the business logic.
    """

    def to_representation(self, instance):
        return {instance.category: instance.amount}

    class Meta:
        model = Transaction
