import time
from concurrent import futures
import grpc


import simulator_pb2
import simulator_pb2_grpc
import simulator

WORKER_COUNT = 0
MAX_PARTICLES = 10000
PARTICLES_LEFT = MAX_PARTICLES


class SimulatorServicer(simulator_pb2_grpc.SimulatorServicer):
    def InitializeWorker(self, request, context):
        global WORKER_COUNT
        response = simulator_pb2.NewWorkerInformation()
        WORKER_COUNT = simulator.get_new_worker_id(WORKER_COUNT)
        response.id = WORKER_COUNT

        return response

    def GetNewTask(self, request, context):
        global PARTICLES_LEFT
        response = simulator_pb2.NewTaskInformation()

        if (PARTICLES_LEFT == 0):
            response.work_complete = 1
            return response

        PARTICLES_LEFT = PARTICLES_LEFT - 1000

        response.particle_count = 1000

        print("particles left: {}".format(PARTICLES_LEFT))

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    simulator_pb2_grpc.add_SimulatorServicer_to_server(
        SimulatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
