## Skibidi Coding Language (SCL) & Skibidi Terminal Language (STL)

```markdown
# 🚽 Skibidi Coding Language (SCL) & Skibidi Terminal Language (STL)

<div align="center">

**"Harder than Bash and Brainfuck combined."**

*"The terminal language that doesn't care. It outputs 🚽✨ anyway."*

[![Version](https://img.shields.io/badge/version-8.0%20%7C%201.0.0-ff69b4?style=for-the-badge)](https://github.com/fish-gang/skibidi)
[![Language](https://img.shields.io/badge/language-C%20%7C%20Python-blue?style=for-the-badge)](https://github.com/fish-gang/skibidi)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Made by Fish Gang](https://img.shields.io/badge/made%20by-Fish%20Gang-00ffff?style=for-the-badge)](https://fish-gang.netlify.app/Company)

[Quick Start](#-quick-start) • [Language Reference](#-language-reference) • [Version History](#-version-history) • [Documentation](#-full-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 What Is This?

**Skibidi** is a family of esoteric programming languages born from a simple question: *"What if Brainfuck, but it was actively hostile?"*

Over **11 major iterations** (and counting), Skibidi has evolved from a 7-instruction chaos engine with a 0.36% success rate into a fully-featured, network-enabled, 3D-rendering, Python-importing, meme-infested programming environment — while **never once abandoning its commitment to being fundamentally unreasonable.**

*There are two parallel implementations:*

| Branch | Description | Status |
|--------|-------------|--------|
| **SCL** (Skibidi Coding Language) | The core language. Batch-executed `.skb` programs. | v8.0 (Python) / v6.1 (C) |
| **STL** (Skibidi Terminal Language) | The interactive REPL. Same opcodes, but you type them live. | v1.0.0 (Python) |

Both share the same **opcode vocabulary**, the same **complex-number memory model**, and the same **spiritual commitment to making you suffer in a funny way.**

---

## ⚡ Quick Start

### Prerequisites

**For Python versions (recommended — most features):**
```bash
python3 --version   # 3.8+ required
# tkinter is bundled with most Python installs
```

- For C versions:

```bash
# Debian/Ubuntu
sudo apt install gcc libssl-dev

# macOS
brew install gcc openssl

# Arch
sudo pacman -S gcc openssl
```

- Installation

```bash
git clone https://github.com/fish-gang/skibidi.git
cd skibidi

# C builds (per version)
gcc -o skibidi_v1 SCL_1.0.c -lm
gcc -o skibidi_v2 SCL_2.0.c -lm -lssl -lcrypto
gcc -o skibidi_v6 SCL_6.1.c -lm -lssl -lcrypto -lpthread

