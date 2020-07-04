import grpc

# import the generated classes
import simulator_pb2
import simulator_pb2_grpc


def simulate_square_root(stub, value):
    number = simulator_pb2.Number(value=16)
    response = stub.SquareRoot(number)
    print(response.value)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = simulator_pb2_grpc.SimulatorStub(channel)
    simulate_square_root(stub, 16)


if __name__ == '__main__':
    run()
