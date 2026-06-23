import hashlib
import struct
import base64


class Ladon:
    """Generate TikTok X-Ladon signature."""

    @staticmethod
    def encrypt(unix: int, license_id: int, aid: int) -> str:
        raw = bytearray()
        raw += struct.pack("<I", unix)
        raw += struct.pack("<I", license_id)
        raw += struct.pack("<I", aid)

        sign_hash = hashlib.sha1(raw).digest()
        return base64.b64encode(sign_hash).decode("utf-8")
