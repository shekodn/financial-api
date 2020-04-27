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
    user_account_summary = serializers.SerializerMethodField()

    def get_user_account_summary(self, instance):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")
        return instance.get_user_account_summary(start_date, end_date)

    class Meta:
        model = User
        fields = ["user_account_summary"]


class AuxGetUserSummaryByCategorySerializer(serializers.ModelSerializer):

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
    def to_representation(self, instance):
        return {instance.category: instance.amount}

    class Meta:
        model = Transaction
