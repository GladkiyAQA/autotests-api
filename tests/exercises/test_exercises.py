from http import HTTPStatus
import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.exercises import assert_create_exercise_response


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
