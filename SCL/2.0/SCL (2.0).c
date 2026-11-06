/*
 * Skibidi v2.0 Interpreter - Chaotic Deterministic Version
 * A brutally hard esoteric programming language
 * 
 * Compilation: gcc -o skibidi skibidi.c -lm
 * Usage: ./skibidi program.skb [--debug]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

#ifdef _WIN32
    #include <windows.h>
    #define DIR_SEPARATOR '\\'
#else
    #include <unistd.h>
    #define DIR_SEPARATOR '/'
#endif

/* OpenSSL MD5 - using system crypto library */
#include <openssl/md5.h>

/* Constants */
#define MEMORY_SIZE 256
#define MAX_PROGRAM_SIZE 100000
#define MAX_TOKEN_SIZE 256
#define MAX_LINE_SIZE 1024
#define STACK_SIZE 1024

/* Complex number structure */
typedef struct {
    double real;
    double imag;
} Complex;

/* Interpreter state */
typedef struct {
    Complex memory[MEMORY_SIZE];
    int pointer;                    /* Current cell index */
    int pitch;                      /* Current pitch in Hz (200-799) */
    Complex rhythm_stack[STACK_SIZE];
    int stack_ptr;
    char** program;                 /* Array of instruction tokens */
    int program_size;
    int instruction_pointer;
    int debug;
    char output[10000];
    unsigned char rng_state[16];    /* MD5 state for deterministic chaos */
    char input_buffer[1024];
    int input_pos;
} SkibidiInterpreter;

/* Function prototypes */
Complex complex_add(Complex a, Complex b);
Complex complex_sub(Complex a, Complex b);
double complex_magnitude(Complex c);
void complex_zero(Complex* c);
void interpreter_init(SkibidiInterpreter* interp, int debug);
void interpreter_reset(SkibidiInterpreter* interp);
void md5_update_state(unsigned char* state);
int hash_to_pitch(unsigned char* state);
void skibidi_chaos(SkibidiInterpreter* interp);
int load_program(SkibidiInterpreter* interp, const char* filename);
int expand_macros(const char* input, char* output, int output_size);
void execute_instruction(SkibidiInterpreter* interp, const char* op);
void run(SkibidiInterpreter* interp);
void print_debug(SkibidiInterpreter* interp, const char* op);

/* Complex math */
Complex complex_add(Complex a, Complex b) {
    Complex result;
    result.real = a.real + b.real;
    result.imag = a.imag + b.imag;
    return result;
}

Complex complex_sub(Complex a, Complex b) {
    Complex result;
    result.real = a.real - b.real;
    result.imag = a.imag - b.imag;
    return result;
}

double complex_magnitude(Complex c) {
    return sqrt(c.real * c.real + c.imag * c.imag);
}

void complex_zero(Complex* c) {
    c->real = 0.0;
    c->imag = 0.0;
}

/* MD5 chaos functions */
void md5_update_state(unsigned char* state) {
    MD5_CTX ctx;
    unsigned char hash[MD5_DIGEST_LENGTH];
    
    /* Hash the current state */
    MD5_Init(&ctx);
    MD5_Update(&ctx, state, 16);
    MD5_Final(hash, &ctx);
    
    /* Copy new state */
    memcpy(state, hash, 16);
}

int hash_to_pitch(unsigned char* state) {
    /* Use first 4 bytes as integer */
    int hash_int = 0;
    hash_int |= state[0] << 24;
    hash_int |= state[1] << 16;
    hash_int |= state[2] << 8;
    hash_int |= state[3];
    
    /* Map to 200-799 Hz range */
    return 200 + (abs(hash_int) % 600);
}

void skibidi_chaos(SkibidiInterpreter* interp) {
    /* Update RNG state deterministically */
    md5_update_state(interp->rng_state);
    /* Set new pitch based on hash */
    interp->pitch = hash_to_pitch(interp->rng_state);
}

