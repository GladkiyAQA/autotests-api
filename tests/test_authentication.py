from http import HTTPStatus
import pytest
from clients.users.public_users_client import get_public_users_client
from clients.authentication.authentication_client import get_authentication_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.authentication.authentication_schema import LoginResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.authentication import assert_login_response

@pytest.mark.regression
@pytest.mark.authentication
def test_login():
    # Инициализация клиентов
    public_users_client = get_public_users_client()
    authentication_client = get_authentication_client()

    # Создание пользователя
    request = CreateUserRequestSchema()
    public_users_client.create_user_api(request)

    # Аутентификация
    login_response = authentication_client.login_api(request)

    # Проверка статус-кода
    assert_status_code(login_response.status_code, HTTPStatus.OK)

    # Десериализация ответа
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    # Проверка содержимого ответа
    assert_login_response(login_response_data)

    # Валидация JSON schema
    validate_json_schema(login_response.json(), login_response_data.model_json_schema())
