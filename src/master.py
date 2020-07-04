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


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_SimulatorServicer_to_server`
# to add the defined class to the created server
simulator_pb2_grpc.add_SimulatorServicer_to_server(SimulatorServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
  while True:
    time.sleep(86400)
except KeyboardInterrupt:
  server.stop(0)