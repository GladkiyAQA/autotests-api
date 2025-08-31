"""
pydantic_create_user.py
=======================

Схемы Pydantic для эндпоинта POST /api/v1/users:

- UserSchema — модель данных пользователя
- CreateUserRequestSchema — запрос на создание пользователя
- CreateUserResponseSchema — ответ с данными созданного пользователя

Сделано в том же стиле, что и пример с CourseSchema:
- alias через Field(alias="...") под camelCase JSON
- EmailStr для валидации email
- примеры инициализации (аргументы, dict, JSON)
"""

from pydantic import BaseModel, Field, EmailStr, ValidationError


class UserSchema(BaseModel):
    """
    Данные пользователя (возвращаются в ответах; без поля password).
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserRequestSchema(BaseModel):
    """
    Тело запроса на создание пользователя (POST /api/v1/users).
    """
    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserResponseSchema(BaseModel):
    """
    Ответ сервиса при успешном создании пользователя.
    """
    user: UserSchema


# --- Примеры использования ---

# 1) Инициализация CreateUserRequestSchema через аргументы
create_req_model = CreateUserRequestSchema(
    email="user@example.com",
    password="string",
    lastName="Bond",
    firstName="Zara",
    middleName="Alise",
)
print("CreateUserRequest (args):", create_req_model)
print(create_req_model.model_dump())
print(create_req_model.model_dump(by_alias=True))

# 2) Инициализация CreateUserRequestSchema через dict
create_req_dict = {
    "email": "user@example.com",
    "password": "string",
    "lastName": "Bond",
    "firstName": "Zara",
    "middleName": "Alise",
}
create_req_from_dict = CreateUserRequestSchema(**create_req_dict)
print("CreateUserRequest (dict):", create_req_from_dict)
print(create_req_from_dict.model_dump())
print(create_req_from_dict.model_dump(by_alias=True))

# 3) Инициализация CreateUserResponseSchema через JSON
create_resp_json = """
{
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "lastName": "Bond",
    "firstName": "Zara",
    "middleName": "Alise"
  }
}
"""
create_resp_model = CreateUserResponseSchema.model_validate_json(create_resp_json)
print("CreateUserResponse (JSON):", create_resp_model)
print(create_resp_model.model_dump())
print(create_resp_model.model_dump(by_alias=True))

# 4) Пример ошибки валидации (некорректный email)
try:
    bad_req = CreateUserRequestSchema(
        email="not-an-email",
        password="string",
        lastName="Doe",
        firstName="John",
        middleName="A",
    )
except ValidationError as err:
    print("ValidationError:")
    print(err)
    print(err.errors())