# Python versions — just run
python3 "SCL (8.0).py" --demo
python3 "STL (1.0.0).py"
```

## Your First Program

- Create hello.skb:

```skibidi
dop(72) rizz
grimace
dop(101) rizz
grimace
dop(108) rizz
grimace
dop(108) rizz
grimace
dop(111) rizz
grimace
dop(32) rizz
grimace
dop(87) rizz
grimace
dop(111) rizz
grimace
dop(114) rizz
grimace
dop(108) rizz
grimace
dop(100) rizz
diddy
```

- Run it:

```bash
python3 "SCL (8.0).py" hello.skb
```

You'll see Hello World (eventually — sometimes the pitch chaos sends your pointer to the wrong cell, in which case you get garbage output, which is canonically correct).

- Generate the built-in demos

```bash
python3 "SCL (8.0).py" --demo
python3 "SCL (8.0).py" --evil-hello
python3 "STL (1.0.0).py" --demo
```

- ...Or launch the interactive REPL and type help:

```bash
python3 "STL (1.0.0).py"
```

---

## 🧠 Core Concepts

- Memory Model

Skibidi has 65,536 memory cells (in Python) or 256 cells (in the early C versions), each holding a complex number (real + imaginary·i).

· A pointer ("the ear") selects the active cell.
· dop increments the real part.
· bop decrements the imaginary part.
· rizz outputs floor(|cell|) as ASCII.
· grimace moves the pointer, based on the pitch.

- The Pitch System

Pitch is an integer in Hz that determines pointer movement direction in grimace:

· pitch >= 440 → move right
· pitch < 440 → move left

- Pitch is updated by the skibidi op:

Version Pitch Behavior
v1.0 Random 200–800 Hz (non-deterministic!)
v2.0+ Deterministic chaos via MD5 hashing of an internal RNG state

This is why v1.0 "Hello World" has a ~0.36% success rate — the pitch must be >= 440 at every grimace for the pointer to land on the right cell. v2.0+ made this reproducible but still chaotic.

## The Opcode Vocabulary

| Op Name | What it does |
|:---|:---:|
| dop | Doppler — Increment real part of current cell |
| bop | Bop — Decrement imaginary part |
| skibidi | Skibidi — Update pitch (chaos) |
| grimace | Grimace — Move pointer based on pitch |
| toilet | Toilet — Push current cell to stack, zero the cell |
| rizz | Rizz — Output floor(magnitude) as ASCII |
| sigma | Sigma — Read input character into cell |
| ohio | Ohio — Jump back floor(magnitude) instructions |
| 67 | Six-Seven — Toggle swap mode (real ↔ imag) |
| mango | Mango — Toggle spoiled mode (reverses all ops) |
| diddy | Diddy — Print milk (crashes if spoiled/undefined) |
| brainrot | Brainrot — Reverse program order, toggle debug |
| gooner | Gooner — Replace all instructions with magical white liquid |
| epstein | Epstein — Execute the next opcode inside this one, isolated |
| gyatt | Gyatt — Peek stack top, jump if magnitude > threshold |
| sigmaflex | Sigmaflex — Fake network flex (cosmetic) |
| dih / vah | Dih/Vah — Set file handle / read file to memory |
| twin / im out | Twin/Im out — Copy/move file |
| let / get | Let/Get — Store/load named variable |
| bred / dawg | Bred/Dawg — Spam "Diddy" / "W Speed❤️‍🩹" |
| patrick | Patrick — Output N random emoji |
| triple t | Triple T — Output T<val>T |
| the dude who no one invited: Import | Import — Import any Python module |
| dude call | Call — Call a function from an imported module |
| 3don / 3doff | 3D on/off — Toggle the native tkinter 3D window |
| cube / sphere | 3D shapes — Add primitives |
| cam | Camera — Move the 3D camera |
| Larp / larp | Larp — Replace meme ops with no-op larp |
| kink | Kink — Spawn 5 Epsteins... you don't want to know |
| tiki / ip / acey / speed / cristiano / messi | Meme ops — See the Meme Ops section |

## The Diddy/Gooner/Epstein Triangle

This is the philosophical heart of v6.x and beyond.

```
diddy gooner "Your custom text"
```

· diddy alone → prints milk milk milk
· diddy while spoiled (mango active) or undefined (both 67 + mango) → hard crash
· diddy gooner "text" → runs gooner inside the diddy context, which prints text instead of destroying the program
· gooner standalone → destroys instructions up to the first diddy, then stops. If no diddy found, destroys everything.

This means placement of diddy matters. It's the only instruction that can "absorb" a gooner wave.

The Epstein Op

```skibidi
epstein rizz
```

Runs rizz in an isolated context inside epstein. Nested up to 16 levels deep. Conceptually, the inner op runs as if it were the only instruction in the universe, then control returns.

```skibidi
epstein epstein epstein rizz   ; runs rizz 3 levels deep
```

---

## 🌐 Networking (v4.1+)

Skibidi has competitive multiplayer. Peers connect over UDP on port 42069 (no, seriously).

```bash
# Terminal 1 — host
python3 "SCL (8.0).py" my_program.skb --connect 0.0.0.0 --port 42069 --name host

