#!/usr/bin/env python3
# Skibidi Terminal Language v1.0.0
# "The Full Port. Now with 100% more -ify."

import sys
import os
import math
import random
import time
import json
import pickle
import hashlib
import socket
import struct
import shutil
import threading
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple

try:
    import readline  # noqa
except ImportError:
    pass

try:
    import tkinter as tk
    HAS_TK = True
except ImportError:
    tk = None
    HAS_TK = False

# ============================================================
# CONFIG
# ============================================================
VERSION = "Skibidi Terminal Language v1.0.0 — The Full Port"
PROMPT = "> "
MEMORY_SIZE = 65536
STACK_SIZE = 4096
NESTED_MAX_DEPTH = 16

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

# ============================================================
# OKAY TRACKER (from STL 0.6.9)
# ============================================================
class OkayTracker:
    def __init__(self):
        self.command_history: List[str] = []
        self.output_history: List[str] = []
        self.memory_snapshots: List[Any] = []
        self.program_snapshots: List[List[str]] = []
        self.variable_snapshots: List[Dict] = []
        self.pointer_history: List[int] = []
        self.pitch_history: List[int] = []
        self.flag_history: List[Dict] = []

    def snapshot(self, state: 'SkibidiState'):
        self.command_history.append(f"[{time.time():.2f}]")
        self.memory_snapshots.append([Complex(c.real, c.imag) for c in state.memory[:10]])
        self.program_snapshots.append(state.program.copy())
        self.variable_snapshots.append(state.variables.copy())
        self.pointer_history.append(state.pointer)
        self.pitch_history.append(state.pitch)
        self.flag_history.append({
            'swapped': state.swapped, 'spoiled': state.spoiled,
            'undefined': state.undefined_behavior,
            'brainrot_count': state.brainrot_count,
            'gooner_activated': state.gooner_activated,
        })

    def redo_everything(self, state: 'SkibidiState'):
        print("\n🔄 OK — Redoing everything...")
        if self.program_snapshots:
            state.program = self.program_snapshots[0].copy()
            state.variables = self.variable_snapshots[0].copy()
            state.pointer = self.pointer_history[0] if self.pointer_history else 0
            state.pitch = self.pitch_history[0] if self.pitch_history else 440
            f = self.flag_history[0] if self.flag_history else {}
            state.swapped = f.get('swapped', False)
            state.spoiled = f.get('spoiled', False)
            state.undefined_behavior = f.get('undefined', False)
            state.brainrot_count = f.get('brainrot_count', 0)
            state.gooner_activated = f.get('gooner_activated', False)
            state.ip = 0
            state.output = ""
            print(f"✨ Redid {len(self.command_history)} commands")
        else:
            print("❌ Nothing to redo (no history)")

    def undo_everything(self, state: 'SkibidiState'):
        print("\n💀 NOT OKAY — Undoing everything...")
        state.memory = [Complex() for _ in range(MEMORY_SIZE)]
        state.pointer = 0
        state.pitch = 440
        state.stack = []
        state.program = []
        state.ip = 0
        state.output = ""
        state.swapped = False
        state.spoiled = False
        state.undefined_behavior = False
        state.brainrot_count = 0
        state.gooner_activated = False
        state.variables = {}
        state.labels = {}
        state.diddy_gooner_inside = 0
        state.gooner_custom_text = None
        state.in_epstein = 0
        print(f"💥 Undid {len(self.command_history)} commands — factory reset")
        for lst in (self.command_history, self.memory_snapshots, self.program_snapshots,
                    self.variable_snapshots, self.pointer_history, self.pitch_history,
                    self.flag_history):
            lst.clear()

okay_tracker = OkayTracker()
terminal_paused = False

# ============================================================
# DATA STRUCTURES
# ============================================================
@dataclass
class Complex:
    real: float = 0.0
    imag: float = 0.0
    def magnitude(self) -> float:
        return math.sqrt(self.real * self.real + self.imag * self.imag)
    def zero(self):
        self.real = 0.0
        self.imag = 0.0
    def swap(self):
        return Complex(self.imag, self.real)

@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    def __add__(self, o): return Vector3(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o): return Vector3(self.x-o.x, self.y-o.y, self.z-o.z)
    def dot(self, o): return self.x*o.x + self.y*o.y + self.z*o.z
    def cross(self, o):
        return Vector3(self.y*o.z - self.z*o.y, self.z*o.x - self.x*o.z, self.x*o.y - self.y*o.x)
    def normalize(self):
        L = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        if L > 0:
            self.x /= L; self.y /= L; self.z /= L
        return self

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
    player_name: str = "PLAYER_1"
    skill_level: int = 100
    rage_quit_timer: int = 0
    packet_loss: int = 0
    latency_ms: int = 0

@dataclass
class Native3D:
    enabled: bool = False
    window: Optional[Any] = None
    canvas: Optional[Any] = None
    width: int = 800
    height: int = 600
    objects: List[dict] = field(default_factory=list)
    camera: Vector3 = field(default_factory=lambda: Vector3(0, 5, 10))
    camera_rot_x: float = 0
    camera_rot_y: float = 0
    fov: float = 90
    running: bool = False

    def project(self, v: Vector3):
        dx = v.x - self.camera.x
        dy = v.y - self.camera.y
        dz = v.z - self.camera.z
        cy, sy = math.cos(self.camera_rot_y), math.sin(self.camera_rot_y)
        x2 = dx*cy - dz*sy
        z2 = dx*sy + dz*cy
        y2 = dy
        cx, sx = math.cos(self.camera_rot_x), math.sin(self.camera_rot_x)
        y3 = y2*cx - z2*sx
        z3 = y2*sx + z2*cx
        if z3 <= 0:
            return None
        scale = self.height / math.tan(math.radians(self.fov / 2))
        return (int(self.width/2 + (x2*scale)/z3), int(self.height/2 - (y3*scale)/z3))

    def add_cube(self, x, y, z, size=1, color="#ff3366"):
        s = size / 2
        verts = [Vector3(x-s,y-s,z-s), Vector3(x+s,y-s,z-s), Vector3(x+s,y-s,z+s), Vector3(x-s,y-s,z+s),
                 Vector3(x-s,y+s,z-s), Vector3(x+s,y+s,z-s), Vector3(x+s,y+s,z+s), Vector3(x-s,y+s,z+s)]
        edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        self.objects.append({"type": "cube", "vertices": verts, "edges": edges, "color": color})

    def add_sphere(self, x, y, z, radius=0.5, color="#33ff66", segments=12):
        verts = []
        for i in range(segments):
            lat = math.pi * (-0.5 + i / segments)
            for j in range(segments):
                lon = 2 * math.pi * j / segments
                verts.append(Vector3(
                    x + radius*math.cos(lat)*math.cos(lon),
                    y + radius*math.sin(lat),
                    z + radius*math.cos(lat)*math.sin(lon)))
        self.objects.append({"type": "sphere", "vertices": verts, "color": color})

    def add_text(self, x, y, z, text, color="#ffffff"):
        self.objects.append({"type": "text", "x": x, "y": y, "z": z, "text": text, "color": color})

    def add_line(self, x1, y1, z1, x2, y2, z2, color="#ff0000"):
        self.objects.append({"type": "line", "p1": Vector3(x1,y1,z1), "p2": Vector3(x2,y2,z2), "color": color})

    def render(self):
        if not self.canvas: return
        self.canvas.delete("all")
        for obj in self.objects:
            t = obj["type"]
            if t == "cube":
                for e in obj["edges"]:
                    p1 = self.project(obj["vertices"][e[0]])
                    p2 = self.project(obj["vertices"][e[1]])
                    if p1 and p2:
                        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=obj["color"], width=2)
            elif t == "sphere":
                for v in obj["vertices"]:
                    p = self.project(v)
                    if p:
                        self.canvas.create_oval(p[0]-2, p[1]-2, p[0]+2, p[1]+2, fill=obj["color"], outline="")
            elif t == "line":
                p1 = self.project(obj["p1"]); p2 = self.project(obj["p2"])
                if p1 and p2:
                    self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=obj["color"], width=2)
            elif t == "text":
                p = self.project(Vector3(obj["x"], obj["y"], obj["z"]))
                if p:
                    self.canvas.create_text(p[0], p[1], text=obj["text"], fill=obj["color"], font=("Arial", 12))
        self.canvas.update()

    def start_window(self):
        if not HAS_TK:
            print("❌ tkinter not available — 3D disabled")
            return
        self.window = tk.Tk()
        self.window.title("Skibidi Native 3D Engine v1.0")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="#111122")
        self.canvas.pack()
        self.running = True
        def on_key(e):
            step = 0.5
            if e.keysym == "w":
                self.camera.z -= step*math.cos(self.camera_rot_y)
                self.camera.x -= step*math.sin(self.camera_rot_y)
            elif e.keysym == "s":
                self.camera.z += step*math.cos(self.camera_rot_y)
                self.camera.x += step*math.sin(self.camera_rot_y)
            elif e.keysym == "a":
                self.camera.x -= step*math.cos(self.camera_rot_y)
                self.camera.z += step*math.sin(self.camera_rot_y)
            elif e.keysym == "d":
                self.camera.x += step*math.cos(self.camera_rot_y)
                self.camera.z -= step*math.sin(self.camera_rot_y)
            elif e.keysym == "q": self.camera.y -= step
            elif e.keysym == "e": self.camera.y += step
            elif e.keysym == "Left":  self.camera_rot_y -= 0.1
            elif e.keysym == "Right": self.camera_rot_y += 0.1
            elif e.keysym == "Up":    self.camera_rot_x -= 0.1
            elif e.keysym == "Down":  self.camera_rot_x += 0.1
            self.render()
        self.window.bind("<Key>", on_key)
        def loop():
            if self.running:
                self.render()
                self.window.after(33, loop)
        loop()
        self.window.mainloop()

    def close(self):
        self.running = False
        if self.window:
            try: self.window.destroy()
            except Exception: pass

