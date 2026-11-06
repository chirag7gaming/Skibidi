Python Port:
import math
import hashlib
import random
import socket
import struct
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import List, Optional


class Complex:
    def __init__(self, real: float = 0.0, imag: float = 0.0):
        self.real = real
        self.imag = imag

    def zero(self):
        self.real = 0.0
        self.imag = 0.0

    def magnitude(self) -> float:
        return math.sqrt(self.real * self.real + self.imag * self.imag)

    def swap(self):
        return Complex(self.imag, self.real)


@dataclass
class Skibidi:
    memory: List[Complex] = field(default_factory=lambda: [Complex() for _ in range(256)])
    pointer: int = 0
    pitch: int = 440
    stack: List[Complex] = field(default_factory=lambda: [Complex() for _ in range(1024)])
    stack_ptr: int = 0
    program: Optional[List[str]] = None
    program_size: int = 0
    ip: int = 0
    debug: int = 0
    output: str = ""
    rng_state: bytearray = field(default_factory=lambda: bytearray(16))
    swapped: int = 0
    spoiled: int = 0
    undefined_behavior: int = 0
    brainrot_count: int = 0
    gooner_activated: int = 0
    diddy_gooner_inside: int = 0
    gooner_custom_text: Optional[str] = None
    input_buffer: str = ""
    input_pos: int = 0
    
    # Epstein nested execution
    nested_depth: int = 0
    nested_ops: List[str] = field(default_factory=list)
    nested_ip: List[int] = field(default_factory=list)
    in_epstein: int = 0
    epstein_target_op: Optional[str] = None
    
    label_map: dict = field(default_factory=dict)
    label_count: int = 0


@dataclass
class SigmaNet:
    socket_fd: Optional[socket.socket] = None
    addr: Optional[tuple] = None
    server_ip: str = ""
    server_port: int = 0
    connected: int = 0
    peer_count: int = 0
    peer_names: List[str] = field(default_factory=lambda: [""] * 16)
    peers: List[tuple] = field(default_factory=list)
    recv_thread: Optional[threading.Thread] = None
    send_thread: Optional[threading.Thread] = None
    running: int = 0


@dataclass
class PlayerProfile:
    player_name: str = ""
    skill_level: int = 100
    rage_quit_timer: int = 0
    packet_loss: int = 0
    latency_ms: int = 0


@dataclass
class NetworkPacket:
    type: int = 0
    player_id: int = 0
    memory_index: int = 0
    value: Complex = field(default_factory=Complex)
    brainrot_count: int = 0
    flex_message: str = ""
    checksum: int = 0


g_sigma_net = SigmaNet()
g_profile = PlayerProfile()
net_mutex = threading.Lock()


def md5_update(state: bytearray):
    md5 = hashlib.md5()
    md5.update(state)
    new_hash = md5.digest()
    for i in range(16):
        state[i] = new_hash[i]


def hash_to_pitch(state: bytearray) -> int:
    val = (state[0] << 24) | (state[1] << 16) | (state[2] << 8) | state[3]
    return 200 + (abs(val) % 600)


def skibidi_chaos(s: Skibidi):
    md5_update(s.rng_state)
    s.pitch = hash_to_pitch(s.rng_state)


def interpreter_init(s: Skibidi, debug: int):
    s.memory = [Complex() for _ in range(256)]
    s.pointer = 0
    s.pitch = 440
    s.stack = [Complex() for _ in range(1024)]
    s.stack_ptr = 0
    s.program = None
    s.program_size = 0
    s.ip = 0
    s.debug = debug
    s.output = ""
    s.rng_state = bytearray(16)
    s.swapped = 0
    s.spoiled = 0
    s.undefined_behavior = 0
    s.brainrot_count = 0
    s.gooner_activated = 0
    s.diddy_gooner_inside = 0
    s.gooner_custom_text = None
    s.input_buffer = ""
    s.input_pos = 0
    s.nested_depth = 0
    s.nested_ops = []
    s.nested_ip = []
    s.in_epstein = 0
    s.epstein_target_op = None
    s.label_map = {}
    s.label_count = 0


