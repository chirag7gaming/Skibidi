"""
Skibidi v8.0 - Must've been the Wind Edition (November 2026) - FULL PORT with LARP
"""

import math
import hashlib
import random
import socket
import struct
import sys
import threading
import time
import tkinter as tk
import shutil
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

ALL_EMOJIS = [
    '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚',
    '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣',
    '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗',
    '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐',
    '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾',
    '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾', '👶', '🧒', '👦', '👧', '🧑', '👨', '👩', '🧔', '🧑‍🦰', '🧑‍🦱',
    '🧑‍🦳', '🧑‍🦲', '👱', '👨‍🦰', '👨‍🦱', '👨‍🦳', '👨‍🦲', '👩‍🦰', '👩‍🦱', '👩‍🦳', '👩‍🦲', '🧓', '👴', '👵', '🙍', '🙍‍♂️', '🙍‍♀️', '🙎', '🙎‍♂️', '🙎‍♀️',
    '🙅', '🙅‍♂️', '🙅‍♀️', '🙆', '🙆‍♂️', '🙆‍♀️', '💁', '💁‍♂️', '💁‍♀️', '🙋', '🙋‍♂️', '🙋‍♀️', '🧏', '🧏‍♂️', '🧏‍♀️', '🙇', '🙇‍♂️', '🙇‍♀️', '🤦', '🤦‍♂️',
    '🤦‍♀️', '🤷', '🤷‍♂️', '🤷‍♀️', '🧑‍🎄', '🎅', '🤶', '🦸', '🦸‍♂️', '🦸‍♀️', '🦹', '🦹‍♂️', '🦹‍♀️', '🧙', '🧙‍♂️', '🧙‍♀️', '🧚', '🧚‍♂️', '🧚‍♀️', '🧛',
    '🧛‍♂️', '🧛‍♀️', '🧜', '🧜‍♂️', '🧜‍♀️', '🧝', '🧝‍♂️', '🧝‍♀️', '🧞', '🧞‍♂️', '🧞‍♀️', '🧟', '🧟‍♂️', '🧟‍♀️', '🙈', '🙉', '🙊', '💋', '💌', '💘',
    '💝', '💖', '💗', '💓', '💞', '💕', '💟', '❣️', '💔', '❤️', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍', '💯', '💢',
    '💥', '💫', '💦', '💨', '🕳️', '💣', '💬', '👁️', '👅', '👄', '🤺', '🏇', '⛷️', '🏂', '🏌️', '🏌️‍♂️', '🏌️‍♀️', '🏄', '🏄‍♂️', '🏄‍♀️',
    '🚣', '🚣‍♂️', '🚣‍♀️', '🏊', '🏊‍♂️', '🏊‍♀️', '⛹️', '⛹️‍♂️', '⛹️‍♀️', '🏋️', '🏋️‍♂️', '🏋️‍♀️', '🚴', '🚴‍♂️', '🚴‍♀️', '🚵', '🚵‍♂️', '🚵‍♀️', '🤸', '🤸‍♂️',
    '🤸‍♀️', '🤼', '🤼‍♂️', '🤼‍♀️', '🤽', '🤽‍♂️', '🤽‍♀️', '🤾', '🤾‍♂️', '🤾‍♀️', '🤹', '🤹‍♂️', '🤹‍♀️', '🧘', '🧘‍♂️', '🧘‍♀️', '🛀', '🛌', '🧖', '🧖‍♂️',
    '🧖‍♀️', '🧗', '🧗‍♂️', '🧗‍♀️', '🤳', '💪', '🦵', '🦶', '👂', '🦻', '👃', '🧠', '🦷', '🦴', '👀', '👁️', '👅', '👄', '💋', '🩸',
    '👕', '👖', '🧣', '🧤', '🧥', '🧦', '👗', '👘', '🥻', '🩱', '🩲', '🩳', '👙', '👚', '👛', '👜', '👝', '🎒', '👞', '👟',
    '🥾', '🥿', '👠', '👡', '👢', '👑', '👒', '🎩', '🎓', '🧢', '⛑️', '📿', '💄', '💍', '💎', '👭', '👫', '👬', '💏', '👩‍❤️‍💋‍👨',
    '👨‍❤️‍💋‍👨', '👩‍❤️‍💋‍👩', '💑', '👩‍❤️‍👨', '👨‍❤️‍👨', '👩‍❤️‍👩', '👪', '👨‍👩‍👧', '👨‍👩‍👧‍👦', '👨‍👩‍👦‍👦', '👨‍👩‍👧‍👧', '👩‍👩‍👦', '👩‍👩‍👧', '👩‍👩‍👧‍👦', '👩‍👩‍👦‍👦', '👩‍👩‍👧‍👧', '👨‍👨‍👦', '👨‍👨‍👧', '👨‍👨‍👧‍👦', '👨‍👨‍👦‍👦',
    '👨‍👨‍👧‍👧', '👮', '👮‍♂️', '👮‍♀️', '🕵️', '🕵️‍♂️', '🕵️‍♀️', '💂', '💂‍♂️', '💂‍♀️', '👷', '👷‍♂️', '👷‍♀️', '🤴', '👸', '👳', '👳‍♂️', '👳‍♀️', '👲', '🧕',
    '🤵', '🤵‍♂️', '🤵‍♀️', '👰', '👰‍♂️', '👰‍♀️', '🤰', '🫃', '🫄', '🤱', '👼', '🎅', '🤶', '🦸', '🦸‍♂️', '🦸‍♀️', '🦹', '🦹‍♂️', '🦹‍♀️', '🧙',
    '🧙‍♂️', '🧙‍♀️', '🧚', '🧚‍♂️', '🧚‍♀️', '🧛', '🧛‍♂️', '🧛‍♀️', '🧜', '🧜‍♂️', '🧜‍♀️', '🧝', '🧝‍♂️', '🧝‍♀️', '🧞', '🧞‍♂️', '🧞‍♀️', '🧟', '🧟‍♂️', '🧟‍♀️',
    '💆', '💆‍♂️', '💆‍♀️', '💇', '💇‍♂️', '💇‍♀️', '🚶', '🚶‍♂️', '🚶‍♀️', '🧍', '🧍‍♂️', '🧍‍♀️', '🧎', '🧎‍♂️', '🧎‍♀️', '🏃', '🏃‍♂️', '🏃‍♀️', '💃', '🕺',
    '🕴️', '👯', '👯‍♂️', '👯‍♀️', '🏻', '🏼', '🏽', '🏾', '🏿'
]

