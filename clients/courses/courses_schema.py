from pydantic import BaseModel, Field, ConfigDict
from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema


class CourseSchema(BaseModel):
    """
    Описание структуры курса (как он возвращается с сервера).
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int | None = Field(default=None, alias="maxScore")
    min_score: int | None = Field(default=None, alias="minScore")
    description: str
    preview_file: FileSchema = Field(alias="previewFile")
    estimated_time: str | None = Field(default=None, alias="estimatedTime")
    created_by_user: UserSchema = Field(alias="createdByUser")


class GetCoursesQuerySchema(BaseModel):
    """
    Структура query-параметров для получения списка курсов.
    """
    user_id: str = Field(alias="userId")


class CreateCourseRequestSchema(BaseModel):
    """
    Структура запроса на создание курса.
    Здесь сервер ожидает ID-шники, а не вложенные объекты.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    max_score: int | None = Field(default=None, alias="maxScore")
    min_score: int | None = Field(default=None, alias="minScore")
    description: str
    estimated_time: str | None = Field(default=None, alias="estimatedTime")
    preview_file_id: str = Field(alias="previewFileId")       # ✅ только ID
    created_by_user_id: str = Field(alias="createdByUserId")  # ✅ только ID


class CreateCourseResponseSchema(BaseModel):
    """
    Ответ при успешном создании курса.
    """
    course: CourseSchema


class UpdateCourseRequestSchema(BaseModel):
    """
    Структура запроса на обновление курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    max_score: int | None = Field(default=None, alias="maxScore")
    min_score: int | None = Field(default=None, alias="minScore")
    description: str | None = None
    estimated_time: str | None = Field(default=None, alias="estimatedTime")
