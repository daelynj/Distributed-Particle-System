#!/bin/bash
echo "Generating proto grpc files..."
python -m grpc_tools.protoc -I=src/ --python_out=src/ --grpc_python_out=src/ src/proto/particle_system.proto
echo "DONE"