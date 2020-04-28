# Financial API

## API Structure
This is the version 1 of the API, so all requests begin
with ``` /api/v1/<the-endpoint> ```

|          Endpoint          | HTTP Method |                                                  Result                                                  |
|:--------------------------:|:-----------:|:--------------------------------------------------------------------------------------------------------:|
|            users           |     GET     | Get all users                                                                                            |
|          users/:id         |     GET     | Get a specific user                                                                                      |
|            users           |     POST    | Create a user                                                                                            |
|          users/:id         |     PUT     | TBD                                                                                                      |
|          users/:id         |    DELETE   | TBD                                                                                                      |
|        transactions        |     GET     | Get all transactions                                                                                     |
|      transactions/:id      |     GET     | Get a specific transaction                                                                               |
|        transactions        |     POST    | Create a transaction (transactions can also be added by bulk)                                            |
|      transactions/:id      |     PUT     | TBD                                                                                                      |
|      transactions/:id      |    DELETE   | TBD                                                                                                      |
|  users/:id/account-summary |     GET     | Get user summary by account. This shows the balance of the account,<br>total inflows, and total outflows.|
| users/:id/category-summary |     GET     | Get user summary by category that shows the sum of amounts per transaction category.                     |


### Users

#### Endpoint /api/v1/users
You can create users by receiving: name, email and age.


#### Input:
```
{"name": "Jane Doe", "email": "jane@email.com", "age": 23}
```

#### Output:
```
{
    "pk": 1,
    "name": "Jane Doe",
    "email": "jane@email.com",
    "age": 23
}
````


#### Endpoint  /api/v1/users
You can see all users


#### Output:
```
[
    {
        "pk": 1,
        "name": "Jane Doe",
        "email": "jane@email.com",
        "age": 23
    },
    {
        "pk": 2,
        "name": "Luis Suarez",
        "email": "testuser@email.com",
        "age": 42
    }
]
````


#### Endpoint /api/v1/users/1
Also, you can see the details of a specific user.


#### Output:
```
{
    "pk": 1,
    "name": "Jane Doe",
    "email": "jane@email.com",
    "age": 23
}
```


### Transactions

#### Endpoint /api/v1/transactions/
You can create users' transactions. Each transaction has: reference
(unique), account, date, amount, type, category and is related to a user.


#### Input:
```
{"reference": "000051", "account": "S00099", "date": "2020-01-13", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": 2}
```

#### Output:
```
{
    "reference": "000051",
    "account": "S00099",
    "date": "2020-01-13",
    "amount": "-51.13",
    "type": "outflow",
    "category": "groceries",
    "user": 2
}
```

#### Remember:
- A transaction reference is unique.
- There are only two type of transactions: inflow and outflow.
- All outflow transactions amounts are negative decimal numbers.
- All inflow transactions amounts are positive decimal numbers.
- We expect to receive transactions in bulk as well.
- The transactions we receive could be already in our system, thus we need to avoid duplicating them in our database.

### Summaries
This is the interesting part. Here we are going to be able to have some insights
related to our users and their behavior with money.

#### Account Summary

Here we are able to see a user's summary by account that shows the balance
of the account, total inflow and total outflows.

Output:
```
{
  "user_account_summary":
  [
    {"account":"C00099","total_inflow":2500.72,"total_outflow":-761.85,"balance":1738.87},
    {"account":"S00012","total_inflow":150.72,"total_outflow":0.0,"balance":150.72}
  ]
}
```

It is also possible to specify a date range, if no date range is given all
transactions should be considered.

Just try this and you will see a different output ;)

```
api/v1/users/1/account-summary?start_date=01-01-2020&end_date=12-01-2020
```
#### Output:
```
{
  "user_account_summary":
  [
    {"account":"C00099","total_inflow":2500.72,"total_outflow":201.85,"balance":2298.87},
    {"account":"S00012","total_inflow":150.72,"total_outflow":0.0,"balance":150.72}
  ]
}
```


#### Summary by Category

Here we are able to see a user's summary by category. This one shows the sum
of amounts per transaction type: (inflow or outflow)


#### Output:
```
{"inflow": {"salary": "2500.72", "savings": "150.72"}, "outflow": {"groceries": "-51.13", "rent": "-560.00", "transfer": "-150.72"}}
```


## How to Run

### Using Docker
Let's pray to the Demo Gods and let's start making some API calls.

0. Make sure you have the docker engine running and to install docker compose ;)
1. Run ```docker-compose up --build```
2. Voilà, you should be ready to go and start making those calls.

### Using Python's virtual environment
1. If you want to run the application from python's virtual environment go to ```financial_api/financial_api/```
and create a ```.env``` file with the following vars:

```
DATABASES_ENGINE=django.db.backends.postgresql_psycopg2
DATABASES_NAME=financial_api_db
DATABASES_USER=financial_api_user
DATABASES_PASSWORD=3x4mpl3P455w0rd
DATABASES_HOST=localhost
DATABASES_PORT=5432
```

2. Make sure you have Postgres running

3. If you don't have Postgres, don't worry just add ``` IS_SQLITE=True ``` to
the ```.env``` file and you should be ready to go

4. Make sure you are running the virtual environment, otherwise just source it:
```
source env/bin/activate
```
5. Now go to your terminal and run:
```
python manage.py makemigrations && python manage.py migrate && python manage.py runserver
```

### Testing
This application has 2 types of tests
  - Views
  - Models

To run them, all you need to do is ``` python manage.py test ```


## Bug or Feature?
Although transactions can be created in bulk, there is a catch.
Let's say there are 6 transactions:

```
[
 {"reference": "000051", "account": "C00099", "date": "2020-01-03", "amount": "-51.13", "type": "outflow", "category": "groceries", "user": 1},
 {"reference": "000052", "account": "C00099", "date": "2020-01-10", "amount": "2500.72", "type": "inflow", category": "salary", "user": 1},
 {"reference": "000053", "account": "C00099", "date": "2020-01-10", "amount": "-150.72", "type": "outflow", category": "transfer", "user": 1},
 {"reference": "000054", "account": "C00099", "date": "2020-01-13", "amount": "-560.00", "type": "outflow", "category": "rent", "user": 1},
 {"reference": "000051", "account": "C00099", "date": "2020-01-04", "amount": "-51.13", "type": "outflow", "category": "other", "user": 1},
 {"reference": "000689", "account": "S00012", "date": "2020-01-10", "amount": "150.72", "type": "inflow", "category": "savings" ,"user": 1},
]
```
By design, the API will:
- Save the first 4 (000051, 000052, 000053, 000054)
- Will not process the one before last (000051), because of an Integrity Error (duplicate key)
- Will not process (ignore) the last one (000689)

I thought about using [bulk_create](https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create),
but in Django's development version, also using bulk_create "has a number of caveats though"
such as save() method will not being called.

Do you think we can improve this? If so, PRs are open and I'm more than happy to
collaborate. After all, if you are reading this you probably know how to contact me ;)


## Tips
This is **not production ready**. Things such as the debugger and the secret
are out there in the plain. Also, make sure to add some other components such
as authentication, authorization, a rate-limiter, and logging. If you want to
know a little bit more about why you need to do it click
[here](https://shekodn.github.io/blog/securing-apis-how-to-design-a-not-so-crapi-one.html).