# Terminal 2 — client
python3 "SCL (8.0).py" my_program.skb --connect 192.168.1.10 --port 42069 --name beta
```

- When connected:

· Memory broadcasts (30% grief chance): other players can overwrite your cells
· Brainrot infection (50% chance): if a peer executes brainrot, you might too
· Gooner virus (20% chance): if a peer executes gooner, your program may be destroyed
· Skill level starts at 100. Hitting diddy while spoiled costs 50 skill. At 0 skill, you RAGE QUIT (exit code 1).

This makes multiplayer actively hostile. It is not a bug.

---

## 🎮 Native 3D (v8.0+)

Skibidi v8.0 has a pure-math 3D renderer using only tkinter (bundled with Python). No OpenGL, no PyGame, no external libraries.

```skibidi
3don
dop dop dop dop cube
dop dop sphere
cam
```

- Controls in the window:

· WASD — move camera forward/left/back/right
· Q/E — camera up/down
· Arrow keys — rotate camera

- Shapes are drawn from memory cell values:

· cube → uses memory[pointer].real, .imag, memory[pointer+1].real, memory[pointer+2].real as x, y, z, size
· sphere → similar, with radius from memory[pointer+2]
· cam → camera position from memory[pointer].real, .imag, memory[pointer+1].real

The projection is a hand-rolled perspective transform with FOV 90°. It's slow but it works.

---

## 🎭 Meme Ops

Skibidi v7.0+ introduced ops that exist purely for the bit.

| Op | Effect |
|----|--------|
| kink | Spawns "5 Epsteins with 9,999 gooners inside" — 30% chance per Epstein of printing `You were so hard daddy~😩😩😩` |
| tiki | Prints the entire Tiki Phonk copypasta |
| ip | Prints `198.234.45.207` |
| acey | Prints `Please, Speed. I need this~~~~ My mum is kinda homeless` |
| speed | Prints `SEWEY` same, +50 skill |
| cristiano | Prints `SUUUUUUUUU`, sets cell to 7 + 77i |
| messi | Prints `stfu` 10 times |
| Larp | Replaces gooner/cristiano/speed/dawg/dih/brainrot with no-op larp |
| larp | Does nothing |

These are not bugs. They are features.

---

## 📚 Full Documentation

- SCL (Batch Mode)

```bash
# Run a program
python3 "SCL (8.0).py" program.skb

# Debug mode (trace every instruction)
python3 "SCL (8.0).py" program.skb --debug

# Generate built-in demos
python3 "SCL (8.0).py" --demo
python3 "SCL (8.0).py" --evil-hello

