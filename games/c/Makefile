all: snake.wasm

snake.wasm: snake.c
	clang \
	-O3 \
	-Wall -Wextra -Werror \
	--target=wasm32 -nostdlib \
	-Wl,--no-entry \
	-Wl,--export=tick \
	-Wl,--export=add_action \
	-Wl,--export=set_rng_state \
	-Wl,--export=score \
	-Wl,--export=screen \
	-Wl,--export-memory \
	-o $@ $<

clean:
	rm -f snake.wasm
