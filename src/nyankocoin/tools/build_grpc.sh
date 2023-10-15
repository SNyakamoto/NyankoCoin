#!/usr/bin/env bash
pushd . > /dev/null
cd $( dirname "${BASH_SOURCE[0]}" )
cd ..

python -m grpc_tools.protoc -I=nyankocoin/protos --python_out=nyankocoin/generated --grpc_python_out=nyankocoin/generated nyankocoin/protos/nyankocoin.proto
python -m grpc_tools.protoc -I=nyankocoin/protos/nyankocoin.proto -I=nyankocoin/protos --python_out=nyankocoin/generated --grpc_python_out=nyankocoin/generated nyankocoin/protos/nyankocoinlegacy.proto
python -m grpc_tools.protoc -I=nyankocoin/protos --python_out=nyankocoin/generated --grpc_python_out=nyankocoin/generated nyankocoin/protos/nyankocoinbase.proto
python -m grpc_tools.protoc -I=nyankocoin/protos --python_out=nyankocoin/generated --grpc_python_out=nyankocoin/generated nyankocoin/protos/nyankocoinmining.proto

# Patch import problem in generated code
sed -i 's|import nyankocoin_pb2 as nyankocoin__pb2|import nyankocoin.generated.nyankocoin_pb2 as nyankocoin__pb2|g' nyankocoin/generated/nyankocoin_pb2_grpc.py
sed -i 's|import nyankocoin_pb2 as nyankocoin__pb2|import nyankocoin.generated.nyankocoin_pb2 as nyankocoin__pb2|g' nyankocoin/generated/nyankocoinlegacy_pb2.py
sed -i 's|import nyankocoin_pb2 as nyankocoin__pb2|import nyankocoin.generated.nyankocoin_pb2 as nyankocoin__pb2|g' nyankocoin/generated/nyankocoinmining_pb2.py

sed -i 's|import nyankocoinlegacy_pb2 as nyankocoinlegacy__pb2|import nyankocoin.generated.nyankocoinlegacy_pb2 as nyankocoinlegacy__pb2|g' nyankocoin/generated/nyankocoinlegacy_pb2_grpc.py
sed -i 's|import nyankocoinbase_pb2 as nyankocoinbase__pb2|import nyankocoin.generated.nyankocoinbase_pb2 as nyankocoinbase__pb2|g' nyankocoin/generated/nyankocoinbase_pb2_grpc.py
sed -i 's|import nyankocoinmining_pb2 as nyankocoinmining__pb2|import nyankocoin.generated.nyankocoinmining_pb2 as nyankocoinmining__pb2|g' nyankocoin/generated/nyankocoinmining_pb2_grpc.py

find nyankocoin/generated -name '*.py'|grep -v migrations|xargs autoflake --in-place

#docker run --rm \
#  -v $(pwd)/docs/proto:/out \
#  -v $(pwd)/nyankocoin/protos:/protos \
#  pseudomuto/protoc-gen-doc --doc_opt=markdown,proto.md
#
#docker run --rm \
#  -v $(pwd)/docs/proto:/out \
#  -v $(pwd)/nyankocoin/protos:/protos \
#  pseudomuto/protoc-gen-doc --doc_opt=html,index.html

popd > /dev/null