# Multiplayer
python3 "SCL (8.0).py" program.skb --connect <ip> --port 42069 --name <player>
```

- STL (Interactive REPL)

```bash
python3 "STL (1.0.0).py"
```

At the > prompt, you can:

· Run a file: run program.skb
· Debug a file: debug program.skb
· Apply a transformation: flip program.skb, invert program.skb, chaos program.skb 10, diddyfy program.skb, larpify program.skb, etc.
· Live-edit a running program: inject "dop dop rizz", replace 5 "bop", swap 3 7, clone 42, splice 2 5 10
· Use the okay? command: 33% redo everything, 33% undo everything, 34% pause the terminal with depends on how i feel later~...
· Attach/detach a debugger: attach, detach, pause, resume
· Go 3D: 3don, 3doff
· Network: connect 192.168.1.10, name SIGMA_BOI, skill 100

Type help for the full command list. Type transforms for all -ify commands.

## The -ify Transformations (STL 1.0.0)

STL 1.0.0 includes ~40 file transformation commands. They read a .skb file, transform it, and write <command>_<original>.skb.

| Category | Commands |
|:---|:---:|
| Structural | flip, invert, chaos N, mutate RATE, compress, expand, corrupt RATE |
| Meme | diddyfy, goonerfy, epsteinize, epsteinify, ohioify, gyattify, gyattify-more |
| Geometry | upside-down, inside-out, mirror, thicc, skinny |
| Op injection | rizzify, skibidiify, toiletify, grimaceify, okayify, sigmaflexify, patrickify, bredify, dawgify, messiify, crossify, dotify |
| Op replacement | larpify, speedify, cristianoify, sigmaify, dopify, bopify |
| Wrapper | kinkify, tikify, ipify, 3dify, cubeify, sphereify, camify, brainrotify |
| Meta | mixify [seed] — apply 3 random transforms |

---

## 📜 Version History

- SCL (Skibidi Coding Language)

v1.0 — The Original Chaos (SCL (1.0).c)

· 7 opcodes: dop, bop, skibidi, toilet, rizz, sigma, ohio
· Random pitch (200–800 Hz) — no two runs the same
· Hello World success rate: ~0.36% (1 in ~278 runs)
· 256 cells, complex memory

v2.0 — Chaotic Deterministic (SCL (2.0).py, SCL (2.0).c)

· Replaced random pitch with MD5-hashed deterministic chaos
· Added grimace (pointer movement based on pitch)
· Hello World now reproducible

v2.1 — The Evil Update (SCL (2.1).c)

· Added 67 (swap real/imag), mango (spoiled mode reverses ops), diddy (prints milk, crashes if spoiled)

v3.0 — Why Would Anyone Do This (SCL (3.0).c)

· Undefined behavior when 67 + mango active simultaneously (random effects)
· Full spoiled/swap interaction matrix

v4.0 — Brainrot & Gooner (SCL (4.0).c)

· brainrot: reverses program order, toggles debug
· gooner: replaces all instructions with magical white liquid (no-op)

v4.1 — SIGMABOII Online (SCL (4.1).c)

· UDP networking on port 42069
· Peer discovery, memory griefing, brainrot/gooner infection
· Player profiles with skill levels, rage quit detection

v5.0 — Internet Edition (SCL (5.0).c, SCL (5.0).py)

· Refined networking, sigmaflex command
· Full Python port

v6.0 — Diddy Gooner Inside (SCL (6.0).c)

· Proper parser: labels (loop:), inline comments (;), quoted strings
· diddy gooner "text" combo — custom text when gooner runs inside diddy
· Gooner now stops at first diddy instead of destroying everything

v6.1 — Epstein Inside (SCL (6.1).c, SCL (6.1).py)

· epstein op: nested isolated execution (up to 16 levels)
· Gooner sequential destruction: destroys 0..first_diddy, then stops

v7.0 — The Uninvited Edition (June 2026) (SCL (7.0).py)

· gyatt (stack peek + conditional jump)
· dih / vah (file I/O), twin / im out (copy/move)
· let / get (named variables)
· the dude who no one invited: (import any Python module)
· dude call (call imported functions)
· bred, dawg, patrick, triple t (output spam)
· 3d, cross, dot (math primitives)
· kink, tiki, ip, acey, speed, cristiano, messi (meme ops)

v8.0 — Must've been the Wind Edition (November 2026) (SCL (8.0).py)

· Native 3D renderer (tkinter, pure math, no libraries)
· 3don, 3doff, cube, sphere, cam, clear3d
· Larp / larp (meme replacement)
· Full gyatt integration
· kink, tiki, ip, acey, speed, cristiano, messi polished
· 65,536 cells, 4,096 stack slots

- STL (Skibidi Terminal Language)

v0.6.7 (STL (0.6.7).c — actually a mislabeled Python file)

· Basic REPL, core opcodes
· --undefined, --chaos, --final, --grow flags

v0.6.9 — Brainrot Edition (STL (0.6.9).py)

· The okay? command (redo / undo / pause)
· ~20 file transformation commands
· Attach/detach debugger
· Command history tracking

v1.0.0 — The Full Port (STL (1.0.0).py)

· Full SCL v8.0 parity inside the REPL
· ~40 -ify transformations
· Networking (connect, name, skill)
· 3D integration (3don, 3doff)
· Live program editing (inject, replace, swap, reverse, clone, splice)
· Complete okay? implementation with --okay? <cmd> flag variant

---

## 🧪 Testing Your Programs

Skibidi is intentionally hostile to testing. There's no test suite because every program is non-deterministic in some way (or deliberately chaotic).

However, you can use --debug on any program to trace every instruction:

```bash
python3 "SCL (8.0).py" hello.skb --debug
```

You'll see:

```
[0] dop | P:440Hz | C:0 | (1.0+0.0i) | Mag:1 | Swp:0 | Spoil:0 | Rot:0 | Goon:0 | Eps:0
[1] dop | P:440Hz | C:0 | (2.0+0.0i) | Mag:2 | ...
...
```

For network debugging, the STL show command displays full state:

```
File: hello.skb
Instructions: 22
IP: 7/22
Pointer: 3
Swapped: 0 | Spoiled: 0
Gooner: 0 | Epstein: 0
Connected: 1 | Skill: 100
```

---

## 🤔 Design Philosophy

Skibidi is a satire of esoteric programming languages that grew into something sincere. The design principles, in order of priority:

1. Every opcode must do something non-obvious. If you can guess what bop does without reading the docs, we've failed.
2. Chaos must be reproducible. v1.0 used real randomness (0.36% success). v2.0+ made it deterministic chaos (MD5). Reproducible chaos is more interesting than unpredictable randomness.
3. Combinations must be dangerous. 67 + mango = undefined behavior. diddy + spoiled = crash. gooner + diddy = custom output. epstein + anything = nested universe.
4. The error messages should make you laugh. CRASH: diddy called while spoiled! (Skibidi rule #67: diddy requires purity).
5. More is more. v8.0 has ~40 opcodes. STL 1.0.0 has ~40 transformations. There is no "minimal version" and there will never be one.

If you're looking for a sane esolang, try Brainfuck, Befunge, or Malbolge. If you want to see how far you can push "intentionally hostile" before it becomes "wow, this actually has a lot of features", Skibidi is for you.

---

## 🛠️ Building From Source

- C versions

```bash
# v1.0 (minimal deps)
gcc -o skibidi_v1 "SCL (1.0).c" -lm

