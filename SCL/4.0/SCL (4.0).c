/*
 * Skibidi v4.0 - "Brainrot & Gooner" Edition
 * Officially harder than Malbodge (probably)
 * 
 * Compile: gcc -o skibidi skibidi_v4.c -lm -lssl -lcrypto
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <time.h>
#include <openssl/md5.h>

#define MEMORY_SIZE 256
#define MAX_PROGRAM 100000
#define STACK_SIZE 1024

/* Complex number */
typedef struct {
    double real;
    double imag;
} Complex;

/* Interpreter state */
typedef struct {
    Complex memory[MEMORY_SIZE];
    int pointer;
    int pitch;
    Complex stack[STACK_SIZE];
    int stack_ptr;
    char** program;
    int program_size;
    int ip;
    int debug;
    char output[100000];
    unsigned char rng_state[16];
    
    /* Evil flags */
    int swapped;
    int spoiled;
    int undefined_behavior;
    
    /* NEW: Brainrot & Gooner */
    int brainrot_count;      /* How many times brainrot called (parity = reversed) */
    int gooner_activated;    /* If true, all ops are "magical white liquid" */
    
    char input_buffer[1024];
    int input_pos;
} Skibidi;

/* Function prototypes */
void complex_zero(Complex* c);
double complex_magnitude(Complex c);
Complex complex_swap(Complex c);
void md5_update(unsigned char* state);
int hash_to_pitch(unsigned char* state);
void skibidi_chaos(Skibidi* s);
void interpreter_init(Skibidi* s, int debug);
int load_program(Skibidi* s, const char* filename);
int expand_macros(const char* input, char* output, int size);
void brainrot(Skibidi* s);
void gooner(Skibidi* s);
void execute(Skibidi* s, const char* op);
void run(Skibidi* s);
void print_debug(Skibidi* s, const char* op);
void free_program(Skibidi* s);

/* Complex math */
double complex_magnitude(Complex c) {
    return sqrt(c.real * c.real + c.imag * c.imag);
}

void complex_zero(Complex* c) {
    c->real = 0.0;
    c->imag = 0.0;
}

Complex complex_swap(Complex c) {
    Complex result;
    result.real = c.imag;
    result.imag = c.real;
    return result;
}

/* MD5 chaos */
void md5_update(unsigned char* state) {
    MD5_CTX ctx;
    unsigned char hash[MD5_DIGEST_LENGTH];
    MD5_Init(&ctx);
    MD5_Update(&ctx, state, 16);
    MD5_Final(hash, &ctx);
    memcpy(state, hash, 16);
}

int hash_to_pitch(unsigned char* state) {
    int val = (state[0] << 24) | (state[1] << 16) | (state[2] << 8) | state[3];
    return 200 + (abs(val) % 600);
}

void skibidi_chaos(Skibidi* s) {
    md5_update(s->rng_state);
    s->pitch = hash_to_pitch(s->rng_state);
}

/* Initialize */
void interpreter_init(Skibidi* s, int debug) {
    memset(s->memory, 0, sizeof(s->memory));
    s->pointer = 0;
    s->pitch = 440;
    memset(s->stack, 0, sizeof(s->stack));
    s->stack_ptr = 0;
    s->program = NULL;
    s->program_size = 0;
    s->ip = 0;
    s->debug = debug;
    memset(s->output, 0, sizeof(s->output));
    memset(s->rng_state, 0, 16);
    s->swapped = 0;
    s->spoiled = 0;
    s->undefined_behavior = 0;
    s->brainrot_count = 0;
    s->gooner_activated = 0;
    memset(s->input_buffer, 0, sizeof(s->input_buffer));
    s->input_pos = 0;
}

/* BRAINROT: Reverse entire program order */
void brainrot(Skibidi* s) {
    if (s->program_size <= 1) return;
    
    /* Reverse the program array */
    for (int i = 0; i < s->program_size / 2; i++) {
        char* temp = s->program[i];
        s->program[i] = s->program[s->program_size - 1 - i];
        s->program[s->program_size - 1 - i] = temp;
    }
    
    s->brainrot_count++;
    s->ip = 0;  /* Reset instruction pointer */
    
    /* Toggle debug mode (stealth) */
    s->debug = !s->debug;
    
    if (s->debug) {
        /* Only print if debug was ON before toggle (now OFF, so this won't show usually) */
        printf("🧠 BRAINROT: Program reversed (count: %d)\n", s->brainrot_count);
    }
}

