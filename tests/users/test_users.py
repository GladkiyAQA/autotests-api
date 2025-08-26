from http import HTTPStatus

import pytest

from clients.errors_schema import ValidationErrorResponseSchema
from clients.files.files_client import FilesClient
from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.files import assert_get_file_with_incorrect_file_id_response
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
class TestUsers:
    @pytest.mark.parametrize("email", ["mail.ru", "gmail.com", "example.com"])
    def test_create_user(self, email: str, public_users_client: PublicUsersClient):
        request = CreateUserRequestSchema(email=fake.email(domain=email))
        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_user_me(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient
    ):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient):
        """
        Проверяет, что при запросе файла с некорректным UUID API
        возвращает ошибку 422 и корректное сообщение о валидации.
        """
        # Отправляем запрос с некорректным file_id
        response = files_client.get_file_api("incorrect-file-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код (422 Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

        # Проверяем, что тело ответа соответствует ожидаемому
        assert_get_file_with_incorrect_file_id_response(response_data)

        # Проверяем JSON-схему
        validate_json_schema(response.json(), response_data.model_json_schema())