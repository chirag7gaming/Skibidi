#!/usr/bin/env python3
"""
Skibidi v2.0 Interpreter
A brutally hard esoteric programming language
"""

import sys
import math
import random
from typing import List, Tuple, Optional

class SkibidiInterpreter:
    def __init__(self, debug=False):
        # Memory: 256 cells of complex numbers
        self.memory = [complex(0, 0) for _ in range(256)]
        self.pointer = 0  # ear pointer (cell index)
        self.pitch = 440  # Hz, starts at 440
        self.rhythm_stack = []  # stores complex numbers
        self.program = []
        self.instruction_pointer = 0
        self.debug = debug
        self.output = ""
        self.input_buffer = ""
        
    def load_program(self, code: str, use_macros=True):
        """Load and preprocess Skibidi code"""
        if use_macros:
            code = self.expand_macros(code)
        
        # Tokenize: split on whitespace, ignore empty tokens
        tokens = [t for t in code.split() if t]
        
        # Validate tokens are valid instructions
        valid_ops = {'dop', 'bop', 'skibidi', 'toilet', 'rizz', 'sigma', 'ohio', 'grimace'}
        
        # Check for unknown ops (macros should already be expanded)
        for token in tokens:
            # Check if it's a raw dop/bop count (e.g., "dop" alone is fine, "dop(72)" should be expanded)
            base_op = token.split('(')[0] if '(' in token else token
            if base_op not in valid_ops:
                # Allow numbers in ops? No, only in macros
                raise SyntaxError(f"Unknown instruction: '{token}'")
        
        self.program = tokens
        return len(self.program)
    
    def expand_macros(self, code: str) -> str:
        """Expand macros like dop(72) into 72 separate 'dop' tokens"""
        import re
        
        def expand_count(match):
            op = match.group(1)  # dop, bop, etc.
            count = int(match.group(2))
            return ' '.join([op] * count)
        
        # Expand patterns: dop(72), bop(5), etc.
        pattern = r'\b(dop|bop)\((\d+)\)'
        expanded = re.sub(pattern, expand_count, code)
        
        # Also allow rizz(n) for debugging? No, rizz takes no args
        # But we'll keep it simple
        
        return expanded
    
    def get_magnitude(self, cell: complex) -> int:
        """Get floor of complex magnitude"""
        return int(math.floor(abs(cell)))
    
    def execute_instruction(self, op: str) -> bool:
        """
        Execute a single instruction.
        Returns True to continue, False to halt
        """
        if self.debug:
            print(f"IP: {self.instruction_pointer}, Op: {op}, Pitch: {self.pitch}Hz, Cell {self.pointer}: {self.memory[self.pointer]}")
        
        # Handle macro-like tokens (should be preprocessed already)
        if '(' in op:
            # If somehow not preprocessed, extract base op
            base_op = op.split('(')[0]
            if base_op in ['dop', 'bop']:
                # Try to extract number
                import re
                match = re.search(r'\((\d+)\)', op)
                if match:
                    count = int(match.group(1))
                    if self.debug:
                        print(f"  Expanding {base_op}({count}) into {count} operations")
                    # We'll handle this by simulating multiple ops
                    for _ in range(count):
                        self.execute_instruction(base_op)
                    return True
            raise SyntaxError(f"Invalid operation format: {op}")
        
        # Standard instructions
        if op == 'dop':
            # Increment real part by 1
            self.memory[self.pointer] += complex(1, 0)
            
        elif op == 'bop':
            # Decrement imaginary part by 1
            self.memory[self.pointer] -= complex(0, 1)
            
        elif op == 'skibidi':
            # Toggle pitch: 440 → 880 → 220 → 440
            if self.pitch == 440:
                self.pitch = 880
            elif self.pitch == 880:
                self.pitch = 220
            elif self.pitch == 220:
                self.pitch = 440
            else:
                self.pitch = 440  # fallback
            
        elif op == 'grimace':
            # Move ear pointer based on pitch
            if self.pitch < 440:
                # Move left
                self.pointer = (self.pointer - 1) % 256
                if self.debug:
                    print(f"  ← Moved left to cell {self.pointer}")
            else:
                # Move right (pitch >= 440)
                self.pointer = (self.pointer + 1) % 256
                if self.debug:
                    print(f"  → Moved right to cell {self.pointer}")
                    
        elif op == 'toilet':
            # Push current cell to stack, then clear
            self.rhythm_stack.append(self.memory[self.pointer])
            self.memory[self.pointer] = complex(0, 0)
            if self.debug:
                print(f"  💩 Pushed {self.rhythm_stack[-1]} to stack, cleared cell")
                
        elif op == 'rizz':
            # Output floor(magnitude) as ASCII
            mag = self.get_magnitude(self.memory[self.pointer])
            char = chr(mag)
            self.output += char
            if self.debug:
                print(f"  📢 Output '{char}' (ASCII {mag})")
                
        elif op == 'sigma':
            # Read one byte from input
            if not self.input_buffer:
                # Wait for input
                self.input_buffer = sys.stdin.read(1)
                if not self.input_buffer:
                    # EOF
                    self.memory[self.pointer] = complex(0, 0)
                    return True
            char = self.input_buffer[0]
            self.input_buffer = self.input_buffer[1:]
            self.memory[self.pointer] = complex(ord(char), 0)
            if self.debug:
                print(f"  📥 Read '{char}' (ASCII {ord(char)})")
                
        elif op == 'ohio':
            # Jump back N ops where N = floor(magnitude(current cell))
            mag = self.get_magnitude(self.memory[self.pointer])
            if mag > 0:
                # Jump back mag instructions
                self.instruction_pointer -= mag
                # Adjust for the upcoming increment
                self.instruction_pointer -= 1
                if self.debug:
                    print(f"  🔄 Jumping back {mag} instructions")
            else:
                if self.debug:
                    print(f"  ⏭️  No jump (magnitude = 0)")
                    
        else:
            raise SyntaxError(f"Unknown instruction: {op}")
            
        return True
    
    def run(self, input_text: str = ""):
        """Run the loaded program"""
        self.input_buffer = input_text
        self.instruction_pointer = 0
        self.output = ""
        
        while self.instruction_pointer < len(self.program):
            op = self.program[self.instruction_pointer]
            
            try:
                self.execute_instruction(op)
            except Exception as e:
                print(f"Error at instruction {self.instruction_pointer} ('{op}'): {e}")
                raise
            
            self.instruction_pointer += 1
            
        return self.output
    
    def reset(self):
        """Reset interpreter state"""
        self.memory = [complex(0, 0) for _ in range(256)]
        self.pointer = 0
        self.pitch = 440
        self.rhythm_stack = []
        self.instruction_pointer = 0
        self.output = ""
        self.input_buffer = ""


