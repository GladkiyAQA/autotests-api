from http import HTTPStatus
import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseResponseSchema, UpdateExerciseRequestSchema, GetExercisesResponseSchema, \
    GetExercisesQuerySchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture
    ):
        """
        Проверяет создание задания через API.
        """
        # Формируем запрос с course_id из фикстуры
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)

        # Отправляем запрос
        response = exercises_client.create_exercise_api(request)

        # Десериализация ответа
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем тело ответа
        assert_create_exercise_response(request, response_data)

        # Проверяем JSON-схему
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Проверяет получение задания по его ID через API.
        """
        # Отправляем запрос к эндпоинту /exercises/{exercise_id}
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)

        # Десериализация ответа
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем тело ответа
        assert_get_exercise_response(response_data, function_exercise.response)

        # Проверяем JSON-схему
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Проверяет обновление задания через API.
        """
        # Формируем данные для обновления
        request = UpdateExerciseRequestSchema()

        # Отправляем PATCH-запрос
        response = exercises_client.update_exercise_api(
            function_exercise.response.exercise.id,
            request
        )

        # Десериализация ответа
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        # Проверка статус-кода
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверка тела ответа
        assert_update_exercise_response(request, response_data)

        # Валидация JSON-схемы
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Проверяет удаление задания через API.
        """
        # DELETE-запрос
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)

        # Проверка статус-кода удаления
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # GET-запрос для проверки, что задание удалено
        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # Проверка статус-кода (ожидаем 404 Not Found)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        # Проверка тела ответа на наличие ошибки "Exercise not found"
        assert_exercise_not_found_response(get_response_data)

        # Валидация JSON-схемы ошибки
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    def test_get_exercises(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture,
            function_exercise: ExerciseFixture
    ):
        """
        Проверяет получение списка заданий по course_id через API.
        """
        # Отправляем GET-запрос со значением course_id
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        response = exercises_client.get_exercises_api(query)

        # Десериализация ответа
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        # Проверка статус-кода
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверка списка
        assert_get_exercises_response(response_data, [function_exercise.response])

        # Валидация JSON-схемы
        validate_json_schema(response.json(), response_data.model_json_schema())