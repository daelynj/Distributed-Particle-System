import grpc

# import the generated classes
import simulator_pb2
import simulator_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = simulator_pb2_grpc.SimulatorStub(channel)

# create a valid request message
number = simulator_pb2.Number(value=16)

# make the call
response = stub.SquareRoot(number)

# et voilà
print(response.value)