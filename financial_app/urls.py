from django.conf.urls import url
from . import views


urlpatterns = [
    # User routes
    url(
        r"^api/v1/users/(?P<pk>[0-9]+)$",
        views.get_delete_put_user,
        name="get_delete_put_user",
    ),
    url(r"^api/v1/users/$", views.get_post_users, name="get_post_users"),
    # Transaction routes
    url(
        r"^api/v1/transactions/(?P<pk>[0-9]+)$",
        views.get_delete_put_transaction,
        name="get_delete_put_transaction",
    ),
    url(
        r"^api/v1/transactions/$",
        views.get_post_transactions,
        name="get_post_transactions",
    ),
    # Summary routes
    # Summary by Account
    url(
        "^api/v1/users/(?P<pk>[0-9]+)/account-summary$",
        views.get_user_account_summary,
        name="get_user_account_summary",
    ),
    # Summary by Category
    url(
        "^api/v1/users/(?P<pk>[0-9]+)/category-summary$",
        views.get_user_summary_by_category,
        name="get_user_summary_by_category",
    ),
]
