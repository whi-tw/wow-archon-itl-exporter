import base64


def string_byte(s, i: int = 1, j: int | None = None) -> list[int] | int | None:
    i = i - 1
    if j is None:
        j = i
    else:
        j = j - 1
    ords = [ord(c) for c in s[i : j + 1]]
    if len(ords) == 1:
        return ords[0]
    else:
        return ords


_byte_to_6bit_char = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "(",
    ")",
]

_6bit_to_byte = {
    97: 0,
    98: 1,
    99: 2,
    100: 3,
    101: 4,
    102: 5,
    103: 6,
    104: 7,
    105: 8,
    106: 9,
    107: 10,
    108: 11,
    109: 12,
    110: 13,
    111: 14,
    112: 15,
    113: 16,
    114: 17,
    115: 18,
    116: 19,
    117: 20,
    118: 21,
    119: 22,
    120: 23,
    121: 24,
    122: 25,
    65: 26,
    66: 27,
    67: 28,
    68: 29,
    69: 30,
    70: 31,
    71: 32,
    72: 33,
    73: 34,
    74: 35,
    75: 36,
    76: 37,
    77: 38,
    78: 39,
    79: 40,
    80: 41,
    81: 42,
    82: 43,
    83: 44,
    84: 45,
    85: 46,
    86: 47,
    87: 48,
    88: 49,
    89: 50,
    90: 51,
    48: 52,
    49: 53,
    50: 54,
    51: 55,
    52: 56,
    53: 57,
    54: 58,
    55: 59,
    56: 60,
    57: 61,
    40: 62,
    41: 63,
}


def EncodeForPrint(s: str) -> str:
    strlen = len(s)
    strlenMinus2 = strlen - 2
    i = 1
    buffer = {}
    buffer_size = 0
    while i <= strlenMinus2:
        x1, x2, x3 = string_byte(s, i, i + 2)
        i += 3
        cache = x1 + x2 * 256 + x3 * 65536
        b1 = int(cache % 64)
        cache = (cache - b1) / 64
        b2 = int(cache % 64)
        cache = (cache - b2) / 64
        b3 = int(cache % 64)
        b4 = int((cache - b3) / 64)
        buffer_size = buffer_size + 1
        buffer[buffer_size] = (
            _byte_to_6bit_char[b1]
            + _byte_to_6bit_char[b2]
            + _byte_to_6bit_char[b3]
            + _byte_to_6bit_char[b4]
        )

    cache = 0
    cache_bitlen = 0
    while i <= strlen:
        x = string_byte(s, i, i)
        cache = cache + x * 2**cache_bitlen
        cache_bitlen = cache_bitlen + 8
        i = i + 1

    while cache_bitlen > 0:
        bit6 = int(cache % 64)
        buffer_size = buffer_size + 1
        buffer[buffer_size] = _byte_to_6bit_char[bit6]
        cache = (cache - bit6) / 64
        cache_bitlen = cache_bitlen - 6

    return "".join(buffer[i] for i in range(1, buffer_size + 1))


def DecodeForPrint(s: str) -> str:
    strlen = len(s)
    if strlen == 1:
        return None
    strlenMinus3 = strlen - 3
    i = 1
    buffer = {}
    buffer_size = 0
    while i <= strlenMinus3:
        x1, x2, x3, x4 = string_byte(s, i, i + 3)
        x1 = _6bit_to_byte[x1]
        x2 = _6bit_to_byte[x2]
        x3 = _6bit_to_byte[x3]
        x4 = _6bit_to_byte[x4]
        if x1 is None or x2 is None or x3 is None or x4 is None:
            return None
        i = i + 4
        cache = x1 + x2 * 64 + x3 * 4096 + x4 * 262144
        b1 = int(cache % 256)
        cache = (cache - b1) / 256
        b2 = int(cache % 256)
        b3 = int((cache - b2) / 256)
        buffer_size += 1
        buffer[buffer_size] = chr(b1) + chr(b2) + chr(b3)

    cache = 0
    cache_bitlen = 0
    while i <= strlen:
        x = string_byte(s, i, i)
        x = _6bit_to_byte[x]
        if x is None:
            return None
        cache = cache + x * 2**cache_bitlen
        cache_bitlen = cache_bitlen + 6
        i = i + 1

    while cache_bitlen >= 8:
        bit8 = int(cache % 256)
        buffer_size = buffer_size + 1
        buffer[buffer_size] = chr(bit8)
        cache = (cache - bit8) / 256
        cache_bitlen = cache_bitlen - 8

    return "".join(buffer[i] for i in range(1, buffer_size + 1))


def DecompressDeflate(s: str) -> str:
    pass


importString = "Jr)uZP8sm3uDkXItjTdLAffKFrLeCjfLzEPxG)ohA2oIdG7zfvUr5BUrLDu5wrKr6Rpv5RVzvsu(Mvu(wv5ajDpPCJYOCJQCOQ2tNYnk3D0OStTsNkj1Il5cm6uiaPa8"

decoded = DecodeForPrint(importString)
print(decoded.encode())
print(base64.b64encode(decoded.encode()))
# encoded = EncodeForPrint(decoded)
# print(encoded)

# encoded = EncodeForPrint("Hello World!")
# decoded = DecodeForPrint(encoded)
# print(encoded)
# print(decoded)
# print(encoded)
# print(decoded)
