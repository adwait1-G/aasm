#!/usr/bin/python3

#############################################################################################
#                                                                                           #
# nasmshell - A simple python3 wrapper for the awesome nasm and ndisasm commandline tools   #
# Author: Adwaith Gautham                                                                   #
# Repo Link: https://github.com/adwait1-G/aasm                                              #
#                                                                                           #
# LICENSE: There is no license! Use it the way you want to!                                 #
#                                                                                           #
#############################################################################################




import subprocess
import sys
import struct

# These are the default files. 
ASM_FILE = '/tmp/assemble.asm'
LISTING_FILE = '/tmp/listing.lst'
ERROR_FILE = '/tmp/nasm.error'
DISASM_FILE = '/tmp/disassemble.hex'

#############################################################
#                                                           #
# There are 2 important functions:                          #
#                                                           #
# 1. Assemble() - Wrapper for nasm                          #
# 2. Disassemble() - Wrapper for ndisasm                    #
#                                                           #
#############################################################

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


#############################################################
#                                                           #
# There following increase the fancyness of nasmshell!      #
#                                                           #
# 1. changeToYellow() - Changes text color to yellow        #
# 2. changeToWhite() - Changes text color to white          #
# 3. changeToRed() - Changes text color to ret              #
# 1. intro() - A simple intro                               #
# 2. help() - quick tutorial on how to use nasmshell        #
#                                                           #
#############################################################

def changeToRed() : 
        print("\033[1;31;40m", end='')

def changeToWhite() : 
        print("\033[1;37;40m", end='')
        
def changeToYellow() : 
        print("\033[1;33;40m", end='')



def intro() : 

        changeToYellow()
        # Intro
        print("Hello!")
        print("\nI am nasmshell! A simple python wrapper for the awesome nasm and ndisasm commandline tools")
        changeToWhite()
        return


# Will print out 1-2 examples of how to use the tool. 
def help() : 

        changeToYellow()
       
        # Short tutorial
        print("\nThis is how you use me: ")
        print("\nThere are 4 commands: ")
        print("\n1. help - Will give you this intro")
        print("\n2. exit - To exit from nasmshell(You can use Ctrl+D also)")
        
        # Main command No 1 - asm
        print("\n3. asm - To assembly instructions")
        
        # Single instruction example
        print("\n\ta. If you have one single instruction to assemble, you can do it this way: ")
        changeToRed()
        print("\tnasmshell>>> \033[1;37;40masm <Inst>")
        changeToYellow()
        print("\n\tExample: ")
        changeToRed()
        print("\tnasmshell>>> \033[1;37;40masm mov rax, rax")
        print("\t\t1                                  section .text")
        print("\t\t2                                  	global _start")
        print("\t\t3   ")
        print("\t\t4                                  _start :")
        print("\t\t5 00000000 4889C0                  mov rax, rax")
        changeToYellow()
        
        # Multiple instruction example
        print("\n\tb. If you have multiple instructions to assemble, you can do it this way: ")
        changeToRed()
        print("\tnasmshell>>> \033[1;37;40masm Inst1; Inst2; Inst3; .... InstN")
        changeToYellow()
        print("\n\tBasically, separate the instructions by a Semi-colon")
        print("\tExample: ")
        changeToRed()
        print("\tnasmshell>>> \033[1;37;40masm mov rax, rax; xor rbx, r15; ret")
        print("\t\t1                                  section .text")
        print("\t\t2                                  	global _start")
        print("\t\t3                      ")
        print("\t\t4                                  _start :")
        print("\t\t5 00000000 4889C0                  mov rax, rax")
        print("\t\t6 00000003 4C31FB                   xor rbx, r15")
        print("\t\t7 00000006 C3                       ret")
        print("\n")
        changeToYellow()

        # Main command No 2 - disasm
        print("4. disasm - To disassemble valid machine code")
        changeToRed()
        print("\tnasmshell>>> \033[1;37;40mdisasm <Valid Machine Code>")
        changeToYellow()
        print("\n\ta. This is how it's done: ")
        changeToRed()
        print("\tnasmshell>>> \033[1;37;40mdisasm 55c34889c0")
        print("\t00000000  55                push rbp")
        print("\t00000001  C3                ret")
        print("\t00000002  4889C0            mov rax,rax")

        changeToWhite()        
        print("\n\nI hope that helped :)")

        return

#############################################################
#                                                           #
# The following functions drives nasmshell                  #
#                                                           #
# 1. ParseUserInput() - Wrapper for nasm                    #
# 2. mainloop() - driver function                           #
#                                                           #
#############################################################

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
                        print('Unknown command: ', Cmd)
        
        return

# The Driver Loop. 
def mainloop() :
    
    while True:
        changeToRed()
        print("nasmshell>>> \033[1;37;40m", end='')
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
