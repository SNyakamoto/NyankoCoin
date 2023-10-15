from nyankocoin.generated import nyankocoinlegacy_pb2


class P2PBaseObserver(object):
    def __init__(self):
        pass

    @staticmethod
    def _validate_message(message: nyankocoinlegacy_pb2.LegacyMessage, expected_func_name):
        if message.func_name != expected_func_name:
            raise ValueError("Invalid func_name")

    def new_channel(self, channel):
        pass
