import time
import copy
import grpc
import simulator_pb2
import simulator_pb2_grpc
from file_service import FileService

from particle import Emitter, smoke_machine

FILE_SERVICE = FileService()


def build_particles(particle_count):
    e = Emitter((100, 100))
    e.add_factory(smoke_machine())

    history = []
    for i in range(particle_count):
        history.append(f"frame {i}\n")
        e.update()
        history.append(copy.deepcopy(e.particles))
        i += 1

    return history


def get_worker_information(stub):
    request = simulator_pb2.NewWorkerInformation()
    return stub.InitializeWorker(request)


def get_task(stub):
    print("Getting new task")
    request = simulator_pb2.NewTaskInformation()
    return stub.GetNewTask(request)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = simulator_pb2_grpc.SimulatorStub(channel)
        worker_information = get_worker_information(stub)
        task = get_task(stub)

        file = FILE_SERVICE.generate_file(worker_information.id)

        while(task.work_complete != 1):
            particles = build_particles(task.particle_count)

            FILE_SERVICE.append_particle_data(file, particles)

            task = get_task(stub)


if __name__ == '__main__':
    run()