@dataclass
class SkibidiState:
    memory: List[Complex] = field(default_factory=lambda: [Complex() for _ in range(MEMORY_SIZE)])
    pointer: int = 0
    pitch: int = 440
    stack: List[Complex] = field(default_factory=list)
    program: List[str] = field(default_factory=list)
    original_program: List[str] = field(default_factory=list)
    ip: int = 0
    debug: bool = False
    output: str = ""
    swapped: bool = False
    spoiled: bool = False
    undefined_behavior: bool = False
    brainrot_count: int = 0
    gooner_activated: bool = False
    paused: bool = False
    variables: Dict[str, float] = field(default_factory=dict)
    labels: Dict[str, int] = field(default_factory=dict)
    imported: Dict[str, Any] = field(default_factory=dict)
    file_handle: Optional[str] = None
    # Epstein nesting
    in_epstein: int = 0
    epstein_target_op: Optional[str] = None
    nested_depth: int = 0
    nested_ops: List[str] = field(default_factory=list)
    nested_ip: List[int] = field(default_factory=list)
    # Diddy+gooner combo
    diddy_gooner_inside: int = 0
    gooner_custom_text: Optional[str] = None
    # Networking
    sigma_net: SigmaNet = field(default_factory=SigmaNet)
    profile: PlayerProfile = field(default_factory=PlayerProfile)
    # 3D
    native3d: Optional[Native3D] = None
    # RNG
    rng_state: bytearray = field(default_factory=lambda: bytearray(16))
    # Metadata
    filename: str = ""
    attached_clients: List[Any] = field(default_factory=list)

# ============================================================
# SCL HELPERS
# ============================================================
def md5_update(state: bytearray):
    h = hashlib.md5(); h.update(state)
    d = h.digest()
    for i in range(16): state[i] = d[i]

def hash_to_pitch(state: bytearray) -> int:
    val = (state[0]<<24) | (state[1]<<16) | (state[2]<<8) | state[3]
    return 200 + (abs(val) % 600)

def skibidi_chaos(s: SkibidiState):
    md5_update(s.rng_state)
    s.pitch = hash_to_pitch(s.rng_state)

def sigma_checksum(data: bytes) -> int:
    c = 0xDEADBEEF
    for b in data:
        c = ((c << 5) + c + b) & 0xFFFFFFFF
        c ^= 0x69696969
    return c

# ============================================================
# NETWORKING
# ============================================================
def sigma_net_init(s: SkibidiState):
    s.sigma_net = SigmaNet()
    s.profile = PlayerProfile()

def sigma_connect(s: SkibidiState, server_ip: str, port: int) -> bool:
    try:
        s.sigma_net.socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sigma_net.socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sigma_net.addr = (server_ip, port)
        bind_port = 42069 + random.randint(0, 999)
        s.sigma_net.socket_fd.bind(('', bind_port))
    except OSError as e:
        print(f"❌ Connect failed: {e}", file=sys.stderr)
        return False
    s.sigma_net.connected = 1
    s.sigma_net.server_ip = server_ip
    s.sigma_net.server_port = port
    print(f"🔗 Connected to {server_ip}:{port} as '{s.profile.player_name}'")
    return True

def sigma_broadcast_memory(s: SkibidiState, index: int):
    if not s.sigma_net.connected: return
    if random.randint(0, 99) < s.profile.packet_loss: return
    try:
        c = s.memory[index]
        pkt = struct.pack('!iiff', 0x534B, index, c.real, c.imag)
        s.sigma_net.socket_fd.sendto(pkt, s.sigma_net.addr)
    except Exception: pass

def sigma_broadcast_action(s: SkibidiState, action: str):
    if not s.sigma_net.connected: return
    try:
        payload = action.encode('utf-8')[:256]
        pkt = struct.pack('!iI', 0x414B, len(payload)) + payload
        s.sigma_net.socket_fd.sendto(pkt, s.sigma_net.addr)
    except Exception: pass

def sigma_rage_quit_check(s: SkibidiState):
    if s.profile.skill_level <= 0:
        print("\n🚪 RAGE QUIT — skill exhausted")
        sys.exit(1)

def sigma_flex(s: SkibidiState, skill_level: int):
    lines = ["packet loss", "skill issue", "lag spike", "buffering", "disconnected"]
    msg = f"{s.profile.player_name}: {lines[random.randint(0,4)]} (skill: {skill_level})"
    print(f"💪 FLEX: {msg}")

def sigma_peer_discovery(s: SkibidiState) -> bool:
    if not s.sigma_net.connected: return False
    print("🔍 Searching for peers...")
    return True

def sigma_receive_thread(s: SkibidiState):
    while s.sigma_net.running:
        try:
            data, addr = s.sigma_net.socket_fd.recvfrom(2048)
            if len(data) >= 12:
                magic = struct.unpack('!i', data[:4])[0]
                if magic == 0x534B:  # mem
                    idx, real, imag = struct.unpack('!iff', data[4:16])
                    if 0 <= idx < MEMORY_SIZE:
                        s.memory[idx].real = real
                        s.memory[idx].imag = imag
                elif magic == 0x414B:  # action
                    ln = struct.unpack('!I', data[4:8])[0]
                    payload = data[8:8+ln].decode('utf-8', errors='replace')
                    if s.debug: print(f"📨 peer action: {payload}")
        except Exception:
            break

def sigma_send_thread(s: SkibidiState):
    while s.sigma_net.running:
        time.sleep(1.0)

# ============================================================
# TOKENIZER + VALID OPS
# ============================================================
MULTI_WORD_OPS = sorted(
    ['magical white liquid', 'the dude who no one invited:', 'dude call', 'triple t', 'im out'],
    key=lambda x: len(x.split()), reverse=True)

