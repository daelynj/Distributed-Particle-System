import grpc
from concurrent import futures
import time
import simulator_pb2
import simulator_pb2_grpc
import simulator

worker_count = 0


class SimulatorServicer(simulator_pb2_grpc.SimulatorServicer):
    def GetTask(self, request, context):
        global worker_count
        response = simulator_pb2.NextTaskInformation()
        worker_count = simulator.get_new_worker_id(worker_count)
        response.id = worker_count

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
