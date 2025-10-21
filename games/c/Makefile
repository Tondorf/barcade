all: snake.wasm

snake.wasm: snake.c
	clang \
	--target=wasm32 \
	-O3 -nostdlib \
	-Wall -Wextra -Werror \
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
