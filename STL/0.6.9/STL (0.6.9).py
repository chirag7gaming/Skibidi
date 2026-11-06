#!/usr/bin/env python3
# stl_v069.py — Skibidi Terminal Language v0.6.9
# "The terminal language that doesn't care. It outputs 🚽✨ anyway."

import sys
import random
import math
import readline
import time
import os
import json
import pickle
import hashlib
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
import threading
import queue

# ============================================================
# CONFIG
# ============================================================
VERSION = "Skibidi Terminal Language v0.6.9 — Brainrot Edition"
PROMPT = "> "
MEMORY_SIZE = 65536
STACK_SIZE = 4096

# ============================================================
# GLOBAL STATE TRACKING FOR "okay?" COMMANDS
# ============================================================
class OkayTracker:
    """Tracks everything for the okay? command's reality-bending powers"""
    def __init__(self):
        self.command_history: List[str] = []
        self.output_history: List[str] = []
        self.memory_snapshots: List[Any] = []
        self.program_snapshots: List[List[str]] = []
        self.variable_snapshots: List[Dict] = []
        self.pointer_history: List[int] = []
        self.pitch_history: List[int] = []
        self.flag_history: List[Dict] = []
        self.file_history: List[str] = []
        self.transformation_history: List[str] = []
        
    def snapshot(self, state: 'SkibidiState'):
        """Take a snapshot of current state"""
        self.command_history.append(f"[{time.time()}]")
        self.memory_snapshots.append([Complex(c.real, c.imag) for c in state.memory[:10]])  # Only track first 10 for memory
        self.program_snapshots.append(state.program.copy())
        self.variable_snapshots.append(state.variables.copy())
        self.pointer_history.append(state.pointer)
        self.pitch_history.append(state.pitch)
        self.flag_history.append({
            'swapped': state.swapped,
            'spoiled': state.spoiled,
            'undefined': state.undefined_behavior,
            'brainrot_count': state.brainrot_count,
            'gooner_activated': state.gooner_activated
        })
        
    def redo_everything(self, state: 'SkibidiState'):
        """Redo everything ever done in the terminal (like a cosmic redo)"""
        print("\n🔄 OK — Redoing everything...")
        if self.program_snapshots:
            # Restore from earliest snapshot
            state.program = self.program_snapshots[0].copy()
            state.variables = self.variable_snapshots[0].copy()
            state.pointer = self.pointer_history[0] if self.pointer_history else 0
            state.pitch = self.pitch_history[0] if self.pitch_history else 440
            flags = self.flag_history[0] if self.flag_history else {}
            state.swapped = flags.get('swapped', False)
            state.spoiled = flags.get('spoiled', False)
            state.undefined_behavior = flags.get('undefined', False)
            state.brainrot_count = flags.get('brainrot_count', 0)
            state.gooner_activated = flags.get('gooner_activated', False)
            state.ip = 0
            state.output = ""
            print(f"✨ Redid {len(self.command_history)} commands worth of history")
        else:
            print("❌ Nothing to redo (no history)")
            
    def undo_everything(self, state: 'SkibidiState'):
        """Undo everything ever done in the terminal (absolute reset)"""
        print("\n💀 NOT OKAY — Undoing everything...")
        # Full reset
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
        print(f"💥 Undid {len(self.command_history)} commands — terminal reset to factory defaults")
        self.command_history.clear()
        self.memory_snapshots.clear()
        self.program_snapshots.clear()
        self.variable_snapshots.clear()
        self.pointer_history.clear()
        self.pitch_history.clear()
        self.flag_history.clear()

# Global tracker instance
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
    
    def swap(self):
        return Complex(self.imag, self.real)

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
    attached_clients: List['STLClient'] = field(default_factory=list)
    filename: str = ""

