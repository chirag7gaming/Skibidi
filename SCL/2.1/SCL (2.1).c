/*
 * Skibidi v2.1 - "The Evil Update"
 * Now with 67, mango, and diddy
 * 
 * Compile: gcc -o skibidi skibidi_v2.1.c -lm -lssl -lcrypto
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

typedef struct {
    double real;
    double imag;
} Complex;

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
    
    /* NEW in v2.1 */
    int swapped;        /* toggled by 67 */
    int spoiled;        /* toggled by mango */
    
    char input_buffer[1024];
    int input_pos;
} Skibidi;

void complex_zero(Complex* c) {
    c->real = 0.0;
    c->imag = 0.0;
}

double complex_magnitude(Complex c) {
    return sqrt(c.real * c.real + c.imag * c.imag);
}

Complex complex_swap(Complex c) {
    Complex result;
    result.real = c.imag;
    result.imag = c.real;
    return result;
}

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
    memset(s->input_buffer, 0, sizeof(s->input_buffer));
    s->input_pos = 0;
}

int expand_macros(const char* input, char* output, int size) {
    char temp[MAX_PROGRAM];
    strncpy(temp, input, MAX_PROGRAM - 1);
    temp[MAX_PROGRAM - 1] = '\0';
    
    output[0] = '\0';
    char* token = strtok(temp, " \t\n");
    
    while (token != NULL) {
        int count = 0;
        char opname[16];
        
        if (sscanf(token, "dop(%d)", &count) == 1) {
            strcpy(opname, "dop");
        } else if (sscanf(token, "bop(%d)", &count) == 1) {
            strcpy(opname, "bop");
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
        
        if (strcmp(tok, "dop") && strcmp(tok, "bop") && strcmp(tok, "skibidi") &&
            strcmp(tok, "grimace") && strcmp(tok, "toilet") && strcmp(tok, "rizz") &&
            strcmp(tok, "sigma") && strcmp(tok, "ohio") && strcmp(tok, "67") &&
            strcmp(tok, "mango") && strcmp(tok, "diddy")) {
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

void print_debug(Skibidi* s, const char* op) {
    double mag = complex_magnitude(s->memory[s->pointer]);
    printf("[%d] %s | P:%dHz | C:%d | (%.1f+%.1fi) | Mag:%.0f | Swp:%d | Spoil:%d\n",
           s->ip, op, s->pitch, s->pointer,
           s->memory[s->pointer].real, s->memory[s->pointer].imag,
           mag, s->swapped, s->spoiled);
}

void execute(Skibidi* s, const char* op) {
    if (s->debug) print_debug(s, op);
    
    if (strcmp(op, "dop") == 0) {
        if (s->spoiled) {
            s->memory[s->pointer].real -= 1.0;
        } else {
            s->memory[s->pointer].real += 1.0;
        }
    }
    else if (strcmp(op, "bop") == 0) {
        if (s->spoiled) {
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
        if (s->spoiled) {
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
        if (s->spoiled) mag *= 2.0;
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
        
        if (s->spoiled) {
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
        if (!s->spoiled) {
            s->swapped = !s->swapped;
            if (s->debug) printf("  🔀 Swap: %s\n", s->swapped ? "ON" : "OFF");
        } else {
            if (s->debug) printf("  💀 67 ignored (spoiled)\n");
        }
    }
    else if (strcmp(op, "mango") == 0) {
        s->spoiled = !s->spoiled;
        if (s->debug) printf("  🥭 Spoiled: %s\n", s->spoiled ? "ON" : "OFF");
    }
    else if (strcmp(op, "diddy") == 0) {
        if (s->spoiled) {
            fprintf(stderr, "\n💀 CRASH: diddy called while spoiled!\n");
            exit(1);
        }
        printf("milk");
        fflush(stdout);
        if (s->debug) printf("  🥛 diddy: milk\n");
    }
}

void run(Skibidi* s) {
    s->ip = 0;
    while (s->ip < s->program_size) {
        execute(s, s->program[s->ip]);
        s->ip++;
    }
}

void create_demo(const char* fname) {
    FILE* fp = fopen(fname, "w");
    fprintf(fp, "; Skibidi v2.1 Demo - The Evil Update\n");
    fprintf(fp, "; This program might work. Or crash. Or both.\n\n");
    fprintf(fp, "dop(72) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(101) rizz\n");
    fprintf(fp, "67\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "mango\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "dop(111) rizz\n");
    fprintf(fp, "dop(100) rizz\n");
    fprintf(fp, "diddy\n");
    fclose(fp);
}

void create_evil_hello(const char* fname) {
    FILE* fp = fopen(fname, "w");
    fprintf(fp, "; Evil Hello World - v2.1 style\n");
    fprintf(fp, "dop(72) rizz\n");
    fprintf(fp, "skibidi grimace\n");
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

int main(int argc, char* argv[]) {
    srand(time(NULL));
    int debug = 0;
    char* filename = NULL;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--debug") == 0) debug = 1;
        else if (strcmp(argv[i], "--demo") == 0) {
            filename = "skibidi_demo.skb";
            create_demo(filename);
            printf("Created: %s\n", filename);
        } else if (strcmp(argv[i], "--evil-hello") == 0) {
            filename = "evil_hello.skb";
            create_evil_hello(filename);
            printf("Created: %s\n", filename);
        } else if (argv[i][0] != '-') {
            filename = argv[i];
        }
    }
    
    if (!filename) {
        printf("Skibidi v2.1 - The Evil Update\n");
        printf("NEW: 67 (swap), mango (spoiled), diddy (prints milk)\n");
        printf("Usage: %s <file.skb> [--debug]\n", argv[0]);
        return 1;
    }
    
    Skibidi skibidi;
    interpreter_init(&skibidi, debug);
    
    if (!load_program(&skibidi, filename)) {
        fprintf(stderr, "Failed to load: %s\n", filename);
        return 1;
    }
    
    printf("=== Skibidi v2.1 - The Evil Update ===\n");
    printf("(67 swaps real/imag, mango toggles spoiled, diddy prints milk)\n");
    printf("Spoiled mode reverses ALL operations\n");
    printf("----------------------------------------\n");
    
    run(&skibidi);
    
    printf("\n----------------------------------------\n");
    printf("Output: %s\n", skibidi.output);
    
    for (int i = 0; i < skibidi.program_size; i++) free(skibidi.program[i]);
    free(skibidi.program);
    
    return 0;
}