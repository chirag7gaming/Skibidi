/*
 * Skibidi v1.0 - The Original Chaos
 * "Harder than Bash and Brainfuck combined"
 * 
 * Compile: gcc -o skibidi skibidi_v1.c -lm
 * 
 * WARNING: This version has RANDOM pitch changes.
 * Success rate for Hello World: ~0.36%
 * Run multiple times until it works.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MEMORY_SIZE 256
#define MAX_PROGRAM 100000
#define STACK_SIZE 1024

/* Complex number structure */
typedef struct {
    double real;
    double imag;
} Complex;

/* Interpreter state */
typedef struct {
    Complex memory[MEMORY_SIZE];
    int pointer;              /* Ear pointer (cell index) */
    int pitch;                /* Current pitch in Hz (200-800) */
    Complex rhythm_stack[STACK_SIZE];
    int stack_ptr;
    char** program;           /* Array of instruction tokens */
    int program_size;
    int instruction_pointer;
    int debug;
    char output[100000];
    char input_buffer[1024];
    int input_pos;
} SkibidiInterpreter;

/* Function prototypes */
double complex_magnitude(Complex c);
void complex_zero(Complex* c);
void interpreter_init(SkibidiInterpreter* interp, int debug);
int load_program(SkibidiInterpreter* interp, const char* filename);
int expand_macros(const char* input, char* output, int size);
void execute_instruction(SkibidiInterpreter* interp, const char* op);
void run(SkibidiInterpreter* interp);
void print_debug(SkibidiInterpreter* interp, const char* op);

/* Complex math */
double complex_magnitude(Complex c) {
    return sqrt(c.real * c.real + c.imag * c.imag);
}

void complex_zero(Complex* c) {
    c->real = 0.0;
    c->imag = 0.0;
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
    
    /* Seed random for pitch generation */
    srand(time(NULL));
}

/* Macro expansion: dop(72) becomes 72 separate 'dop' tokens */
int expand_macros(const char* input, char* output, int size) {
    char temp[MAX_PROGRAM];
    strncpy(temp, input, MAX_PROGRAM - 1);
    temp[MAX_PROGRAM - 1] = '\0';
    
    output[0] = '\0';
    char* token = strtok(temp, " \t\n");
    
    while (token != NULL) {
        int count = 0;
        char op_name[16];
        
        /* Check for dop(N) or bop(N) pattern */
        if (sscanf(token, "dop(%d)", &count) == 1) {
            strcpy(op_name, "dop");
        } else if (sscanf(token, "bop(%d)", &count) == 1) {
            strcpy(op_name, "bop");
        } else {
            /* Not a macro, just copy token */
            strncat(output, token, size - strlen(output) - 1);
            strncat(output, " ", size - strlen(output) - 1);
            token = strtok(NULL, " \t\n");
            continue;
        }
        
        /* Expand macro: add 'count' copies of op_name */
        for (int i = 0; i < count; i++) {
            strncat(output, op_name, size - strlen(output) - 1);
            strncat(output, " ", size - strlen(output) - 1);
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
    char raw_program[MAX_PROGRAM];
    size_t bytes_read = fread(raw_program, 1, MAX_PROGRAM - 1, fp);
    raw_program[bytes_read] = '\0';
    fclose(fp);
    
    /* Expand macros */
    char expanded[MAX_PROGRAM];
    expand_macros(raw_program, expanded, MAX_PROGRAM);
    
    /* Tokenize */
    char* tokens[MAX_PROGRAM];
    int token_count = 0;
    
    char* saveptr;
    char* token = strtok_r(expanded, " \t\n\r", &saveptr);
    while (token != NULL && token_count < MAX_PROGRAM) {
        /* Skip comments (lines starting with ;) */
        if (token[0] == ';') {
            token = strtok_r(NULL, " \t\n\r", &saveptr);
            continue;
        }
        
        /* Validate token is valid instruction (v1.0: only 7 ops) */
        if (strcmp(token, "dop") != 0 && 
            strcmp(token, "bop") != 0 &&
            strcmp(token, "skibidi") != 0 &&
            strcmp(token, "toilet") != 0 &&
            strcmp(token, "rizz") != 0 &&
            strcmp(token, "sigma") != 0 &&
            strcmp(token, "ohio") != 0) {
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

/* Generate random pitch between 200-800 Hz */
int random_pitch() {
    return 200 + (rand() % 601);  /* 200-800 inclusive */
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
        /* RANDOM pitch change (200-800 Hz) - v1.0 chaos! */
        interp->pitch = random_pitch();
        if (interp->debug) {
            printf("  🎵 RANDOM Pitch: %dHz\n", interp->pitch);
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

/* Create Hello World program */
void create_hello_world(const char* filename) {
    FILE* fp = fopen(filename, "w");
    if (!fp) {
        fprintf(stderr, "Error: Cannot create file\n");
        return;
    }
    
    fprintf(fp, "; Skibidi v1.0 Hello World\n");
    fprintf(fp, "; WARNING: Success rate is ~0.36%%\n");
    fprintf(fp, "; Run multiple times until it works!\n");
    fprintf(fp, "\n");
    fprintf(fp, "dop(72) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(101) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(111) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(32) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(87) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(111) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(114) rizz\n");
    fprintf(fp, "skibidi\n");
    fprintf(fp, "dop(108) rizz\n");
    fprintf(fp, "skibidi\n");
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
        } else if (strcmp(argv[i], "--hello") == 0) {
            filename = "hello_v1.skb";
            create_hello_world(filename);
            printf("Created Hello World program: %s\n", filename);
            printf("Success rate: ~0.36%% (1 in 278 runs)\n");
        } else if (argv[i][0] != '-') {
            filename = argv[i];
        }
    }
    
    if (!filename) {
        printf("Skibidi v1.0 - The Original Chaos\n");
        printf("\"Harder than Bash and Brainfuck combined\"\n");
        printf("\n");
        printf("Commands: dop, bop, skibidi, toilet, rizz, sigma, ohio\n");
        printf("\n");
        printf("Usage: %s <program.skb> [--debug]\n", argv[0]);
        printf("       %s --hello\n", argv[0]);
        printf("\n");
        printf("WARNING: Pitch changes are RANDOM (200-800 Hz)\n");
        printf("Movement depends on pitch of last executed op\n");
        printf("Success is NOT guaranteed!\n");
        return 1;
    }
    
    /* Initialize and run */
    SkibidiInterpreter interp;
    interpreter_init(&interp, debug);
    
    if (!load_program(&interp, filename)) {
        return 1;
    }
    
    printf("=== Skibidi v1.0 Running ===\n");
    printf("⚠️  PITCH IS RANDOM - Good luck!\n");
    printf("Pitch >= 440Hz = move right, < 440Hz = move left\n");
    printf("Success rate for Hello World: ~0.36%%\n");
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