# ============================================================
# THE "okay?" COMMAND HANDLER
# ============================================================
def handle_okay_command(state: SkibidiState, args: List[str] = None) -> bool:
    """
    Handle the chaotic "okay?" command.
    Returns True if the command was handled (terminal should pause if needed)
    """
    global terminal_paused
    
    # Random chance for each outcome
    roll = random.random()
    
    # Check if it's a flag version --okay?
    if args and args[0] == "--okay?":
        # Apply to specific command only
        if len(args) > 1:
            cmd_to_affect = args[1]
            print(f"\n🎲 okay? checking command: {cmd_to_affect}")
            sub_roll = random.random()
            
            if sub_roll < 0.33:
                print(f"✨ OK — Redoing '{cmd_to_affect}'")
                return True  # Signal that command should be redone
            elif sub_roll < 0.66:
                print(f"💀 NOT OKAY — Undoing '{cmd_to_affect}'")
                return False  # Signal that command should be skipped
            else:
                print(f"⏸️ depends on how i feel later~... — Pausing after '{cmd_to_affect}'")
                terminal_paused = True
                return None  # Signal pause
    else:
        # Standalone okay? command
        if roll < 0.33:
            # "Ok" — redoes everything
            okay_tracker.redo_everything(state)
            return True
        elif roll < 0.66:
            # "Not okay" — undoes everything
            okay_tracker.undo_everything(state)
            return True
        else:
            # "depends on how i feel later~..." — pauses terminal
            print("\n⏸️ depends on how i feel later~... — Terminal paused. Type 'resume' to continue.")
            terminal_paused = True
            return True
    
    return True

# ============================================================
# FILE TRANSFORMATION ENGINES
# ============================================================

def load_skibidi_file(filename: str) -> List[str]:
    """Load and parse a .skb file into instructions"""
    instructions = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Remove comments
                if ';' in line:
                    line = line[:line.index(';')]
                # Split into tokens
                for token in line.split():
                    token = token.strip()
                    if token:
                        instructions.append(token)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []
    return instructions

