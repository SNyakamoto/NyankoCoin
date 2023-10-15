from nyankocoin.core import config
from nyankocoin.core.nyankocoinnode import NyankoCoinNode
from nyankocoin.generated import nyankocoindebug_pb2
from nyankocoin.generated.nyankocoindebug_pb2_grpc import DebugAPIServicer
from nyankocoin.services.grpcHelper import GrpcExceptionWrapper


class DebugAPIService(DebugAPIServicer):
    MAX_REQUEST_QUANTITY = 100

    def __init__(self, nyankocoinnode: NyankoCoinNode):
        self.nyankocoinnode = nyankocoinnode

    @GrpcExceptionWrapper(nyankocoindebug_pb2.GetFullStateResp)
    def GetFullState(self, request: nyankocoindebug_pb2.GetFullStateReq, context) -> nyankocoindebug_pb2.GetFullStateResp:
        return nyankocoindebug_pb2.GetFullStateResp(
            coinbase_state=self.nyankocoinnode.get_address_state(config.dev.coinbase_address).pbdata,
            addresses_state=self.nyankocoinnode.get_all_address_state()
        )