/*
 * Skibidi v5.0 - Internet Edition
 * 
 * Compile: gcc -o skibidi skibidi_v5.c -lm -lssl -lcrypto -lpthread
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
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
    int swapped;
    int spoiled;
    int undefined_behavior;
    int brainrot_count;
    int gooner_activated;
    char input_buffer[1024];
    int input_pos;
} Skibidi;

typedef struct {
    int socket_fd;
    struct sockaddr_in addr;
    char server_ip[64];
    int server_port;
    int connected;
    int peer_count;
    char peer_names[16][64];
    struct sockaddr_in peers[16];
    pthread_t recv_thread;
    pthread_t send_thread;
    int running;
} SigmaNet;

typedef struct {
    char player_name[32];
    int skill_level;
    int rage_quit_timer;
    int packet_loss;
    int latency_ms;
} PlayerProfile;

#define PACKET_MEMORY_UPDATE 0x01
#define PACKET_POINTER_MOVE  0x02
#define PACKET_BRAINROT      0x03
#define PACKET_GOONER        0x04
#define PACKET_DIDDY_SPAM    0x05
#define PACKET_SKILL_ISSUE   0x69
#define PACKET_SIGMA_FLEX    0x96

typedef struct {
    unsigned char type;
    unsigned char player_id;
    int memory_index;
    Complex value;
    int brainrot_count;
    char flex_message[256];
    unsigned int checksum;
} NetworkPacket;

SigmaNet g_sigma_net;
PlayerProfile g_profile;
pthread_mutex_t net_mutex = PTHREAD_MUTEX_INITIALIZER;

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
    s->undefined_behavior = 0;
    s->brainrot_count = 0;
    s->gooner_activated = 0;
    memset(s->input_buffer, 0, sizeof(s->input_buffer));
    s->input_pos = 0;
}

void brainrot(Skibidi* s) {
    if (s->program_size <= 1) return;
    
    for (int i = 0; i < s->program_size / 2; i++) {
        char* temp = s->program[i];
        s->program[i] = s->program[s->program_size - 1 - i];
        s->program[s->program_size - 1 - i] = temp;
    }
    
    s->brainrot_count++;
    s->ip = 0;
    s->debug = !s->debug;
}

void gooner(Skibidi* s) {
    if (s->gooner_activated) return;
    
    for (int i = 0; i < s->program_size; i++) {
        free(s->program[i]);
        s->program[i] = strdup("magical white liquid");
    }
    
    s->gooner_activated = 1;
    s->ip = 0;
}

int load_program(Skibidi* s, const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (!fp) return 0;
    
    char line[1024];
    char* tokens[MAX_PROGRAM];
    int tokc = 0;
    
    while (fgets(line, sizeof(line), fp)) {
        char* saveptr;
        char* tok = strtok_r(line, " \t\n\r", &saveptr);
        
        while (tok != NULL && tokc < MAX_PROGRAM) {
            if (tok[0] == ';') {
                break;
            }
            
            if (strcmp(tok, "dop") && strcmp(tok, "bop") && strcmp(tok, "skibidi") &&
                strcmp(tok, "grimace") && strcmp(tok, "toilet") && strcmp(tok, "rizz") &&
                strcmp(tok, "sigma") && strcmp(tok, "ohio") && strcmp(tok, "67") &&
                strcmp(tok, "mango") && strcmp(tok, "diddy") && 
                strcmp(tok, "brainrot") && strcmp(tok, "gooner") &&
                strcmp(tok, "magical white liquid") && strcmp(tok, "sigmaflex")) {
                fprintf(stderr, "Unknown op: %s\n", tok);
                fclose(fp);
                return 0;
            }
            
            tokens[tokc++] = strdup(tok);
            tok = strtok_r(NULL, " \t\n\r", &saveptr);
        }
    }
    
    fclose(fp);
    
    s->program = malloc(sizeof(char*) * tokc);
    s->program_size = tokc;
    for (int i = 0; i < tokc; i++) {
        s->program[i] = tokens[i];
    }
    return 1;
}

void print_debug(Skibidi* s, const char* op) {
    double mag = complex_magnitude(s->memory[s->pointer]);
    printf("[%d] %-20s | P:%3dHz | C:%2d | (%.1f+%.1fi) | Mag:%.0f | Swp:%d | Spoil:%d | Rot:%d | Goon:%d\n",
           s->ip, op, s->pitch, s->pointer,
           s->memory[s->pointer].real, s->memory[s->pointer].imag,
           mag, s->swapped, s->spoiled, s->brainrot_count % 2, s->gooner_activated);
}

unsigned int sigma_checksum(void* data, int len) {
    unsigned int sum = 0xDEADBEEF;
    unsigned char* bytes = (unsigned char*)data;
    for (int i = 0; i < len; i++) {
        sum = (sum << 5) + sum + bytes[i];
        sum ^= 0x69696969;
    }
    return sum;
}

void sigma_net_init(PlayerProfile* profile) {
    memset(&g_sigma_net, 0, sizeof(g_sigma_net));
    g_sigma_net.socket_fd = -1;
    g_sigma_net.connected = 0;
    g_sigma_net.peer_count = 0;
    
    strcpy(profile->player_name, "PLAYER_1");
    profile->skill_level = 100;
    profile->rage_quit_timer = 0;
    profile->packet_loss = 0;
    profile->latency_ms = 0;
}

int sigma_connect(const char* server_ip, int port) {
    g_sigma_net.socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (g_sigma_net.socket_fd < 0) {
        printf("Failed to create socket\n");
        return 0;
    }
    
    int broadcast_enable = 1;
    setsockopt(g_sigma_net.socket_fd, SOL_SOCKET, SO_BROADCAST, 
               &broadcast_enable, sizeof(broadcast_enable));
    
    memset(&g_sigma_net.addr, 0, sizeof(g_sigma_net.addr));
    g_sigma_net.addr.sin_family = AF_INET;
    g_sigma_net.addr.sin_addr.s_addr = inet_addr(server_ip);
    g_sigma_net.addr.sin_port = htons(port);
    
    struct sockaddr_in bind_addr;
    bind_addr.sin_family = AF_INET;
    bind_addr.sin_addr.s_addr = INADDR_ANY;
    bind_addr.sin_port = htons(42069 + (rand() % 1000));
    
    bind(g_sigma_net.socket_fd, (struct sockaddr*)&bind_addr, sizeof(bind_addr));
    
    g_sigma_net.connected = 1;
    strcpy(g_sigma_net.server_ip, server_ip);
    g_sigma_net.server_port = port;
    
    printf("Connected to %s:%d as '%s'\n", server_ip, port, g_profile.player_name);
    
    char announce[256];
    snprintf(announce, sizeof(announce), "%s_SKILL_%d", 
             g_profile.player_name, g_profile.skill_level);
    sigma_broadcast_action(announce);
    
    return 1;
}

void sigma_broadcast_memory(Skibidi* s, int index) {
    if (!g_sigma_net.connected) return;
    
    if (rand() % 100 < g_profile.packet_loss) {
        return;
    }
    
    NetworkPacket pkt;
    memset(&pkt, 0, sizeof(pkt));
    pkt.type = PACKET_MEMORY_UPDATE;
    pkt.player_id = (unsigned char)(g_profile.skill_level / 10);
    pkt.memory_index = index;
    pkt.value = s->memory[index];
    pkt.brainrot_count = s->brainrot_count;
    snprintf(pkt.flex_message, sizeof(pkt.flex_message), 
             "%s (skill: %d)", g_profile.player_name, g_profile.skill_level);
    pkt.checksum = sigma_checksum(&pkt, sizeof(pkt) - 4);
    
    pthread_mutex_lock(&net_mutex);
    for (int i = 0; i < g_sigma_net.peer_count; i++) {
        sendto(g_sigma_net.socket_fd, &pkt, sizeof(pkt), 0,
               (struct sockaddr*)&g_sigma_net.peers[i], 
               sizeof(g_sigma_net.peers[i]));
    }
    pthread_mutex_unlock(&net_mutex);
}

void sigma_broadcast_action(const char* action) {
    if (!g_sigma_net.connected) return;
    
    NetworkPacket pkt;
    memset(&pkt, 0, sizeof(pkt));
    pkt.type = PACKET_SIGMA_FLEX;
    snprintf(pkt.flex_message, sizeof(pkt.flex_message), "%s", action);
    pkt.checksum = sigma_checksum(&pkt, sizeof(pkt) - 4);
    
    pthread_mutex_lock(&net_mutex);
    for (int i = 0; i < g_sigma_net.peer_count; i++) {
        sendto(g_sigma_net.socket_fd, &pkt, sizeof(pkt), 0,
               (struct sockaddr*)&g_sigma_net.peers[i], 
               sizeof(g_sigma_net.peers[i]));
    }
    pthread_mutex_unlock(&net_mutex);
}

void* sigma_receive_thread(void* arg) {
    Skibidi* s = (Skibidi*)arg;
    NetworkPacket pkt;
    struct sockaddr_in sender_addr;
    socklen_t addr_len = sizeof(sender_addr);
    
    while (g_sigma_net.running) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(g_sigma_net.socket_fd, &fds);
        
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 100000;
        
        int ret = select(g_sigma_net.socket_fd + 1, &fds, NULL, NULL, &tv);
        if (ret <= 0) continue;
        
        int n = recvfrom(g_sigma_net.socket_fd, &pkt, sizeof(pkt), 0,
                         (struct sockaddr*)&sender_addr, &addr_len);
        
        if (n <= 0) continue;
        
        unsigned int received_csum = pkt.checksum;
        pkt.checksum = 0;
        if (sigma_checksum(&pkt, sizeof(pkt)) != received_csum) {
            continue;
        }
        pkt.checksum = received_csum;
        
        int known = 0;
        pthread_mutex_lock(&net_mutex);
        for (int i = 0; i < g_sigma_net.peer_count; i++) {
            if (g_sigma_net.peers[i].sin_addr.s_addr == sender_addr.sin_addr.s_addr) {
                known = 1;
                break;
            }
        }
        if (!known && g_sigma_net.peer_count < 16) {
            g_sigma_net.peers[g_sigma_net.peer_count++] = sender_addr;
            printf("New peer joined (Total: %d)\n", g_sigma_net.peer_count);
        }
        pthread_mutex_unlock(&net_mutex);
        
        if (pkt.type == PACKET_MEMORY_UPDATE) {
            pthread_mutex_lock(&net_mutex);
            if (rand() % 100 < 30) {
                s->memory[pkt.memory_index] = pkt.value;
            }
            pthread_mutex_unlock(&net_mutex);
        }
        else if (pkt.type == PACKET_BRAINROT) {
            if (!s->gooner_activated && (rand() % 100 < 50)) {
                brainrot(s);
            }
        }
        else if (pkt.type == PACKET_GOONER) {
            if (!s->gooner_activated && (rand() % 100 < 20)) {
                gooner(s);
            }
        }
    }
    return NULL;
}

void* sigma_send_thread(void* arg) {
    Skibidi* s = (Skibidi*)arg;
    int last_brainrot = 0;
    
    while (g_sigma_net.running) {
        sleep(1);
        
        if (!g_sigma_net.connected) continue;
        
        NetworkPacket pkt;
        memset(&pkt, 0, sizeof(pkt));
        pkt.type = PACKET_POINTER_MOVE;
        pkt.memory_index = s->pointer;
        pkt.checksum = sigma_checksum(&pkt, sizeof(pkt) - 4);
        
        pthread_mutex_lock(&net_mutex);
        for (int i = 0; i < g_sigma_net.peer_count; i++) {
            sendto(g_sigma_net.socket_fd, &pkt, sizeof(pkt), 0,
                   (struct sockaddr*)&g_sigma_net.peers[i], 
                   sizeof(g_sigma_net.peers[i]));
        }
        pthread_mutex_unlock(&net_mutex);
        
        if (s->brainrot_count != last_brainrot) {
            pkt.type = PACKET_BRAINROT;
            pkt.brainrot_count = s->brainrot_count;
            pkt.checksum = sigma_checksum(&pkt, sizeof(pkt) - 4);
            
            pthread_mutex_lock(&net_mutex);
            for (int i = 0; i < g_sigma_net.peer_count; i++) {
                sendto(g_sigma_net.socket_fd, &pkt, sizeof(pkt), 0,
                       (struct sockaddr*)&g_sigma_net.peers[i], 
                       sizeof(g_sigma_net.peers[i]));
            }
            pthread_mutex_unlock(&net_mutex);
            last_brainrot = s->brainrot_count;
        }
        
        if (g_profile.skill_level < 50) {
            g_profile.latency_ms = 500;
        } else if (g_profile.skill_level < 80) {
            g_profile.latency_ms = 200;
        } else {
            g_profile.latency_ms = 0;
        }
    }
    return NULL;
}

void sigma_rage_quit_check(PlayerProfile* p) {
    if (p->skill_level <= 0) {
        printf("\nRAGE QUIT\n");
        exit(1);
    }
}

void sigma_flex(int skill_level) {
    char flex_msg[256];
    const char* flex_lines[] = {
        "packet loss",
        "skill issue",
        "lag spike",
        "buffering",
        "disconnected"
    };
    
    snprintf(flex_msg, sizeof(flex_msg), "%s: %s (skill: %d)", 
             g_profile.player_name, 
             flex_lines[rand() % 5],
             skill_level);
    
    sigma_broadcast_action(flex_msg);
    printf("FLEX: %s\n", flex_msg);
}

int sigma_peer_discovery(void) {
    if (!g_sigma_net.connected) return 0;
    
    NetworkPacket discover;
    memset(&discover, 0, sizeof(discover));
    discover.type = 0xFF;
    snprintf(discover.flex_message, sizeof(discover.flex_message), 
             "DISCOVER_%s", g_profile.player_name);
    
    int broadcast_sock = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in broadcast_addr;
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_addr.s_addr = INADDR_BROADCAST;
    broadcast_addr.sin_port = htons(42069);
    
    setsockopt(broadcast_sock, SOL_SOCKET, SO_BROADCAST, &(int){1}, sizeof(int));
    sendto(broadcast_sock, &discover, sizeof(discover), 0,
           (struct sockaddr*)&broadcast_addr, sizeof(broadcast_addr));
    close(broadcast_sock);
    
    printf("Searching for peers...\n");
    return 1;
}

void execute(Skibidi* s, const char* op) {
    if (s->debug) print_debug(s, op);
    
    s->undefined_behavior = (s->swapped && s->spoiled) ? 1 : 0;
    
    if (strcmp(op, "magical white liquid") == 0) {
        return;
    }
    
    if (strcmp(op, "brainrot") == 0) {
        if (g_sigma_net.connected && g_profile.skill_level < 80) {
            return;
        }
        brainrot(s);
        if (g_sigma_net.connected) {
            g_profile.skill_level += 1;
            sigma_broadcast_action("BRAINROT");
        }
        return;
    }
    
    if (strcmp(op, "gooner") == 0) {
        gooner(s);
        if (g_sigma_net.connected) sigma_broadcast_action("GOONER");
        return;
    }
    
    if (strcmp(op, "sigmaflex") == 0) {
        sigma_flex(g_profile.skill_level);
        return;
    }
    
    if (s->gooner_activated) {
        return;
    }
    
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
        if (g_sigma_net.connected) sigma_broadcast_memory(s, s->pointer);
    }
    else if (strcmp(op, "bop") == 0) {
        if (s->spoiled && !s->undefined_behavior) {
            s->memory[s->pointer].imag += 1.0;
        } else {
            s->memory[s->pointer].imag -= 1.0;
        }
        if (g_sigma_net.connected) sigma_broadcast_memory(s, s->pointer);
    }
    else if (strcmp(op, "skibidi") == 0) {
        skibidi_chaos(s);
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
        } else {
            s->pointer = (s->pointer - 1 + MEMORY_SIZE) % MEMORY_SIZE;
        }
    }
    else if (strcmp(op, "toilet") == 0) {
        if (s->stack_ptr < STACK_SIZE) {
            s->stack[s->stack_ptr++] = s->memory[s->pointer];
            complex_zero(&s->memory[s->pointer]);
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
    }
    else if (strcmp(op, "sigma") == 0) {
        char ch = getchar();
        if (ch == EOF) ch = 0;
        s->memory[s->pointer].real = (double)ch;
        s->memory[s->pointer].imag = 0;
    }
    else if (strcmp(op, "ohio") == 0) {
        double mag = complex_magnitude(s->memory[s->pointer]);
        int jump = (int)floor(mag);
        
        if (s->spoiled && !s->undefined_behavior) {
            if (jump > 0) {
                s->ip += jump;
            }
        } else {
            if (jump > 0 && jump <= s->ip) {
                s->ip -= jump;
            }
        }
    }
    else if (strcmp(op, "67") == 0) {
        if (s->undefined_behavior) {
            if (rand() % 2) {
                s->swapped = !s->swapped;
            }
        } else if (!s->spoiled) {
            s->swapped = !s->swapped;
        }
    }
    else if (strcmp(op, "mango") == 0) {
        if (s->undefined_behavior) {
            if (rand() % 2) {
                s->spoiled = !s->spoiled;
            }
        } else {
            s->spoiled = !s->spoiled;
        }
    }
    else if (strcmp(op, "diddy") == 0) {
        if (s->spoiled || s->undefined_behavior) {
            fprintf(stderr, "\nCRASH\n");
            if (g_sigma_net.connected) {
                g_profile.skill_level -= 50;
                sigma_rage_quit_check(&g_profile);
            }
            exit(1);
        }
        printf("milk");
        fflush(stdout);
    }
}

void run(Skibidi* s) {
    s->ip = 0;
    while (s->ip < s->program_size) {
        execute(s, s->program[s->ip]);
        s->ip++;
        
        if (g_sigma_net.connected) {
            sigma_rage_quit_check(&g_profile);
        }
    }
}

void free_program(Skibidi* s) {
    for (int i = 0; i < s->program_size; i++) {
        free(s->program[i]);
    }
    free(s->program);
}

void create_demo(const char* fname) {
    FILE* fp = fopen(fname, "w");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "brainrot\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "gooner\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "diddy\n");
    fclose(fp);
}

void create_evil_hello(const char* fname) {
    FILE* fp = fopen(fname, "w");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "skibidi grimace\n");
    fprintf(fp, "dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop dop rizz\n");
    fprintf(fp, "diddy\n");
    fclose(fp);
}

int main(int argc, char* argv[]) {
    srand(time(NULL));
    int debug = 0;
    char* filename = NULL;
    char* server_ip = NULL;
    int server_port = 42069;
    
    sigma_net_init(&g_profile);
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--debug") == 0) debug = 1;
        else if (strcmp(argv[i], "--connect") == 0 && i+1 < argc) {
            server_ip = argv[++i];
        } else if (strcmp(argv[i], "--port") == 0 && i+1 < argc) {
            server_port = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--skill") == 0 && i+1 < argc) {
            g_profile.skill_level = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--name") == 0 && i+1 < argc) {
            strncpy(g_profile.player_name, argv[++i], 31);
        } else if (strcmp(argv[i], "--demo") == 0) {
            filename = "skibidi_demo.skb";
            create_demo(filename);
        } else if (strcmp(argv[i], "--evil-hello") == 0) {
            filename = "evil_hello.skb";
            create_evil_hello(filename);
        } else if (argv[i][0] != '-') {
            filename = argv[i];
        }
    }
    
    if (server_ip) {
        if (!sigma_connect(server_ip, server_port)) {
            fprintf(stderr, "Connection failed\n");
            return 1;
        }
        
        Skibidi skibidi_dummy;
        interpreter_init(&skibidi_dummy, debug);
        g_sigma_net.running = 1;
        pthread_create(&g_sigma_net.recv_thread, NULL, sigma_receive_thread, &skibidi_dummy);
        pthread_create(&g_sigma_net.send_thread, NULL, sigma_send_thread, &skibidi_dummy);
        
        sigma_peer_discovery();
        sleep(1);
    }
    
    if (!filename) {
        printf("Skibidi v5.0\n");
        printf("Commands: dop, bop, skibidi, grimace, toilet, rizz, sigma, ohio\n");
        printf("          67, mango, diddy, brainrot, gooner, sigmaflex\n");
        printf("\nUsage: %s <file.skb> [--debug]\n", argv[0]);
        printf("       %s --connect <ip> [--port <port>] [--name <name>]\n", argv[0]);
        printf("       %s --demo\n", argv[0]);
        return 1;
    }
    
    Skibidi skibidi;
    interpreter_init(&skibidi, debug);
    
    if (!load_program(&skibidi, filename)) {
        fprintf(stderr, "Failed to load: %s\n", filename);
        return 1;
    }
    
    printf("=== Skibidi v5.0 ===\n");
    if (server_ip) {
        printf("Multiplayer: connected to %s:%d\n", server_ip, server_port);
    } else {
        printf("Offline mode\n");
    }
    printf("----------------------------------------\n\n");
    
    run(&skibidi);
    
    printf("\n----------------------------------------\n");
    printf("Output: %s\n", skibidi.output);
    
    if (g_sigma_net.connected) {
        g_sigma_net.running = 0;
        pthread_join(g_sigma_net.recv_thread, NULL);
        pthread_join(g_sigma_net.send_thread, NULL);
        close(g_sigma_net.socket_fd);
    }
    
    free_program(&skibidi);
    return 0;
}