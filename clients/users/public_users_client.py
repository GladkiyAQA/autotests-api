from typing import TypedDict
import httpx

from clients.api_client import APIClient


class UserCreateRequest(TypedDict):
    """
    Структура тела запроса для создания пользователя.

    Обязательные поля:
        email (str): Электронная почта пользователя.
        password (str): Пароль.
        lastName (str): Фамилия.
        firstName (str): Имя.
        middleName (str): Отчество.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    Клиент для публичных методов Users API, не требующих авторизации.

    Предназначен для вызова эндпоинтов `/api/v1/users`, для регистрации нового пользователя.
    """

    def create_user_api(self, request: UserCreateRequest) -> httpx.Response:
        """
        Создать пользователя через публичный эндпоинт.

        Выполняет POST-запрос к `/api/v1/users` с переданным телом запроса.

        Args:
            request (UserCreateRequest):
                Словарь с обязательными полями:
                    - email (str): Электронная почта.
                    - password (str): Пароль.
                    - lastName (str): Фамилия.
                    - firstName (str): Имя.
                    - middleName (str): Отчество.

        Returns:
            httpx.Response: HTTP-ответ сервера.
                - 200: Успешное создание пользователя (JSON с данными пользователя).
                - 422: Ошибка валидации (JSON с detail).
        """
        return self.post("/api/v1/users", json=request)
