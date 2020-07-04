import grpc
import time

# import the generated classes
import simulator_pb2
import simulator_pb2_grpc


def get_task(stub):
    request = simulator_pb2.NextTaskInformation()
    return stub.GetTask(request)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = simulator_pb2_grpc.SimulatorStub(channel)
        task = get_task(stub)
        print("Assigned worker ID: " + str(task.id))
        print("Wind variance: " + str(task.wind_variance))
        print("Doing work ...")
        time.sleep(10)


if __name__ == '__main__':
    run()