MEMORY_SIZE = 65536
STACK_SIZE = 4096

@dataclass
class Complex:
    real: float = 0.0
    imag: float = 0.0
    
    def zero(self):
        self.real = 0.0
        self.imag = 0.0
    
    def magnitude(self) -> float:
        return math.sqrt(self.real * self.real + self.imag * self.imag)
    
    def swap(self):
        return Complex(self.imag, self.real)

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
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def normalize(self):
        length = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        if length > 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return self

@dataclass
class Native3D:
    enabled: bool = False
    window: Optional[tk.Tk] = None
    canvas: Optional[tk.Canvas] = None
    width: int = 800
    height: int = 600
    objects: List[dict] = field(default_factory=list)
    camera: Vector3 = field(default_factory=lambda: Vector3(0, 5, 10))
    camera_rot_x: float = 0
    camera_rot_y: float = 0
    fov: float = 90
    running: bool = False
    
    def project(self, v: Vector3) -> tuple:
        """3D to 2D projection - pure math, no libraries"""
        dx = v.x - self.camera.x
        dy = v.y - self.camera.y
        dz = v.z - self.camera.z
        
        cos_y = math.cos(self.camera_rot_y)
        sin_y = math.sin(self.camera_rot_y)
        x2 = dx * cos_y - dz * sin_y
        z2 = dx * sin_y + dz * cos_y
        y2 = dy
        
        cos_x = math.cos(self.camera_rot_x)
        sin_x = math.sin(self.camera_rot_x)
        y3 = y2 * cos_x - z2 * sin_x
        z3 = y2 * sin_x + z2 * cos_x
        
        if z3 <= 0:
            return None
        
        scale = self.height / math.tan(math.radians(self.fov / 2))
        x_screen = int(self.width / 2 + (x2 * scale) / z3)
        y_screen = int(self.height / 2 - (y3 * scale) / z3)
        
        return (x_screen, y_screen)
    
    def add_cube(self, x, y, z, size=1, color="#ff3366"):
        s = size / 2
        vertices = [
            Vector3(x-s, y-s, z-s), Vector3(x+s, y-s, z-s),
            Vector3(x+s, y-s, z+s), Vector3(x-s, y-s, z+s),
            Vector3(x-s, y+s, z-s), Vector3(x+s, y+s, z-s),
            Vector3(x+s, y+s, z+s), Vector3(x-s, y+s, z+s)
        ]
        edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        self.objects.append({"type": "cube", "vertices": vertices, "edges": edges, "color": color})
    
    def add_sphere(self, x, y, z, radius=0.5, color="#33ff66", segments=12):
        vertices = []
        for i in range(segments):
            lat = math.pi * (-0.5 + i / segments)
            for j in range(segments):
                lon = 2 * math.pi * j / segments
                vx = x + radius * math.cos(lat) * math.cos(lon)
                vy = y + radius * math.sin(lat)
                vz = z + radius * math.cos(lat) * math.sin(lon)
                vertices.append(Vector3(vx, vy, vz))
        self.objects.append({"type": "sphere", "vertices": vertices, "color": color, "radius": radius, "center": Vector3(x,y,z)})
    
    def add_text(self, x, y, z, text, color="#ffffff"):
        self.objects.append({"type": "text", "x": x, "y": y, "z": z, "text": text, "color": color})
    
    def add_line(self, x1, y1, z1, x2, y2, z2, color="#ff0000"):
        self.objects.append({"type": "line", "p1": Vector3(x1,y1,z1), "p2": Vector3(x2,y2,z2), "color": color})
    
    def render(self):
        if not self.canvas:
            return
        self.canvas.delete("all")
        
        for obj in self.objects:
            if obj["type"] == "cube":
                for edge in obj["edges"]:
                    p1 = self.project(obj["vertices"][edge[0]])
                    p2 = self.project(obj["vertices"][edge[1]])
                    if p1 and p2:
                        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=obj["color"], width=2)
            
            elif obj["type"] == "sphere":
                for v in obj["vertices"]:
                    p = self.project(v)
                    if p:
                        self.canvas.create_oval(p[0]-2, p[1]-2, p[0]+2, p[1]+2, fill=obj["color"], outline="")
            
            elif obj["type"] == "line":
                p1 = self.project(obj["p1"])
                p2 = self.project(obj["p2"])
                if p1 and p2:
                    self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=obj["color"], width=2)
            
            elif obj["type"] == "text":
                p = self.project(Vector3(obj["x"], obj["y"], obj["z"]))
                if p:
                    self.canvas.create_text(p[0], p[1], text=obj["text"], fill=obj["color"], font=("Arial", 12))
        
        self.canvas.update()
    
    def start_window(self):
        self.window = tk.Tk()
        self.window.title("Skibidi Native 3D Engine")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="#111122")
        self.canvas.pack()
        self.running = True
        
        def on_key(e):
            step = 0.5
            if e.keysym == "w":
                self.camera.z -= step * math.cos(self.camera_rot_y)
                self.camera.x -= step * math.sin(self.camera_rot_y)
            elif e.keysym == "s":
                self.camera.z += step * math.cos(self.camera_rot_y)
                self.camera.x += step * math.sin(self.camera_rot_y)
            elif e.keysym == "a":
                self.camera.x -= step * math.cos(self.camera_rot_y)
                self.camera.z += step * math.sin(self.camera_rot_y)
            elif e.keysym == "d":
                self.camera.x += step * math.cos(self.camera_rot_y)
                self.camera.z -= step * math.sin(self.camera_rot_y)
            elif e.keysym == "q":
                self.camera.y -= step
            elif e.keysym == "e":
                self.camera.y += step
            elif e.keysym == "Left":
                self.camera_rot_y -= 0.1
            elif e.keysym == "Right":
                self.camera_rot_y += 0.1
            elif e.keysym == "Up":
                self.camera_rot_x -= 0.1
            elif e.keysym == "Down":
                self.camera_rot_x += 0.1
            self.render()
        
        self.window.bind("<Key>", on_key)
        
        def update_loop():
            if self.running:
                self.render()
                self.window.after(33, update_loop)
        
        update_loop()
        self.window.mainloop()
    
    def close(self):
        self.running = False
        if self.window:
            self.window.destroy()

