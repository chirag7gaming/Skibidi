import math
import ctypes
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
    input_buffer: str = ""
    input_pos: int = 0


@dataclass
class SigmaNet:
    socket_fd: int = -1
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
    s.input_buffer = ""
    s.input_pos = 0


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
    
    for i in range(s.program_size):
        s.program[i] = "magical white liquid"
    
    s.gooner_activated = 1
    s.ip = 0


def load_program(s: Skibidi, filename: str) -> bool:
    try:
        with open(filename, 'r') as fp:
            content = fp.read()
    except IOError:
        return False
    
    valid_ops = {"dop", "bop", "skibidi", "grimace", "toilet", "rizz",
                 "sigma", "ohio", "67", "mango", "diddy", "brainrot",
                 "gooner", "magical white liquid", "sigmaflex"}
    
    tokens = []
    for token in content.split():
        clean_token = token.strip()
        if clean_token.startswith(';'):
            break
        if clean_token not in valid_ops:
            print(f"Unknown op: {clean_token}", file=sys.stderr)
            return False
        tokens.append(clean_token)
    
    s.program = tokens
    s.program_size = len(tokens)
    return True


def print_debug(s: Skibidi, op: str):
    mag = s.memory[s.pointer].magnitude()
    print(f"[{s.ip}] {op:<20} | P:{s.pitch:3d}Hz | C:{s.pointer:2d} | "
          f"({s.memory[s.pointer].real:.1f}+{s.memory[s.pointer].imag:.1f}i) | "
          f"Mag:{mag:.0f} | Swp:{s.swapped} | Spoil:{s.spoiled} | "
          f"Rot:{s.brainrot_count % 2} | Goon:{s.gooner_activated}")


def sigma_checksum(data: bytes) -> int:
    checksum = 0xDEADBEEF
    for byte in data:
        checksum = ((checksum << 5) + checksum + byte) & 0xFFFFFFFF
        checksum ^= 0x69696969
    return checksum


def sigma_net_init(profile: PlayerProfile):
    global g_sigma_net
    g_sigma_net = SigmaNet()
    g_sigma_net.socket_fd = -1
    g_sigma_net.connected = 0
    g_sigma_net.peer_count = 0
    
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
    
    bind_port = 42069 + (random.randint(0, 999))
    g_sigma_net.socket_fd.bind(('', bind_port))
    
    g_sigma_net.connected = 1
    g_sigma_net.server_ip = server_ip
    g_sigma_net.server_port = port
    
    print(f"Connected to {server_ip}:{port} as '{g_profile.player_name}'")
    
    announce = f"{g_profile.player_name}_SKILL_{g_profile.skill_level}"
    sigma_broadcast_action(announce)
    
    return True


def sigma_broadcast_memory(s: Skibidi, index: int):
    if not g_sigma_net.connected:
        return
    
    if random.randint(0, 99) < g_profile.packet_loss:
        return
    
    pkt = NetworkPacket()
    pkt.type = 0x01
    pkt.player_id = g_profile.skill_level // 10
    pkt.memory_index = index
    pkt.value = s.memory[index]
    pkt.brainrot_count = s.brainrot_count
    pkt.flex_message = f"{g_profile.player_name} (skill: {g_profile.skill_level})"
    
    pkt_data = struct.pack('!BBiq2d', pkt.type, pkt.player_id, pkt.memory_index,
                           pkt.brainrot_count, pkt.value.real, pkt.value.imag)
    pkt_data += pkt.flex_message.encode()[:256].ljust(256, b'\x00')
    pkt.checksum = sigma_checksum(pkt_data)
    
    with net_mutex:
        for peer in g_sigma_net.peers:
            g_sigma_net.socket_fd.sendto(pkt_data + struct.pack('!I', pkt.checksum), peer)


def sigma_broadcast_action(action: str):
    if not g_sigma_net.connected:
        return
    
    pkt = NetworkPacket()
    pkt.type = 0x96
    pkt.flex_message = action
    
    pkt_data = struct.pack('!B', pkt.type)
    pkt_data += pkt.flex_message.encode()[:256].ljust(256, b'\x00')
    pkt.checksum = sigma_checksum(pkt_data)
    
    with net_mutex:
        for peer in g_sigma_net.peers:
            g_sigma_net.socket_fd.sendto(pkt_data + struct.pack('!I', pkt.checksum), peer)


def sigma_receive_thread(s: Skibidi):
    global g_sigma_net
    
    g_sigma_net.socket_fd.settimeout(0.1)
    
    while g_sigma_net.running:
        try:
            data, sender_addr = g_sigma_net.socket_fd.recvfrom(1024)
        except socket.timeout:
            continue
        
        received_csum = struct.unpack('!I', data[-4:])[0]
        pkt_data = data[:-4]
        
        if sigma_checksum(pkt_data) != received_csum:
            continue
        
        known = False
        with net_mutex:
            for peer in g_sigma_net.peers:
                if peer[0] == sender_addr[0]:
                    known = True
                    break
            if not known and g_sigma_net.peer_count < 16:
                g_sigma_net.peers.append(sender_addr)
                g_sigma_net.peer_count += 1
                print(f"New peer joined (Total: {g_sigma_net.peer_count})")
        
        pkt_type = pkt_data[0]
        
        if pkt_type == 0x01:
            with net_mutex:
                if random.randint(0, 99) < 30:
                    fields = struct.unpack('!BBiq2d', pkt_data[:28])
                    s.memory[fields[2]].real = fields[4]
                    s.memory[fields[2]].imag = fields[5]
        elif pkt_type == 0x03:
            if not s.gooner_activated and random.randint(0, 99) < 50:
                brainrot(s)
        elif pkt_type == 0x04:
            if not s.gooner_activated and random.randint(0, 99) < 20:
                gooner(s)


