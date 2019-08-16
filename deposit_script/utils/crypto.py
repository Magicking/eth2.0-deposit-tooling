from hashlib import (
    sha256 as _sha256,
    sha512 as _sha512,
)
import hmac
from Crypto.Hash import keccak as _keccak
from Crypto.Cipher import AES as _AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import (
    scrypt as _scrypt,
    PBKDF2 as _PBKDF2,
    HKDF as _HKDF,
)
from typing import Union

_hash_func = _sha256  # Declared once to ensure future uses use correct version


def hash(x):
    return _hash_func(x).digest()


def sha256(x):
    return _sha256(x).digest()


def sha512(x):
    return _sha512(x).digest()


hash_func_bytes = _hash_func().digest_size


def keccak(x):
    return _keccak.new(digest_bits=256).update(x).digest()


def num_bits_to_num_bytes(x: int) -> int:
    return -(-x // 8)


def scrypt(*, password: str, salt: str, n: int, r: int, p: int, dklen: int) -> bytes:
    res = _scrypt(password=password, salt=salt, key_len=dklen, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, password: bytes, salt: bytes, iters: int=2048) -> bytes:
    return _PBKDF2(
        password=bytes.decode(password),
        salt=salt,
        dkLen=64,
        count=iters,
        prf=lambda p, s: hmac_sha512(key=p, msg=s),
    )


def hkdf(*, ikm: bytes, key_len: int, salt: str) -> bytes:
    res = _HKDF(master=ikm, key_len=key_len, salt=salt, hashmod=_sha256)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES(*, key: bytes, secret, iv: Union[bytes, str]) -> bytes:
    iv_hex = iv.hex() if isinstance(iv, bytes) else iv
    counter = Counter.new(128, initial_value=int(iv_hex, 16))
    aes = _AES.new(key=key, mode=_AES.MODE_CTR, counter=counter)
    return aes.encrypt(secret)


def hmac_sha512(*, key: bytes, msg) -> bytes:
    return hmac.new(key=key, msg=msg, digestmod=_sha512).digest()