@dataclass
class Skibidi8:
    memory: List[Complex] = field(default_factory=lambda: [Complex() for _ in range(MEMORY_SIZE)])
    pointer: int = 0
    pitch: int = 440
    stack: List[Complex] = field(default_factory=lambda: [Complex() for _ in range(STACK_SIZE)])
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
    nested_depth: int = 0
    nested_ops: List[str] = field(default_factory=list)
    nested_ip: List[int] = field(default_factory=list)
    in_epstein: int = 0
    epstein_target_op: Optional[str] = None
    label_map: dict = field(default_factory=dict)
    label_count: int = 0
    sigma_net: SigmaNet = field(default_factory=SigmaNet)
    profile: PlayerProfile = field(default_factory=PlayerProfile)
    file_handle: Optional[str] = None
    variables: Dict[str, float] = field(default_factory=dict)
    imported: Dict[str, Any] = field(default_factory=dict)
    native3d: Optional[Any] = None

def md5_update(state: bytearray):
    md5 = hashlib.md5()
    md5.update(state)
    new_hash = md5.digest()
    for i in range(16):
        state[i] = new_hash[i]

def hash_to_pitch(state: bytearray) -> int:
    val = (state[0] << 24) | (state[1] << 16) | (state[2] << 8) | state[3]
    return 200 + (abs(val) % 600)

def skibidi_chaos(s: Skibidi8):
    md5_update(s.rng_state)
    s.pitch = hash_to_pitch(s.rng_state)

def sigma_checksum(data: bytes) -> int:
    checksum = 0xDEADBEEF
    for byte in data:
        checksum = ((checksum << 5) + checksum + byte) & 0xFFFFFFFF
        checksum ^= 0x69696969
    return checksum

def sigma_net_init(s: Skibidi8):
    s.sigma_net = SigmaNet()
    s.sigma_net.connected = 0
    s.sigma_net.peer_count = 0
    s.sigma_net.peers = []
    s.profile.player_name = "PLAYER_1"
    s.profile.skill_level = 100
    s.profile.rage_quit_timer = 0
    s.profile.packet_loss = 0
    s.profile.latency_ms = 0

