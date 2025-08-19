import grpc
from concurrent import futures

import course_service_pb2 as pb2
import course_service_pb2_grpc as pb2_grpc


class CourseService(pb2_grpc.CourseServiceServicer):
    def GetCourse(self, request, context):
        return pb2.GetCourseResponse(
            course_id=request.course_id,
            title="Автотесты API",
            description="Будем изучать написание API автотестов",
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # ВАЖНО: регистрируем нашу реализацию CourseService(), а не базовый Servicer
    pb2_grpc.add_CourseServiceServicer_to_server(CourseService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC сервер запущен на порту 50051…")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()