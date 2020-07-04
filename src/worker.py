import grpc
import time

# import the generated classes
import simulator_pb2
import simulator_pb2_grpc
from file_service import FileService

file_service = FileService()


def get_task(stub):
    request = simulator_pb2.NextTaskInformation()
    return stub.GetTask(request)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        global file

        stub = simulator_pb2_grpc.SimulatorStub(channel)
        task = get_task(stub)

        file = file_service.generate_file(task.id)

        file_service.append_particle_position(file, 1, 2)
        file_service.append_particle_position(file, 3, 4)


if __name__ == '__main__':
    run()
