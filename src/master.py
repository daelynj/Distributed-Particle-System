import grpc
from concurrent import futures
import time

# import the generated classes
import simulator_pb2
import simulator_pb2_grpc

# import the original simulator.py
import simulator

# create a class to define the server functions
# derived from simulator_pb2_grpc.SimulatorServicer


class SimulatorServicer(simulator_pb2_grpc.SimulatorServicer):

    # simulator.square_root is exposed here
    # the request and response are of the data types
    # generated as simulator_pb2.Number
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
