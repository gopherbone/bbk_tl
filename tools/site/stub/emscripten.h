#pragma once
#include <stdlib.h>
#define EMSCRIPTEN_KEEPALIVE
static inline void emscripten_force_exit(int s){ exit(100+s); }
#define EM_ASM(...) ((void)0)
