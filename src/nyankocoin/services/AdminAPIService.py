from nyankocoin.core.nyankocoinnode import nyankocoinNode
from nyankocoin.generated.nyankocoin_pb2_grpc import AdminAPIServicer


class AdminAPIService(AdminAPIServicer):
    
    def __init__(self, nyankocoinnode: NyankoCoinNode):
        self.nyankocoinnode = nyankocoinnode
