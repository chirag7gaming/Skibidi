/*
 * Skibidi v4.1 - "SIGMABOII Online" Edition
 * Now with 100% more packet loss and skill issues
 * 
 * Compile: gcc -o skibidi skibidi_v4.1.c -lm -lssl -lcrypto -lpthread
 * 
 * Additional deps: sudo apt install libwebsockets-dev (if you're not a beta)
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

/* ... (keep all previous defines and structs) ... */

/* NEW: SIGMABOII Network Structures */
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
    int skill_level;      /* 0 = beta, 100 = SIGMA */
    int rage_quit_timer;
    int packet_loss;      /* Simulated for "hard" mode */
    int latency_ms;       /* Added for realism */
} PlayerProfile;

/* NEW: Network packet types */
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
    unsigned int checksum;  /* "Security" */
} NetworkPacket;

/* Global sigma network state */
SigmaNet g_sigma_net;
PlayerProfile g_profile;
pthread_mutex_t net_mutex = PTHREAD_MUTEX_INITIALIZER;

/* Function prototypes for sigma features */
void sigma_net_init(PlayerProfile* profile);
int sigma_connect(const char* server_ip, int port);
void sigma_broadcast_memory(Skibidi* s, int index);
void sigma_broadcast_action(const char* action);
void sigma_sync_all(Skibidi* s);
void* sigma_receive_thread(void* arg);
void* sigma_send_thread(void* arg);
void sigma_handle_packet(NetworkPacket* pkt, Skibidi* s);
unsigned int sigma_checksum(void* data, int len);
void sigma_rage_quit_check(PlayerProfile* p);
void sigma_flex(int skill_level);
int sigma_peer_discovery(void);

/* Calculate "sigma checksum" (totally secure, don't hack bro) */
unsigned int sigma_checksum(void* data, int len) {
    unsigned int sum = 0xDEADBEEF;  /* SIGMA seed */
    unsigned char* bytes = (unsigned char*)data;
    for (int i = 0; i < len; i++) {
        sum = (sum << 5) + sum + bytes[i];
        sum ^= 0x69696969;  /* Hard-coded sigma value */
    }
    return sum;
}

/* Initialize sigma networking with HARD defaults */
void sigma_net_init(PlayerProfile* profile) {
    memset(&g_sigma_net, 0, sizeof(g_sigma_net));
    g_sigma_net.socket_fd = -1;
    g_sigma_net.connected = 0;
    g_sigma_net.peer_count = 0;
    
    /* Sigma profile defaults */
    strcpy(profile->player_name, "SIGMA_BOI");
    profile->skill_level = 100;     /* MAXIMUM SKILL */
    profile->rage_quit_timer = 0;
    profile->packet_loss = 0;       /* Start perfect, get worse */
    profile->latency_ms = 0;
}

/* Connect to sigma server (or peer-to-peer if you're alpha enough) */
int sigma_connect(const char* server_ip, int port) {
    g_sigma_net.socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (g_sigma_net.socket_fd < 0) {
        printf("❌ SIGMA FAILED: Can't even create socket (skill issue)\n");
        return 0;
    }
    
    /* Enable broadcast for maximum sigma energy */
    int broadcast_enable = 1;
    setsockopt(g_sigma_net.socket_fd, SOL_SOCKET, SO_BROADCAST, 
               &broadcast_enable, sizeof(broadcast_enable));
    
    memset(&g_sigma_net.addr, 0, sizeof(g_sigma_net.addr));
    g_sigma_net.addr.sin_family = AF_INET;
    g_sigma_net.addr.sin_addr.s_addr = inet_addr(server_ip);
    g_sigma_net.addr.sin_port = htons(port);
    
    /* Bind to random high port (sigma ports only) */
    struct sockaddr_in bind_addr;
    bind_addr.sin_family = AF_INET;
    bind_addr.sin_addr.s_addr = INADDR_ANY;
    bind_addr.sin_port = htons(42069 + (rand() % 1000));  /* 42069-43068 sigma range */
    
    if (bind(g_sigma_net.socket_fd, (struct sockaddr*)&bind_addr, sizeof(bind_addr)) < 0) {
        printf("⚠️ Port binding failed, using any port (beta behavior)\n");
    }
    
    g_sigma_net.connected = 1;
    strcpy(g_sigma_net.server_ip, server_ip);
    g_sigma_net.server_port = port;
    
    printf("🔥 SIGMA CONNECTED to %s:%d as '%s'\n", 
           server_ip, port, g_profile.player_name);
    
    /* Announce presence with sigma energy */
    char announce[256];
    snprintf(announce, sizeof(announce), 
             "SIGMA_BOI_%s_SKILL_%d", 
             g_profile.player_name, g_profile.skill_level);
    sigma_broadcast_action(announce);
    
    return 1;
}

