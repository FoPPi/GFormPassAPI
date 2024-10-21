# Endpoints

## Global Variables

Define key variables at the start of the file for easy configuration and management of frequently used data like host URLs, API keys, and user keys.

```http
@host = http://127.0.0.1:8000
@api_key = your_actual_api_key_here
@admin_key = your_actual_admin_key_here
@donatello_key = your_actual_donatello_api_key_here
@user_key = Enter_Key_Here_After_Generation
```

## API Endpoints

### 1. Generate User

This endpoint generates a new `user_key` for your application.

```http
POST {{host}}/user/donates
Content-Type: application/json
X-Key: {{donatello_key}}

{
  "pubId": "D41-123123",
  "message": "your@email.com",
  "amount": "5",
  "currency": "USD"
}
```

#### Generate User Returning

* 200 OK
```json
{
  "status": "success"
}
```

* 403 Forbidden Forbidden
```json
{
  "detail": "Donation amount must be greater than 5 USD/EUR"
}
```
```json
{
  "detail": "Donation amount must be greater than 200 UAH"
}
```

* 500 Internal Server Error
```json
{
  "detail": "duplicate key value violates unique constraint \"users_pub_id_key\"\nDETAIL:  Key (pub_id)=(D41-497724) already exists."
}
```

### 2. Activate User

Once the user key is generated, activate it using this endpoint.

```http
POST {{host}}/user/activate
Content-Type: application/json
X-Api-Key: {{api_key}}
X-User-Key: {{user_key}}
```

#### Activate User Returning

* 200 OK
```json
{
  "status": "success"
}
```

* 403 Forbidden Forbidden
```json
{
  "detail": "Key is already active"
}
```

### 3. GPT Request

This endpoint allows you to send a question for processing via GPT with the given parameters.

```http
POST {{host}}/question
Content-Type: application/json
X-Api-Key: {{api_key}}
X-User-Key: {{user_key}}

{
  "test_url": "123535",
  "title": "У чому різниця між локальною та глобальною змінною?",
  "id": "Q-1",
  "type": "radio",
  "options": [
    {
      "text": "Відмінностей немає",
      "id": "O-0"
    },
    {
      "text": "Локальні видно всюди, глобальні лише у функціях",
      "id": "O-1"
    },
    {
      "text": "Глобальні можна перевизначати, локальні не можна",
      "id": "O-2"
    },
    {
      "text": "Локальні можна перевизначати, глобальні не можна",
      "id": "O-3"
    },
    {
      "text": "Глобальні видно всюди, локальні лише у функціях",
      "id": "O-4"
    }
  ]
}
```

#### GPT Request Returning

* 200 OK
```json
{
  "info": "new",
  "answers": {
    "type": "select",
    "text": [
      "Глобальні видно всюди, локальні лише у функціях"
    ]
  }
}
```
```json
{
  "info": "cached",
  "answers": {
    "type": "select",
    "text": [
      "Глобальні видно всюди, локальні лише у функціях"
    ]
  }
}
```

* 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

* 403 Forbidden Forbidden
```json
{
  "detail": "Key not found"
}
```
```json
{
  "detail": "Key not active"
}
```


### 4. Update Day Limit

Use this endpoint to update the daily limit for a user.

```http
PATCH {{host}}/user/update_keys
Content-Type: application/json
X-Admin-Key: {{admin_key}}
```

#### Update Day Returning

* 200 OK
```json
{
  "status": "success"
}
```


### 5. Delete Expired Questions

This endpoint deletes all expired questions from the system.

```http
DELETE {{host}}/question
Content-Type: application/json
X-Admin-Key: {{admin_key}}
```

#### Delete Expired Questions Returning

* 200 OK
```json
{
  "status": "success"
}
```