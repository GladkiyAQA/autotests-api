import grpc
import course_service_pb2 as pb2
import course_service_pb2_grpc as pb2_grpc


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.CourseServiceStub(channel)
        resp = stub.GetCourse(pb2.GetCourseRequest(course_id="api-course"))
        print(resp)

if __name__ == "__main__":
    main()