/* Broadcast memory state to all sigma peers */
void sigma_broadcast_memory(Skibidi* s, int index) {
    if (!g_sigma_net.connected) return;
    
    /* Simulate packet loss for "HARD" mode */
    if (rand() % 100 < g_profile.packet_loss) {
        if (s->debug) printf("📡 PACKET LOSS: Sigma energy dissipated\n");
        return;
    }
    
    NetworkPacket pkt;
    memset(&pkt, 0, sizeof(pkt));
    pkt.type = PACKET_MEMORY_UPDATE;
    pkt.player_id = (unsigned char)(g_profile.skill_level / 10); /* Flex */
    pkt.memory_index = index;
    pkt.value = s->memory[index];
    pkt.brainrot_count = s->brainrot_count;
    snprintf(pkt.flex_message, sizeof(pkt.flex_message), 
             "%s just flexed on you (skill: %d)", 
             g_profile.player_name, g_profile.skill_level);
    pkt.checksum = sigma_checksum(&pkt, sizeof(pkt) - 4);
    
    /* Send to all peers */
    pthread_mutex_lock(&net_mutex);
    for (int i = 0; i < g_sigma_net.peer_count; i++) {
        sendto(g_sigma_net.socket_fd, &pkt, sizeof(pkt), 0,
               (struct sockaddr*)&g_sigma_net.peers[i], 
               sizeof(g_sigma_net.peers[i]));
    }
    pthread_mutex_unlock(&net_mutex);
    
    if (s->debug) printf("📡 SIGMA BROADCAST: Memory[%d] = (%.1f+%.1fi)\n", 
                         index, pkt.value.real, pkt.value.imag);
}

/* Broadcast any action for maximum sigma sync */
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

/* Receive thread - handles sigma packets with HARD skills */
void* sigma_receive_thread(void* arg) {
    Skibidi* s = (Skibidi*)arg;
    NetworkPacket pkt;
    struct sockaddr_in sender_addr;
    socklen_t addr_len = sizeof(sender_addr);
    char buffer[2048];
    
    while (g_sigma_net.running) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(g_sigma_net.socket_fd, &fds);
        
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 100000;  /* 100ms timeout - FAST reflexes */
        
        int ret = select(g_sigma_net.socket_fd + 1, &fds, NULL, NULL, &tv);
        if (ret <= 0) continue;
        
        int n = recvfrom(g_sigma_net.socket_fd, &pkt, sizeof(pkt), 0,
                         (struct sockaddr*)&sender_addr, &addr_len);
        
        if (n <= 0) continue;
        
        /* Verify checksum (hackers will never break this) */
        unsigned int received_csum = pkt.checksum;
        pkt.checksum = 0;
        if (sigma_checksum(&pkt, sizeof(pkt)) != received_csum) {
            if (s->debug) printf("⚠️ HACKER DETECTED! Checksum mismatch (nice try)\n");
            continue;
        }
        pkt.checksum = received_csum;
        
        /* Add new peer if unknown */
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
            printf("👥 NEW SIGMA PEER JOINED! (Total: %d)\n", g_sigma_net.peer_count);
        }
        pthread_mutex_unlock(&net_mutex);
        
        sigma_handle_packet(&pkt, s);
    }
    return NULL;
}