def create_hello_world_program():
    """Generate the full Hello World program with macro expansion"""
    chars = [72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]
    
    code_lines = []
    code_lines.append("; Skibidi v2.0 Hello World Program")
    code_lines.append("; Generated automatically")
    code_lines.append("")
    
    for i, ascii_val in enumerate(chars):
        code_lines.append(f"; Character {i+1}: '{chr(ascii_val)}' (ASCII {ascii_val})")
        code_lines.append(f"dop({ascii_val})")
        code_lines.append("rizz")
        if i < len(chars) - 1:
            code_lines.append("grimace  ; move to next cell")
        code_lines.append("")
    
    code_lines.append("toilet  ; mandatory end")
    
    return "\n".join(code_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python skibidi.py <filename.skb> [--debug]")
        print("   or: python skibidi.py --demo")
        sys.exit(1)
    
    debug = "--debug" in sys.argv
    
    if sys.argv[1] == "--demo":
        # Run the demo Hello World
        print("=== Skibidi v2.0 Hello World Demo ===")
        print("Generating program...")
        program = create_hello_world_program()
        print("\n" + program)
        print("\n" + "="*40)
        print("Running...\n")
        
        interp = SkibidiInterpreter(debug=debug)
        interp.load_program(program, use_macros=True)
        output = interp.run()
        print(f"\nOutput: {output}")
        
    else:
        # Run from file
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            program = f.read()
        
        interp = SkibidiInterpreter(debug=debug)
        try:
            interp.load_program(program, use_macros=True)
            output = interp.run()
            print(output, end='')
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Runtime error: {e}")
            if debug:
                raise
            sys.exit(1)


if __name__ == "__main__":
    main()