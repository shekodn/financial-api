# Financial API

## API Structure

|          Endpoint          | HTTP Method |                                                  Result                                                  |
|:--------------------------:|:-----------:|:--------------------------------------------------------------------------------------------------------:|
|            users           |     GET     | Get all users                                                                                            |
|          users/:id         |     GET     | Get a specific user                                                                                      |
|            users           |     POST    | Create a user                                                                                            |
|          users/:id         |     PUT     | TBD                                                                                                      |
|          users/:id         |    DELETE   | TBD                                                                                                      |
|        transactions        |     GET     | Get all transactions                                                                                     |
|      transactions/:id      |     GET     | Get a specific transaction                                                                               |
|        transactions        |     POST    | Create a user (transactions can also be added by bulk)                                                   |
|      transactions/:id      |     PUT     | TBD                                                                                                      |
|      transactions/:id      |    DELETE   | TBD                                                                                                      |
|  users/:id/account-summary |     GET     | Get user summary by account. This shows the balance of the account,<br>total inflows, and total outflows |
| users/:id/category-summary |     GET     | Get user summary by category that shows the sum of amounts per transaction category                      |


### Users

### Transactions

### Summaries

#### Account Summary

#### Summary by Category
