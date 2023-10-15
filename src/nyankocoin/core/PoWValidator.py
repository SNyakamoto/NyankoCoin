from nyankocoin.core import config
from nyankocoin.core.Singleton import Singleton
from nyankocoin.core.miners.qryptonight7.CNv1PoWValidator import CNv1PoWValidator
from nyankocoin.core.miners.qrandomx.QRXPoWValidator import QRXPoWValidator


class PoWValidator(object, metaclass=Singleton):
    def __init__(self):
        self.qryptonight_7_pow_validator = CNv1PoWValidator()
        self.qryptonight_r_pow_validator = QRXPoWValidator()

    def verify_input(self, block_number, seed_height, seed_hash, mining_blob, target):
        if block_number < config.dev.hard_fork_heights[0]:
            return self.qryptonight_7_pow_validator.verify_input(mining_blob, target)
        else:
            return self.qryptonight_r_pow_validator.verify_input(block_number,
                                                                 seed_height,
                                                                 seed_hash,
                                                                 mining_blob,
                                                                 target)
