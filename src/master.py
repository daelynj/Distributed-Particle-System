import time
from concurrent import futures
import grpc


import simulator_pb2
import simulator_pb2_grpc
import simulator

WORKER_COUNT = 0
MAX_FRAMES = 4000
FRAMES_REMAINING = MAX_FRAMES
SERVER = None

class SimulatorServicer(simulator_pb2_grpc.SimulatorServicer):
    def InitializeWorker(self, request, context):
        global WORKER_COUNT
        response = simulator_pb2.NewWorkerInformation()
        WORKER_COUNT = simulator.get_new_worker_id(WORKER_COUNT)
        response.id = WORKER_COUNT

        return response

    def GetNewTask(self, request, context):
        global FRAMES_REMAINING
        response = simulator_pb2.NewTaskInformation()

        if (FRAMES_REMAINING <= 0):
            response.work_complete = 1
            return response

        FRAMES_REMAINING -= 1000

        response.frame_count = 1000

        print(f'frames left: {FRAMES_REMAINING}')

        return response


def serve():
    global SERVER
    SERVER = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    simulator_pb2_grpc.add_SimulatorServicer_to_server(
        SimulatorServicer(), SERVER)
    SERVER.add_insecure_port('[::]:50051')
    SERVER.start()
    SERVER.wait_for_termination()


if __name__ == '__main__':
    serve()
