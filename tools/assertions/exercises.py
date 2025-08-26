from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from tools.assertions.base import assert_equal


def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на создание задания (exercise) соответствует запросу.

    :param request: Объект запроса на создание задания.
    :param response: Объект ответа API при создании задания.
    :raises AssertionError: Если поля ответа не совпадают с полями запроса.
    """
    exercise = response.exercise

    assert_equal(exercise.course_id, request.course_id, "course_id")
    assert_equal(exercise.title, request.title, "title")
    assert_equal(exercise.description, request.description, "description")
    assert_equal(exercise.max_score, request.max_score, "max_score")
    assert_equal(exercise.min_score, request.min_score, "min_score")
    assert_equal(exercise.estimated_time, request.estimated_time, "estimated_time")
