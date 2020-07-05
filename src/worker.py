import time
import grpc
import simulator_pb2
import simulator_pb2_grpc
from file_service import FileService

FILE_SERVICE = FileService()


def get_task(stub):
    request = simulator_pb2.NextTaskInformation()
    return stub.GetTask(request)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = simulator_pb2_grpc.SimulatorStub(channel)
        task = get_task(stub)

        file = FILE_SERVICE.generate_file(task.id)

        FILE_SERVICE.append_particle_position(file, 1, 2)
        FILE_SERVICE.append_particle_position(file, 3, 4)


if __name__ == '__main__':
    run()
