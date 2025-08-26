from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    ExerciseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
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

def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные (ExerciseSchema).
    :param expected: Ожидаемые данные (ExerciseSchema).
    :raises AssertionError: Если данные не совпадают.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение задания соответствует ответу на его создание.

    :param get_exercise_response: Ответ API при GET-запросе задания.
    :param create_exercise_response: Ответ API при создании задания.
    :raises AssertionError: Если данные не совпадают.
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)

def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
):
    """
    Проверяет, что ответ на обновление задания соответствует данным из запроса.

    :param request: Объект запроса на обновление задания.
    :param response: Ответ API при обновлении задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    exercise = response.exercise

    assert_equal(exercise.title, request.title, "title")
    assert_equal(exercise.description, request.description, "description")
    assert_equal(exercise.max_score, request.max_score, "max_score")
    assert_equal(exercise.min_score, request.min_score, "min_score")
    assert_equal(exercise.estimated_time, request.estimated_time, "estimated_time")