/* Handle incoming sigma packets - MERGE other players' state */
void sigma_handle_packet(NetworkPacket* pkt, Skibidi* s) {
    switch(pkt->type) {
        case PACKET_MEMORY_UPDATE:
            /* COMPETITIVE MULTIPLAYER: Other player's memory overwrites yours */
            /* This is the "HARD" part - other players can grief your state */
            pthread_mutex_lock(&net_mutex);
            if (rand() % 100 < 30) {  /* 30% chance of griefing - SKILL ISSUE */
                s->memory[pkt->memory_index] = pkt->value;
                if (s->debug) {
                    printf("💀 GRIEFED! Player %d set memory[%d] = (%.1f+%.1fi)\n",
                           pkt->player_id, pkt->memory_index, 
                           pkt->value.real, pkt->value.imag);
                }
            }
            pthread_mutex_unlock(&net_mutex);
            break;
            
        case PACKET_BRAINROT:
            /* BRAINROT SPREADS VIA NETWORK */
            if (!s->gooner_activated && (rand() % 100 < 50)) {
                printf("🧠 NETWORK BRAINROT! Other player infected you!\n");
                brainrot(s);
            }
            break;
            
        case PACKET_GOONER:
            /* GOONER VIRUS */
            if (!s->gooner_activated && (rand() % 100 < 20)) {
                printf("💦 NETWORK GOONER! Your program is now gooned!\n");
                gooner(s);
            }
            break;
            
        case PACKET_SIGMA_FLEX:
            if (s->debug) {
                printf("💪 SIGMA FLEX: %s\n", pkt->flex_message);
            }
            break;
            
        case PACKET_SKILL_ISSUE:
            printf("🎮 SKILL ISSUE DETECTED: %s\n", pkt->flex_message);
            g_profile.skill_level = (g_profile.skill_level * 0.9); /* Lose skill */
            break;
    }
}

