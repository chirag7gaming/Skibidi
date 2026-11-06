#!/usr/bin/env python3
# stl.py — Skibidi Terminal Language (STL) Interpreter
# The terminal language that doesn't care. It outputs 🚽✨ anyway.

import sys
import random
import math
import readline  # so you can arrow-up through history
import time

# ============================================================
# CONFIG
# ============================================================
VERSION = "Skibidi Terminal Language v1.0"
PROMPT = "> "
MAX_STEPS = 1000

# ============================================================
# GLOBALS (the sacred state)
# ============================================================
memory = [0j] * 256          # complex cells (real + imag chaos)
ptr = 0                      # pointer
stack = []                   # push/pop with `toilet`
debug = False
swapped = False
spoiled = False
brainrot = False
program = []                 # loaded instructions
ip = 0                       # instruction pointer
output = ""                  # rizz output accumulator

# ============================================================
# HELP
# ============================================================
def show_help():
    print(f"""{VERSION}

Commands (type them directly at the prompt):

  dop N        – increment real part by N (or decrement if spoiled)
  bop N        – decrement imaginary part by N (or increment if spoiled)
  skibidi      – chaos (randomize pitch)
  grimace      – move pointer based on imaginary pitch
  toilet       – push current cell to stack, zero the cell
  rizz         – output magnitude of current cell as ASCII
  sigma        – read user input into current cell (real part)
  ohio N       – jump back N steps (if magnitude > 0)
  67           – toggle swapped flag
  mango        – toggle spoiled mode
  diddy        – print "milk", crashes if spoiled or undefined
  brainrot     – reverse program order, toggle debug mode
  gooner       – replace all instructions with "magical white liquid"
  sigmaflex N  – fake internet flex (packet loss simulation)
  --grow       – exponential output (enabled before run)
  --final      – final mode (hide all output until end)
  --chaos      – chaos mode (random instruction swaps every 0.42s)
  --brainrot   – reverse terminal scroll direction (mood)
  --undefined  – enable undefined behavior (swapped + spoiled)
  show         – show current memory cell (complex)
  cells        – show all non‑zero memory cells
  help         – show this help
  exit         – leave the void

Examples:
  dop 42
  rizz
  toilet
  sigma
  brainrot
  gooner
  67 mango diddy

Tic Black. 🚽✨
""")

# ============================================================
# UTILS (chaos, pitch, magnitude)
# ============================================================
def pitch():
    # imaginary chaos determines movement direction
    return memory[ptr].imag

def magnitude(c):
    return int(math.floor(math.sqrt(c.real**2 + c.imag**2)))

def update_output(cell):
    global output
    mag = magnitude(cell)
    if spoiled:
        mag *= 2
    output += chr(mag)

# ============================================================
# CORE EXECUTION (one instruction at a time)
# ============================================================
undefined_mode = False   # --undefined flag
chaos_mode = False       # --chaos flag
final_mode = False       # --final flag
grow_mode = False        # --grow flag

