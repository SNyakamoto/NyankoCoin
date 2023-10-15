from nyankocoin.core.notification.Observable import Observable
from nyankocoin.generated import nyankocoinlegacy_pb2


class P2PObservable(Observable):
    def __init__(self, source):
        super().__init__(source)

    def notify(self, message: nyankocoinlegacy_pb2.LegacyMessage):
        super().notify(message)
