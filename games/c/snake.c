#include <stdint.h>

#undef abs
#define abs(x) ((x) < 0 ? -(x) : (x))

#define WIDTH 64
#define HEIGHT 4
#define PIXELS (WIDTH * HEIGHT)
#define TICK_FREQUENCY 4
#define RNG_SEED 0x12345678U

uint32_t screen[PIXELS / 32] = {0x22U, 0U, 0U, 0U, 0U, 0U, 0U, 0U};
int32_t score = 2;

int32_t tick(float t);
int32_t add_action(int32_t scancode);
void set_rng_state(uint32_t seed);

static int32_t alive = 1;
static float ticks = 0.0F;
static int32_t head = 1;
static uint8_t snake[PIXELS] = {1, 5};
static int32_t v = HEIGHT;
static int32_t action = -1;
static int32_t apple = -1;
static uint32_t rng_state = RNG_SEED;

enum
{
    SCANCODE_W = 26,
    SCANCODE_S = 22,
    SCANCODE_A = 4,
    SCANCODE_D = 7,
    SCANCODE_UP = 82,
    SCANCODE_DOWN = 81,
    SCANCODE_LEFT = 80,
    SCANCODE_RIGHT = 79
};

enum
{
    KEY_UP,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT,
};

static uint32_t rng_next(uint32_t state)
{
    return 1664525U * state + 1013904223U;
}

static void screen_set(int32_t idx)
{
    screen[idx / 32] |= (1u << (idx % 32));
}

static void screen_unset(int32_t idx)
{
    screen[idx / 32] &= ~(1u << (idx % 32));
}

static int32_t handle_action(int32_t action)
{
    switch (action)
    {
    case KEY_UP:
        if (v != -1)
        {
            return 1;
        }
        break;
    case KEY_DOWN:
        if (v != 1)
        {
            return -1;
        }
        break;
    case KEY_LEFT:
        if (v != HEIGHT)
        {
            return -HEIGHT;
        }
        break;
    case KEY_RIGHT:
        if (v != -HEIGHT)
        {
            return HEIGHT;
        }
        break;
    default:
        break;
    }

    return v;
}

static int32_t advance(int32_t idx, int32_t v)
{
    const int32_t x = idx / HEIGHT + (abs(v) == HEIGHT) * v / HEIGHT;
    const int32_t y = idx % HEIGHT + (abs(v) == 1) * v;

    return ((x + WIDTH) % WIDTH) * HEIGHT + (y + HEIGHT) % HEIGHT;
}

static int32_t distance(int32_t a, int32_t b)
{
    int32_t dx = abs(a / HEIGHT - b / HEIGHT);
    int32_t dy = abs(a % HEIGHT - b % HEIGHT);
    dx = (dx < (WIDTH - dx)) ? dx : (WIDTH - dx);
    dy = (dy < (HEIGHT - dy)) ? dy : (HEIGHT - dy);

    return (dx > dy) ? dx : dy;
}

static int32_t try_spawn_apple(void)
{
    rng_state = rng_next(rng_state);
    apple = (int)(rng_state % PIXELS);

    for (int32_t i = 0; i < score; i++)
    {
        if (distance(snake[(head - i + PIXELS) % PIXELS], apple) < 2)
        {
            apple = -1;
            return -1;
        }
    }

    screen_set(apple);

    return 1;
}

int32_t tick(float t)
{
    if (alive < 0 || (t - ticks) < 1.0F / TICK_FREQUENCY)
    {
        return alive;
    }

    ticks = t;

    v = handle_action(action);
    action = -1;

    const int32_t next = advance(snake[head], v);
    if (next == apple)
    {
        apple = -1;
        score += 1;
    }
    else
    {
        screen_unset(snake[(head - score + 1 + PIXELS) % PIXELS]);
        screen_set(next);
    }

    head = (head + 1) % PIXELS;
    snake[head] = next;

    for (int32_t i = 1; i < score; i++)
    {
        if (snake[(head - i + PIXELS) % PIXELS] == next)
        {
            {
                alive = -1;
                return alive;
            }
        }
    }

    if (apple < 0)
    {
        try_spawn_apple();
    }

    return alive;
}

int32_t add_action(int32_t scancode)
{
    if (action >= 0)
    {
        return -1;
    }

    switch (scancode)
    {
    case SCANCODE_W:
    case SCANCODE_UP:
        action = KEY_UP;
        break;
    case SCANCODE_S:
    case SCANCODE_DOWN:
        action = KEY_DOWN;
        break;
    case SCANCODE_A:
    case SCANCODE_LEFT:
        action = KEY_LEFT;
        break;
    case SCANCODE_D:
    case SCANCODE_RIGHT:
        action = KEY_RIGHT;
        break;
    default:
        break;
    }

    return 1;
}

void set_rng_state(uint32_t seed)
{
    rng_state = seed;
}
