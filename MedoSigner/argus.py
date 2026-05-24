import hashlib
import struct
import base64
import time


class Argus:
    """Generate TikTok X-Argus signature."""

    @staticmethod
    def get_sign(
        params: str,
        x_ss_stub: str = None,
        unix: int = None,
        platform: int = 19,
        aid: int = 567753,
        license_id: int = 1611921764,
        sec_device_id: str = "",
        sdk_version: str = "2.3.1.i18n",
        sdk_version_int: int = 2,
    ) -> str:
        if unix is None:
            unix = int(time.time())

        params_hash = hashlib.md5(params.encode("utf-8")).hexdigest()

        raw = bytearray()
        raw += struct.pack("<I", unix)
        raw += struct.pack("<I", aid)
        raw += struct.pack("<I", license_id)
        raw += struct.pack("<I", platform)
        raw += struct.pack("<I", sdk_version_int)
        raw += bytes.fromhex(params_hash)

        if x_ss_stub:
            raw += bytes.fromhex(x_ss_stub)
        else:
            raw += b"\x00" * 16

        raw += sec_device_id.encode("utf-8")[:16].ljust(16, b"\x00")

        sign_hash = hashlib.sha256(raw).digest()
        return base64.b64encode(sign_hash).decode("utf-8")