/* GOONER: Replace every instruction with "magical white liquid" */
void gooner(Skibidi* s) {
    if (s->gooner_activated) return;  /* Already gooned */
    
    /* Free old instructions and replace */
    for (int i = 0; i < s->program_size; i++) {
        free(s->program[i]);
        s->program[i] = strdup("magical white liquid");
    }
    
    s->gooner_activated = 1;
    s->ip = 0;  /* Reset to start of gooned program */
    
    if (s->debug) {
        printf("💦 GOONER: All instructions now 'magical white liquid'\n");
    }
}

/* Macro expansion */
int expand_macros(const char* input, char* output, int size) {
    char temp[MAX_PROGRAM];
    strncpy(temp, input, MAX_PROGRAM - 1);
    temp[MAX_PROGRAM - 1] = '\0';
    
    output[0] = '\0';
    char* token = strtok(temp, " \t\n");
    
    while (token != NULL) {
        int count = 0;
        char opname[32];
        
        if (sscanf(token, "dop(%d)", &count) == 1) {
            strcpy(opname, "dop");
        } else if (sscanf(token, "bop(%d)", &count) == 1) {
            strcpy(opname, "bop");
        } else if (sscanf(token, "67(%d)", &count) == 1) {
            strcpy(opname, "67");
        } else if (sscanf(token, "brainrot(%d)", &count) == 1) {
            strcpy(opname, "brainrot");
        } else if (sscanf(token, "gooner(%d)", &count) == 1) {
            strcpy(opname, "gooner");
        } else {
            strncat(output, token, size - strlen(output) - 1);
            strncat(output, " ", size - strlen(output) - 1);
            token = strtok(NULL, " \t\n");
            continue;
        }
        
        for (int i = 0; i < count; i++) {
            strncat(output, opname, size - strlen(output) - 1);
            strncat(output, " ", size - strlen(output) - 1);
        }
        token = strtok(NULL, " \t\n");
    }
    return strlen(output);
}

/* Load program */
int load_program(Skibidi* s, const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (!fp) return 0;
    
    char raw[MAX_PROGRAM];
    size_t n = fread(raw, 1, MAX_PROGRAM - 1, fp);
    raw[n] = '\0';
    fclose(fp);
    
    char expanded[MAX_PROGRAM];
    expand_macros(raw, expanded, MAX_PROGRAM);
    
    char* tokens[MAX_PROGRAM];
    int tokc = 0;
    char* saveptr;
    char* tok = strtok_r(expanded, " \t\n\r", &saveptr);
    
    while (tok != NULL && tokc < MAX_PROGRAM) {
        if (tok[0] == ';') {
            tok = strtok_r(NULL, " \t\n\r", &saveptr);
            continue;
        }
        
        /* Valid ops including new ones */
        if (strcmp(tok, "dop") && strcmp(tok, "bop") && strcmp(tok, "skibidi") &&
            strcmp(tok, "grimace") && strcmp(tok, "toilet") && strcmp(tok, "rizz") &&
            strcmp(tok, "sigma") && strcmp(tok, "ohio") && strcmp(tok, "67") &&
            strcmp(tok, "mango") && strcmp(tok, "diddy") && 
            strcmp(tok, "brainrot") && strcmp(tok, "gooner") &&
            strcmp(tok, "magical white liquid")) {
            fprintf(stderr, "Unknown op: %s\n", tok);
            return 0;
        }
        
        tokens[tokc++] = strdup(tok);
        tok = strtok_r(NULL, " \t\n\r", &saveptr);
    }
    
    s->program = malloc(sizeof(char*) * tokc);
    s->program_size = tokc;
    for (int i = 0; i < tokc; i++) {
        s->program[i] = tokens[i];
    }
    return 1;
}

/* Debug */
void print_debug(Skibidi* s, const char* op) {
    double mag = complex_magnitude(s->memory[s->pointer]);
    printf("[%d] %-20s | P:%3dHz | C:%2d | (%.1f+%.1fi) | Mag:%.0f | Swp:%d | Spoil:%d | Rot:%d | Goon:%d\n",
           s->ip, op, s->pitch, s->pointer,
           s->memory[s->pointer].real, s->memory[s->pointer].imag,
           mag, s->swapped, s->spoiled, s->brainrot_count % 2, s->gooner_activated);
}

