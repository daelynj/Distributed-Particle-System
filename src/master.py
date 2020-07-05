import time
from concurrent import futures
import grpc


import simulator_pb2
import simulator_pb2_grpc
import simulator

WORKER_COUNT = 0


class SimulatorServicer(simulator_pb2_grpc.SimulatorServicer):
    def GetTask(self, request, context):
        global WORKER_COUNT
        response = simulator_pb2.NextTaskInformation()
        WORKER_COUNT = simulator.get_new_worker_id(WORKER_COUNT)
        response.id = WORKER_COUNT

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simulator_pb2_grpc.add_SimulatorServicer_to_server(
        SimulatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
