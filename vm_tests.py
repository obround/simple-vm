from vm import *

vm = VM(registers = 30)
print(vm.registers)
vml = vm.append_line

vml(LOAD, 0, 5)
vml(LOAD, 1, 10)
vml(MOV, 0, 1)
vml(DEC, 0, 3)
vml(PRINTF, 0)
vml(READ, 0, "Change register 0 to: ")
vml(PRINTF, 0)
vml(PRINTF, 2)

vml(SEGM, "test_segment", [
    [PRINTF, 0],
    [PRINTF, 2]
])

vml(SEGM, "test_segment2", [
    [PRINTF, 2],
    [PRINTF, 0],
    [LOAD, 6, 3.1415],
    [INC, 7, 1],
    [RETURN, 6]
])

vml(CALL, "test_segment2", 9)
vml(PRINTF, 9)
#vml(IF, 8, 0, "test_segment")
#vml(IF_ELS, 8, 10, "test_segment", "test_segment2")

vml(LOAD, 2, 10)
vml(POW, 2, 2, 1)
vml(LEQ, 5, 3, 1)
vml(PRINTF, 5)
vml(PRINTF, 2)
vml(WHILE_LOOP, 7, 10,"test_segment2")
vml(FOR_LOOP, 0, 100, 9, "test_segment")
vml(EXIT)

vm.execute()