/* Initialize interpreter */
void interpreter_init(SkibidiInterpreter* interp, int debug) {
    memset(interp->memory, 0, sizeof(interp->memory));
    interp->pointer = 0;
    interp->pitch = 440;  /* Starting pitch */
    memset(interp->rhythm_stack, 0, sizeof(interp->rhythm_stack));
    interp->stack_ptr = 0;
    interp->program = NULL;
    interp->program_size = 0;
    interp->instruction_pointer = 0;
    interp->debug = debug;
    memset(interp->output, 0, sizeof(interp->output));
    memset(interp->input_buffer, 0, sizeof(interp->input_buffer));
    interp->input_pos = 0;
    
    /* Initialize RNG state with seed 0 */
    memset(interp->rng_state, 0, 16);
}

void interpreter_reset(SkibidiInterpreter* interp) {
    memset(interp->memory, 0, sizeof(interp->memory));
    interp->pointer = 0;
    interp->pitch = 440;
    memset(interp->rhythm_stack, 0, sizeof(interp->rhythm_stack));
    interp->stack_ptr = 0;
    interp->instruction_pointer = 0;
    memset(interp->output, 0, sizeof(interp->output));
    memset(interp->input_buffer, 0, sizeof(interp->input_buffer));
    interp->input_pos = 0;
    memset(interp->rng_state, 0, 16);
}

/* Macro expansion: dop(72) -> "dop dop dop ..." (72 times) */
int expand_macros(const char* input, char* output, int output_size) {
    char temp[MAX_LINE_SIZE];
    strncpy(temp, input, MAX_LINE_SIZE - 1);
    temp[MAX_LINE_SIZE - 1] = '\0';
    
    output[0] = '\0';
    
    char* token = strtok(temp, " \t\n");
    while (token != NULL) {
        /* Check for dop(N) or bop(N) pattern */
        int count = 0;
        char op_name[16];
        
        if (sscanf(token, "dop(%d)", &count) == 1) {
            strcpy(op_name, "dop");
        } else if (sscanf(token, "bop(%d)", &count) == 1) {
            strcpy(op_name, "bop");
        } else {
            /* Not a macro, just copy token */
            strncat(output, token, output_size - strlen(output) - 1);
            strncat(output, " ", output_size - strlen(output) - 1);
            token = strtok(NULL, " \t\n");
            continue;
        }
        
        /* Expand macro: add 'count' copies of op_name */
        for (int i = 0; i < count; i++) {
            strncat(output, op_name, output_size - strlen(output) - 1);
            strncat(output, " ", output_size - strlen(output) - 1);
        }
        
        token = strtok(NULL, " \t\n");
    }
    
    return strlen(output);
}

/* Load program from file */
int load_program(SkibidiInterpreter* interp, const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Error: Cannot open file '%s'\n", filename);
        return 0;
    }
    
    /* Read entire file */
    char raw_program[MAX_PROGRAM_SIZE];
    size_t bytes_read = fread(raw_program, 1, MAX_PROGRAM_SIZE - 1, fp);
    raw_program[bytes_read] = '\0';
    fclose(fp);
    
    /* Expand macros */
    char expanded[MAX_PROGRAM_SIZE];
    expand_macros(raw_program, expanded, MAX_PROGRAM_SIZE);
    
    /* Tokenize */
    char* tokens[MAX_PROGRAM_SIZE];
    int token_count = 0;
    
    char* saveptr;
    char* token = strtok_r(expanded, " \t\n\r", &saveptr);
    while (token != NULL && token_count < MAX_PROGRAM_SIZE) {
        /* Skip comments (lines starting with ;) */
        if (token[0] == ';') {
            /* Skip rest of line? Already tokenized, just skip this token */
            token = strtok_r(NULL, " \t\n\r", &saveptr);
            continue;
        }
        
        /* Validate token is valid instruction */
        if (strcmp(token, "dop") != 0 && 
            strcmp(token, "bop") != 0 &&
            strcmp(token, "skibidi") != 0 &&
            strcmp(token, "toilet") != 0 &&
            strcmp(token, "rizz") != 0 &&
            strcmp(token, "sigma") != 0 &&
            strcmp(token, "ohio") != 0 &&
            strcmp(token, "grimace") != 0) {
            fprintf(stderr, "Syntax error: Unknown instruction '%s'\n", token);
            return 0;
        }
        
        tokens[token_count++] = strdup(token);
        token = strtok_r(NULL, " \t\n\r", &saveptr);
    }
    
    /* Store program */
    interp->program = malloc(sizeof(char*) * token_count);
    interp->program_size = token_count;
    for (int i = 0; i < token_count; i++) {
        interp->program[i] = tokens[i];
    }
    
    return 1;
}

