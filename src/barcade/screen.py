class Screen:
    def __init__(self):
        self._width = 64
        self._height = 4
        n_pxl = self._width * self._height

        assert n_pxl % 8 == 0
        self._screen = bytearray(b"\x00" * (n_pxl // 8))

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def _resolve_index(self, x, y):
        if x < 0:
            x += self._width

        if y < 0:
            y += self._height

        if not (0 <= x < self._width and 0 <= y < self._height):
            raise IndexError(f"Pixel index ({x}, {y}) out of range")

        bit_index = x * self._height + y
        byte_index = bit_index // 8
        bit_offset = bit_index % 8

        return byte_index, bit_offset

    def set(self, x, y):
        byte_index, bit_offset = self._resolve_index(x, y)
        self._screen[byte_index] |= 1 << bit_offset

    def unset(self, x, y):
        byte_index, bit_offset = self._resolve_index(x, y)
        self._screen[byte_index] &= ~(1 << bit_offset)

    def get(self, x, y):
        byte_index, bit_offset = self._resolve_index(x, y)
        return bool(self._screen[byte_index] & (1 << bit_offset))

    def serialize(self):
        return bytes(self._screen)

    @staticmethod
    def deserialize(data):
        screen = Screen()
        if len(data) != len(screen._screen):
            raise ValueError(
                f"Invalid data length: {len(data)} != {len(screen._screen)}"
            )

        screen._screen = bytearray(data)
        return screen
