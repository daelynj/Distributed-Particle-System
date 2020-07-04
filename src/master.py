import grpc
from concurrent import futures
import time
import simulator_pb2
import simulator_pb2_grpc
import simulator


class SimulatorServicer(simulator_pb2_grpc.SimulatorServicer):
    def SquareRoot(self, request, context):
        response = simulator_pb2.Number()
        response.value = simulator.square_root(request.value)
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
