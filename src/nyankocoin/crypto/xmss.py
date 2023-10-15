from pyqrllib import pyqrllib
from pyqrllib.pyqrllib import bin2hstr, getRandomSeed, str2bin, bin2mnemonic, mnemonic2bin  # noqa
from pyqrllib.pyqrllib import XmssFast, QRLDescriptor

hash_functions = {
    "shake128": pyqrllib.SHAKE_128,
    "shake256": pyqrllib.SHAKE_256,
    "sha2_256": pyqrllib.SHA2_256
}
hash_functions_reverse = {v: k for k, v in hash_functions.items()}


class XMSS(object):
    @staticmethod
    def from_extended_seed(extended_seed: bytes):
        if len(extended_seed) != 51:
            raise Exception('Extended seed should be 51 bytes long')

        descr = QRLDescriptor.fromBytes(extended_seed[0:3])
        if descr.getSignatureType() != pyqrllib.XMSS:
            raise Exception('Signature type nor supported')

        height = descr.getHeight()
        hash_function = descr.getHashFunction()
        tmp = XmssFast(extended_seed[3:], height, hash_function)
        return XMSS(tmp)

    @staticmethod
    def from_height(tree_height: int, hash_function="shake128"):
        if hash_function not in hash_functions:
            raise Exception("XMSS does not support this hash function!")

        seed = getRandomSeed(48, '')
        return XMSS(XmssFast(seed, tree_height, hash_functions[hash_function]))

    def __init__(self, _xmssfast):
        self._xmss = _xmssfast

    @property
    def hash_function(self) -> str:
        descr = self._xmss.getDescriptor()
        function_num = descr.getHashFunction()
        function_name = hash_functions_reverse[function_num]
        if not function_name:
            raise Exception("Could not reverse-lookup the hash function")

        return function_name

    @property
    def signature_type(self):
        descr = self._xmss.getDescriptor()
        answer = descr.getSignatureType()
        return answer

    @property
    def height(self):
        return self._xmss.getHeight()

    @property
    def _sk(self):
        return bytes(self._xmss.getSK())

    @property
    def pk(self):
        return bytes(self._xmss.getPK())

    @property
    def number_signatures(self) -> int:
        return self._xmss.getNumberSignatures()

    @property
    def remaining_signatures(self):
        return self._xmss.getRemainingSignatures()

    @property
    def mnemonic(self) -> str:
        return bin2mnemonic(self._xmss.getExtendedSeed())

    @property
    def address(self) -> bytes:
        return bytes(self._xmss.getAddress())

    @property
    def qaddress(self) -> str:
        return 'Q' + bin2hstr(self.address)

    @property
    def ots_index(self) -> int:
        return self._xmss.getIndex()

    def set_ots_index(self, new_index):
        self._xmss.setIndex(new_index)

    @property
    def hexseed(self) -> str:
        return bin2hstr(self._xmss.getExtendedSeed())

    @property
    def extended_seed(self):
        return self._xmss.getExtendedSeed()

    @property
    def seed(self):
        return self._xmss.getSeed()

    def sign(self, message: bytes) -> bytes:
        return bytes(self._xmss.sign(message))

    @staticmethod
    def get_height_from_sig_size(sig_size: int) -> int:
        min_size = 4 + 32 + 67 * 32

        if sig_size < min_size:
            raise Exception("Invalid Signature Size")

        if (sig_size - 4) % 32 != 0:
            raise Exception("Invalid Signature Size")

        height = (sig_size - min_size) // 32

        return height

    @staticmethod
    def validate_signature(signature, PK):
        height = XMSS.get_height_from_sig_size(len(signature))

        if height == 0 or 2 * int(bin2hstr(PK)[2:4]) != height:
            return False

        return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