VALID_OPS = {
    # core
    'dop', 'bop', 'skibidi', 'grimace', 'toilet', 'rizz', 'sigma', 'ohio',
    '67', 'mango', 'diddy', 'brainrot', 'gooner', 'magical white liquid',
    'sigmaflex', 'epstein', 'gyatt', 'dih', 'vah', 'twin', 'im out',
    'bred', 'dawg', 'triple t', 'patrick', '3d', 'cross', 'dot', 'let', 'get',
    'the dude who no one invited:', 'dude call',
    'kink', 'tiki', 'ip', 'acey', 'speed', 'cristiano', 'messi',
    # 3D
    '3don', '3doff', 'cube', 'sphere', 'cam', 'clear3d',
    # larp
    'Larp', 'larp',
    # STL-specific
    'okay?',
}

def tokenize_program_line(line: str) -> List[str]:
    raw = []
    i, n = 0, len(line)
    while i < n:
        while i < n and line[i].isspace(): i += 1
        if i >= n: break
        if line[i] == ';':
            raw.append(';'); i += 1; continue
        if line[i] == '"':
            j = i + 1
            while j < n and line[j] != '"': j += 1
            if j < n: j += 1
            raw.append(line[i:j]); i = j; continue
        j = i
        while j < n and not line[j].isspace() and line[j] != ';': j += 1
        raw.append(line[i:j]); i = j
    out, i = [], 0
    while i < len(raw):
        matched = False
        for mw in MULTI_WORD_OPS:
            parts = mw.split()
            if i + len(parts) <= len(raw) and raw[i:i+len(parts)] == parts:
                out.append(mw); i += len(parts); matched = True; break
        if not matched:
            out.append(raw[i]); i += 1
    return out

def load_program(s: SkibidiState, filename: str) -> bool:
    try:
        with open(filename, 'r') as fp:
            content = fp.read()
    except IOError as e:
        print(f"Error loading {filename}: {e}", file=sys.stderr)
        return False
    tokens = []
    for line in content.split('\n'):
        if line.lstrip().startswith(';'): continue
        # strip inline comments but keep quoted text
        cleaned = []
        for tok in tokenize_program_line(line):
            cleaned.append(tok)
        # second pass: skip tokens after ';' until EOL
        killed = False
        for tok in cleaned:
            if tok == ';':
                killed = True; continue
            if killed: continue
            if tok.endswith(':') and tok not in VALID_OPS and tok != ':':
                label = tok[:-1]
                s.labels[label] = len(tokens)
                continue
            tokens.append(tok)
    s.program = tokens
    s.original_program = list(tokens)
    return True