/* Execute with spoiled, swapped, brainrot, gooner logic */
void execute(Skibidi* s, const char* op) {
    if (s->debug) print_debug(s, op);
    
    /* Check undefined behavior */
    s->undefined_behavior = (s->swapped && s->spoiled) ? 1 : 0;
    
    /* GOONER HANDLER: "magical white liquid" does nothing */
    if (strcmp(op, "magical white liquid") == 0) {
        if (s->debug) printf("  💧 magical white liquid (no-op)\n");
        return;
    }
    
    /* BRAINROT */
    if (strcmp(op, "brainrot") == 0) {
        brainrot(s);
        return;
    }
    
    /* GOONER */
    if (strcmp(op, "gooner") == 0) {
        gooner(s);
        return;
    }
    
    /* If gooner activated, only brainrot/gooner should work above */
    if (s->gooner_activated) {
        if (s->debug) printf("  🚫 Gooned: ignoring %s\n", op);
        return;
    }
    
    /* Get current cell with possible swap interpretation */
    Complex current = s->memory[s->pointer];
    if (s->swapped && !s->undefined_behavior) {
        current = complex_swap(current);
    }
    
    if (strcmp(op, "dop") == 0) {
        if (s->spoiled && !s->undefined_behavior) {
            s->memory[s->pointer].real -= 1.0;
        } else {
            s->memory[s->pointer].real += 1.0;
        }
    }
    else if (strcmp(op, "bop") == 0) {
        if (s->spoiled && !s->undefined_behavior) {
            s->memory[s->pointer].imag += 1.0;
        } else {
            s->memory[s->pointer].imag -= 1.0;
        }
    }
    else if (strcmp(op, "skibidi") == 0) {
        skibidi_chaos(s);
        if (s->debug) printf("  🎵 Pitch: %dHz\n", s->pitch);
    }
    else if (strcmp(op, "grimace") == 0) {
        int move_right;
        if (s->spoiled && !s->undefined_behavior) {
            move_right = (s->pitch < 440);
        } else {
            move_right = (s->pitch >= 440);
        }
        
        if (move_right) {
            s->pointer = (s->pointer + 1) % MEMORY_SIZE;
            if (s->debug) printf("  → RIGHT\n");
        } else {
            s->pointer = (s->pointer - 1 + MEMORY_SIZE) % MEMORY_SIZE;
            if (s->debug) printf("  ← LEFT\n");
        }
    }
    else if (strcmp(op, "toilet") == 0) {
        if (s->stack_ptr < STACK_SIZE) {
            s->stack[s->stack_ptr++] = s->memory[s->pointer];
            complex_zero(&s->memory[s->pointer]);
            if (s->debug) printf("  💾 PUSH (depth:%d)\n", s->stack_ptr);
        }
    }
    else if (strcmp(op, "rizz") == 0) {
        double mag = complex_magnitude(s->memory[s->pointer]);
        if (s->spoiled && !s->undefined_behavior) {
            mag *= 2.0;
        }
        int ascii = (int)floor(mag);
        char c = (char)ascii;
        int len = strlen(s->output);
        s->output[len] = c;
        s->output[len+1] = '\0';
        if (s->debug) printf("  📢 '%c' (mag:%.0f)\n", c, mag);
    }
    else if (strcmp(op, "sigma") == 0) {
        char ch = getchar();
        if (ch == EOF) ch = 0;
        s->memory[s->pointer].real = (double)ch;
        s->memory[s->pointer].imag = 0;
        if (s->debug) printf("  📥 '%c'\n", ch);
    }
    else if (strcmp(op, "ohio") == 0) {
        double mag = complex_magnitude(s->memory[s->pointer]);
        int jump = (int)floor(mag);
        
        if (s->spoiled && !s->undefined_behavior) {
            if (jump > 0) {
                s->ip += jump;
                if (s->debug) printf("  🔄 FWD +%d\n", jump);
            }
        } else {
            if (jump > 0 && jump <= s->ip) {
                s->ip -= jump;
                if (s->debug) printf("  🔄 BACK -%d\n", jump);
            }
        }
    }
    else if (strcmp(op, "67") == 0) {
        if (s->undefined_behavior) {
            if (rand() % 2) {
                s->swapped = !s->swapped;
                if (s->debug) printf("  🔀 67 toggled swap (UNDEFINED)\n");
            }
        } else if (!s->spoiled) {
            s->swapped = !s->swapped;
            if (s->debug) printf("  🔀 Swap: %s\n", s->swapped ? "ON" : "OFF");
        } else {
            if (s->debug) printf("  💀 67 ignored (spoiled)\n");
        }
    }
    else if (strcmp(op, "mango") == 0) {
        if (s->undefined_behavior) {
            if (rand() % 2) {
                s->spoiled = !s->spoiled;
                if (s->debug) printf("  🥭 Mango toggled spoiled (UNDEFINED)\n");
            }
        } else {
            s->spoiled = !s->spoiled;
            if (s->debug) printf("  🥭 Spoiled: %s\n", s->spoiled ? "ON" : "OFF");
        }
    }
    else if (strcmp(op, "diddy") == 0) {
        if (s->spoiled || s->undefined_behavior) {
            fprintf(stderr, "\n💀 CRASH: diddy called while spoiled!\n");
            exit(1);
        }
        printf("milk");
        fflush(stdout);
        if (s->debug) printf("  🥛 diddy: milk\n");
    }
}

