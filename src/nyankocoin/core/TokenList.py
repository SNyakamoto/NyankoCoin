from google.protobuf.json_format import MessageToJson, Parse
from nyankocoin.generated import nyankocoin_pb2


class TokenList(object):
    """
    Maintains the list of tokens in the network.
    """
    def __init__(self, protobuf_data=None):
        self._data = protobuf_data
        if protobuf_data is None:
            self._data = nyankocoin_pb2.TokenList()

    @property
    def pbdata(self):
        """
        Returns a protobuf object that contains persistable data representing this object
        :return: A protobuf TokenList object
        :rtype: nyankocoin_pb2.TokenList
        """
        return self._data

    @property
    def token_txhash(self):
        return self._data.token_txhash

    @staticmethod
    def create(token_txhashes: list):
        token_list = TokenList()

        token_list._data.token_txhash.extend(token_txhashes)

        return token_list

    def update(self, token_txhashes: list):
        self.token_txhash.extend(token_txhashes)

    def to_json(self):
        return MessageToJson(self._data, sort_keys=True)

    @staticmethod
    def from_json(json_data):
        pbdata = nyankocoin_pb2.TokenList()
        Parse(json_data, pbdata)
        return TokenList(pbdata)