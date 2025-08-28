from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from config import settings

# ---------- Создание пользователя ----------
public_users_client = get_public_users_client()
create_user_request = CreateUserRequestSchema(
)
create_user_response = public_users_client.create_user(create_user_request)
print("User created:", create_user_response)

# ---------- Авторизация и клиенты ----------
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

# ---------- Загрузка файла ----------
create_file_request = CreateFileRequestSchema(
    upload_file=settings.test_data.image_png_file
)
create_file_response = files_client.create_file(create_file_request)
print("File uploaded:", create_file_response)

# ---------- Создание курса ----------
create_course_request = CreateCourseRequestSchema(
    preview_file_id=create_file_response.file.id,
    created_by_user_id=create_user_response.user.id,
)
create_course_response: CreateCourseResponseSchema = courses_client.create_course(create_course_request)
print("Course created:", create_course_response)

# ---------- Создание задания ----------
create_exercise_request = CreateExerciseRequestSchema(
    course_id=create_course_response.course.id,
    created_by_user_id=create_user_response.user.id
)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print("Exercise created:", create_exercise_response)
