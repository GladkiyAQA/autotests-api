from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import get_random_email


# 1. Создание пользователя
public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
create_user_response = public_users_client.create_user(create_user_request)
print("User created:", create_user_response)

# 2. Аутентификация
auth_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)

# 3. Инициализация клиентов
files_client = get_files_client(auth_user)
courses_client = get_courses_client(auth_user)

# 4. Загрузка файла
create_file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print("File uploaded:", create_file_response)

# 5. Создание курса
create_course_request = CreateCourseRequestSchema(
    title="Python",
    max_score=100,
    min_score=10,
    description="Python API course",
    estimated_time="2 weeks",
    preview_file_id=create_file_response.file.id,       # snake_case
    created_by_user_id=create_user_response.user.id     # snake_case
)

create_course_response = courses_client.create_course(create_course_request)
print("Course created:", create_course_response)
