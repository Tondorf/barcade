import pathlib

import wasmtime


class WASMGame:
    def __init__(self, wasm_file, seed=0):
        if not pathlib.Path(wasm_file).is_file():
            raise FileNotFoundError(f"File {wasm_file} not found")

        engine = wasmtime.Engine()
        module = wasmtime.Module.from_file(engine, wasm_file)
        self._store = wasmtime.Store(engine)
        instance = wasmtime.Instance(self._store, module, [])
        exports = instance.exports(self._store)

        self._tick = exports["tick"]
        self._add_action = exports["add_action"]
        self._score = exports["score"].value(self._store)

        self._memory = exports["memory"].data_ptr(self._store)
        self._screen = exports["screen"].value(self._store)

        if seed is not None and seed > 0:
            exports["set_rng_state"](self._store, seed)

    def tick(self, t):
        return self._tick(self._store, float(t)) > 0

    def add_action(self, scancode):
        return self._add_action(self._store, scancode) > 0

    @property
    def score(self):
        return int.from_bytes(
            self._memory[self._score : self._score + 4], "little", signed=True
        )

    @property
    def screen(self):
        return bytes(self._memory[self._screen : self._screen + 32])