# legacy loader used by transformations
def load_skibidi_file(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []
    tokens = []
    for line in content.split('\n'):
        if line.lstrip().startswith(';'): continue
        killed = False
        for tok in tokenize_program_line(line):
            if tok == ';': killed = True; continue
            if killed: continue
            if tok.endswith(':') and tok not in VALID_OPS and tok != ':':
                continue  # drop labels on transform
            tokens.append(tok)
    return tokens

def save_skibidi_file(filename: str, instructions: List[str]):
    try:
        with open(filename, 'w') as f:
            f.write(f"; Generated by STL v1.0.0\n; {'='*60}\n\n")
            for i in range(0, len(instructions), 8):
                f.write(" ".join(instructions[i:i+8]) + "\n")
        print(f"✅ Saved to {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# ============================================================
# EXECUTION
# ============================================================
def print_debug(s: SkibidiState, op: str):
    mag = s.memory[s.pointer].magnitude()
    print(f"[{s.ip}] {op:<20} | P:{s.pitch:3d}Hz | C:{s.pointer:2d} | "
          f"({s.memory[s.pointer].real:.1f}+{s.memory[s.pointer].imag:.1f}i) | "
          f"Mag:{mag:.0f} | Swp:{int(s.swapped)} | Spoil:{int(s.spoiled)} | "
          f"Rot:{s.brainrot_count%2} | Goon:{int(s.gooner_activated)} | Eps:{s.in_epstein}")

def gooner(s: SkibidiState):
    if s.gooner_activated: return
    if s.diddy_gooner_inside:
        final_msg = ""
        if s.gooner_custom_text:
            final_msg = f"[DIDDY_GOONER_INSIDE]: {s.gooner_custom_text}"
        else:
            for i in range(256):
                mag = s.memory[i].magnitude()
                if 0 < mag < 128: final_msg += chr(int(mag) % 95 + 32)
                if 0 < s.memory[i].real < 128: final_msg += chr(int(s.memory[i].real) % 95 + 32)
        s.output += final_msg + "\n"
        print(f"\n🔥 [DIDDY+GOONER INSIDE]: {final_msg}")
        sys.stdout.flush()
        s.diddy_gooner_inside = 0
        s.gooner_custom_text = None
    first_diddy = None
    for i, op in enumerate(s.program):
        if op == "diddy": first_diddy = i; break
    if first_diddy is not None:
        print(f"\n⚠️ Gooner wave: destroying 0..{first_diddy}")
        for i in range(first_diddy + 1):
            if s.program[i] != "magical white liquid":
                s.program[i] = "magical white liquid"
        print("⚠️ Gooner stopped after destroying diddy!")
        s.ip = first_diddy + 1
        return
    print("\n⚠️ Gooner: no diddy found — destroying ALL instructions!")
    for i in range(len(s.program)):
        if s.program[i] != "magical white liquid":
            s.program[i] = "magical white liquid"
    s.gooner_activated = 1
    s.ip = 0

def epstein_execute_inside(s: SkibidiState, outer_op: str, inner_op: str):
    if s.nested_depth >= NESTED_MAX_DEPTH:
        print("Epstein nested too deep!"); return
    s.nested_ops.append(outer_op); s.nested_ip.append(s.ip)
    s.nested_depth += 1
    s.in_epstein = 1
    s.epstein_target_op = inner_op
    execute_instruction(s, inner_op)
    s.nested_depth -= 1
    s.nested_ops.pop(); s.nested_ip.pop()
    s.in_epstein = 1 if s.nested_depth > 0 else 0
    s.epstein_target_op = None

def execute_instruction(state: SkibidiState, op: str):
    """Execute one op. Can modify state.ip; run_program will NOT add 1
    when execute_instruction returns a truthy value indicating ip was set."""
    if state.debug: print_debug(state, op)
    state.undefined_behavior = bool(state.swapped and state.spoiled)

    # ---- pass-throughs ----
    if op == "magical white liquid": return True
    if op == "larp": return True

    if op == "Larp":
        for i in range(len(state.program)):
            if state.program[i] in ('gooner','cristiano','speed','dawg','dih','brainrot'):
                state.program[i] = "larp"
        return True

    if op == "epstein":
        nxt = state.ip + 1
        if nxt < len(state.program):
            inner = state.program[nxt]
            state.ip = nxt
            epstein_execute_inside(state, "epstein", inner)
            return True
        print("Epstein needs an opcode to run inside!"); return True

    if op == "brainrot":
        if state.sigma_net.connected and state.profile.skill_level < 80:
            return True
        if len(state.program) > 1:
            state.program = list(reversed(state.program))
        state.brainrot_count += 1
        state.ip = 0
        state.debug = not state.debug
        if state.sigma_net.connected:
            state.profile.skill_level += 1
            sigma_broadcast_action(state, "BRAINROT")
        return True

    if op == "gooner":
        gooner(state)
        if state.sigma_net.connected:
            sigma_broadcast_action(state, "GOONER")
        return True

    if op == "sigmaflex":
        sigma_flex(state, state.profile.skill_level); return True

    if op == "dih":
        if state.ip + 1 < len(state.program):
            state.file_handle = state.program[state.ip + 1]
            state.ip += 1
        return True

    if op == "vah" and state.file_handle:
        try:
            with open(state.file_handle, 'r') as f:
                data = f.read(4096)
                for i, ch in enumerate(data):
                    if state.pointer + i < MEMORY_SIZE:
                        state.memory[state.pointer + i].real = float(ord(ch))
        except Exception: pass
        return True

    if op == "twin" and state.ip + 1 < len(state.program) and state.file_handle:
        try:
            shutil.copy(state.file_handle, state.program[state.ip + 1]); state.ip += 1
        except Exception: pass
        return True

    if op == "im out" and state.ip + 1 < len(state.program) and state.file_handle:
        try:
            shutil.move(state.file_handle, state.program[state.ip + 1])
            state.file_handle = state.program[state.ip + 1]
            state.ip += 1
        except Exception: pass
        return True

    if op == "bred":
        for _ in range(50): print("Diddy", end=" ")
        print(); return True

    if op == "dawg":
        for _ in range(50): print("W Speed❤️‍🩹", end=" ")
        print(); return True

    if op == "patrick":
        cnt = 10
        if state.ip + 1 < len(state.program):
            try: cnt = int(state.program[state.ip + 1]); state.ip += 1
            except ValueError: pass
        out = "".join(random.choice(ALL_EMOJIS) for _ in range(min(abs(cnt), 100)))
        state.output += out
        print(out)
        return True

    if op == "triple t" and state.ip + 1 < len(state.program):
        var = state.program[state.ip + 1]
        val = state.variables.get(var, state.memory[state.pointer].magnitude())
        state.output += f"T{val:.4f}T"
        print(f"T{val:.4f}T", end="")
        state.ip += 1
        return True

    if op == "the dude who no one invited:":
        spec = ""
        temp_ip = state.ip + 1
        while (temp_ip < len(state.program)
               and state.program[temp_ip] != ";"
               and state.program[temp_ip] != "then"
               and state.program[temp_ip] not in VALID_OPS):
            spec += state.program[temp_ip] + " "
            temp_ip += 1
        spec = spec.strip()
        parts = spec.split()
        if parts:
            mod_name = parts[0]
            alias = parts[2] if len(parts) >= 3 and parts[1] == "as" else mod_name
            try:
                imp = __import__(mod_name)
                for part in mod_name.split('.')[1:]:
                    imp = getattr(imp, part)
                state.imported[alias] = imp
                print(f"🧑 {alias} joined")
            except Exception as e:
                print(f"🧑 {mod_name} didn't show: {e}")
        state.ip = temp_ip - 1  # FIX: resume at first unconsumed token
        return True

    if op == "dude call" and state.ip + 1 < len(state.program):
        call_str = state.program[state.ip + 1]
        parts = call_str.split('.')
        if len(parts) >= 2 and parts[0] in state.imported:
            module = state.imported[parts[0]]
            func_name = '.'.join(parts[1:])
            args = []
            temp_ip = state.ip + 2
            while (temp_ip < len(state.program)
                   and state.program[temp_ip] != ";"
                   and state.program[temp_ip] not in VALID_OPS):
                try: args.append(int(state.program[temp_ip]))
                except ValueError:
                    try: args.append(float(state.program[temp_ip]))
                    except ValueError: args.append(state.program[temp_ip])
                temp_ip += 1
            try:
                fn = eval(f"module.{func_name}")
                res = fn(*args)
                if isinstance(res, (int, float)):
                    state.memory[state.pointer].real = float(res)
                print(f"🧑 {call_str} → {res}")
            except Exception as e:
                print(f"🧑 call failed: {e}")
            state.ip = temp_ip - 1  # FIX
        else:
            print(f"🧑 module {parts[0] if parts else '?'} not found")
            state.ip += 1
        return True

    if op == "let" and state.ip + 2 < len(state.program):
        state.variables[state.program[state.ip + 1]] = state.memory[state.pointer].magnitude()
        state.ip += 2
        return True

    if op == "get" and state.ip + 1 < len(state.program):
        if state.program[state.ip + 1] in state.variables:
            state.memory[state.pointer].real = state.variables[state.program[state.ip + 1]]
        state.ip += 1
        return True

    if op == "3d":
        if state.pointer + 2 < MEMORY_SIZE:
            state.memory[state.pointer + 1].real = state.memory[state.pointer + 2].real = 0
        return True

    if op == "cross" and state.ip + 3 < len(state.program):
        ax, ay, az = state.pointer, state.pointer + 1, state.pointer + 2
        bx = int(state.program[state.ip + 1]) % MEMORY_SIZE
        by = int(state.program[state.ip + 2]) % MEMORY_SIZE
        bz = int(state.program[state.ip + 3]) % MEMORY_SIZE
        cx = state.memory[ay].real * state.memory[bz].real - state.memory[az].real * state.memory[by].real
        cy = state.memory[az].real * state.memory[bx].real - state.memory[ax].real * state.memory[bz].real
        cz = state.memory[ax].real * state.memory[by].real - state.memory[ay].real * state.memory[bx].real
        state.memory[ax].real, state.memory[ay].real, state.memory[az].real = cx, cy, cz
        state.ip += 3
        return True

    if op == "dot" and state.ip + 3 < len(state.program):
        ax, ay, az = state.pointer, state.pointer + 1, state.pointer + 2
        bx = int(state.program[state.ip + 1]) % MEMORY_SIZE
        by = int(state.program[state.ip + 2]) % MEMORY_SIZE
        bz = int(state.program[state.ip + 3]) % MEMORY_SIZE
        state.memory[state.pointer].real = (
            state.memory[ax].real * state.memory[bx].real
            + state.memory[ay].real * state.memory[by].real
            + state.memory[az].real * state.memory[bz].real)
        state.ip += 3
        return True

    if op == "diddy":
        nxt = state.ip + 1
        found_gooner = False
        custom = None
        end_ip = nxt
        if nxt < len(state.program) and state.program[nxt] == "gooner":
            found_gooner = True
            end_ip = nxt + 1
            if end_ip < len(state.program) and state.program[end_ip].startswith('"'):
                m = state.program[end_ip]
                if len(m) >= 2 and m[0] == '"' and m[-1] == '"':
                    custom = m[1:-1]
                end_ip += 1
        if found_gooner:
            if state.spoiled or state.undefined_behavior:
                print("\n💥 CRASH", file=sys.stderr)
                if state.sigma_net.connected:
                    state.profile.skill_level -= 50
                    sigma_rage_quit_check(state)
                sys.exit(1)
            state.diddy_gooner_inside = 1
            state.gooner_custom_text = custom
            gooner(state)
            if state.ip < end_ip - 1:
                state.ip = end_ip - 1
        else:
            if state.spoiled or state.undefined_behavior:
                print("\n💥 CRASH", file=sys.stderr)
                if state.sigma_net.connected:
                    state.profile.skill_level -= 50
                    sigma_rage_quit_check(state)
                sys.exit(1)
            print("milk milk milk")
        return True

    # ---- 3D ----
    if op == "3don":
        if state.native3d is None: state.native3d = Native3D()
        state.native3d.enabled = True
        if not state.native3d.window:
            threading.Thread(target=state.native3d.start_window, daemon=True).start()
        return True

    if op == "3doff":
        if state.native3d and state.native3d.enabled: state.native3d.close()
        return True

    if op == "cube":
        if state.native3d and state.native3d.enabled:
            x = state.memory[state.pointer].real
            y = state.memory[state.pointer].imag
            z = state.memory[state.pointer + 1].real if state.pointer + 1 < MEMORY_SIZE else 0
            sz = state.memory[state.pointer + 2].real if state.pointer + 2 < MEMORY_SIZE else 1
            state.native3d.add_cube(x, y, z, sz)
        return True

    if op == "sphere":
        if state.native3d and state.native3d.enabled:
            x = state.memory[state.pointer].real
            y = state.memory[state.pointer].imag
            z = state.memory[state.pointer + 1].real if state.pointer + 1 < MEMORY_SIZE else 0
            r = state.memory[state.pointer + 2].real if state.pointer + 2 < MEMORY_SIZE else 0.5
            state.native3d.add_sphere(x, y, z, r)
        return True

    if op == "cam":
        if state.native3d and state.native3d.enabled:
            state.native3d.camera.x = state.memory[state.pointer].real
            state.native3d.camera.y = state.memory[state.pointer].imag
            state.native3d.camera.z = state.memory[state.pointer + 1].real if state.pointer + 1 < MEMORY_SIZE else 10
        return True

    if op == "clear3d":
        if state.native3d and state.native3d.enabled:
            state.native3d.objects.clear()
        return True

    # ---- requested meme ops ----
    if op == "kink":
        print("\n🔥 KINK ACTIVATED: 5 Epsteins × 9,999 gooners...")
        for i in range(5):
            print(f"  Epstein #{i+1}...")
            time.sleep(0.1)
            if random.random() < 0.3:
                print("You were so hard daddy~😩😩😩")
                return True
        print("✅ spawned")
        state.profile.skill_level += 100
        return True

    if op == "tiki":
        copypasta = ("Hey brother 😭🙏 I gotta ask, why didn't you use Tiki Phonk this time? 🗿 Honestly, Tiki Phonk would've matched the whole vibe perfectly and made the edit way more energetic ⚡🔥 The bass, the cowbells, and the overall atmosphere would've gone absolutely crazy 🎧💥 I was genuinely expecting that style because it always makes the clips feel smoother, harder, and way more satisfying to watch 👌💯 Don't get me wrong though, the edit was still clean 🍷 but Tiki Phonk would've pushed it to another level entirely 🚀 The way those distorted beats sync with transitions is unmatched 😭 Every flash, zoom, and movement would've hit ten times harder 💣 The music basically gives edits an aura 👁️🗿 Like the second the beat drops, everything suddenly feels cinematic and dangerous 😈⚔️ Brother, your editing style already fits Tiki Phonk perfectly too 🤝 The pacing, the transitions, the effects — all of it screams for that aggressive energy 🔥 Imagine the bass dropping exactly when the clips switch 💥 or the cowbells echoing during the slow motion parts 🎶 That would've been legendary 😭🙏 People definitely would've replayed the edit over and over because the vibe would've been addicting 📈🌀 That's the thing with Tiki Phonk 🎧 It doesn't just sound cool — it transforms the whole experience 🌌 Even simple clips start feeling powerful and memorable 🗿 The atmosphere becomes darker, cleaner, and way more hype ⚡ Without it, the edit still looks good, but with it? Brother… it becomes generational 🍷🔥 Next time, trust the vision and let the Tiki Phonk carry the edit 😭🙏 Let the bass shake the screen 💣 let the transitions breathe with the beat 🎶 and let the aura consume the entire video 👁️🗿 Trust me brother, everything will sound cleaner, hit harder, and feel way more unforgettable 💯 Capiche boy? 🍷🗿")
        print(copypasta)
        state.output += copypasta
        return True

    if op == "ip":
        print("198.234.45.207")
        if state.native3d and state.native3d.enabled:
            state.native3d.add_text(0, 2, 0, "198.234.45.207", "#ff6600")
        return True

    if op == "acey":
        print('Please, Speed. I need this~~~~ My mum is kinda homeless')
        return True

    if op == "speed":
        print("SEWEY same")
        state.profile.skill_level += 50
        return True

    if op == "cristiano":
        print("SUUUUUUUUU")
        state.memory[state.pointer].real = 7
        state.memory[state.pointer].imag = 77
        return True

    if op == "messi":
        for _ in range(10): print("stfu", end=" ")
        print(); return True

    # ---- okay? (STL-specific) ----
    if op == "okay?":
        handle_okay_command(state)
        return True

    # ---- core ops (blocked by gooner) ----
    if state.gooner_activated:
        return True

    if op == "dop":
        if state.spoiled and not state.undefined_behavior:
            state.memory[state.pointer].real -= 1.0
        else:
            state.memory[state.pointer].real += 1.0
        if state.sigma_net.connected: sigma_broadcast_memory(state, state.pointer)
    elif op == "bop":
        if state.spoiled and not state.undefined_behavior:
            state.memory[state.pointer].imag += 1.0
        else:
            state.memory[state.pointer].imag -= 1.0
        if state.sigma_net.connected: sigma_broadcast_memory(state, state.pointer)
    elif op == "skibidi":
        skibidi_chaos(state)
    elif op == "grimace":
        move_right = (state.pitch < 440) if (state.spoiled and not state.undefined_behavior) else (state.pitch >= 440)
        state.pointer = (state.pointer + 1) % MEMORY_SIZE if move_right else (state.pointer - 1 + MEMORY_SIZE) % MEMORY_SIZE
    elif op == "toilet":
        if len(state.stack) < STACK_SIZE:
            state.stack.append(Complex(state.memory[state.pointer].real, state.memory[state.pointer].imag))
            state.memory[state.pointer].zero()
    elif op == "rizz":
        mag = state.memory[state.pointer].magnitude()
        if state.spoiled and not state.undefined_behavior: mag *= 2.0
        state.output += chr(int(math.floor(mag)) % 128)
    elif op == "sigma":
        try:
            ch = sys.stdin.read(1)
            state.memory[state.pointer].real = float(ord(ch)) if ch else 0.0
            state.memory[state.pointer].imag = 0.0
        except Exception:
            state.memory[state.pointer].real = 0.0
    elif op == "ohio":
        jump = int(math.floor(state.memory[state.pointer].magnitude()))
        if state.spoiled and not state.undefined_behavior:
            if jump > 0: state.ip += jump
        else:
            if jump > 0 and jump <= state.ip: state.ip -= jump
    elif op == "67":
        if state.undefined_behavior:
            if random.randint(0, 1): state.swapped = not state.swapped
        elif not state.spoiled:
            state.swapped = not state.swapped
    elif op == "mango":
        if state.undefined_behavior:
            if random.randint(0, 1): state.spoiled = not state.spoiled
        else:
            state.spoiled = not state.spoiled
    elif op == "gyatt":
        if state.stack:
            mag = state.stack[-1].magnitude()
            threshold = 50 if state.spoiled else 100
            if state.sigma_net.connected:
                sigma_broadcast_action(state, f"GYATT (mag={mag:.1f})")
            if mag > threshold:
                jump = max(1, int(math.floor(mag / 10)))
                if state.undefined_behavior:
                    state.ip += jump if random.randint(0, 1) else -jump
                else:
                    state.ip += jump
        elif state.debug:
            print(" | GYATT fail (stack empty)")
    return True  # executed cleanly

def run_program(state: SkibidiState, chaos_mode: bool = False):
    state.ip = 0
    state.output = ""
    guard = 0
    while 0 <= state.ip < len(state.program):
        guard += 1
        if guard > 5_000_000:
            print("⚠️ infinite loop guard tripped"); break
        if terminal_paused:
            time.sleep(0.1); continue
        if state.paused:
            time.sleep(0.1); continue
        op = state.program[state.ip]
        if chaos_mode and random.random() < 0.10:
            chaos_ops = ['skibidi', 'gyatt', 'brainrot', 'mango', '67', 'okay?']
            ins = random.choice(chaos_ops)
            print(f"🎲 CHAOS INSERT: {ins}")
            execute_instruction(state, ins)
        before = state.ip
        execute_instruction(state, op)
        if state.ip == before:
            state.ip += 1
        if state.undefined_behavior and random.random() < 0.05:
            print("💀 REALITY COLLAPSE")
            break

# ============================================================
# OKAY? HANDLER
# ============================================================
def handle_okay_command(state: SkibidiState, args: List[str] = None):
    global terminal_paused
    roll = random.random()
    if args and args[0] == "--okay?":
        if len(args) > 1:
            print(f"\n🎲 okay? checking '{args[1]}'")
            sub = random.random()
            if sub < 0.33:
                print(f"✨ OK — redoing"); return True
            elif sub < 0.66:
                print(f"💀 NOT OKAY — undoing"); return False
            else:
                print(f"⏸️ depends on how i feel later~"); terminal_paused = True; return None
    if roll < 0.33:
        okay_tracker.redo_everything(state); return True
    elif roll < 0.66:
        okay_tracker.undo_everything(state); return True
    else:
        print("\n⏸️ depends on how i feel later~... type 'resume'")
        terminal_paused = True; return True

# ============================================================
# TRANSFORMATION ENGINES (all -ify commands)
# ============================================================
def flip_program(p): return list(reversed(p))

def invert_program(p):
    m = {'dop':'bop','bop':'dop','real':'imag','imag':'real'}
    return [m.get(x, x) for x in p]

def chaos_program(p, times=5):
    r = p.copy()
    for _ in range(times): random.shuffle(r)
    print(f"🎲 shuffled ×{times}"); return r

def mutate_program(p, rate=0.1):
    valid = ['dop','bop','skibidi','grimace','toilet','rizz','sigma','ohio','67','mango',
             'diddy','brainrot','gooner','gyatt','okay?']
    r = p.copy()
    n = int(len(r) * rate)
    for pos in random.sample(range(len(r)), min(n, len(r))):
        r[pos] = random.choice(valid)
    print(f"🧬 mutated {n}"); return r

def compress_program(p): return [x for x in p if x != "magical white liquid"]
def expand_program(p):
    r = []
    for x in p: r += [x, "magical white liquid"]
    return r

def corrupt_program(p, rate=0.01):
    r = []
    for x in p:
        if random.random() < rate and x:
            pos = random.randint(0, len(x)-1)
            x = x[:pos] + chr(ord(x[pos]) ^ (1 << random.randint(0,7))) + x[pos+1:]
        r.append(x)
    print(f"💀 corrupted ~{int(len(p)*rate)}"); return r

def diddyfy_program(p): return ["diddy"] * len(p)
def goonerfy_program(p): return ["magical white liquid"] * len(p)
def epsteinize_program(p):
    r = []
    for x in p: r += ["epstein", x]
    return r

def ohioify_program(p):
    r = []
    i = 0
    while i < len(p):
        r.append(p[i])
        if p[i] == "ohio" and i+1 < len(p):
            try:
                v = int(p[i+1]); r.append(str(-v if v > 0 else abs(v))); i += 2; continue
            except ValueError: pass
        i += 1
    return r

def gyattify_program(p):
    r = []
    for x in p:
        r.append(x)
        if x == "toilet": r.append("gyatt")
    return r

def upside_down_program(p):
    m = {'dop':'bop','bop':'dop','real':'imag'}
    return [m.get(x, x) for x in p]

def inside_out_program(p):
    m = {'dop':'bop','grimace':'skibidi'}
    return [m.get(x, x) for x in p]

def mirror_program(p): return p + list(reversed(p))

def thicc_program(p):
    out = []
    for x in p:
        try: out.append(str(int(x)*69))
        except ValueError:
            try: out.append(str(float(x)*69))
            except ValueError: out.append(x)
    print("🍑 ×69"); return out

def skinny_program(p):
    out = []
    for x in p:
        try:
            v = int(x)
            out.append(str(v // 69) if v % 69 == 0 else str(v / 69))
        except ValueError:
            try: out.append(str(float(x)/69))
            except ValueError: out.append(x)
    print("💀 ÷69"); return out

# ---- NEW v1.0 -ify commands ----
def larpify_program(p):
    """Replace gooner/cristiano/speed/dawg/dih/brainrot with larp."""
    m = {'gooner':'larp','cristiano':'larp','speed':'larp','dawg':'larp','dih':'larp','brainrot':'larp'}
    return [m.get(x, x) for x in p]

def rizzify_program(p):
    """Append rizz after every op."""
    r = []
    for x in p: r += [x, "rizz"]
    return r

def skibidiify_program(p):
    r = []
    for x in p: r += [x, "skibidi"]
    return r

def toiletify_program(p):
    r = []
    for x in p: r += [x, "toilet"]
    return r

def grimaceify_program(p):
    r = []
    for x in p: r += [x, "grimace"]
    return r

def okayify_program(p):
    """Randomly insert okay? between ops."""
    r = []
    for x in p:
        r.append(x)
        if random.random() < 0.5: r.append("okay?")
    return r

def sigmaflexify_program(p):
    r = []
    for x in p: r += [x, "sigmaflex"]
    return r

def patrickify_program(p):
    r = []
    for x in p: r += [x, "patrick"]
    return r

def bredify_program(p):
    r = []
    for x in p: r += [x, "bred"]
    return r

def dawgify_program(p):
    r = []
    for x in p: r += [x, "dawg"]
    return r

def speedify_program(p):
    m = {'gooner':'speed','cristiano':'speed','dawg':'speed','dih':'speed','brainrot':'speed'}
    return [m.get(x, x) for x in p]

def cristianoify_program(p):
    m = {'gooner':'cristiano','speed':'cristiano','dawg':'cristiano','dih':'cristiano','brainrot':'cristiano'}
    return [m.get(x, x) for x in p]

def messiify_program(p):
    """Append messi after every 3rd op."""
    r = []
    for i, x in enumerate(p):
        r.append(x)
        if i % 3 == 0: r.append("messi")
    return r

def kinkify_program(p):
    return ["kink"] + list(p)

def tikify_program(p):
    return ["tiki"] + list(p)

def ipify_program(p):
    return ["ip"] + list(p) + ["ip"]

def 3dify_program(p):
    return ["3don"] + list(p)

def cubeify_program(p):
    return ["3don", "cube"] + list(p)

def sphereify_program(p):
    return ["3don", "sphere"] + list(p)

def camify_program(p):
    return ["cam"] + list(p)

def crossify_program(p):
    r = []
    for x in p:
        r.append(x)
        if x in ('dop','bop'): r += ["cross", "0", "1", "2"]
    return r

def dotify_program(p):
    r = []
    for x in p:
        r.append(x)
        if x in ('dop','bop'): r += ["dot", "0", "1", "2"]
    return r

def sigmaify_program(p):
    m = {'gooner':'sigma','cristiano':'sigma','speed':'sigma','dawg':'sigma','dih':'sigma','brainrot':'sigma'}
    return [m.get(x, x) for x in p]

def dopify_program(p):
    m = {'bop':'dop','skibidi':'dop','grimace':'dop'}
    return [m.get(x, x) for x in p]

def bopify_program(p):
    m = {'dop':'bop','skibidi':'bop','grimace':'bop'}
    return [m.get(x, x) for x in p]

def brainrotify_program(p):
    return list(p) + ["brainrot"]

def gyattify_more_program(p):
    """Full gyatt-ification: gyatt after every op."""
    r = []
    for x in p: r += [x, "gyatt"]
    return r

def epsteinify_program(p):
    """Wrap each op with epstein prefix (alias for epsteinize)."""
    r = []
    for x in p: r += ["epstein", x]
    return r

def mixify_program(p, seed=0):
    """Apply 3 random transformations."""
    rnd = random.Random(seed) if seed else random
    fns = [flip_program, invert_program, chaos_program, mutate_program,
           larpify_program, rizzify_program, skibidiify_program, gyattify_program,
           mirror_program, inside_out_program, upside_down_program, dotify_program]
    chosen = rnd.sample(fns, k=3)
    r = list(p)
    for fn in chosen:
        print(f"  → {fn.__name__}")
        r = fn(r)
    return r

# Registry for REPL dispatch
TRANSFORMS = {
    'flip': flip_program, 'invert': invert_program,
    'chaos': lambda p, times=5: chaos_program(p, times),
    'mutate': lambda p, rate=0.1: mutate_program(p, rate),
    'compress': compress_program, 'expand': expand_program,
    'corrupt': corrupt_program,
    'diddyfy': diddyfy_program, 'goonerfy': goonerfy_program,
    'epsteinize': epsteinize_program, 'epsteinify': epsteinify_program,
    'ohioify': ohioify_program, 'gyattify': gyattify_program,
    'upside-down': upside_down_program, 'inside-out': inside_out_program,
    'mirror': mirror_program, 'thicc': thicc_program, 'skinny': skinny_program,
    # v1.0
    'larpify': larpify_program, 'rizzify': rizzify_program,
    'skibidiify': skibidiify_program, 'toiletify': toiletify_program,
    'grimaceify': grimaceify_program, 'okayify': okayify_program,
    'sigmaflexify': sigmaflexify_program, 'patrickify': patrickify_program,
    'bredify': bredify_program, 'dawgify': dawgify_program,
    'speedify': speedify_program, 'cristianoify': cristianoify_program,
    'messiify': messiify_program, 'kinkify': kinkify_program,
    'tikify': tikify_program, 'ipify': ipify_program,
    '3dify': 3dify_program, 'cubeify': cubeify_program,
    'sphereify': sphereify_program, 'camify': camify_program,
    'crossify': crossify_program, 'dotify': dotify_program,
    'sigmaify': sigmaify_program, 'dopify': dopify_program,
    'bopify': bopify_program, 'brainrotify': brainrotify_program,
    'gyattify-more': gyattify_more_program, 'mixify': mixify_program,
}

# ============================================================
# DEBUGGER / ATTACH
# ============================================================
class STLDebugger:
    def __init__(self):
        self.active_states: Dict[str, SkibidiState] = {}
        self.clients: Dict[str, Any] = {}
    def attach(self, sid: str, state: SkibidiState) -> str:
        cid = hashlib.md5(f"{sid}{time.time()}".encode()).hexdigest()[:8]
        self.active_states[cid] = state
        self.clients[cid] = {"id": cid, "connected_at": time.time()}
        print(f"🔗 Attached to {sid} as {cid}")
        return cid
    def detach(self, cid: str):
        if cid in self.active_states:
            del self.active_states[cid]; del self.clients[cid]
            print(f"🔌 Detached {cid}")
        else:
            print(f"❌ Client {cid} not found")
    def pause(self, cid: str):
        if cid in self.active_states:
            self.active_states[cid].paused = True; print("⏸️ Paused")
    def resume(self, cid: str):
        if cid in self.active_states:
            self.active_states[cid].paused = False; print("▶️ Resumed")

debugger = STLDebugger()

# ============================================================
# HELPERS FOR REPL
# ============================================================
def inject_instructions(state, instrs, at_ip):
    state.program = state.program[:at_ip] + instrs + state.program[at_ip:]
    print(f"💉 Injected {len(instrs)} at {at_ip}")

def replace_instruction(state, pos, new_op):
    if 0 <= pos < len(state.program):
        old = state.program[pos]; state.program[pos] = new_op
        print(f"🔄 [{pos}]: {old} → {new_op}")
    else: print(f"❌ {pos} out of range")

def swap_instructions(state, a, b):
    if 0 <= a < len(state.program) and 0 <= b < len(state.program):
        state.program[a], state.program[b] = state.program[b], state.program[a]
        print(f"🔀 [{a}] ↔ [{b}]")
    else: print(f"❌ invalid positions")

def clone_cell(state, ptr):
    if 0 <= ptr < MEMORY_SIZE:
        state.memory[ptr] = Complex(state.memory[state.pointer].real, state.memory[state.pointer].imag)
        print(f"📋 {state.pointer} → {ptr}")
    else: print(f"❌ {ptr}")

def splice_instructions(state, a, b, at):
    if 0 <= a < b <= len(state.program) and 0 <= at <= len(state.program):
        cut = state.program[a:b]
        state.program = state.program[:a] + state.program[b:]
        state.program = state.program[:at] + cut + state.program[at:]
        print(f"✂️ [{a}:{b}] → {at}")
    else: print(f"❌ invalid splice")

# ============================================================
# DEMO GENERATORS
# ============================================================
def create_demo(fname):
    with open(fname, 'w') as fp:
        fp.write("; STL v1.0 demo\n")
        fp.write("dop " * 65 + "rizz\n")
        fp.write("grimace\n")
        fp.write("epstein rizz\n")
        fp.write("dop dop dop dop toilet\n")
        fp.write("gyatt\n")
        fp.write('diddy gooner "Hello from Epstein inside Diddy!"\n')
        fp.write("diddy\n")
    print(f"✅ wrote {fname}")

def create_evil_hello(fname):
    with open(fname, 'w') as fp:
        fp.write("; Evil Hello\n")
        fp.write("dop " * 65 + "rizz\n")
        fp.write("skibidi grimace\n")
        fp.write("dop " * 11 + "toilet\n")
        fp.write("gyatt\n")
        fp.write("epstein sigmaflex\n")
        fp.write('diddy gooner "EVIL FROM EPSTEIN"\n')
    print(f"✅ wrote {fname}")

# ============================================================
# REPL
# ============================================================
def repl():
    global terminal_paused
    state = SkibidiState()
    sigma_net_init(state)
    attached_id = None
    chaos_runtime = False

    print(f"{VERSION}")
    print("Type 'help' for commands, 'exit' to leave.")
    print("✨ 'okay?' → OK (redo) | NOT OKAY (undo) | depends... (pause)")

    while True:
        try:
            if terminal_paused:
                choice = input("⏸️ [PAUSED] resume? (y/n): ").strip().lower()
                if choice in ('y', 'resume'):
                    terminal_paused = False; print("▶️ Resumed")
                continue

            line = input(PROMPT).strip()
            if not line: continue
            if line == "exit":
                print("🚽✨"); break

            okay_tracker.snapshot(state)

            parts = line.split()
            cmd, args = parts[0], parts[1:]

            if cmd == "okay?":
                handle_okay_command(state, args); continue
            if cmd == "resume":
                terminal_paused = False; print("▶️ Resumed"); continue

            # run / debug
            if cmd == "run" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    state.program = prog; state.filename = args[0]
                    print(f"🏃 Running {args[0]} ({len(prog)} ops)")
                    run_program(state, chaos_runtime)
                    print(f"\n📤 Output: {state.output}")

            elif cmd == "debug" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    state.debug = True; state.program = prog
                    print(f"🐛 Debug: {args[0]}")
                    run_program(state, chaos_runtime)
                    state.debug = False

            elif cmd in TRANSFORMS and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    extra = args[1:]
                    try:
                        result = TRANSFORMS[cmd](prog, *extra)
                    except TypeError:
                        try:
                            result = TRANSFORMS[cmd](prog, *map(float, extra))
                        except Exception as e:
                            print(f"❌ {e}"); continue
                    save_skibidi_file(f"{cmd}_{args[0]}", result)

            elif cmd == "attach":
                if state.filename:
                    attached_id = debugger.attach(state.filename, state)
                else: print("No loaded program")

            elif cmd == "detach":
                if attached_id: debugger.detach(attached_id); attached_id = None
                else: print("Not attached")

            elif cmd == "pause" and attached_id: debugger.pause(attached_id)
            elif cmd == "resume" and attached_id: debugger.resume(attached_id)

            elif cmd == "inject" and len(args) >= 1:
                inject_instructions(state, args[0].split(), state.ip)
            elif cmd == "replace" and len(args) >= 2:
                replace_instruction(state, int(args[0]), args[1])
            elif cmd == "swap" and len(args) >= 2:
                swap_instructions(state, int(args[0]), int(args[1]))
            elif cmd == "reverse":
                state.program = list(reversed(state.program))
                print("🔀 reversed")
            elif cmd == "clone" and args:
                clone_cell(state, int(args[0]))
            elif cmd == "splice" and len(args) >= 3:
                splice_instructions(state, int(args[0]), int(args[1]), int(args[2]))

            elif cmd == "--chaos":
                chaos_runtime = not chaos_runtime
                print(f"🎲 Chaos: {'ON' if chaos_runtime else 'OFF'}")

            # networking
            elif cmd == "connect" and args:
                ip = args[0]
                port = int(args[1]) if len(args) > 1 else 42069
                if sigma_connect(state, ip, port):
                    state.sigma_net.running = 1
                    state.sigma_net.recv_thread = threading.Thread(
                        target=sigma_receive_thread, args=(state,), daemon=True)
                    state.sigma_net.send_thread = threading.Thread(
                        target=sigma_send_thread, args=(state,), daemon=True)
                    state.sigma_net.recv_thread.start()
                    state.sigma_net.send_thread.start()
                    sigma_peer_discovery(state)

            elif cmd == "name" and args:
                state.profile.player_name = args[0][:31]
                print(f"🧑 name → {state.profile.player_name}")

            elif cmd == "skill" and args:
                state.profile.skill_level = int(args[0])
                print(f"💪 skill → {state.profile.skill_level}")

            elif cmd == "3don":
                execute_instruction(state, "3don")
            elif cmd == "3doff":
                execute_instruction(state, "3doff")

            elif cmd == "demo":
                create_demo("stl_demo.skb")
            elif cmd == "evil-hello":
                create_evil_hello("stl_evil.skb")

            elif cmd == "show":
                print(f"File: {state.filename or 'none'}")
                print(f"Instructions: {len(state.program)}")
                print(f"IP: {state.ip}/{len(state.program)}")
                print(f"Pointer: {state.pointer}")
                print(f"Output length: {len(state.output)}")
                print(f"Swapped: {state.swapped} | Spoiled: {state.spoiled}")
                print(f"Gooner: {state.gooner_activated} | Epstein: {state.in_epstein}")
                print(f"Chaos: {chaos_runtime} | Paused: {terminal_paused}")
                print(f"Connected: {state.sigma_net.connected} | Skill: {state.profile.skill_level}")
                print(f"History size: {len(okay_tracker.command_history)} commands")
                print(f"3D: {state.native3d.enabled if state.native3d else False}")

            elif cmd == "history":
                print(f"\n📜 History ({len(okay_tracker.command_history)}):")
                for i, e in enumerate(okay_tracker.command_history[-20:]):
                    print(f"  {i}: {e}")

            elif cmd == "transforms":
                print("🛠️  Available -ify commands:")
                for name in sorted(TRANSFORMS): print(f"   {name} <file.skb>")

            elif cmd == "help":
                print("""
╔══════════════════════════════════════════════════════════════════╗
║  STL v1.0.0 — The Full Port                                      ║
╠══════════════════════════════════════════════════════════════════╣
║  ✨ okay? — 33% OK / 33% NOT OKAY / 34% depends...                ║
║    --okay? <cmd>           apply to specific command             ║
║                                                                  ║
║  📁 FILE                                                         ║
║    run <file.skb>          execute                               ║
║    debug <file.skb>        step-by-step                          ║
║    flip / invert / chaos / mutate / compress / expand / corrupt  ║
║    diddyfy / goonerfy / epsteinize / epsteinify / ohioify        ║
║    gyattify / upside-down / inside-out / mirror / thicc / skinny ║
║                                                                  ║
║  🆕 v1.0 -ify commands                                           ║
║    larpify / rizzify / skibidiify / toiletify / grimaceify       ║
║    okayify / sigmaflexify / patrickify / bredify / dawgify       ║
║    speedify / cristianoify / messiify / kinkify / tikify         ║
║    ipify / 3dify / cubeify / sphereify / camify / crossify       ║
║    dotify / sigmaify / dopify / bopify / brainrotify             ║
║    gyattify-more / mixify                                        ║
║                                                                  ║
║  🌐 NETWORKING                                                   ║
║    connect <ip> [port]     join sigma net                        ║
║    name <name>             set player name                       ║
║    skill <n>               set skill level                       ║
║                                                                  ║
║  🎮 3D                                                            ║
║    3don / 3doff            toggle native 3D window               ║
║                                                                  ║
║  🔧 LIVE                                                         ║
║    attach / detach / pause / resume                              ║
║    inject "ops..." / replace N "op" / swap A B                   ║
║    reverse / clone N / splice A B C                              ║
║                                                                  ║
║  🌈 MODES                                                        ║
║    --chaos                 random injection on each step         ║
║                                                                  ║
║  📊 INFO                                                         ║
║    show / history / transforms / demo / evil-hello               ║
║    help / exit                                                   ║
╚══════════════════════════════════════════════════════════════════╝
                """)
            else:
                print(f"Unknown command: {cmd}. Type 'help'.")

        except EOFError:
            print("\n🚽✨"); break
        except KeyboardInterrupt:
            print("\n⏸️ Interrupted — type 'resume' or 'exit'")
            terminal_paused = True
        except Exception as e:
            print(f"Error: {e}")

# ============================================================
# CLI MAIN
# ============================================================
def main():
    random.seed(int(time.time()))
    if len(sys.argv) == 1:
        repl(); return 0

    args = sys.argv[1:]
    s = SkibidiState()
    sigma_net_init(s)
    filename = None
    server_ip = None
    server_port = 42069
    run_after = False

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--debug": s.debug = True
        elif a == "--connect" and i+1 < len(args):
            i += 1; server_ip = args[i]
        elif a == "--port" and i+1 < len(args):
            i += 1; server_port = int(args[i])
        elif a == "--skill" and i+1 < len(args):
            i += 1; s.profile.skill_level = int(args[i])
        elif a == "--name" and i+1 < len(args):
            i += 1; s.profile.player_name = args[i][:31]
        elif a == "--demo":
            create_demo("stl_demo.skb"); return 0
        elif a == "--evil-hello":
            create_evil_hello("stl_evil.skb"); return 0
        elif a == "--run":
            run_after = True
        elif a == "--repl":
            repl(); return 0
        elif not a.startswith('-'):
            filename = a
        i += 1

    if server_ip:
        if not sigma_connect(s, server_ip, server_port):
            print("Connection failed", file=sys.stderr); return 1
        s.sigma_net.running = 1
        s.sigma_net.recv_thread = threading.Thread(target=sigma_receive_thread, args=(s,), daemon=True)
        s.sigma_net.send_thread = threading.Thread(target=sigma_send_thread, args=(s,), daemon=True)
        s.sigma_net.recv_thread.start(); s.sigma_net.send_thread.start()
        sigma_peer_discovery(s); time.sleep(0.5)

    if not filename:
        print(f"Usage: {sys.argv[0]} <file.skb> [--debug] [--run]")
        print(f"       {sys.argv[0]} --connect <ip> [--port N] [--name X]")
        print(f"       {sys.argv[0]} --demo | --evil-hello")
        print(f"       {sys.argv[0]}           (opens REPL)")
        return 0

    if not load_program(s, filename):
        print(f"Failed to load: {filename}", file=sys.stderr); return 1

    print(f"=== STL v1.0.0 === ({filename})")
    run_program(s)
    print(f"\n--- done ---\nOutput: {s.output}")
    if s.sigma_net.connected and s.sigma_net.socket_fd:
        s.sigma_net.running = 0
        try: s.sigma_net.socket_fd.close()
        except Exception: pass
    return 0

if __name__ == "__main__":
    sys.exit(main())