def execute(op):
    global ptr, swapped, spoiled, debug, brainrot, output, memory, stack, ip, undefined_mode, chaos_mode

    # undefined behavior: swapped AND spoiled = reality collapse
    if undefined_mode and swapped and spoiled:
        if random.random() < 0.1:
            print("💀 REALITY COLLAPSE — restarting shell", file=sys.stderr)
            sys.exit(1)

    if op == "magical white liquid":
        return

    if op.startswith("--"):
        # flags handled before execution, ignore here
        return

    if op == "brainrot":
        debug = not debug
        brainrot = not brainrot
        print("🧠 brainrot toggled" if debug else "🧠 brainrot off")
        return

    if op == "gooner":
        print("gooner activated — returning 'magical white liquid'")
        # in real STL this would replace all future instructions
        return

    if op == "sigmaflex":
        skill = random.randint(0, 100)
        loss = random.randint(0, 70)
        latency = random.randint(100, 2000)
        print(f"💪 sigma flex — skill: {skill}, packet loss: {loss}%, latency: {latency}ms")
        return

    if op == "dop":
        val = 1
        if spoiled:
            memory[ptr] -= complex(val, 0)
        else:
            memory[ptr] += complex(val, 0)
        if debug:
            print(f"dop +{val} → {memory[ptr]}")
        return

    if op == "bop":
        val = 1
        if spoiled:
            memory[ptr] += complex(0, val)
        else:
            memory[ptr] -= complex(0, val)
        if debug:
            print(f"bop -{val}i → {memory[ptr]}")
        return

    if op == "skibidi":
        # pure chaos — randomize pointer and imaginary part
        ptr = random.randint(0, 255)
        memory[ptr] += complex(0, random.randint(-50, 50))
        print("🎭 skibidi chaos — pointer jumped, imaginary shifted")
        return

    if op == "grimace":
        step = 1 if pitch() >= 0 else -1
        ptr = (ptr + step) % 256
        if debug:
            print(f"grimace → pointer {ptr}")
        return

    if op == "toilet":
        stack.append(memory[ptr])
        memory[ptr] = 0j
        print("🚽 toilet flushed (pushed to stack, cell zeroed)")
        return

    if op == "rizz":
        mag = magnitude(memory[ptr])
        if spoiled:
            mag *= 2
        out_char = chr(mag % 128) if mag < 128 else '?'
        if not final_mode:
            print(f"rizz → '{out_char}' (magnitude {mag})")
        else:
            # final mode stores output for end
            global output
            output += out_char
        return

    if op == "sigma":
        val = input("sigma input (real number): ")
        try:
            memory[ptr] = complex(float(val), memory[ptr].imag)
        except:
            print("sigma error — invalid number")
        return

    if op == "ohio":
        mag = magnitude(memory[ptr])
        steps = min(mag, ip)
        ip -= steps
        if debug:
            print(f"ohio → jump back {steps} steps")
        return

    if op == "67":
        swapped = not swapped
        if debug:
            print(f"67 → swapped = {swapped}")
        return

    if op == "mango":
        spoiled = not spoiled
        if debug:
            print(f"mango → spoiled = {spoiled}")
        return

    if op == "diddy":
        if spoiled or (swapped and undefined_mode):
            print("💥 diddy crashed — you're spoiled or undefined. system unstable.", file=sys.stderr)
            sys.exit(1)
        print("milk")
        return

    if op == "show":
        print(f"cell[{ptr}] = {memory[ptr]} (real: {memory[ptr].real:.2f}, imag: {memory[ptr].imag:.2f}, mag: {magnitude(memory[ptr])})")
        return

    if op == "cells":
        for i, val in enumerate(memory):
            if val != 0j:
                print(f"cell[{i}] = {val}")
        return

    if op == "help":
        show_help()
        return

    print(f"unknown command: {op}. type 'help'.")


# ============================================================
# REPL
# ============================================================
def repl():
    global ip, program, debug, brainrot, output, ptr, swapped, spoiled, memory, stack, undefined_mode, chaos_mode, final_mode, grow_mode

    print(f"{VERSION} — type 'help' or 'exit'. May Skibidi be with you.")
    while True:
        try:
            line = input(PROMPT).strip()
            if not line:
                continue
            if line == "exit":
                print("🚽✨")
                break

            # handle flags before interpreting rest of line
            args = line.split()
            cmd = args[0]

            # global flags
            if cmd == "--undefined":
                undefined_mode = True
                print("⚠️ undefined behavior enabled (swapped + spoiled = collapse)")
                continue
            if cmd == "--chaos":
                chaos_mode = True
                print("🎲 chaos mode enabled — instructions may swap randomly")
                continue
            if cmd == "--final":
                final_mode = True
                print("🔚 final mode enabled — output hidden until the end")
                continue
            if cmd == "--grow":
                grow_mode = True
                print("🌱 grow mode enabled — exponential output (simulated)")
                continue

            # normal instruction
            if chaos_mode and random.random() < 0.3:
                # swap instruction to something random
                rnd = random.choice(["dop", "bop", "skibidi", "grimace", "rizz", "toilet", "brainrot"])
                print(f"⚠️ chaos swapped '{cmd}' → '{rnd}'")
                cmd = rnd

            if cmd in ("dop", "bop", "ohio", "sigmaflex"):
                if len(args) > 1:
                    val = args[1]
                    execute(f"{cmd} {val}")
                else:
                    execute(cmd)
            else:
                execute(cmd)

            # if final mode and we just finished a line, maybe flush nothing
            if final_mode and output:
                if grow_mode:
                    output = output * 10
                print(f"🚽✨ {output}")
                output = ""

        except EOFError:
            print("\n🚽✨")
            break
        except KeyboardInterrupt:
            print("\n🚽✨")
            break
        except Exception as e:
            print(f"skibidi error: {e}")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    # if user passed a .skibidi file, run that first
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                code = f.read()
            # here you'd implement batch mode, but for now
            print(f"📄 reading {filename} — interactive mode still active")
        except:
            print(f"can't read {filename}")
    repl()