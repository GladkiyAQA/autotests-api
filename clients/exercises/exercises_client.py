from typing import TypedDict
from httpx import Response

from clients.api_client import APIClient


class GetExercisesQueryDict(TypedDict):
    """
    Структура query-параметров для получения списка заданий курса.

    Атрибуты:
        courseId: Идентификатор курса, для которого запрашиваются задания.
    """
    courseId: str


class CreateExerciseRequestDict(TypedDict):
    """
    Структура тела запроса на создание задания.

    Атрибуты:
        courseId: Идентификатор курса, к которому относится задание.
        title: Название задания.
        description: Описание задания.
        maxScore: Максимальный балл за выполнение.
        minScore: Минимальный проходной балл (если используется).
        estimatedTime: Оценочное время выполнения (например, '30m', '1h').
        createdByUserId: Идентификатор пользователя-автора.
    """
    courseId: str
    title: str
    description: str
    maxScore: int
    minScore: int
    estimatedTime: str
    createdByUserId: str


class UpdateExerciseRequestDict(TypedDict):
    """
    Структура тела запроса на частичное обновление задания.

    Примечание:
        Все поля опциональны: передавай только то, что нужно изменить.
        Используем `| None`, чтобы явно разрешить передачу пустых значений
    """
    title: str | None
    description: str | None
    maxScore: int | None
    minScore: int | None
    estimatedTime: str | None


class ExercisesClient(APIClient):
    """
    Клиент для работы с эндпоинтами /api/v1/exercises.

    Содержит CRUD-методы:
      - get_exercises_api:   GET  /api/v1/exercises
      - get_exercise_api:    GET  /api/v1/exercises/{exercise_id}
      - create_exercise_api: POST /api/v1/exercises
      - update_exercise_api: PATCH /api/v1/exercises/{exercise_id}
      - delete_exercise_api: DELETE /api/v1/exercises/{exercise_id}
    """

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Получить список заданий для заданного курса.

        Args:
            query (GetExercisesQueryDict): Словарь с ключом `courseId`.
        """
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Получить информацию о задании по идентификатору.

        Args:
            exercise_id (str): Идентификатор задания.
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """
        Создать новое задание.

        Args:
            request (CreateExerciseRequestDict): Тело запроса с полями:
                - courseId (str): Идентификатор курса.
                - title (str): Название.
                - description (str): Описание.
                - maxScore (int): Максимальный балл.
                - minScore (int): Минимальный проходной балл.
                - estimatedTime (str): Оценочное время выполнения.
                - createdByUserId (str): Автор.
        """
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """
        Частично обновить данные задания.

        Args:
            exercise_id (str): Идентификатор задания.
            request (UpdateExerciseRequestDict): Любая подмножина полей:
                title, description, maxScore, minScore, estimatedTime.
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Удалить задание.

        Args:
            exercise_id (str): Идентификатор задания.
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")
