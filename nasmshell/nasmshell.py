#!/usr/bin/python3

import subprocess
import sys
import struct

# These are the default files. 
ASM_FILE = '/tmp/assemble.asm'
LISTING_FILE = '/tmp/listing.lst'
ERROR_FILE = '/tmp/nasm.error'
DISASM_FILE = '/tmp/disassemble.hex'


# This function assembles the given Payload. 
def Assemble(Payload) :
        
        # Create a list of individual instructions(or instructions seperated by ';')
        AsmInst = Payload.split(';')

        # Generate an assembly file with path: '/tmp/assemble.asm'
        fo = open(ASM_FILE, 'w')
        fo.write('section .text\n\tglobal _start\n\n_start : \n')
        for Inst in AsmInst :
                fo.write(Inst)
                fo.write('\n')

        fo.close()

        # Assemble the file ASM_FILE using nasm. 
        # Catch the listing in LISTING_FILE
        # Catch the errors in ERROR_FILE 
        ErrorFile = open(ERROR_FILE, 'w+')
        subprocess.run(['nasm', ASM_FILE, '-f', 'elf64', '-l', LISTING_FILE], stderr = ErrorFile)
        NasmError = ErrorFile.read()
        ErrorFile.close()

        # Not using the ErrorFile as of now. 

        # Get the complete listing. 
        try :  
                ListingFile = open(LISTING_FILE, 'r')
                Listing = ListingFile.read()
                ListingFile.close()

        except FileNotFoundError : 
                print('LISTING_FILE not created. (Hint: Might be an error in the Payload entered to assemble) ')
                return

        # The main print statement which prints the Hexadecimal Listing!
        print(Listing)

        # Cleanup all the temporary files created. 
        subprocess.run(['rm', ASM_FILE, LISTING_FILE, ERROR_FILE])


# This function disassembles the given Payload. 
def Disassemble(Payload) :
        
        # Convert hex to bytes
        try: 
                hexBytes = bytes.fromhex(Payload)
        
        except ValueError: 
                print("Unknown hex value")
                return

        # Write those bytes into a file
        fd = open(DISASM_FILE, 'wb')
        fd.write(hexBytes)
        fd.close()
        
        ErrorFile = open(ERROR_FILE, 'w+')
        subprocess.run(['ndisasm', DISASM_FILE, '-b', '64'], stderr = ErrorFile)
        NasmError = ErrorFile.read()
        ErrorFile.close()

        # If no error, the disassembly would have already got printed!

        # Cleanup the temporary file
        subprocess.run(['rm', DISASM_FILE])


def intro() : 

        # Change text color to yello-bold
        print("\033[1;33;40m")
        # Intro
        print("Hello!")
        print("\nI am nasmshell! A simple python wrapper for the awesome nasm and ndisasm commandline tools")
        return


# Will print out 1-2 examples of how to use the tool. 
def help() : 

        # Change text color to yellow-bold
        print("\033[1;33;40m")
       
        # Short tutorial
        print("\nThis is how you use me: ")
        print("\n-->There are 4 commands: ")
        print("\n1. help - Will give you this intro")
        print("\n2. exit - To exit from nasmshell(You can use Ctrl+D also)")
        
        # Main command No 1 - asm
        print("\n3. asm - To assembly instructions")
        
        # Single instruction example
        print("\n\ta. If you have one single instruction to assemble, you can do it this way: ")
        print("\t\033[1;31;40mnasmshell>>> \033[1;37;40masm <Inst>")
        print("\033[1;33;40m")
        print("\tExample: ")
        print("\t\033[1;31;40mnasmshell>>> \033[1;37;40masm mov rax, rax")
        print("\t\t1                                  section .text")
        print("\t\t2                                  	global _start")
        print("\t\t3   ")
        print("\t\t4                                  _start :")
        print("\t\t5 00000000 4889C0                  mov rax, rax")
        print("\033[1;33;40m")
        
        # Multiple instruction example
        print("\n\tb. If you have multiple instructions to assemble, you can do it this way: ")
        print("\t\033[1;31;40mnasmshell>>> \033[1;37;40masm Inst1; Inst2; Inst3; .... InstN")
        print("\033[1;33;40m")
        print("\tBasically, separate the instructions by a Semi-colon")
        print("\tExample: ")
        print("\t\033[1;31;40mnasmshell>>> \033[1;37;40masm mov rax, rax; xor rbx, r15; ret")
        print("\t\t1                                  section .text")
        print("\t\t2                                  	global _start")
        print("\t\t3                      ")
        print("\t\t4                                  _start :")
        print("\t\t5 00000000 4889C0                  mov rax, rax")
        print("\t\t6 00000003 4C31FB                   xor rbx, r15")
        print("\t\t7 00000006 C3                       ret")
        print("\n")
        print("\033[1;33;40m")

        # Main command No 2 - disasm
        print("4. disasm - To disassemble valid machine code")
        print("\t\033[1;31;40mnasmshell>>> \033[1;37;40mdisasm <Valid Machine Code>")
        print("\033[1;33;40m")
        print("\n\ta. This is how it's done: ")
        print("\t\033[1;31;40mnasmshell>>> \033[1;37;40mdisasm 55c34889c0")
        print("\t00000000  55                push rbp")
        print("\t00000001  C3                ret")
        print("\t00000002  4889C0            mov rax,rax")
        print("\033[1;33;40m")

        return

# The name says it all!
def ParseUserInput(UserInput) :

        UserInput = UserInput.strip()

        # Exit from nasmshell
        if UserInput == 'exit' :
                print('Gracefully exiting!')               
                sys.exit(1)

        # Valid commands given but no payload given. 
        if UserInput == 'asm' :  
                print('You gave me nothing to assemble :(')
                return

        elif UserInput == 'disasm' : 
                print('You gave me nothing to disassemble :(')
        
        elif UserInput == "help" : 
                help()

        # For commands(asm, disasm or unknown) with Payload
        else : 
                # Get the index of first space. 
                try : 
                        FirstSpace = UserInput.index(' ', 0)
                
                except : 
                        print("Unknown command: ", UserInput)
                        return

                # Split the Userinput
                Cmd = UserInput[0 : FirstSpace]
                Payload = UserInput[FirstSpace+1 : ]


                if Cmd == 'asm' :
                        Assemble(Payload)
                
                elif Cmd == 'disasm' :
                        Disassemble(Payload)

                else :
                        print('Unknown Command: ', Cmd)
        
        return

# The Driver Loop. 
def mainloop() :
    
    while True:
        print("\033[1;31;40mnasmshell>>> \033[1;37;40m", end='')
        try :
                UserInput = str(input())
        except EOFError :
                print("\nGracefully exiting!")
                return
        
        except KeyboardInterrupt : 
                print("\nOh, come on!")
                continue

        if len(UserInput) != 0 :
                ParseUserInput(UserInput)
                 
        

if __name__ == "__main__" :
        
        intro()
        mainloop()






