def sigma_connect(s: Skibidi8, server_ip: str, port: int) -> bool:
    s.sigma_net.socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sigma_net.socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sigma_net.addr = (server_ip, port)
    bind_port = 42069 + random.randint(0, 999)
    s.sigma_net.socket_fd.bind(('', bind_port))
    s.sigma_net.connected = 1
    s.sigma_net.server_ip = server_ip
    s.sigma_net.server_port = port
    print(f"Connected to {server_ip}:{port} as '{s.profile.player_name}'")
    return True

def sigma_broadcast_memory(s: Skibidi8, index: int):
    if not s.sigma_net.connected:
        return
    if random.randint(0, 99) < s.profile.packet_loss:
        return

def sigma_broadcast_action(s: Skibidi8, action: str):
    if not s.sigma_net.connected:
        return

def sigma_rage_quit_check(s: Skibidi8):
    if s.profile.skill_level <= 0:
        print("\nRAGE QUIT")
        sys.exit(1)

def sigma_flex(s: Skibidi8, skill_level: int):
    flex_lines = ["packet loss", "skill issue", "lag spike", "buffering", "disconnected"]
    flex_msg = f"{s.profile.player_name}: {flex_lines[random.randint(0, 4)]} (skill: {skill_level})"
    print(f"FLEX: {flex_msg}")

def sigma_peer_discovery(s: Skibidi8) -> bool:
    if not s.sigma_net.connected:
        return False
    print("Searching for peers...")
    return True

def sigma_receive_thread(s: Skibidi8):
    pass

def sigma_send_thread(s: Skibidi8):
    pass

