"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        # program count
        self.pc = 0
        # stack counter
        self.sp = 7
        self.return_pc = 0
        # self.stack_start = 16
        # self.stack_end = 240
        # self.stacksize = "?"
        self.reg = [None] * 8
        self.running = True
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.ADD = 0b10100000
        self.SUB = 0b10100001
        self.MUL = 0b10100010
        self.DIV = 0b10100011
        self.MOD = 0b10100100
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001

    def load(self, program):
        """Load a program into memory."""
        # wipe RAM
        for address in self.ram:
            ram = 0
        # wipe REG
        for reg in self.reg:
            reg = 0
        # reset process counter
        self.pc = 0

        # assign reg[7] = 243
        self.reg[self.sp] = 0xF3

        # reset FL????

        # boot program
        #    index     value        provide from arg
        # Initializing Address of Stackhead to REG
        for address, instruction in enumerate(program):
            self.ram[address] = instruction
            address += 1

    def run(self):
        """Run the CPU.       
        1. read mem at PC
        2. store result in local var
        3. turn into hash_tables
        """

        while self.running is True:
            IR = self.ram[self.pc]
            branch_table = {
                self.LDI: self.ldi,
                self.PRN: self.prn,
                self.HLT: self.hlt,
                self.ADD: self.add,
                self.SUB: self.sub,
                self.MUL: self.mul,
                self.DIV: self.div,
                self.MOD: self.mod,
                self.PUSH: self.push,
                self.POP: self.pop,
                self.CALL: self.call,
                self.RET: self.ret,
            }
            if IR in branch_table:
                branch_table[IR]()
            else:
                print(f'Unknown instruction: {IR}, at address PC: {self.pc}')
                sys.exit(1)
            # branch_table.get(IR)()

    def alu(self, op, reg_a, reg_b):
        """ALU operations.
        Algorythmic Logic Units
        # add masking?
            use repl
        """
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
            print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
            print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
            print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
            self.pc += 3
            print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
            self.pc += 3
            print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        else:
            raise Exception(f"Unsupported ALU operation: {op}")
            self.trace()

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        # accept address
        # return it's value
        return self.ram[address]

    def ram_write(self, value, address):
        # take a value
        # write to address
        # no return
        self.ram[address] = value

    def hlt(self):
        self.pc += 1
        self.running = False

    def prn(self):
        reg_id = self.ram[self.pc + 1]
        self.reg[reg_id]
        print("Returning", self.reg[reg_id])
        self.pc += 2

    def ldi(self):
        reg_id = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[reg_id] = value
        # what are values? atomic numbers OR addresses to RAM?
        self.pc += 3

    def add(self):
        self.alu("ADD", 0, 0)

    def sub(self):
        self.alu("SUB", 0, 1)

    def mul(self):
        self.alu("MUL", 0, 1)

    def div(self):
        self.alu("DIV", 0, 1)

    def mod(self):
        self.alu("MOD", 0, 1)

    def push(self):
        # decrements the VALUE stored at reg[7], which is the address in Stack, "new head"
        self.reg[self.sp] -= 1
        # storing value of next instruction
        reg_val = self.ram_read(self.pc + 1)
        # reg_val = self.ram[self.pc + 1]
        # writing the saved value from ram into the reg
        value = self.reg[reg_val]
        # saving the new head (stack address) into a variable
        top_loc = self.reg[self.sp] 
        # linking the value/address in REG[7] to loc in RAM
        self.ram_write(value, top_loc)
        # self.ram[top_loc] = value
        # print("PUSH", "Reg_LOC:", self.sp , "Ram_Loc:",  reg_id, "Val:", self.ram[top_loc])
        # incrementing PC count by 2 (1 line for insturction, 1 line for reg[address])
        self.pc += 2

    def pop(self):
        # getting addrees of old stack head that will be changed from REG (always R[7])
        # print("POP!")
        top_loc = self.reg[self.sp]
        # print("TOP_LOC:", top_loc)
        
        # get the index of new stack head from RAM
        stack_index = self.ram[self.pc + 1]
        # print("stack_index:", stack_index)

        # overwrite our reg address with the value of our memory address we are looking at
        self.reg[stack_index] = self.ram[top_loc]

        # increment value (not index) of sp to point to new top of stack
        self.reg[self.sp] += 1
        # print("RAM_ID:", self.ram[self.reg[7]])
        # increase counter by 2 (2 lines of instructions)
        # print("RAM:", self.ram)
        self.pc += 2

    def call(self):
        # Calls a subroutine at the address stored in the register
        # 1. The address of the instruction directly after CALL is pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        return_pc = self.pc + 2
        # Set value in the stack to the PC value we want to return to after we call the function
        self.reg[self.sp] -= 1
        top_of_stack_address = self.reg[self.sp]
        self.ram[top_of_stack_address] = return_pc
        # 2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backward from its current location.
        subroutine_pc = self.ram[self.pc + 1]
        self.pc = self.reg[subroutine_pc]
    
    def ret(self):
        # Return from subroutine
        # Pop the value from the top of the stack and store it in the PC
        # print("REG: ", self.reg)
        top_of_stack_address = self.reg[self.sp]
        return_pc = self.ram[top_of_stack_address]
        self.pc = return_pc

        
"""
Todos:
    Instructions for implementing each day?
    reg_read func
    reg_write func
    specify stack params in RAM?
    Stretch goals

Notes:
    - stack only contains return address for functions/subroutines, but not that subroutines actual instructions
    -  register used to return a value, direct or indirectly
    - pass things in via the register
    - Interupts = how peripherals(hardware) indicate to CPU action needs to be taken
        - like callbacks
        - polling: has a key been pre
        - take PC of interrupt
            - send to code to handle interrupt
        - IRET = interrupt return
            - saves all registers
        - IV save addresses
            - serve as pointers
            - set PC to that value

Research:
    - Difference between JMP and CALL?
    - Jupytr
    - books:
        - the design of the UNIX operating system
        - Advanced Programming in the UNIX Environment, 3rd Editio

lambda: reg_a, reg_b: reg[reg_a] += reg[reb_b]

"""
