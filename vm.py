from opcodes import *


class VM:
    def __init__(self, registers = 10):
        self.registers = [0] * registers
        self.segments = {}

        self.pc = 0
        self.code = []

    def append_line(self, opcode, *args):
        self.code.append((opcode, args))
    
    def set_registers(self, registers):
        self.registers = registers
    
    def bytecode(self, code):
        self.code = code
    
    def build(self):
        opcode, self.args = self.code[self.pc]

        exec_map = {
            LOAD : self._LOAD,
            MOV : self._MOV,
            EXIT : self._EXIT,
            PRINTF : self._PRINTF,
            READ : self._READ,
            SEGM : self._SEGM,
            CALL : self._CALL,
            ADD : self._ADD,
            SUB : self._SUB,
            MUL : self._MUL,
            DIV : self._DIV,
            POW : self._POW,
            LT : self._LT,
            GT : self._GT,
            EQ : self._EQ,
            NEQ : self._NEQ,
            GEQ : self._GEQ,
            LEQ : self._LEQ,
            IF : self._IF,
            IF_ELS : self._IF_ELS,
            INC : self._INC,
            DEC : self._DEC,
            RETURN : self._RETURN,
            WHILE_LOOP : self._WHILE_LOOP,
            FOR_LOOP : self._FOR_LOOP
        }
        
        exec_map[opcode]()
    
    def execute(self):
        while self.pc < len(self.code):
            self.build()
            self.pc += 1
    
    def _LOAD(self):
        self.registers[self.args[0]] = self.args[1]

    def _MOV(self):
        self.registers[self.args[0]] = self.registers[self.args[1]]
    
    def _WHILE_LOOP(self):
        local_vm = VM(registers = len(self.registers))
        local_vm.set_registers(self.registers)

        while self.registers[self.args[0]] != self.args[1]:

            for line in self.segments[self.args[2]]:
                local_vm.append_line(line[0], *line[1:])
                local_vm.execute()
    
    def _FOR_LOOP(self):
        local_vm = VM(registers = len(self.registers))
        local_vm.set_registers(self.registers)

        for x in range(self.args[0], self.args[1]):
            self.registers[self.args[2]] = x

            for line in self.segments[self.args[3]]:
                local_vm.append_line(line[0], *line[1:])
                local_vm.execute()
    
    def _PRINTF(self):
        print(self.registers[self.args[0]])
    
    def _READ(self):
        inp = input(self.args[1])
        self.registers[self.args[0]] = inp
    
    def _SEGM(self):
        self.segments[self.args[0]] = self.args[1]
    
    def _CALL(self):
        local_vm = VM(registers = len(self.registers))
        local_vm.set_registers(self.registers)

        for line in self.segments[self.args[0]]:
            if line[0] == RETURN:
                store = False
                try:
                    self.args[1]
                    store = True
                
                except:
                    pass

                if store:
                    self.registers[self.args[1]] = self.registers[line[1]]

            local_vm.append_line(line[0], *line[1:])
            local_vm.execute()
    
    def _ADD(self):
        self.registers[self.args[0]] = self.args[1] + self.args[2]
    
    def _SUB(self):
        self.registers[self.args[0]] = self.args[1] - self.args[2]
    
    def _MUL(self):
        self.registers[self.args[0]] = self.args[1] * self.args[2]
    
    def _DIV(self):
        self.registers[self.args[0]] = self.args[1] / self.args[2]
    
    def _POW(self):
        self.registers[self.args[0]] = self.args[1] ** self.args[2]
    
    def _LT(self):
        self.registers[self.args[0]] = self.args[1] < self.args[2]
    
    def _GT(self):
        self.registers[self.args[0]] = self.args[1] > self.args[2]
    
    def _EQ(self):
        self.registers[self.args[0]] = self.args[1] == self.args[2]
    
    def _NEQ(self):
        self.registers[self.args[0]] = self.args[1] != self.args[2]

    def _GEQ(self):
        self.registers[self.args[0]] = self.args[1] >= self.args[2]

    def _LEQ(self):
        self.registers[self.args[0]] = self.args[1] <= self.args[2]
    
    def _IF(self):
        if self.registers[self.args[0]] == self.args[1]:
            local_vm = VM(registers = len(self.registers))
            local_vm.set_registers(self.registers)

            for line in self.segments[self.args[2]]:
                local_vm.append_line(line[0], *line[1:])
                local_vm.execute()
    
    def _IF_ELS(self):
        local_vm = VM(registers = len(self.registers))
        local_vm.set_registers(self.registers)

        if self.registers[self.args[0]] == self.args[1]:
            for line in self.segments[self.args[2]]:
                local_vm.append_line(line[0], *line[1:])
                local_vm.execute()
        
        else:
            for line in self.segments[self.args[3]]:
                local_vm.append_line(line[0], *line[1:])
                local_vm.execute()
    
    def _INC(self):
        self.registers[self.args[0]] += self.args[1]
    
    def _DEC(self):
        self.registers[self.args[0]] -= self.args[1]
    
    def _RETURN(self):
        pass

    def _EXIT(self):
        self.pc = len(self.code)