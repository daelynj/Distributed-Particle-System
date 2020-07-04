# Distributed-Particle-System

To install dependencies from the root directory:
`pip install -r requirements.txt`

To run tests from the root directory:
`python -m pytest`

To run the application from the root directory:
`python src/master.py`

Then in a separate terminal run:
`python src/worker.py`

To update the proto and `_pb2` modules from the root directory run:

`python3 -m grpc_tools.protoc -I.src/protos --python_out=src/ --grpc_python_out=src/ src/protos/simulator.proto`
