import time
import grpc
import simulator_pb2
import simulator_pb2_grpc
from file_service import FileService

from particle import Emitter, smoke_machine

FILE_SERVICE = FileService()


def build_particles(particle_count):
    e = Emitter((100, 100))
    e.add_factory(smoke_machine(), particle_count)

    for i in range(10):
        e.update()

    return e.particles


def get_task(stub):
    request = simulator_pb2.NextTaskInformation()
    return stub.GetTask(request)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = simulator_pb2_grpc.SimulatorStub(channel)
        task = get_task(stub)
        particle_count = 1000

        file = FILE_SERVICE.generate_file(task.id)

        particles = build_particles(particle_count)

        FILE_SERVICE.append_particle_data(file, particles)


if __name__ == '__main__':
    run()