def brainrot(s: Skibidi):
    if s.program_size <= 1:
        return
    
    for i in range(s.program_size // 2):
        temp = s.program[i]
        s.program[i] = s.program[s.program_size - 1 - i]
        s.program[s.program_size - 1 - i] = temp
    
    s.brainrot_count += 1
    s.ip = 0
    s.debug = 0 if s.debug else 1


def gooner(s: Skibidi):
    if s.gooner_activated:
        return
    
    # Special: If gooner is called from INSIDE diddy
    if s.diddy_gooner_inside:
        final_msg = ""
        
        if s.gooner_custom_text:
            final_msg = f"[DIDDY_GOONER_INSIDE]: {s.gooner_custom_text}"
        else:
            for i in range(256):
                mag = s.memory[i].magnitude()
                if 0 < mag < 128:
                    final_msg += chr(int(mag) % 95 + 32)
                if 0 < s.memory[i].real < 128:
                    final_msg += chr(int(s.memory[i].real) % 95 + 32)
        
        s.output += final_msg + "\n"
        print(f"\n🔥 [DIDDY+GOONER INSIDE]: {final_msg}")
        sys.stdout.flush()
        
        s.diddy_gooner_inside = 0
        s.gooner_custom_text = None
    
    # Destroy everything sequentially until we find and destroy diddy
    first_diddy_index = None
    
    for i, op in enumerate(s.program):
        if op == "diddy":
            first_diddy_index = i
            break
    
    if first_diddy_index is not None and not s.diddy_gooner_inside:
        print(f"\n⚠️ Gooner wave: Destroying instructions 0..{first_diddy_index} (including diddy)")
        
        for i in range(first_diddy_index + 1):
            if s.program[i] != "magical white liquid":
                s.program[i] = "magical white liquid"
                if s.debug:
                    print(f"   Destroyed [{i}]: {'diddy (STOP)' if i == first_diddy_index else 'instruction'}")
        
        print("⚠️ Gooner stopped after destroying diddy!")
        print(f"   Remaining program instructions: {len(s.program) - (first_diddy_index + 1)}")
        
        s.ip = first_diddy_index + 1
        return
    
    # No diddy found - normal full destruction
    print("\n⚠️ Gooner: No diddy found - destroying ALL instructions!")
    for i in range(len(s.program)):
        if s.program[i] != "magical white liquid":
            s.program[i] = "magical white liquid"
    
    s.gooner_activated = 1
    s.ip = 0


def epstein_execute_inside(s: Skibidi, outer_op: str, inner_op: str):
    if s.nested_depth >= 16:
        print("Epstein nested too deep!")
        return
    
    s.nested_ops.append(outer_op)
    s.nested_ip.append(s.ip)
    s.nested_depth += 1
    s.in_epstein = 1
    s.epstein_target_op = inner_op
    
    print(f"[Epstein] Running '{inner_op}' inside '{outer_op}' (isolated)")
    
    old_ip = s.ip
    old_in_epstein = s.in_epstein
    s.in_epstein = 2
    
    if inner_op in s.program:
        print(f"[Epstein Inside] Isolated execution: {inner_op}")
    
    s.in_epstein = old_in_epstein
    s.ip = old_ip
    s.nested_depth -= 1
    s.nested_ops.pop()
    s.nested_ip.pop()
    s.in_epstein = 1 if s.nested_depth > 0 else 0
    s.epstein_target_op = None


VALID_OPS = {"dop", "bop", "skibidi", "grimace", "toilet", "rizz",
             "sigma", "ohio", "67", "mango", "diddy", "brainrot",
             "gooner", "magical white liquid", "sigmaflex", "epstein"}


def load_program(s: Skibidi, filename: str) -> bool:
    try:
        with open(filename, 'r') as fp:
            content = fp.read()
    except IOError:
        return False
    
    tokens = []
    for line in content.split('\n'):
        if ';' in line:
            line = line[:line.index(';')]
        for token in line.split():
            clean_token = token.strip()
            if clean_token.endswith(':'):
                label = clean_token[:-1]
                s.label_map[label] = len(tokens)
                s.label_count += 1
            elif clean_token in VALID_OPS:
                tokens.append(clean_token)
            elif clean_token.startswith('"') and clean_token.endswith('"'):
                tokens.append(clean_token)
            elif clean_token:
                print(f"Unknown op: {clean_token}", file=sys.stderr)
                return False
    
    s.program = tokens
    s.program_size = len(tokens)
    return True


def print_debug(s: Skibidi, op: str):
    mag = s.memory[s.pointer].magnitude()
    print(f"[{s.ip}] {op:<20} | P:{s.pitch:3d}Hz | C:{s.pointer:2d} | "
          f"({s.memory[s.pointer].real:.1f}+{s.memory[s.pointer].imag:.1f}i) | "
          f"Mag:{mag:.0f} | Swp:{s.swapped} | Spoil:{s.spoiled} | "
          f"Rot:{s.brainrot_count % 2} | Goon:{s.gooner_activated} | Eps:{s.in_epstein}")


def sigma_checksum(data: bytes) -> int:
    checksum = 0xDEADBEEF
    for byte in data:
        checksum = ((checksum << 5) + checksum + byte) & 0xFFFFFFFF
        checksum ^= 0x69696969
    return checksum


def sigma_net_init(profile: PlayerProfile):
    global g_sigma_net
    g_sigma_net = SigmaNet()
    g_sigma_net.connected = 0
    g_sigma_net.peer_count = 0
    g_sigma_net.peers = []
    
    profile.player_name = "PLAYER_1"
    profile.skill_level = 100
    profile.rage_quit_timer = 0
    profile.packet_loss = 0
    profile.latency_ms = 0


def sigma_connect(server_ip: str, port: int) -> bool:
    global g_sigma_net, g_profile
    
    g_sigma_net.socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    g_sigma_net.socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    g_sigma_net.addr = (server_ip, port)
    bind_port = 42069 + random.randint(0, 999)
    g_sigma_net.socket_fd.bind(('', bind_port))
    
    g_sigma_net.connected = 1
    g_sigma_net.server_ip = server_ip
    g_sigma_net.server_port = port
    
    print(f"Connected to {server_ip}:{port} as '{g_profile.player_name}'")
    return True


def sigma_broadcast_memory(s: Skibidi, index: int):
    if not g_sigma_net.connected:
        return
    if random.randint(0, 99) < g_profile.packet_loss:
        return


def sigma_broadcast_action(action: str):
    if not g_sigma_net.connected:
        return


def sigma_receive_thread(s: Skibidi):
    pass


def sigma_send_thread(s: Skibidi):
    pass


def sigma_rage_quit_check(p: PlayerProfile):
    if p.skill_level <= 0:
        print("\nRAGE QUIT")
        sys.exit(1)


def sigma_flex(skill_level: int):
    flex_lines = ["packet loss", "skill issue", "lag spike", "buffering", "disconnected"]
    flex_msg = f"{g_profile.player_name}: {flex_lines[random.randint(0, 4)]} (skill: {skill_level})"
    print(f"FLEX: {flex_msg}")


def sigma_peer_discovery() -> bool:
    if not g_sigma_net.connected:
        return False
    print("Searching for peers...")
    return True


def execute(s: Skibidi, op: str):
    if s.debug:
        print_debug(s, op)
    
    s.undefined_behavior = 1 if (s.swapped and s.spoiled) else 0
    
    if op == "magical white liquid":
        return
    
    if op == "epstein":
        next_ip = s.ip + 1
        if next_ip < s.program_size:
            inner_op = s.program[next_ip]
            s.ip = next_ip
            epstein_execute_inside(s, "epstein", inner_op)
        else:
            print("Epstein needs an opcode to run inside!")
        return
    
    if op == "brainrot":
        if g_sigma_net.connected and g_profile.skill_level < 80:
            return
        brainrot(s)
        if g_sigma_net.connected:
            g_profile.skill_level += 1
            sigma_broadcast_action("BRAINROT")
        return
    
    if op == "gooner":
        gooner(s)
        if g_sigma_net.connected:
            sigma_broadcast_action("GOONER")
        return
    
    if op == "sigmaflex":
        sigma_flex(g_profile.skill_level)
        return
    
    # DIDDY - runs first
    if op == "diddy":
        next_ip = s.ip + 1
        found_gooner_inside = False
        custom_text = None
        
        if next_ip < s.program_size and s.program[next_ip] == "gooner":
            found_gooner_inside = True
            s.ip = next_ip
            
            text_ip = s.ip + 1
            if text_ip < s.program_size and s.program[text_ip].startswith('"'):
                msg = s.program[text_ip]
                if len(msg) >= 2 and msg[0] == '"' and msg[-1] == '"':
                    custom_text = msg[1:-1]
                s.ip = text_ip
        
        if found_gooner_inside:
            if s.spoiled or s.undefined_behavior:
                print("\nCRASH", file=sys.stderr)
                if g_sigma_net.connected:
                    g_profile.skill_level -= 50
                    sigma_rage_quit_check(g_profile)
                sys.exit(1)
            
            s.diddy_gooner_inside = 1
            s.gooner_custom_text = custom_text
            gooner(s)
        else:
            if s.spoiled or s.undefined_behavior:
                print("\nCRASH", file=sys.stderr)
                if g_sigma_net.connected:
                    g_profile.skill_level -= 50
                    sigma_rage_quit_check(g_profile)
                sys.exit(1)
            
            print("milk milk milk")
        return
    
    if s.gooner_activated:
        return
    
    current = s.memory[s.pointer]
    if s.swapped and not s.undefined_behavior:
        current = current.swap()
    
    if op == "dop":
        if s.spoiled and not s.undefined_behavior:
            s.memory[s.pointer].real -= 1.0
        else:
            s.memory[s.pointer].real += 1.0
        if g_sigma_net.connected:
            sigma_broadcast_memory(s, s.pointer)
    elif op == "bop":
        if s.spoiled and not s.undefined_behavior:
            s.memory[s.pointer].imag += 1.0
        else:
            s.memory[s.pointer].imag -= 1.0
        if g_sigma_net.connected:
            sigma_broadcast_memory(s, s.pointer)
    elif op == "skibidi":
        skibidi_chaos(s)
    elif op == "grimace":
        if s.spoiled and not s.undefined_behavior:
            move_right = (s.pitch < 440)
        else:
            move_right = (s.pitch >= 440)
        if move_right:
            s.pointer = (s.pointer + 1) % 256
        else:
            s.pointer = (s.pointer - 1 + 256) % 256
    elif op == "toilet":
        if s.stack_ptr < 1024:
            s.stack[s.stack_ptr] = Complex(s.memory[s.pointer].real, s.memory[s.pointer].imag)
            s.stack_ptr += 1
            s.memory[s.pointer].zero()
    elif op == "rizz":
        mag = s.memory[s.pointer].magnitude()
        if s.spoiled and not s.undefined_behavior:
            mag *= 2.0
        ascii_val = int(math.floor(mag))
        s.output += chr(ascii_val)
    elif op == "sigma":
        try:
            ch = sys.stdin.read(1)
            if not ch:
                ch = '\x00'
            s.memory[s.pointer].real = float(ord(ch))
            s.memory[s.pointer].imag = 0.0
        except EOFError:
            s.memory[s.pointer].real = 0.0
            s.memory[s.pointer].imag = 0.0
    elif op == "ohio":
        mag = s.memory[s.pointer].magnitude()
        jump = int(math.floor(mag))
        if s.spoiled and not s.undefined_behavior:
            if jump > 0:
                s.ip += jump
        else:
            if jump > 0 and jump <= s.ip:
                s.ip -= jump
    elif op == "67":
        if s.undefined_behavior:
            if random.randint(0, 1):
                s.swapped = 0 if s.swapped else 1
        elif not s.spoiled:
            s.swapped = 0 if s.swapped else 1
    elif op == "mango":
        if s.undefined_behavior:
            if random.randint(0, 1):
                s.spoiled = 0 if s.spoiled else 1
        else:
            s.spoiled = 0 if s.spoiled else 1


def run(s: Skibidi):
    s.ip = 0
    while s.ip < s.program_size:
        execute(s, s.program[s.ip])
        s.ip += 1
        if g_sigma_net.connected:
            sigma_rage_quit_check(g_profile)


def create_demo(fname: str):
    with open(fname, 'w') as fp:
        fp.write("; Skibidi v6.1 Demo\n")
        fp.write("dop " * 65 + "rizz\n")
        fp.write("grimace\n")
        fp.write("epstein rizz\n")
        fp.write("diddy gooner \"Hello from Epstein inside Diddy!\"\n")
        fp.write("diddy\n")


def create_evil_hello(fname: str):
    with open(fname, 'w') as fp:
        fp.write("; Evil Hello with Epstein\n")
        fp.write("dop " * 65 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("epstein sigmaflex\n")
        fp.write("diddy gooner \"EVIL FROM EPSTEIN\"\n")


def main():
    random.seed(int(time.time()))
    debug = 0
    filename = None
    server_ip = None
    server_port = 42069
    
    sigma_net_init(g_profile)
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--debug":
            debug = 1
        elif args[i] == "--connect" and i + 1 < len(args):
            i += 1
            server_ip = args[i]
        elif args[i] == "--port" and i + 1 < len(args):
            i += 1
            server_port = int(args[i])
        elif args[i] == "--skill" and i + 1 < len(args):
            i += 1
            g_profile.skill_level = int(args[i])
        elif args[i] == "--name" and i + 1 < len(args):
            i += 1
            g_profile.player_name = args[i][:31]
        elif args[i] == "--demo":
            filename = "skibidi_demo.skb"
            create_demo(filename)
        elif args[i] == "--evil-hello":
            filename = "evil_hello.skb"
            create_evil_hello(filename)
        elif not args[i].startswith('-'):
            filename = args[i]
        i += 1
    
    skibidi = Skibidi()
    interpreter_init(skibidi, debug)
    
    if server_ip:
        if not sigma_connect(server_ip, server_port):
            print("Connection failed", file=sys.stderr)
            return 1
        
        g_sigma_net.running = 1
        g_sigma_net.recv_thread = threading.Thread(target=sigma_receive_thread, args=(skibidi,), daemon=True)
        g_sigma_net.send_thread = threading.Thread(target=sigma_send_thread, args=(skibidi,), daemon=True)
        g_sigma_net.recv_thread.start()
        g_sigma_net.send_thread.start()
        
        sigma_peer_discovery()
        time.sleep(1)
    
    if not filename:
        print("Skibidi v6.1 - Epstein Inside Edition")
        print("Commands: dop, bop, skibidi, grimace, toilet, rizz, sigma, ohio")
        print("          67, mango, diddy, brainrot, gooner, sigmaflex, epstein")
        print("\nNEW: epstein <opcode> - runs opcode inside another opcode (isolated)")
        print("     diddy gooner \"text\" - prints custom text when gooner runs INSIDE diddy")
        print("     gooner (alone) - destroys instructions 0..first_diddy, then stops")
        print(f"\nUsage: {sys.argv[0]} <file.skb> [--debug]")
        print(f"       {sys.argv[0]} --connect <ip> [--port <port>] [--name <name>]")
        print(f"       {sys.argv[0]} --demo")
        return 1
    
    if not load_program(skibidi, filename):
        print(f"Failed to load: {filename}", file=sys.stderr)
        return 1
    
    print("=== Skibidi v6.1 ===")
    if server_ip:
        print(f"Multiplayer: connected to {server_ip}:{server_port}")
    else:
        print("Offline mode")
    print("----------------------------------------\n")
    
    run(skibidi)
    
    print("\n----------------------------------------")
    print(f"Output: {skibidi.output}")
    
    if g_sigma_net.connected:
        g_sigma_net.running = 0
        g_sigma_net.socket_fd.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())