/* Debug output */
void print_debug(SkibidiInterpreter* interp, const char* op) {
    double mag = complex_magnitude(interp->memory[interp->pointer]);
    printf("[IP:%d] %s | Pitch:%dHz | Cell:%d | (%.1f+%.1fi) | Mag:%.0f | Stack:%d\n",
           interp->instruction_pointer, op, interp->pitch, interp->pointer,
           interp->memory[interp->pointer].real,
           interp->memory[interp->pointer].imag,
           mag, interp->stack_ptr);
}

/* Execute single instruction */
void execute_instruction(SkibidiInterpreter* interp, const char* op) {
    if (interp->debug) {
        print_debug(interp, op);
    }
    
    if (strcmp(op, "dop") == 0) {
        /* Increment real part */
        interp->memory[interp->pointer].real += 1.0;
    }
    else if (strcmp(op, "bop") == 0) {
        /* Decrement imaginary part */
        interp->memory[interp->pointer].imag -= 1.0;
    }
    else if (strcmp(op, "skibidi") == 0) {
        /* Chaotic deterministic pitch change */
        skibidi_chaos(interp);
        if (interp->debug) {
            printf("  🎵 Pitch changed to %dHz (MD5 chaos)\n", interp->pitch);
        }
    }
    else if (strcmp(op, "grimace") == 0) {
        /* Move pointer based on pitch */
        if (interp->pitch < 440) {
            /* Move left */
            interp->pointer = (interp->pointer - 1 + MEMORY_SIZE) % MEMORY_SIZE;
            if (interp->debug) {
                printf("  ← Moved LEFT to cell %d (pitch %dHz < 440)\n", 
                       interp->pointer, interp->pitch);
            }
        } else {
            /* Move right (pitch >= 440) */
            interp->pointer = (interp->pointer + 1) % MEMORY_SIZE;
            if (interp->debug) {
                printf("  → Moved RIGHT to cell %d (pitch %dHz >= 440)\n", 
                       interp->pointer, interp->pitch);
            }
        }
    }
    else if (strcmp(op, "toilet") == 0) {
        /* Push to stack and clear */
        if (interp->stack_ptr < STACK_SIZE) {
            interp->rhythm_stack[interp->stack_ptr++] = interp->memory[interp->pointer];
            complex_zero(&interp->memory[interp->pointer]);
            if (interp->debug) {
                printf("  💾 Pushed to stack (depth: %d)\n", interp->stack_ptr);
            }
        } else {
            fprintf(stderr, "Error: Rhythm stack overflow!\n");
        }
    }
    else if (strcmp(op, "rizz") == 0) {
        /* Output magnitude as ASCII */
        double mag = complex_magnitude(interp->memory[interp->pointer]);
        int ascii = (int)floor(mag);
        char c = (char)ascii;
        
        int len = strlen(interp->output);
        interp->output[len] = c;
        interp->output[len + 1] = '\0';
        
        if (interp->debug) {
            printf("  📢 Output '%c' (ASCII %d, magnitude %.0f)\n", c, ascii, mag);
        }
    }
    else if (strcmp(op, "sigma") == 0) {
        /* Read input */
        if (interp->input_buffer[interp->input_pos] == '\0') {
            /* Need more input - read from stdin */
            char ch = getchar();
            if (ch == EOF) {
                interp->memory[interp->pointer].real = 0;
                interp->memory[interp->pointer].imag = 0;
            } else {
                interp->memory[interp->pointer].real = (double)ch;
                interp->memory[interp->pointer].imag = 0;
                if (interp->debug) {
                    printf("  📥 Read '%c' (ASCII %d)\n", ch, ch);
                }
            }
        } else {
            /* Use buffered input */
            char ch = interp->input_buffer[interp->input_pos++];
            interp->memory[interp->pointer].real = (double)ch;
            interp->memory[interp->pointer].imag = 0;
            if (interp->debug) {
                printf("  📥 Read '%c' (ASCII %d)\n", ch, ch);
            }
        }
    }
    else if (strcmp(op, "ohio") == 0) {
        /* Jump back N ops where N = floor(magnitude) */
        double mag = complex_magnitude(interp->memory[interp->pointer]);
        int jump = (int)floor(mag);
        
        if (jump > 0 && jump <= interp->instruction_pointer) {
            interp->instruction_pointer -= jump;
            if (interp->debug) {
                printf("  🔄 Jumped back %d instructions (new IP: %d)\n", 
                       jump, interp->instruction_pointer);
            }
        } else if (jump > 0) {
            if (interp->debug) {
                printf("  ⚠️  Cannot jump back %d (only %d instructions before)\n",
                       jump, interp->instruction_pointer);
            }
        } else {
            if (interp->debug) {
                printf("  ⏭️  No jump (magnitude = 0)\n");
            }
        }
    }
    else {
        fprintf(stderr, "Runtime error: Unknown instruction '%s'\n", op);
        exit(1);
    }
}