def brainrot(s: Skibidi8):
    if s.program_size <= 1:
        return
    for i in range(s.program_size // 2):
        temp = s.program[i]
        s.program[i] = s.program[s.program_size - 1 - i]
        s.program[s.program_size - 1 - i] = temp
    s.brainrot_count += 1
    s.ip = 0
    s.debug = 0 if s.debug else 1

def gooner(s: Skibidi8):
    if s.gooner_activated:
        return
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
    print("\n⚠️ Gooner: No diddy found - destroying ALL instructions!")
    for i in range(len(s.program)):
        if s.program[i] != "magical white liquid":
            s.program[i] = "magical white liquid"
    s.gooner_activated = 1
    s.ip = 0

def epstein_execute_inside(s: Skibidi8, outer_op: str, inner_op: str):
    if s.nested_depth >= 16:
        print("Epstein nested too deep!")
        return
    s.nested_ops.append(outer_op)
    s.nested_ip.append(s.ip)
    s.nested_depth += 1
    s.in_epstein = 1
    s.epstein_target_op = inner_op
    execute(s, inner_op)
    s.nested_depth -= 1
    s.nested_ops.pop()
    s.nested_ip.pop()
    s.in_epstein = 1 if s.nested_depth > 0 else 0
    s.epstein_target_op = None

def load_program(s: Skibidi8, filename: str) -> bool:
    try:
        with open(filename, 'r') as fp:
            content = fp.read()
    except IOError:
        return False
    tokens = []
    for line in content.split('\n'):
        if line.lstrip().startswith(';'):
            continue
        for clean in tokenize_program_line(line):
            if clean == ';':
                tokens.append(';')
            elif clean.endswith(':') and clean not in VALID_OPS:
                label = clean[:-1]
                s.label_map[label] = len(tokens)
                s.label_count += 1
            else:
                tokens.append(clean)
    s.program = tokens
    s.program_size = len(tokens)
    return True

def print_debug(s: Skibidi8, op: str):
    mag = s.memory[s.pointer].magnitude()
    print(f"[{s.ip}] {op:<20} | P:{s.pitch:3d}Hz | C:{s.pointer:2d} | "
          f"({s.memory[s.pointer].real:.1f}+{s.memory[s.pointer].imag:.1f}i) | "
          f"Mag:{mag:.0f} | Swp:{s.swapped} | Spoil:{s.spoiled} | "
          f"Rot:{s.brainrot_count % 2} | Goon:{s.gooner_activated} | Eps:{s.in_epstein}")

MULTI_WORD_OPS = sorted(
    ['magical white liquid', 'the dude who no one invited:', 'dude call', 'triple t', 'im out'],
    key=lambda x: len(x.split()), reverse=True
)

def tokenize_program_line(line):
    raw = []
    i, n = 0, len(line)
    while i < n:
        while i < n and line[i].isspace():
            i += 1
        if i >= n:
            break
        if line[i] == ';':
            raw.append(';')
            i += 1
            continue
        if line[i] == '"':
            j = i + 1
            while j < n and line[j] != '"':
                j += 1
            if j < n:
                j += 1
            raw.append(line[i:j])
            i = j
            continue
        j = i
        while j < n and not line[j].isspace() and line[j] != ';':
            j += 1
        raw.append(line[i:j])
        i = j
    out, i = [], 0
    while i < len(raw):
        matched = False
        for mw in MULTI_WORD_OPS:
            parts = mw.split()
            if i + len(parts) <= len(raw) and raw[i:i+len(parts)] == parts:
                out.append(mw)
                i += len(parts)
                matched = True
                break
        if not matched:
            out.append(raw[i])
            i += 1
    return out

VALID_OPS = {
    'dop', 'bop', 'skibidi', 'grimace', 'toilet', 'rizz', 'sigma', 'ohio',
    '67', 'mango', 'diddy', 'brainrot', 'gooner', 'magical white liquid',
    'sigmaflex', 'epstein', 'gyatt', 'dih', 'vah', 'twin', 'im out',
    'bred', 'dawg', 'triple t', 'patrick', '3d', 'cross', 'dot', 'let', 'get',
    'the dude who no one invited:', 'dude call',
    'kink', 'tiki', 'ip', 'acey', 'speed', 'cristiano', 'messi',
    '3don', '3doff', 'cube', 'sphere', 'cam', 'clear3d',
    'Larp', 'larp',
}

def execute(s: Skibidi8, op: str):
    if s.debug:
        print_debug(s, op)
    s.undefined_behavior = 1 if (s.swapped and s.spoiled) else 0
    if op == "magical white liquid":
        return
    if op == "Larp":
        for i in range(s.program_size):
            if s.program[i] in ('gooner', 'cristiano', 'speed', 'dawg', 'dih', 'brainrot'):
                s.program[i] = "larp"
        return
    if op == "larp":
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
        if s.sigma_net.connected and s.profile.skill_level < 80:
            return
        brainrot(s)
        if s.sigma_net.connected:
            s.profile.skill_level += 1
            sigma_broadcast_action(s, "BRAINROT")
        return
    if op == "gooner":
        gooner(s)
        if s.sigma_net.connected:
            sigma_broadcast_action(s, "GOONER")
        return
    if op == "sigmaflex":
        sigma_flex(s, s.profile.skill_level)
        return
    if op == "dih":
        if s.ip + 1 < s.program_size:
            s.file_handle = s.program[s.ip + 1]
            s.ip += 1
        return
    if op == "vah" and s.file_handle:
        try:
            with open(s.file_handle, 'r') as f:
                data = f.read(4096)
                for i, ch in enumerate(data):
                    if s.pointer + i < MEMORY_SIZE:
                        s.memory[s.pointer + i].real = float(ord(ch))
        except:
            pass
        return
    if op == "twin" and s.ip + 1 < s.program_size and s.file_handle:
        try:
            shutil.copy(s.file_handle, s.program[s.ip + 1])
            s.ip += 1
        except:
            pass
        return
    if op == "im out" and s.ip + 1 < s.program_size and s.file_handle:
        try:
            shutil.move(s.file_handle, s.program[s.ip + 1])
            s.file_handle = s.program[s.ip + 1]
            s.ip += 1
        except:
            pass
        return
    if op == "bred":
        for _ in range(50):
            print("Diddy", end=" ")
        print()
        return
    if op == "dawg":
        for _ in range(50):
            print("W Speed❤️‍🩹", end=" ")
        print()
        return
    if op == "patrick":
        cnt = 10
        if s.ip + 1 < s.program_size:
            try:
                cnt = int(s.program[s.ip + 1])
                s.ip += 1
            except:
                pass
        for _ in range(min(abs(cnt), 100)):
            s.output += random.choice(ALL_EMOJIS)
        print(s.output[-200:])
        return
    if op == "triple t" and s.ip + 1 < s.program_size:
        var = s.program[s.ip + 1]
        val = s.variables.get(var, s.memory[s.pointer].magnitude())
        s.output += f"T{val:.4f}T"
        print(f"T{val:.4f}T", end="")
        s.ip += 1
        return
    if op == "the dude who no one invited:":
        module_spec = ""
        temp_ip = s.ip + 1
        while (temp_ip < s.program_size
               and s.program[temp_ip] != ";"
               and s.program[temp_ip] != "then"
               and s.program[temp_ip] not in VALID_OPS):
            module_spec += s.program[temp_ip] + " "
            temp_ip += 1
        module_spec = module_spec.strip()
        parts = module_spec.split()
        if len(parts) >= 1:
            mod_name = parts[0]
            alias = parts[2] if len(parts) >= 3 and parts[1] == "as" else mod_name
            try:
                imported = __import__(mod_name)
                for part in mod_name.split('.')[1:]:
                    imported = getattr(imported, part)
                s.imported[alias] = imported
                print(f"[Dude] {alias} joined")
            except Exception as e:
                print(f"[Dude] {mod_name} didnt show: {e}")
        s.ip = temp_ip
        return
    if op == "dude call" and s.ip + 1 < s.program_size:
        call_str = s.program[s.ip + 1]
        parts = call_str.split('.')
        if len(parts) >= 2 and parts[0] in s.imported:
            module = s.imported[parts[0]]
            func_name = '.'.join(parts[1:])
            args = []
            temp_ip = s.ip + 2
            while (temp_ip < s.program_size
                   and s.program[temp_ip] != ";"
                   and s.program[temp_ip] not in VALID_OPS):
                try:
                    args.append(int(s.program[temp_ip]))
                except ValueError:
                    try:
                        args.append(float(s.program[temp_ip]))
                    except ValueError:
                        args.append(s.program[temp_ip])
                temp_ip += 1
            try:
                func = eval(f"module.{func_name}")
                result = func(*args)
                if isinstance(result, (int, float)):
                    s.memory[s.pointer].real = float(result)
                print(f"[Dude] {call_str} -> {result}")
            except Exception as e:
                print(f"[Dude] call failed: {e}")
            s.ip = temp_ip
        else:
            print(f"[Dude] module {parts[0]} not found")
            s.ip += 2
        return
    if op == "let" and s.ip + 2 < s.program_size:
        s.variables[s.program[s.ip + 1]] = s.memory[s.pointer].magnitude()
        s.ip += 2
        return
    if op == "get" and s.ip + 1 < s.program_size:
        if s.program[s.ip + 1] in s.variables:
            s.memory[s.pointer].real = s.variables[s.program[s.ip + 1]]
        s.ip += 1
        return
    if op == "3d":
        if s.pointer + 2 < MEMORY_SIZE:
            s.memory[s.pointer + 1].real = s.memory[s.pointer + 2].real = 0
        return
    if op == "cross" and s.ip + 3 < s.program_size:
        ax, ay, az = s.pointer, s.pointer + 1, s.pointer + 2
        bx = int(s.program[s.ip+1]) % MEMORY_SIZE
        by = int(s.program[s.ip+2]) % MEMORY_SIZE
        bz = int(s.program[s.ip+3]) % MEMORY_SIZE
        cx = s.memory[ay].real * s.memory[bz].real - s.memory[az].real * s.memory[by].real
        cy = s.memory[az].real * s.memory[bx].real - s.memory[ax].real * s.memory[bz].real
        cz = s.memory[ax].real * s.memory[by].real - s.memory[ay].real * s.memory[bx].real
        s.memory[ax].real, s.memory[ay].real, s.memory[az].real = cx, cy, cz
        s.ip += 3
        return
    if op == "dot" and s.ip + 3 < s.program_size:
        ax, ay, az = s.pointer, s.pointer + 1, s.pointer + 2
        bx = int(s.program[s.ip+1]) % MEMORY_SIZE
        by = int(s.program[s.ip+2]) % MEMORY_SIZE
        bz = int(s.program[s.ip+3]) % MEMORY_SIZE
        result = (s.memory[ax].real * s.memory[bx].real + 
                  s.memory[ay].real * s.memory[by].real + 
                  s.memory[az].real * s.memory[bz].real)
        s.memory[s.pointer].real = result
        s.ip += 3
        return
    if op == "diddy":
        next_ip = s.ip + 1
        found_gooner_inside = False
        custom_text = None
        end_ip = next_ip
        if next_ip < s.program_size and s.program[next_ip] == "gooner":
            found_gooner_inside = True
            end_ip = next_ip + 1
            if end_ip < s.program_size and s.program[end_ip].startswith('"'):
                msg = s.program[end_ip]
                if len(msg) >= 2 and msg[0] == '"' and msg[-1] == '"':
                    custom_text = msg[1:-1]
                end_ip += 1
        if found_gooner_inside:
            if s.spoiled or s.undefined_behavior:
                print("\nCRASH", file=sys.stderr)
                if s.sigma_net.connected:
                    s.profile.skill_level -= 50
                    sigma_rage_quit_check(s)
                sys.exit(1)
            s.diddy_gooner_inside = 1
            s.gooner_custom_text = custom_text
            gooner(s)
            if s.ip < end_ip - 1:
                s.ip = end_ip - 1
        else:
            if s.spoiled or s.undefined_behavior:
                print("\nCRASH", file=sys.stderr)
                if s.sigma_net.connected:
                    s.profile.skill_level -= 50
                    sigma_rage_quit_check(s)
                sys.exit(1)
            print("milk milk milk")
        return

    # === NATIVE 3D OPS ===
    if op == "3don":
        if s.native3d is None:
            s.native3d = Native3D()
        s.native3d.enabled = True
        if not s.native3d.window:
            threading.Thread(target=s.native3d.start_window, daemon=True).start()
        return

    if op == "3doff":
        if s.native3d and s.native3d.enabled:
            s.native3d.close()
        return

    if op == "cube":
        if s.native3d and s.native3d.enabled:
            x = s.memory[s.pointer].real
            y = s.memory[s.pointer].imag if s.pointer + 1 < MEMORY_SIZE else 0
            z = s.memory[s.pointer + 1].real if s.pointer + 1 < MEMORY_SIZE else 0
            size = s.memory[s.pointer + 2].real if s.pointer + 2 < MEMORY_SIZE else 1
            s.native3d.add_cube(x, y, z, size)
        return

    if op == "sphere":
        if s.native3d and s.native3d.enabled:
            x = s.memory[s.pointer].real
            y = s.memory[s.pointer].imag if s.pointer + 1 < MEMORY_SIZE else 0
            z = s.memory[s.pointer + 1].real if s.pointer + 1 < MEMORY_SIZE else 0
            r = s.memory[s.pointer + 2].real if s.pointer + 2 < MEMORY_SIZE else 0.5
            s.native3d.add_sphere(x, y, z, r)
        return

    if op == "cam":
        if s.native3d and s.native3d.enabled:
            s.native3d.camera.x = s.memory[s.pointer].real
            s.native3d.camera.y = s.memory[s.pointer].imag
            s.native3d.camera.z = s.memory[s.pointer + 1].real if s.pointer + 1 < MEMORY_SIZE else 10
        return

    if op == "clear3d":
        if s.native3d and s.native3d.enabled:
            s.native3d.objects.clear()
        return

    # === REQUESTED OPS ===
    if op == "kink":
        print("\n🔥 KINK ACTIVATED: Spawning 5 Epsteins with 9,999 gooners inside...")
        for i in range(5):
            print(f"  Spawning Epstein #{i+1}...")
            time.sleep(0.1)
            if random.random() < 0.3:
                print("You were so hard daddy~😩😩😩😩😩")
                return
        print("✅ 5 INDESTRUCTIBLE EPSTEINS SPAWNED with 9,999 gooners + random diddys!")
        s.profile.skill_level += 100
        return

    if op == "tiki":
        copypasta = """Hey brother 😭🙏 I gotta ask, why didn't you use Tiki Phonk this time? 🗿 Honestly, Tiki Phonk would've matched the whole vibe perfectly and made the edit way more energetic ⚡🔥 The bass, the cowbells, and the overall atmosphere would've gone absolutely crazy 🎧💥 I was genuinely expecting that style because it always makes the clips feel smoother, harder, and way more satisfying to watch 👌💯

Don't get me wrong though, the edit was still clean 🍷 but Tiki Phonk would've pushed it to another level entirely 🚀 The way those distorted beats sync with transitions is unmatched 😭 Every flash, zoom, and movement would've hit ten times harder 💣 The music basically gives edits an aura 👁️🗿 Like the second the beat drops, everything suddenly feels cinematic and dangerous 😈⚔️

Brother, your editing style already fits Tiki Phonk perfectly too 🤝 The pacing, the transitions, the effects — all of it screams for that aggressive energy 🔥 Imagine the bass dropping exactly when the clips switch 💥 or the cowbells echoing during the slow motion parts 🎶 That would've been legendary 😭🙏 People definitely would've replayed the edit over and over because the vibe would've been addicting 📈🌀

That's the thing with Tiki Phonk 🎧 It doesn't just sound cool — it transforms the whole experience 🌌 Even simple clips start feeling powerful and memorable 🗿 The atmosphere becomes darker, cleaner, and way more hype ⚡ Without it, the edit still looks good, but with it? Brother… it becomes generational 🍷🔥

Next time, trust the vision and let the Tiki Phonk carry the edit 😭🙏 Let the bass shake the screen 💣 let the transitions breathe with the beat 🎶 and let the aura consume the entire video 👁️🗿 Trust me brother, everything will sound cleaner, hit harder, and feel way more unforgettable 💯

Capiche boy? 🍷🗿"""
        print(copypasta)
        s.output += copypasta
        return

    if op == "ip":
        print("198.234.45.207")
        if s.native3d and s.native3d.enabled:
            s.native3d.add_text(0, 2, 0, "198.234.45.207", "#ff6600")
        return

    if op == "acey":
        print('Please, Speed. I need this~~~~ My mum is kinda homeless')
        return

    if op == "speed":
        print("SEWEY same")
        s.profile.skill_level += 50
        return

    if op == "cristiano":
        print("SUUUUUUUUU")
        s.memory[s.pointer].real = 7
        s.memory[s.pointer].imag = 77
        return

    if op == "messi":
        for _ in range(10):
            print("stfu", end=" ")
        print()
        return

    if s.gooner_activated:
        return
    if op == "dop":
        if s.spoiled and not s.undefined_behavior:
            s.memory[s.pointer].real -= 1.0
        else:
            s.memory[s.pointer].real += 1.0
        if s.sigma_net.connected:
            sigma_broadcast_memory(s, s.pointer)
    elif op == "bop":
        if s.spoiled and not s.undefined_behavior:
            s.memory[s.pointer].imag += 1.0
        else:
            s.memory[s.pointer].imag -= 1.0
        if s.sigma_net.connected:
            sigma_broadcast_memory(s, s.pointer)
    elif op == "skibidi":
        skibidi_chaos(s)
    elif op == "grimace":
        if s.spoiled and not s.undefined_behavior:
            move_right = (s.pitch < 440)
        else:
            move_right = (s.pitch >= 440)
        if move_right:
            s.pointer = (s.pointer + 1) % MEMORY_SIZE
        else:
            s.pointer = (s.pointer - 1 + MEMORY_SIZE) % MEMORY_SIZE
    elif op == "toilet":
        if s.stack_ptr < STACK_SIZE:
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
    elif op == "gyatt":
        if s.stack_ptr > 0:
            top = s.stack[s.stack_ptr - 1]
            mag = top.magnitude()
            if s.spoiled and not s.undefined_behavior:
                threshold = 50
            else:
                threshold = 100
            if s.sigma_net.connected:
                sigma_broadcast_action(s, f"GYATT (mag={mag:.1f})")
            if mag > threshold:
                jump = max(1, int(math.floor(mag / 10)))
                if s.undefined_behavior:
                    if random.randint(0, 1):
                        s.ip += jump
                    else:
                        s.ip = max(0, s.ip - jump)
                else:
                    s.ip += jump
                if s.debug:
                    print(f" | GYATT JUMP +{jump}")
            elif s.debug:
                print(f" | GYATT no jump (mag={mag:.1f} ≤ {threshold})")
        elif s.debug:
            print(" | GYATT fail (stack empty)")

def run(s: Skibidi8):
    s.ip = 0
    while s.ip < s.program_size:
        execute(s, s.program[s.ip])
        s.ip += 1
        if s.sigma_net.connected:
            sigma_rage_quit_check(s)

def create_demo(fname: str):
    with open(fname, 'w') as fp:
        fp.write("; Skibidi v8.0 Demo\n")
        fp.write("dop " * 65 + "rizz\n")
        fp.write("grimace\n")
        fp.write("epstein rizz\n")
        fp.write("dop dop dop dop toilet\n")
        fp.write("gyatt\n")
        fp.write("diddy gooner \"Hello from Epstein inside Diddy!\"\n")
        fp.write("diddy\n")

def create_evil_hello(fname: str):
    with open(fname, 'w') as fp:
        fp.write("; Evil Hello with Gyatt\n")
        fp.write("dop " * 65 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop dop dop dop dop dop dop dop dop dop dop toilet\n")
        fp.write("gyatt\n")
        fp.write("epstein sigmaflex\n")
        fp.write("diddy gooner \"EVIL FROM EPSTEIN\"\n")

def main():
    random.seed(int(time.time()))
    debug = 0
    filename = None
    server_ip = None
    server_port = 42069
    s = Skibidi8()
    sigma_net_init(s)
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
            s.profile.skill_level = int(args[i])
        elif args[i] == "--name" and i + 1 < len(args):
            i += 1
            s.profile.player_name = args[i][:31]
        elif args[i] == "--demo":
            filename = "skibidi_demo.skb"
            create_demo(filename)
        elif args[i] == "--evil-hello":
            filename = "evil_hello.skb"
            create_evil_hello(filename)
        elif not args[i].startswith('-'):
            filename = args[i]
        i += 1
    s.debug = debug
    if server_ip:
        if not sigma_connect(s, server_ip, server_port):
            print("Connection failed", file=sys.stderr)
            return 1
        s.sigma_net.running = 1
        s.sigma_net.recv_thread = threading.Thread(target=sigma_receive_thread, args=(s,), daemon=True)
        s.sigma_net.send_thread = threading.Thread(target=sigma_send_thread, args=(s,), daemon=True)
        s.sigma_net.recv_thread.start()
        s.sigma_net.send_thread.start()
        sigma_peer_discovery(s)
        time.sleep(1)
    if not filename:
        print("Skibidi v8.0 - The Uninvited Edition (June 2026)")
        print("Commands: dop, bop, skibidi, grimace, toilet, rizz, sigma, ohio")
        print("          67, mango, diddy, brainrot, gooner, sigmaflex, epstein, gyatt")
        print("          dih, vah, twin, im out, bred, dawg, triple t, patrick")
        print("          3d, cross, dot, let, get, the dude who no one invited:, dude call")
        print("          Larp - replace gooner/cristiano/speed/dih/brainrot with larp (no-op)")
        print("          larp - no-op")
        print("gyatt - checks stack top, jumps if magnitude > threshold (100/50)")
        print("     dih/vah - push/pull file operations")
        print("     the dude who no one invited: - import any Python module")
        print(f"\nUsage: {sys.argv[0]} <file.skb> [--debug]")
        print(f"       {sys.argv[0]} --connect <ip> [--port <port>] [--name <name>]")
        print(f"       {sys.argv[0]} --demo")
        return 1
    if not load_program(s, filename):
        print(f"Failed to load: {filename}", file=sys.stderr)
        return 1
    print("=== Skibidi v8.0 ===")
    if server_ip:
        print(f"Multiplayer: connected to {server_ip}:{server_port}")
    else:
        print("Offline mode")
    print("----------------------------------------\n")
    run(s)
    print("\n----------------------------------------")
    print(f"Output: {s.output}")
    if s.sigma_net.connected:
        s.sigma_net.running = 0
        s.sigma_net.socket_fd.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
