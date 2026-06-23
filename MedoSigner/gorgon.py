import hashlib


class Gorgon:
    """Generate TikTok X-Gorgon and X-Khronos signatures."""

    def __init__(self, params: str, unix: int, payload: str = None, cookie: str = None):
        self.params = params
        self.unix = unix
        self.payload = payload
        self.cookie = cookie

    def _hash(self, data: str) -> str:
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    def get_value(self) -> dict:
        khronos = str(self.unix)

        params_hash = self._hash(self.params)
        payload_hash = self._hash(self.payload) if self.payload else "00" * 16
        cookie_hash = self._hash(self.cookie) if self.cookie else "00" * 16

        hash_input = params_hash + payload_hash + cookie_hash
        gorgon_hash = hashlib.md5(hash_input.encode("utf-8")).hexdigest()

        gorgon = self._encode(gorgon_hash, khronos)

        return {
            "x-gorgon": gorgon,
            "x-khronos": khronos,
        }

    @staticmethod
    def _encode(gorgon_hash: str, khronos: str) -> str:
        unix_hex = format(int(khronos), "08x")
        hash_bytes = bytes.fromhex(gorgon_hash)
        key_bytes = bytes.fromhex(unix_hex * 4)

        encoded = bytearray(len(hash_bytes))
        for i in range(len(hash_bytes)):
            encoded[i] = hash_bytes[i] ^ key_bytes[i % len(key_bytes)]

        return "0404b0d30000" + encoded.hex()