/* Run the program */
void run(SkibidiInterpreter* interp) {
    interp->instruction_pointer = 0;
    
    while (interp->instruction_pointer < interp->program_size) {
        const char* op = interp->program[interp->instruction_pointer];
        execute_instruction(interp, op);
        interp->instruction_pointer++;
    }
}

/* Create demo Hello World program file */
void create_demo_program(const char* filename) {
    FILE* fp = fopen(filename, "w");
    if (!fp) {
        fprintf(stderr, "Error: Cannot create demo file\n");
        return;
    }
    
    fprintf(fp, "; Skibidi v2.0 Hello World\n");
    fprintf(fp, "; Chaotic deterministic version\n");
    fprintf(fp, "\n");
    fprintf(fp, "dop(72) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(101) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(111) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(32) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(87) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(111) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(114) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop(100) rizz\n");
    fprintf(fp, "toilet\n");
    
    fclose(fp);
}

/* Main */
int main(int argc, char* argv[]) {
    int debug = 0;
    char* filename = NULL;
    
    /* Parse arguments */
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--debug") == 0) {
            debug = 1;
        } else if (strcmp(argv[i], "--demo") == 0) {
            filename = "skibidi_demo.skb";
            create_demo_program(filename);
            printf("Created demo program: %s\n", filename);
        } else if (argv[i][0] != '-') {
            filename = argv[i];
        }
    }
    
    if (!filename) {
        printf("Skibidi v2.0 Interpreter - Chaotic Deterministic\n");
        printf("Usage: %s <program.skb> [--debug]\n", argv[0]);
        printf("       %s --demo\n", argv[0]);
        return 1;
    }
    
    /* Initialize and run */
    SkibidiInterpreter interp;
    interpreter_init(&interp, debug);
    
    if (!load_program(&interp, filename)) {
        return 1;
    }
    
    printf("Running Skibidi program: %s\n", filename);
    printf("(Pitch changes are deterministic but chaotic - MD5 hashing)\n");
    printf("Movement: pitch >= 440Hz = right, < 440Hz = left\n");
    printf("----------------------------------------\n");
    
    run(&interp);
    
    printf("\n----------------------------------------\n");
    printf("Output: %s\n", interp.output);
    
    /* Cleanup */
    for (int i = 0; i < interp.program_size; i++) {
        free(interp.program[i]);
    }
    free(interp.program);
    
    return 0;
}