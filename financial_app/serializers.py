from rest_framework import serializers
from .models import User, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "name", "email", "age"]


class TransactionListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        """
        Description:
            Although transactions can be created in bulk, there is a catch.
            Let's say there are 6 transactions with the following references:
            "reference": "000051"
            "reference": "000052"
            "reference": "000053"
            "reference": "000054"
            "reference": "000051" (duplicate)
            "reference": "000689"

            By design, the API:
                - Will save the first 4 (000051, 000052, 000053, 000054)
                - Will not process the one before last (000051), because of an Integrity Error (duplicated key)
                - Will not process (ignore) the last one (000689)
                - Will return all the transaction objects (might lead to a bad
                user (or developer?) experience)

            As a result we need to overwrite create method to only create
            the ones that are not duplicated. By doing so, the following
            transactions will be handled: 000051, 000052, 000053, 000054,
            and 000689. While the duplicated one will be ignored.

        Params:
            validated_data: Returns the validated incoming data

        Returns:
            unique_transactions list
        """

        # list containing all transactions which have been validated
        all_transactions = [Transaction(**item) for item in validated_data]

        # This helper set will allow us to keep track which
        # transactions (using tx.reference) are unique.
        unique_transactions_helper_set = set()
        unique_transactions = []
        for tx in all_transactions:
            if tx.reference not in unique_transactions_helper_set:
                unique_transactions.append(tx)
                unique_transactions_helper_set.add(tx.reference)
        return Transaction.objects.bulk_create(unique_transactions)


class TransactionSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        """
        Description:
            TL;DR: Maps "user_id" json key to "user" attribute in Transaction Model.

            Overrides implementation of to_internal_value() method. We do this
            in order to map the "user_id" key name we receive in our request with
            "user" (our Transaction attribute name). We did the override in
            this method in particular, because we need to take the
            unvalidated incoming data as input. If we don't do it here, a
            validation error will raise, because transactions need to have a user.
        Parameter:
            data (dict): dict containing the data of the request
        Return:
            data (dict): dictionary of validated data
        """
        data = {
            "reference": data.get("reference"),
            "account": data.get("account"),
            "date": data.get("date"),
            "amount": data.get("amount"),
            "type": data.get("type"),
            "category": data.get("category"),
            "user": data.get("user_id"),
        }

        ret = super().to_internal_value(data)
        return ret

    class Meta:
        list_serializer_class = TransactionListSerializer
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
