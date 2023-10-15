from grpc import StatusCode
from pyqrllib.pyqrllib import bin2hstr

from nyankocoin.core import config
from nyankocoin.core.nyankocoinnode import NyankoCoinNode
from nyankocoin.crypto.Qryptonight import Qryptonight
from nyankocoin.generated import nyankocoinmining_pb2
from nyankocoin.generated.nyankocoinmining_pb2_grpc import MiningAPIServicer
from nyankocoin.services.grpcHelper import GrpcExceptionWrapper


class MiningAPIService(MiningAPIServicer):
    MAX_REQUEST_QUANTITY = 100

    def __init__(self, nyankocoinnode: NyankoCoinNode):
        self.nyankocoinnode = nyankocoinnode
        self._qn = Qryptonight()

    @GrpcExceptionWrapper(nyankocoinmining_pb2.GetBlockMiningCompatibleResp, StatusCode.UNKNOWN)
    def GetBlockMiningCompatible(self,
                                 request: nyankocoinmining_pb2.GetBlockMiningCompatibleReq,
                                 context) -> nyankocoinmining_pb2.GetBlockMiningCompatibleResp:

        blockheader, block_metadata = self.nyankocoinnode.get_blockheader_and_metadata(request.height)

        response = nyankocoinmining_pb2.GetBlockMiningCompatibleResp()
        if blockheader is not None and block_metadata is not None:
            response = nyankocoinmining_pb2.GetBlockMiningCompatibleResp(
                blockheader=blockheader.pbdata,
                blockmetadata=block_metadata.pbdata)

        return response

    @GrpcExceptionWrapper(nyankocoinmining_pb2.GetLastBlockHeaderResp, StatusCode.UNKNOWN)
    def GetLastBlockHeader(self,
                           request: nyankocoinmining_pb2.GetLastBlockHeaderReq,
                           context) -> nyankocoinmining_pb2.GetLastBlockHeaderResp:
        response = nyankocoinmining_pb2.GetLastBlockHeaderResp()

        blockheader, block_metadata = self.nyankocoinnode.get_blockheader_and_metadata(request.height)

        response.difficulty = int(bin2hstr(block_metadata.block_difficulty), 16)
        response.height = blockheader.block_number
        response.timestamp = blockheader.timestamp
        response.reward = blockheader.block_reward + blockheader.fee_reward
        response.hash = bin2hstr(blockheader.headerhash)
        response.depth = self.nyankocoinnode.block_height - blockheader.block_number

        return response

    @GrpcExceptionWrapper(nyankocoinmining_pb2.GetBlockToMineResp, StatusCode.UNKNOWN)
    def GetBlockToMine(self,
                       request: nyankocoinmining_pb2.GetBlockToMineReq,
                       context) -> nyankocoinmining_pb2.GetBlockToMineResp:

        response = nyankocoinmining_pb2.GetBlockToMineResp()

        blocktemplate_blob_and_difficulty = self.nyankocoinnode.get_block_to_mine(request.wallet_address)

        if blocktemplate_blob_and_difficulty:
            response.blocktemplate_blob = blocktemplate_blob_and_difficulty[0]
            response.difficulty = blocktemplate_blob_and_difficulty[1]
            response.height = self.nyankocoinnode.block_height + 1
            response.reserved_offset = config.dev.extra_nonce_offset
            seed_block_number = self._qn.get_seed_height(response.height)
            response.seed_hash = bin2hstr(self.nyankocoinnode.get_block_header_hash_by_number(seed_block_number))

        return response

    @GrpcExceptionWrapper(nyankocoinmining_pb2.GetBlockToMineResp, StatusCode.UNKNOWN)
    def SubmitMinedBlock(self,
                         request: nyankocoinmining_pb2.SubmitMinedBlockReq,
                         context) -> nyankocoinmining_pb2.SubmitMinedBlockResp:
        response = nyankocoinmining_pb2.SubmitMinedBlockResp()

        response.error = not self.nyankocoinnode.submit_mined_block(request.blob)

        return response