def save_skibidi_file(filename: str, instructions: List[str]):
    """Save instructions to a .skb file"""
    try:
        with open(filename, 'w') as f:
            f.write("; Generated by STL v0.6.9\n")
            f.write("; " + "="*60 + "\n\n")
            # Group into lines of 8 for readability
            for i in range(0, len(instructions), 8):
                f.write(" ".join(instructions[i:i+8]) + "\n")
        print(f"✅ Saved to {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def flip_program(instructions: List[str]) -> List[str]:
    """Reverse instruction order (brainrot but permanent)"""
    return list(reversed(instructions))

def invert_program(instructions: List[str]) -> List[str]:
    """Swap dop↔bop, real↔imag throughout"""
    mapping = {
        'dop': 'bop',
        'bop': 'dop',
        'real': 'imag',
        'imag': 'real',
    }
    return [mapping.get(instr, instr) for instr in instructions]

def chaos_program(instructions: List[str], times: int = 5) -> List[str]:
    """Randomly shuffle instructions N times"""
    result = instructions.copy()
    for _ in range(times):
        random.shuffle(result)
    print(f"🎲 Shuffled {times} times")
    return result

def mutate_program(instructions: List[str], rate: float = 0.1) -> List[str]:
    """Replace X% of ops with random others"""
    valid_ops = ['dop', 'bop', 'skibidi', 'grimace', 'toilet', 'rizz', 'sigma', 
                 'ohio', '67', 'mango', 'diddy', 'brainrot', 'gooner', 'gyatt', 'okay?']
    result = instructions.copy()
    mutation_count = int(len(result) * rate)
    positions = random.sample(range(len(result)), min(mutation_count, len(result)))
    for pos in positions:
        result[pos] = random.choice(valid_ops)
    print(f"🧬 Mutated {mutation_count} instructions ({rate*100:.0f}%)")
    return result

def compress_program(instructions: List[str]) -> List[str]:
    """Remove all magical white liquid"""
    return [instr for instr in instructions if instr != "magical white liquid"]

def expand_program(instructions: List[str]) -> List[str]:
    """Insert magical white liquid between every op"""
    result = []
    for instr in instructions:
        result.append(instr)
        result.append("magical white liquid")
    return result

def corrupt_program(instructions: List[str], bit_flip_rate: float = 0.01) -> List[str]:
    """Flip random bits in the instruction strings"""
    result = []
    for instr in instructions:
        if random.random() < bit_flip_rate:
            # Simulate bit flip by randomly changing characters
            if instr and len(instr) > 0:
                pos = random.randint(0, len(instr)-1)
                new_char = chr(ord(instr[pos]) ^ (1 << random.randint(0, 7)))
                instr = instr[:pos] + new_char + instr[pos+1:]
        result.append(instr)
    print(f"💀 Corrupted ~{int(len(instructions)*bit_flip_rate)} instructions")
    return result

def diddyfy_program(instructions: List[str]) -> List[str]:
    """Replace every instruction with diddy"""
    return ["diddy"] * len(instructions)

def goonerfy_program(instructions: List[str]) -> List[str]:
    """Replace everything with magical white liquid"""
    return ["magical white liquid"] * len(instructions)

def epsteinize_program(instructions: List[str]) -> List[str]:
    """Wrap each instruction in epstein ..."""
    result = []
    for instr in instructions:
        result.append("epstein")
        result.append(instr)
    return result

def ohioify_program(instructions: List[str]) -> List[str]:
    """Reverse polarity of all jumps (ohio N → ohio -N roughly)"""
    result = []
    for i, instr in enumerate(instructions):
        if instr == "ohio" and i+1 < len(instructions):
            try:
                val = int(instructions[i+1])
                result.append("ohio")
                result.append(str(-val) if val > 0 else str(abs(val)))
            except:
                result.append(instr)
        else:
            result.append(instr)
    return result

def gyattify_program(instructions: List[str]) -> List[str]:
    """Add gyatt after every toilet"""
    result = []
    for instr in instructions:
        result.append(instr)
        if instr == "toilet":
            result.append("gyatt")
    return result

def upside_down_program(instructions: List[str]) -> List[str]:
    """Flip complex plane (swap real↔imag in operations)"""
    mapping = {
        'dop': 'bop',  # real changes become imag changes
        'bop': 'dop',
        'real': 'imag',
    }
    return [mapping.get(instr, instr) for instr in instructions]

def backwards_program(instructions: List[str]) -> List[str]:
    """Reverse execution order (different from flip - this is runtime)"""
    return instructions  # Handled by runtime flag

def inside_out_program(instructions: List[str]) -> List[str]:
    """Replace all dop with bop, all grimace with skibidi"""
    mapping = {
        'dop': 'bop',
        'grimace': 'skibidi',
    }
    return [mapping.get(instr, instr) for instr in instructions]

def mirror_program(instructions: List[str]) -> List[str]:
    """Duplicate every instruction in reverse order"""
    return instructions + list(reversed(instructions))

def thicc_program(instructions: List[str]) -> List[str]:
    """Multiply all numeric constants by 69"""
    result = []
    for instr in instructions:
        try:
            val = int(instr)
            result.append(str(val * 69))
        except ValueError:
            try:
                val = float(instr)
                result.append(str(val * 69))
            except ValueError:
                result.append(instr)
    print("🍑 THICC mode: all numbers ×69")
    return result

def skinny_program(instructions: List[str]) -> List[str]:
    """Divide all numeric constants by 69 ( ͡° ͜ʖ ͡°)"""
    result = []
    for instr in instructions:
        try:
            val = int(instr)
            result.append(str(int(val / 69)) if val % 69 == 0 else str(val / 69))
        except ValueError:
            try:
                val = float(instr)
                result.append(str(val / 69))
            except ValueError:
                result.append(instr)
    print("💀 SKINNY mode: all numbers ÷69")
    return result

# ============================================================
# INSTRUCTION EXECUTION
# ============================================================

def execute_instruction(state: SkibidiState, op: str):
    """Execute a single instruction"""
    if state.gooner_activated and op != "magical white liquid":
        return
    
    if op == "magical white liquid":
        return
    
    # Handle okay? instruction
    if op == "okay?":
        handle_okay_command(state)
        return
    
    current = state.memory[state.pointer]
    if state.swapped and not state.undefined_behavior:
        current = current.swap()
    
    # Undefined behavior check
    if state.swapped and state.spoiled:
        state.undefined_behavior = True
    
    # Instruction handling
    if op == "dop":
        if state.spoiled and not state.undefined_behavior:
            state.memory[state.pointer].real -= 1.0
        else:
            state.memory[state.pointer].real += 1.0
    elif op == "bop":
        if state.spoiled and not state.undefined_behavior:
            state.memory[state.pointer].imag += 1.0
        else:
            state.memory[state.pointer].imag -= 1.0
    elif op == "skibidi":
        state.pitch = random.randint(200, 800)
    elif op == "grimace":
        if state.spoiled and not state.undefined_behavior:
            move_right = (state.pitch < 440)
        else:
            move_right = (state.pitch >= 440)
        if move_right:
            state.pointer = (state.pointer + 1) % MEMORY_SIZE
        else:
            state.pointer = (state.pointer - 1) % MEMORY_SIZE
    elif op == "toilet":
        state.stack.append(Complex(state.memory[state.pointer].real, 
                                   state.memory[state.pointer].imag))
        state.memory[state.pointer] = Complex()
    elif op == "rizz":
        mag = state.memory[state.pointer].magnitude()
        if state.spoiled and not state.undefined_behavior:
            mag *= 2.0
        state.output += chr(int(mag) % 128)
    elif op == "sigma":
        try:
            ch = sys.stdin.read(1)
            state.memory[state.pointer].real = float(ord(ch)) if ch else 0
        except:
            state.memory[state.pointer].real = 0
    elif op == "ohio":
        mag = state.memory[state.pointer].magnitude()
        jump = int(mag)
        if jump > 0 and jump <= state.ip:
            state.ip -= jump
    elif op == "67":
        if not state.spoiled:
            state.swapped = not state.swapped
    elif op == "mango":
        state.spoiled = not state.spoiled
    elif op == "diddy":
        if state.spoiled or state.undefined_behavior:
            print("\n💥 CRASH — Diddy in spoiled/undefined mode")
            sys.exit(1)
        print("milk")
    elif op == "brainrot":
        state.brainrot_count += 1
        state.debug = not state.debug
        if state.debug:
            print("🧠 Brainrot mode enabled")
    elif op == "gooner":
        print("⚠️ Gooner activated")
        state.gooner_activated = True
    elif op == "gyatt" and state.stack:
        top = state.stack[-1]
        mag = top.magnitude()
        threshold = 50 if state.spoiled else 100
        if mag > threshold:
            state.ip += max(1, int(mag / 10))
    elif state.debug and op not in ['rizz', 'sigma']:
        print(f"[{state.ip}] {op} | ptr:{state.pointer} | mag:{state.memory[state.pointer].magnitude():.1f}")

def run_program(state: SkibidiState, chaos_mode: bool = False, backwards: bool = False):
    """Run the loaded program"""
    global terminal_paused
    
    state.ip = 0
    state.output = ""
    instructions = state.program
    
    if backwards:
        instructions = list(reversed(instructions))
        print("🔀 Running backwards")
    
    while state.ip < len(instructions):
        if terminal_paused:
            time.sleep(0.1)
            continue
            
        if state.paused:
            time.sleep(0.1)
            continue
            
        op = instructions[state.ip]
        
        if chaos_mode and random.random() < 0.1:
            # 10% chance to insert chaos
            chaos_ops = ['skibidi', 'gyatt', 'brainrot', 'mango', '67', 'okay?']
            inserted = random.choice(chaos_ops)
            print(f"🎲 CHAOS INSERT: {inserted}")
            execute_instruction(state, inserted)
            
        execute_instruction(state, op)
        state.ip += 1
        
        if state.undefined_behavior and random.random() < 0.05:
            print("💀 REALITY COLLAPSE — undefined behavior triggered")
            break

# ============================================================
# ATTACH/DETACH SYSTEM
# ============================================================

class STLDebugger:
    def __init__(self):
        self.active_states: Dict[str, SkibidiState] = {}
        self.clients: Dict[str, 'STLClient'] = {}
        
    def attach(self, state_id: str, state: SkibidiState) -> str:
        client_id = hashlib.md5(f"{state_id}{time.time()}".encode()).hexdigest()[:8]
        self.active_states[client_id] = state
        self.clients[client_id] = STLClient(id=client_id, connected_at=time.time())
        print(f"🔗 Attached to {state_id} as {client_id}")
        return client_id
    
    def detach(self, client_id: str):
        if client_id in self.active_states:
            del self.active_states[client_id]
            del self.clients[client_id]
            print(f"🔌 Detached {client_id}")
        else:
            print(f"❌ Client {client_id} not found")
    
    def pause(self, client_id: str):
        if client_id in self.active_states:
            self.active_states[client_id].paused = True
            print("⏸️ Paused")
    
    def resume(self, client_id: str):
        if client_id in self.active_states:
            self.active_states[client_id].paused = False
            print("▶️ Resumed")

@dataclass
class STLClient:
    id: str
    connected_at: float
    last_command: str = ""

debugger = STLDebugger()

# ============================================================
# REPL
# ============================================================

def repl():
    global terminal_paused
    
    state = SkibidiState()
    current_file = None
    attached_id = None
    chaos_runtime = False
    backwards_runtime = False
    
    print(f"{VERSION}")
    print("Type 'help' for commands, 'exit' to leave. May Skibidi be with you.")
    print("✨ NEW: 'okay?' — random outcome: OK (redo) | NOT OKAY (undo) | depends on how i feel later~ (pause)")
    
    while True:
        try:
            if terminal_paused:
                # Special paused prompt
                paused_input = input("⏸️ [PAUSED] resume? (y/n): ").strip().lower()
                if paused_input == 'y' or paused_input == 'resume':
                    terminal_paused = False
                    print("▶️ Resumed")
                continue
                
            line = input(PROMPT).strip()
            if not line:
                continue
            if line == "exit":
                print("🚽✨")
                break
            
            # Take snapshot before command for undo/redo
            okay_tracker.snapshot(state)
            
            parts = line.split()
            cmd = parts[0]
            args = parts[1:]
            
            # Handle okay? with --okay? flag
            if cmd == "okay?":
                handle_okay_command(state, args)
                continue
            
            # Handle resume command (to unpause from depends on how i feel later~)
            if cmd == "resume":
                terminal_paused = False
                print("▶️ Resumed")
                continue
            
            # File operations
            if cmd == "run" and args:
                filename = args[0]
                prog = load_skibidi_file(filename)
                if prog:
                    state.program = prog
                    state.filename = filename
                    print(f"🏃 Running {filename} ({len(prog)} instructions)")
                    run_program(state, chaos_runtime, backwards_runtime)
                    print(f"\n📤 Output: {state.output}")
                    
            elif cmd == "debug" and args:
                filename = args[0]
                prog = load_skibidi_file(filename)
                if prog:
                    state.debug = True
                    state.program = prog
                    print(f"🐛 Debug mode: {filename}")
                    run_program(state, chaos_runtime, backwards_runtime)
                    state.debug = False
                    
            elif cmd == "flip" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    flipped = flip_program(prog)
                    save_skibidi_file(f"flipped_{args[0]}", flipped)
                    
            elif cmd == "invert" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    inverted = invert_program(prog)
                    save_skibidi_file(f"inverted_{args[0]}", inverted)
                    
            elif cmd == "chaos" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    times = int(args[1]) if len(args) > 1 else 5
                    chaosed = chaos_program(prog, times)
                    save_skibidi_file(f"chaos_{args[0]}", chaosed)
                    
            elif cmd == "mutate" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    rate = float(args[1]) if len(args) > 1 else 0.1
                    mutated = mutate_program(prog, rate)
                    save_skibidi_file(f"mutated_{args[0]}", mutated)
                    
            elif cmd == "compress" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    compressed = compress_program(prog)
                    save_skibidi_file(f"compressed_{args[0]}", compressed)
                    
            elif cmd == "expand" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    expanded = expand_program(prog)
                    save_skibidi_file(f"expanded_{args[0]}", expanded)
                    
            elif cmd == "corrupt" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    corrupted = corrupt_program(prog)
                    save_skibidi_file(f"corrupted_{args[0]}", corrupted)
                    
            elif cmd == "diddyfy" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    diddyfied = diddyfy_program(prog)
                    save_skibidi_file(f"diddy_{args[0]}", diddyfied)
                    
            elif cmd == "goonerfy" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    goonerfied = goonerfy_program(prog)
                    save_skibidi_file(f"gooner_{args[0]}", goonerfied)
                    
            elif cmd == "epsteinize" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    epsteined = epsteinize_program(prog)
                    save_skibidi_file(f"epstein_{args[0]}", epsteined)
                    
            elif cmd == "ohioify" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    ohiofied = ohioify_program(prog)
                    save_skibidi_file(f"ohio_{args[0]}", ohiofied)
                    
            elif cmd == "gyattify" and args:
                prog = load_skibidi_file(args[0])
                if prog:
                    gyattified = gyattify_program(prog)
                    save_skibidi_file(f"gyatt_{args[0]}", gyattified)
                    
            # Live management
            elif cmd == "attach":
                if state.filename:
                    attached_id = debugger.attach(state.filename, state)
                else:
                    print("No loaded program to attach to")
                    
            elif cmd == "detach":
                if attached_id:
                    debugger.detach(attached_id)
                    attached_id = None
                else:
                    print("Not attached")
                    
            elif cmd == "pause" and attached_id:
                debugger.pause(attached_id)
                
            elif cmd == "resume" and attached_id:
                debugger.resume(attached_id)
                
            elif cmd == "inject" and len(args) >= 1:
                instrs = args[0].split()
                inject_instructions(state, instrs, state.ip)
                
            elif cmd == "replace" and len(args) >= 2:
                replace_instruction(state, int(args[0]), args[1])
                
            elif cmd == "swap" and len(args) >= 2:
                swap_instructions(state, int(args[0]), int(args[1]))
                
            elif cmd == "reverse":
                state.program = list(reversed(state.program))
                print("🔀 Program reversed")
                
            elif cmd == "clone" and args:
                clone_cell(state, int(args[0]))
                
            elif cmd == "splice" and len(args) >= 3:
                splice_instructions(state, int(args[0]), int(args[1]), int(args[2]))
                
            # Runtime flags
            elif cmd == "--chaos":
                chaos_runtime = not chaos_runtime
                print(f"🎲 Chaos mode: {'ON' if chaos_runtime else 'OFF'}")
                
            elif cmd == "--backwards":
                backwards_runtime = not backwards_runtime
                print(f"🔀 Backwards mode: {'ON' if backwards_runtime else 'OFF'}")
                
            elif cmd == "--upside-down":
                if state.program:
                    state.program = upside_down_program(state.program)
                    print("🔄 Upside-down mode applied")
                    
            elif cmd == "--inside-out":
                if state.program:
                    state.program = inside_out_program(state.program)
                    print("🔄 Inside-out mode applied")
                    
            elif cmd == "--mirror":
                if state.program:
                    state.program = mirror_program(state.program)
                    print("🪞 Mirror mode applied")
                    
            elif cmd == "--thicc":
                if state.program:
                    state.program = thicc_program(state.program)
                    
            elif cmd == "--skinny":
                if state.program:
                    state.program = skinny_program(state.program)
                    
            elif cmd == "show":
                print(f"File: {state.filename or 'none'}")
                print(f"Instructions: {len(state.program)}")
                print(f"IP: {state.ip}/{len(state.program)}")
                print(f"Pointer: {state.pointer}")
                print(f"Output length: {len(state.output)}")
                print(f"Swapped: {state.swapped} | Spoiled: {state.spoiled}")
                print(f"Chaos: {chaos_runtime} | Backwards: {backwards_runtime}")
                print(f"Terminal Paused: {terminal_paused}")
                print(f"History size: {len(okay_tracker.command_history)} commands tracked")
                
            elif cmd == "history":
                print(f"\n📜 Command history ({len(okay_tracker.command_history)} commands):")
                for i, entry in enumerate(okay_tracker.command_history[-20:]):
                    print(f"  {i}: {entry}")
                    
            elif cmd == "help":
                print("""
╔═══════════════════════════════════════════════════════════════╗
║  STL v0.6.9 — The Brainrot Update                            ║
╠═══════════════════════════════════════════════════════════════╣
║  ✨ NEW: "okay?" — Chaos command with 3 outcomes:            ║
║      33%: "Ok"           → Redoes everything in terminal     ║
║      33%: "Not okay"     → Undoes everything in terminal     ║
║      34%: "depends..."   → Pauses terminal                   ║
║    --okay? <cmd>         → Apply to specific command only    ║
║                                                               ║
║  📁 FILE OPERATIONS                                           ║
║    run <file.skb>        — Execute normally                   ║
║    debug <file.skb>      — Step-by-step debugging             ║
║    flip <file.skb>       — Reverse instruction order          ║
║    invert <file.skb>     — Swap dop↔bop, real↔imag            ║
║    chaos <file.skb> [N]  — Shuffle N times (default 5)        ║
║    mutate <file.skb> [%] — Replace X% with random ops         ║
║    compress <file.skb>   — Remove magical white liquid        ║
║    expand <file.skb>     — Insert magical white liquid        ║
║    corrupt <file.skb>    — Flip random bits in file           ║
║                                                               ║
║  🧠 BRAINROT SPECIALS                                         ║
║    diddyfy <file.skb>    — Every instruction → diddy          ║
║    goonerfy <file.skb>   — Everything → magical white liquid  ║
║    epsteinize <file.skb> — Wrap each op in epstein ...        ║
║    ohioify <file.skb>    — Reverse polarity of all jumps      ║
║    gyattify <file.skb>   — Add gyatt after every toilet       ║
║                                                               ║
║  🔧 LIVE MANAGEMENT (while running)                           ║
║    attach               — Connect to running process          ║
║    detach               — Disconnect                          ║
║    pause                — Freeze execution                    ║
║    resume               — Continue                            ║
║    inject "ops..."      — Insert instructions at current IP   ║
║    replace N "op"       — Replace instruction N               ║
║    swap A B             — Swap instructions at positions      ║
║    reverse              — Reverse remaining program           ║
║    clone N              — Clone current cell to pointer N     ║
║    splice A B C         — Cut [A:B] and insert at C           ║
║                                                               ║
║  🌈 TRANSFORMATION MODES                                      ║
║    --upside-down        — Flip complex plane (real↔imag)      ║
║    --backwards          — Reverse execution order             ║
║    --inside-out         — Replace dop→bop, grimace→skibidi    ║
║    --mirror             — Duplicate instructions in reverse   ║
║    --thicc              — Multiply all numbers by 69          ║
║    --skinny             — Divide all numbers by 69 ( ͡° ͜ʖ ͡°)  ║
║    --chaos              — Random instruction injection        ║
║                                                               ║
║  📊 INFO                                                      ║
║    show                 — Show current state                  ║
║    history              — Show command history                ║
║    help                 — This help menu                      ║
║    exit                 — Leave the void                      ║
╚═══════════════════════════════════════════════════════════════╝
                """)
            else:
                print(f"Unknown command: {cmd}. Type 'help'.")
                
        except EOFError:
            print("\n🚽✨")
            break
        except KeyboardInterrupt:
            print("\n⏸️ Interrupted — Type 'resume' to continue or 'exit' to quit")
            terminal_paused = True
        except Exception as e:
            print(f"Error: {e}")

# ============================================================
# Helper functions missing from earlier
# ============================================================

def inject_instructions(state: SkibidiState, instructions: List[str], at_ip: int):
    """Insert instructions at current IP"""
    state.program = state.program[:at_ip] + instructions + state.program[at_ip:]
    print(f"💉 Injected {len(instructions)} instructions at position {at_ip}")

def replace_instruction(state: SkibidiState, position: int, new_op: str):
    """Replace instruction at position"""
    if 0 <= position < len(state.program):
        old = state.program[position]
        state.program[position] = new_op
        print(f"🔄 Replaced [{position}]: {old} → {new_op}")
    else:
        print(f"❌ Position {position} out of range")

def swap_instructions(state: SkibidiState, pos1: int, pos2: int):
    """Swap two instructions"""
    if 0 <= pos1 < len(state.program) and 0 <= pos2 < len(state.program):
        state.program[pos1], state.program[pos2] = state.program[pos2], state.program[pos1]
        print(f"🔀 Swapped [{pos1}] ↔ [{pos2}]")
    else:
        print(f"❌ Invalid positions")

def clone_cell(state: SkibidiState, target_ptr: int):
    """Clone current cell to another pointer"""
    if 0 <= target_ptr < MEMORY_SIZE:
        state.memory[target_ptr] = Complex(state.memory[state.pointer].real,
                                           state.memory[state.pointer].imag)
        print(f"📋 Cloned cell {state.pointer} → {target_ptr}")
    else:
        print(f"❌ Invalid pointer {target_ptr}")

def splice_instructions(state: SkibidiState, start: int, end: int, insert_at: int):
    """Cut instructions and move elsewhere"""
    if 0 <= start < end <= len(state.program) and 0 <= insert_at <= len(state.program):
        cut = state.program[start:end]
        state.program = state.program[:start] + state.program[end:]
        state.program = state.program[:insert_at] + cut + state.program[insert_at:]
        print(f"✂️ Spliced {len(cut)} instructions from [{start}:{end}] to {insert_at}")
    else:
        print(f"❌ Invalid splice range")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    repl()