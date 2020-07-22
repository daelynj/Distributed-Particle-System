import time, grpc
from concurrent import futures

from particle import Emitter, smoke_machine

import proto.particle_system_pb2 as ps
import proto.particle_system_pb2_grpc as rpc

class Server(rpc.GenerateServicer):
  def GenerateParticles(self, request, context):

    emitter = Emitter((100, 100))
    emitter.add_factory(smoke_machine())

    for i in range(request.frame_count):
      emitter.update()

      particles = map(self.encode_grpc, emitter.particles)

      frame = ps.Frame()
      frame.index = i
      frame.particles.extend(particles)

      yield frame

  @staticmethod
  def encode_grpc(particle):
    p = ps.Particle()
    
    p.x = particle.x
    p.y = particle.y
    p.size = particle.size
    p.color = particle.color

    return p 

if __name__ == '__main__':
  port = 50051
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
  rpc.add_GenerateServicer_to_server(Server(), server)
  server.add_insecure_port('[::]:' + str(port))

  server.start()
  server.wait_for_termination()