/* Run */
void run(Skibidi* s) {
    s->ip = 0;
    while (s->ip < s->program_size) {
        execute(s, s->program[s->ip]);
        s->ip++;
    }
}

void free_program(Skibidi* s) {
    for (int i = 0; i < s->program_size; i++) {
        free(s->program[i]);
    }
    free(s->program);
}

/* Demo program that shows off all commands */
void create_demo(const char* fname) {
    FILE* fp = fopen(fname, "w");
    fprintf(fp, "; Skibidi v4.0 - Brainrot & Gooner Demo\n");
    fprintf(fp, "; Warning: This program is intentionally broken\n\n");
    
    fprintf(fp, "; First, print some characters\n");
    fprintf(fp, "dop(72) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(101) rizz\n\n");
    
    fprintf(fp, "; BRAINROT reverses the program!\n");
    fprintf(fp, "brainrot\n\n");
    
    fprintf(fp, "; After brainrot, we're now executing backwards\n");
    fprintf(fp, "; The remaining instructions will be reversed order\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "dop(111) rizz\n\n");
    
    fprintf(fp, "; GOONER destroys everything\n");
    fprintf(fp, "gooner\n\n");
    
    fprintf(fp, "; These will become 'magical white liquid' and do nothing\n");
    fprintf(fp, "dop(100) rizz\n");
    fprintf(fp, "diddy\n");
    
    fclose(fp);
}

/* Evil Hello World that might actually work */
void create_evil_hello(const char* fname) {
    FILE* fp = fopen(fname, "w");
    fprintf(fp, "; Evil Hello World - Might work, might not\n");
    fprintf(fp, "; Strategy: No mango, no 67, no brainrot, no gooner\n");
    fprintf(fp, "; Just pure deterministic chaos\n\n");
    
    fprintf(fp, "dop(72) rizz\n");
    fprintf(fp, "skibidi grimace\n");      /* Move right with chaotic pitch */
    fprintf(fp, "dop(101) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(111) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(32) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(87) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(111) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(114) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop(100) rizz\n");
    fprintf(fp, "diddy\n");
    
    fclose(fp);
}

/* Main */
int main(int argc, char* argv[]) {
    srand(time(NULL));
    int debug = 0;
    char* filename = NULL;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--debug") == 0) debug = 1;
        else if (strcmp(argv[i], "--demo") == 0) {
            filename = "skibidi_demo.skb";
            create_demo(filename);
            printf("Created demo: %s (intentionally broken)\n", filename);
        } else if (strcmp(argv[i], "--evil-hello") == 0) {
            filename = "evil_hello.skb";
            create_evil_hello(filename);
            printf("Created evil Hello World: %s\n", filename);
        } else if (argv[i][0] != '-') {
            filename = argv[i];
        }
    }
    
    if (!filename) {
        printf("Skibidi v4.0 - Brainrot & Gooner Edition\n");
        printf("Harder than Malbodge (probably)\n\n");
        printf("Commands:\n");
        printf("  dop, bop, skibidi, grimace, toilet, rizz, sigma, ohio\n");
        printf("  67, mango, diddy, brainrot, gooner\n\n");
        printf("Usage: %s <file.skb> [--debug]\n", argv[0]);
        printf("       %s --demo\n", argv[0]);
        printf("       %s --evil-hello\n", argv[0]);
        return 1;
    }
    
    Skibidi skibidi;
    interpreter_init(&skibidi, debug);
    
    if (!load_program(&skibidi, filename)) {
        fprintf(stderr, "Failed to load: %s\n", filename);
        return 1;
    }
    
    printf("=== Skibidi v4.0 Running ===\n");
    printf("🧠 brainrot = reverses program + toggles debug\n");
    printf("💦 gooner  = all ops become 'magical white liquid'\n");
    printf("🥛 diddy   = prints 'milk' (crashes if spoiled)\n");
    printf("⚠️  67 + mango active together = UNDEFINED BEHAVIOR\n");
    printf("----------------------------------------\n\n");
    
    run(&skibidi);
    
    printf("\n----------------------------------------\n");
    printf("Final output: %s\n", skibidi.output);
    
    free_program(&skibidi);
    
    return 0;
}