def sigma_send_thread(s: Skibidi):
    global g_sigma_net
    
    last_brainrot = 0
    
    while g_sigma_net.running:
        time.sleep(1)
        
        if not g_sigma_net.connected:
            continue
        
        pkt_data = struct.pack('!Bi', 0x02, s.pointer)
        pkt_data += b'\x00' * 250
        checksum = sigma_checksum(pkt_data)
        
        with net_mutex:
            for peer in g_sigma_net.peers:
                g_sigma_net.socket_fd.sendto(pkt_data + struct.pack('!I', checksum), peer)
        
        if s.brainrot_count != last_brainrot:
            pkt_data = struct.pack('!Bi', 0x03, s.brainrot_count)
            pkt_data += b'\x00' * 250
            checksum = sigma_checksum(pkt_data)
            
            with net_mutex:
                for peer in g_sigma_net.peers:
                    g_sigma_net.socket_fd.sendto(pkt_data + struct.pack('!I', checksum), peer)
            last_brainrot = s.brainrot_count
        
        if g_profile.skill_level < 50:
            g_profile.latency_ms = 500
        elif g_profile.skill_level < 80:
            g_profile.latency_ms = 200
        else:
            g_profile.latency_ms = 0


def sigma_rage_quit_check(p: PlayerProfile):
    if p.skill_level <= 0:
        print("\nRAGE QUIT")
        sys.exit(1)


def sigma_flex(skill_level: int):
    flex_lines = ["packet loss", "skill issue", "lag spike", "buffering", "disconnected"]
    flex_msg = f"{g_profile.player_name}: {flex_lines[random.randint(0, 4)]} (skill: {skill_level})"
    sigma_broadcast_action(flex_msg)
    print(f"FLEX: {flex_msg}")


def sigma_peer_discovery() -> bool:
    if not g_sigma_net.connected:
        return False
    
    discover_msg = f"DISCOVER_{g_profile.player_name}"
    pkt_data = struct.pack('!B', 0xFF) + discover_msg.encode()[:256].ljust(256, b'\x00')
    
    broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_sock.sendto(pkt_data, ('255.255.255.255', 42069))
    broadcast_sock.close()
    
    print("Searching for peers...")
    return True


def execute(s: Skibidi, op: str):
    if s.debug:
        print_debug(s, op)
    
    s.undefined_behavior = 1 if (s.swapped and s.spoiled) else 0
    
    if op == "magical white liquid":
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
    elif op == "diddy":
        if s.spoiled or s.undefined_behavior:
            print("\nCRASH", file=sys.stderr)
            if g_sigma_net.connected:
                g_profile.skill_level -= 50
                sigma_rage_quit_check(g_profile)
            sys.exit(1)
        print("milk", end="", flush=True)


def run(s: Skibidi):
    s.ip = 0
    while s.ip < s.program_size:
        execute(s, s.program[s.ip])
        s.ip += 1
        
        if g_sigma_net.connected:
            sigma_rage_quit_check(g_profile)


def create_demo(fname: str):
    with open(fname, 'w') as fp:
        fp.write("dop " * 65 + "rizz\n")
        fp.write("grimace\n")
        fp.write("dop " * 85 + "rizz\n")
        fp.write("brainrot\n")
        fp.write("dop " * 87 + "rizz\n")
        fp.write("dop " * 89 + "rizz\n")
        fp.write("dop " * 91 + "rizz\n")
        fp.write("gooner\n")
        fp.write("dop " * 93 + "rizz\n")
        fp.write("diddy\n")


def create_evil_hello(fname: str):
    with open(fname, 'w') as fp:
        fp.write("dop " * 65 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 85 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 87 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 89 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 91 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 93 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 95 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 97 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 99 + "rizz\n")
        fp.write("diddy\n")


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
        print("Skibidi v5.0")
        print("Commands: dop, bop, skibidi, grimace, toilet, rizz, sigma, ohio")
        print("          67, mango, diddy, brainrot, gooner, sigmaflex")
        print(f"\nUsage: {sys.argv[0]} <file.skb> [--debug]")
        print(f"       {sys.argv[0]} --connect <ip> [--port <port>] [--name <name>]")
        print(f"       {sys.argv[0]} --demo")
        return 1
    
    if not load_program(skibidi, filename):
        print(f"Failed to load: {filename}", file=sys.stderr)
        return 1
    
    print("=== Skibidi v5.0 ===")
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