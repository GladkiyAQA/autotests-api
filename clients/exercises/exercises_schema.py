from pydantic import BaseModel, Field, ConfigDict

from tools.fakers import fake


class ExerciseSchema(BaseModel):
    """
    Описание структуры задания (как возвращает сервер).
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int | None = Field(default=None, alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class GetExercisesQuerySchema(BaseModel):
    """
    Структура query-параметров для получения списка заданий.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")


class CreateExerciseRequestSchema(BaseModel):
    """
    Запрос на создание задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(alias="courseId", default_factory=fake.uuid4)
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int | None = Field(alias="orderIndex", default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class CreateExerciseResponseSchema(BaseModel):
    """
    Ответ при создании задания.
    """
    exercise: ExerciseSchema


class GetExercisesResponseSchema(BaseModel):
    """
    Ответ при получении списка заданий.
    """
    exercises: list[ExerciseSchema]


class GetExerciseResponseSchema(BaseModel):
    """
    Ответ при получении одного задания.
    """
    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    """
    Запрос на обновление задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default_factory=fake.sentence)
    description: str | None = Field(default_factory=fake.text)
    max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int | None = Field(alias="orderIndex", default_factory=fake.integer)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class UpdateExerciseResponseSchema(BaseModel):
    """
    Ответ при обновлении задания.
    """
    exercise: ExerciseSchema
