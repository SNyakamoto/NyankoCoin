import sys

import os
from grpc._cython.cygrpc import StatusCode

from nyankocoin.core.nyankocoinnode import NyankoCoinNode
from nyankocoin.generated.nyankocoinbase_pb2 import GetNodeInfoReq, GetNodeInfoResp
from nyankocoin.generated.nyankocoinbase_pb2_grpc import BaseServicer


class BaseService(BaseServicer):
    def __init__(self, nyankocoinnode: NyankoCoinNode):
        self.nyankocoinnode = nyankocoinnode

    def GetNodeInfo(self, request: GetNodeInfoReq, context) -> GetNodeInfoResp:
        try:
            resp = GetNodeInfoResp()
            resp.version = self.nyankocoinnode.version

            pkgdir = os.path.dirname(sys.modules['nyankocoin'].__file__)
            grpcprotopath = os.path.join(pkgdir, "protos", "nyankocoin.proto")
            with open(grpcprotopath, 'r') as infile:
                resp.grpcProto = infile.read()

            return resp
        except Exception as e:
            context.set_code(StatusCode.unknown)
            context.set_details(e)
            return GetNodeInfoResp()
