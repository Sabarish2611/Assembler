import string
import numpy as np
import pandas as pd

Dest = {'null': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'}
Comp = {'0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        '!D': '001101',
        '!A': '110001',
        '-D': '001111',
        '-A': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101',
        'M': '110000',
        '!M': '110001',
        '-M': '110011',
        'M+1': '110111',
        'M-1': '110010',
        'D+M': '000010',
        'D-M': '010011',
        'M-D': '000111',
        'D&M': '000000',
        'D|M': '010101'

        }
Jump = {'null': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'}
Symbols = {'R0': '0',
           'R1': '1',
           'R2': '2',
           'R3': '3',
           'R4': '4',
           'R5': '5',
           'R6': '6',
           'R7': '7',
           'R8': '8',
           'R9': '9',
           'R10': '10',
           'R11': '11',
           'R12': '12',
           'R13': '13',
           'R14': '14',
           'R15': '15',
           'SCREEN': '16384',
           'KBD': '24576',
           'SP': '0',
           'LCL': '1',
           'ARG': '2',
           'THIS': '3',
           'THAT': '4'}

Op_code = ['0', '1']

Labels = {}

file = input('File : ')
Assembly_Language = pd.read_csv(file, skip_blank_lines=True, squeeze=True, header=None)

Assembly_Language_copy = Assembly_Language.copy()


def Preprocess(code):
    for instruction in code:
        if '//' in instruction:
            if '=' in instruction:
                p = instruction.split('//')
                q = p[0]
                valid_instruction = q.translate({ord(c): None for c in string.whitespace})
                code = code.replace(instruction, valid_instruction)
            elif ';' in instruction and '=' not in instruction:
                r = instruction.split('//')
                s = r[0]
                valid_instruction = s.translate({ord(c): None for c in string.whitespace})
                code = code.replace(instruction, valid_instruction)
            else:
                o = instruction.split('//')
                n = o[0].split()
                valid_instruction = n[0]
                code = code.replace(instruction, valid_instruction)
        a = instruction.translate({ord(c): None for c in string.whitespace})
        code = code.replace(instruction, a)
    return code


def Label_Instruction(code):
    count = 0
    for instruction in code:
        count += 1
        if instruction.startswith('('):
            count -= 1
            pos = instruction.find(')')
            t = instruction[1:pos]
            Labels[t] = count
            code = code.replace(instruction, "")
        if instruction.startswith(" "):
            a = instruction.split()
            code = code.replace(instruction, a[0])
    return code


def Blank_Lines_Eliminator(code):
    a = []
    for instruction in code:
        if len(instruction) != 0:
            a.append(instruction)
    valid_instruction = pd.Series(a)
    return valid_instruction


def A_Instruction(code):
    for instructions in code:
        if instructions.startswith('@'):
            if instructions[1].isdigit() == True:
                value = instructions[1:]
                if value.isdigit():
                    binary_value = np.binary_repr(int(value), width=15)
                    binary_instruction = Op_code[0] + binary_value
                    code = code.replace(instructions, binary_instruction)
    return code


def C_instruction(code):
    for instruction in code:
        if instruction[0].isalpha():
            if '=' in instruction:
                z = instruction.split('=')
                destination = z[0]
                y = z[1]
                if ';' in y:
                    x = y.split(';')
                    jump = x[1]
                    computation = x[0]
                else:
                    jump = '000'
                    computation = z[1]
                if 'M' in computation:
                    a = '1'
                else:
                    a = '0'
                if destination in Dest:
                    destination = Dest[destination]
                if computation in Comp:
                    computation = Comp[computation]
                if jump in Jump:
                    jump = Jump[jump]
                binary_instruction = Op_code[1] + '11' + a + computation + destination + jump
                code = code.replace(instruction, binary_instruction)
            else:
                if ';' in instruction:
                    destination = '000'
                    v = instruction.split(';')
                    computation = v[0]
                    jump = v[1]
                    a = '0'
                    if computation in Comp:
                        computation = Comp[computation]
                    if jump in Jump:
                        jump = Jump[jump]
                    binary_instruction = Op_code[1] + '11' + a + computation + destination + jump
                    code = code.replace(instruction, binary_instruction)
        else:
            if ';' in instruction:
                destination = '000'
                v = instruction.split(';')
                computation = v[0]
                jump = v[1]
                a = '0'
                if computation in Comp:
                    computation = Comp[computation]
                if jump in Jump:
                    jump = Jump[jump]
                binary_instruction = Op_code[1] + '11' + a + computation + destination + jump
                code = code.replace(instruction, binary_instruction)
    return code


def Symbol_Instruction(code):
    count = 0
    for instruction in code:
        if instruction.startswith('@'):
            if instruction[1].isalpha() == True:
                value = instruction[1:]
                if value in Symbols and value not in Labels:
                    value = Symbols[value]
                    binary_value = np.binary_repr(int(value), width=15)
                elif value in Symbols and value in Labels:
                    value = Symbols[value]
                    binary_value = np.binary_repr(int(value), width=15)
                elif value not in Symbols and value not in Labels:
                    while True:
                        count += 1
                        u = 16 + count - 1
                        break
                    Symbols[value] = str(u)
                    binary_value = np.binary_repr(int(u), width=15)
                elif value not in Symbols and value in Labels:
                    p = Labels[value]
                    Symbols[value] = str(p)
                    binary_value = np.binary_repr(int(p), width=15)

                binary_instruction = Op_code[0] + binary_value
                code = code.replace(instruction, binary_instruction)
    return code


def Assembler(code):
    Hack_Language_P = Preprocess(Assembly_Language_copy)
    Hack_Language_L = Label_Instruction(Hack_Language_P)
    Hack_Language_B = Blank_Lines_Eliminator(Hack_Language_L)
    Hack_Language_A = A_Instruction(Hack_Language_B)
    Hack_Language_C = C_instruction(Hack_Language_A)
    Hack_Language = Symbol_Instruction(Hack_Language_C)
    return Hack_Language


print(Assembler(Assembly_Language_copy))