/* Send thread - continuously sync state with sigma energy */
void* sigma_send_thread(void* arg) {
    Skibidi* s = (Skibidi*)arg;
    int last_brainrot = 0;
    
    while (g_sigma_net.running) {
        sleep(1);  /* Sync every second - FAST ENOUGH FOR SIGMAS */
        
        if (!g_sigma_net.connected) continue;
        
        /* Broadcast current pointer position */
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
        
        /* Check if brainrot spread */
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
        
        /* Simulate latency increasing with skill loss */
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

/* Rage quit detection - TRUE SIGMA NEVER RAGE QUITS */
void sigma_rage_quit_check(PlayerProfile* p) {
    if (p->skill_level <= 0) {
        printf("\n💢 RAGE QUIT DETECTED! Skill level: 0\n");
        printf("💢 You are now a BETA. The program will self-destruct.\n");
        printf("💢 (This is why we can't have nice things)\n");
        exit(1);
    }
}

/* FLEX on other players - demonstrates absolute sigma energy */
void sigma_flex(int skill_level) {
    char flex_msg[256];
    const char* flex_lines[] = {
        "Your code is cringe",
        "I wrote this in 5 minutes with 99% packet loss",
        "Skill issue + ratio + you fell off",
        "My brainrot is bigger than your entire program",
        "Stay mad, I'm sigma",
        "L + bozo + didn't ask + cope harder"
    };
    
    snprintf(flex_msg, sizeof(flex_msg), "%s: %s (skill: %d)", 
             g_profile.player_name, 
             flex_lines[rand() % 6],
             skill_level);
    
    sigma_broadcast_action(flex_msg);
    printf("💪 SIGMA FLEX: %s\n", flex_msg);
}

/* Discover peers via sigma broadcast */
int sigma_peer_discovery(void) {
    if (!g_sigma_net.connected) return 0;
    
    /* Send discovery packet */
    NetworkPacket discover;
    memset(&discover, 0, sizeof(discover));
    discover.type = 0xFF;  /* Discovery magic */
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
    
    printf("🔍 SIGMA DISCOVERY: Searching for other sigmas...\n");
    return 1;
}

/* Modified execute function with sigma sync */
void execute_sigma(Skibidi* s, const char* op) {
    /* Original execute logic here... (same as before) */
    
    /* Add sigma broadcasting on memory modifications */
    if (strcmp(op, "dop") == 0 || strcmp(op, "bop") == 0) {
        sigma_broadcast_memory(s, s->pointer);
    }
    
    /* Add rage quit on diddy crash */
    if (strcmp(op, "diddy") == 0 && (s->spoiled || s->undefined_behavior)) {
        g_profile.skill_level -= 50;
        sigma_broadcast_action("RAGE QUIT IMMINENT");
        sigma_rage_quit_check(&g_profile);
    }
    
    /* Skill check on brainrot */
    if (strcmp(op, "brainrot") == 0) {
        if (g_profile.skill_level < 80) {
            printf("⚠️ Low skill brainrot! Effect reduced!\n");
            return;  /* Can't brainrot if you're not sigma enough */
        }
        g_profile.skill_level += 1;  /* Brainrot increases skill (somehow) */
        sigma_broadcast_action("BRAINROT ACTIVATED - SKILL UP");
    }
    
    /* Sigma flex command - NEW */
    if (strcmp(op, "sigmaflex") == 0) {
        sigma_flex(g_profile.skill_level);
        return;
    }
}

/* Modified main with sigma networking */
int main(int argc, char* argv[]) {
    srand(time(NULL));
    int debug = 0;
    char* filename = NULL;
    char* server_ip = NULL;
    int server_port = 42069;
    
    /* Parse sigma args */
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
    
    /* Initialize sigma */
    sigma_net_init(&g_profile);
    
    /* Connect to sigma server if specified */
    if (server_ip) {
        if (!sigma_connect(server_ip, server_port)) {
            fprintf(stderr, "❌ Failed to connect to sigma server\n");
            return 1;
        }
        
        /* Start network threads */
        g_sigma_net.running = 1;
        pthread_create(&g_sigma_net.recv_thread, NULL, sigma_receive_thread, &skibidi);
        pthread_create(&g_sigma_net.send_thread, NULL, sigma_send_thread, &skibidi);
        
        /* Discover peers */
        sigma_peer_discovery();
        sleep(1);
    }
    
    /* Rest of original main... */
    Skibidi skibidi;
    interpreter_init(&skibidi, debug);
    
    if (!load_program(&skibidi, filename)) {
        fprintf(stderr, "Failed to load: %s\n", filename);
        return 1;
    }
    
    printf("=== Skibidi v4.1 SIGMABOII Online ===\n");
    printf("🎮 Player: %s (Skill: %d)\n", g_profile.player_name, g_profile.skill_level);
    if (server_ip) {
        printf("🌐 ONLINE MODE - Connected to %s:%d\n", server_ip, server_port);
        printf("⚠️ Other players can GRIEF your memory!\n");
        printf("⚠️ Network brainrot/gooner can INFECT you!\n");
    } else {
        printf("💿 OFFLINE MODE - Add --connect <ip> for sigma multiplayer\n");
    }
    printf("----------------------------------------\n\n");
    
    /* Run with sigma integration */
    skibidi.ip = 0;
    while (skibidi.ip < skibidi.program_size) {
        execute_sigma(&skibidi, skibidi.program[skibidi.ip]);
        skibidi.ip++;
        
        /* Check rage quit every iteration */
        sigma_rage_quit_check(&g_profile);
    }
    
    /* Cleanup */
    g_sigma_net.running = 0;
    if (server_ip) {
        pthread_join(g_sigma_net.recv_thread, NULL);
        pthread_join(g_sigma_net.send_thread, NULL);
        close(g_sigma_net.socket_fd);
    }
    
    free_program(&skibidi);
    return 0;
}