# v2.1 (MD5)
gcc -o skibidi_v21 "SCL (2.1).c" -lm -lssl -lcrypto

# v4.1 (networking)
gcc -o skibidi_v41 "SCL (4.1).c" -lm -lssl -lcrypto -lpthread

# v6.1 (full features)
gcc -o skibidi_v61 "SCL (6.1).c" -lm -lssl -lcrypto -lpthread
```

`Note: SCL (4.1).c has a known compilation error — sigma_receive_thread and sigma_send_thread reference skibidi before its declaration in main(). See Known Issues.`

- Python versions

```bash
# No build needed
python3 "SCL (8.0).py" --demo
python3 "STL (1.0.0).py"
```

Python requirements: Python 3.8+ with tkinter (bundled in most installations). For headless environments, tkinter is only needed for the 3don opcode.

---

## 🐛 Known Issues

SCL (4.1).c

· Won't compile. pthread_create(&g_sigma_net.recv_thread, ..., &skibidi) references skibidi before it's declared in main(). Move the Skibidi skibidi; declaration above the if (server_ip) block.
· execute_sigma is defined but never called — main() calls execute() directly. The networking broadcast hooks in execute_sigma are dead code.
· create_demo and create_evil_hello are referenced but not defined in this file.

SCL (6.1).c

· In gooner(), the check if (first_diddy_index >= 0 && !s->diddy_gooner_inside) uses s->diddy_gooner_inside after the inside-diddy branch has already reset it to 0. The sequential destruction only triggers when gooner is called standalone, which is correct — but the naming is confusing.

STL (1.0.0).py

· epstein_execute_inside calls execute_instruction(s, inner_op). If inner_op is epstein itself, the depth guard (16) prevents infinite recursion, but the behavior is undefined (each level tries to execute the next op).
· the dude who no one invited: sets state.ip = temp_ip - 1 which combined with the run loop's +1 correctly resumes — but the dude call branch has a similar pattern that may skip a token in edge cases.
· The --okay? flag variant of okay? returns True/False/None to signal "redo"/"skip"/"pause", but the REPL ignores the return value — the flag variant currently just prints a message and does nothing else.

All versions

· No test suite. Every program is non-deterministic in some way (or deliberately chaotic). Testing is manual.
· Diddy crash is a sys.exit(1) — it cannot be caught. If you want to handle it, run the interpreter in a subprocess.

---

## 🤝 Contributing

We welcome contributions, provided they respect the design philosophy: more is more, chaos is reproducibility, error messages should be funny.

- How to contribute

1. Fork the repo
2. Create a branch: git checkout -b feature/my-new-op
3. Add your opcode to both SCL (Python) and STL (Python)
4. Add a -ify transformation if it makes sense
5. Document it in this README
6. Submit a PR

- Opcode proposal checklist

Before proposing a new opcode, ask:

☐ Does it do something non-obvious?
☐ Is its behavior deterministic (in the "reproducible chaos" sense)?
☐ Does it interact interestingly with 67, mango, diddy, gooner, or epstein?
☐ Is the error message funny?
☐ Can it be abused in multiplayer?
☐ Does it have a -ify transformation counterpart?

If you answered "yes" to all six, you're in.

- Reporting bugs

Open an issue with:

· Which file (e.g., SCL (8.0).py)
· The .skb program that triggers it
· The exact command
· What you expected vs. what happened

Please do not report "the program crashed" as a bug unless the crash isn't diddy-related. diddy crashing is a feature.

---

## 📄 License

MIT — see LICENSE for details.

You can do whatever you want with this code. If it breaks, you get to keep both pieces.

---

## 🐟 About Fish Gang

<div align="center">

Fish Gang is a one-man noncorporate company who make software that shouldn't exist but does anyway.

🌐 fish-gang.netlify.app/Company

I built Skibidi because someone had to.

</div>

---

## 🙏 Acknowledgments

· Brainfuck — for proving that esolang doesn't mean "small"
· Malbolge — for proving that "harder than" is a competitive sport
· Befunge — for proving that 2D programs are viable
· The diddy/gooner/epstein triad — for philosophical depth we didn't ask for
· Every user who ran v1.0 Hello World 278 times — why...
· The MD5 hash — for being terrible cryptography but excellent chaos

---

<div align="center">

🚽 Skibidi v8.0 — It's not a bug. It's a lifestyle. ✨

"Harder than Bash and Brainfuck combined."

</div>
```
