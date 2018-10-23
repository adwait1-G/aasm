#!/usr/bin/python3

import subprocess
import sys

# These are the default files. 
ASM_FILE = '/tmp/assemble.asm'
LISTING_FILE = '/tmp/listing.lst'
ERROR_FILE = '/tmp/nasm.error'


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

        DisasmHex = Payload
        print('Payload: ', DisasmHex)


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
        

# The Driver Loop. 
def mainloop() :
    
    while True:
        print("nasmshell>>> ", end='')
        try :
                UserInput = str(input())
        except EOFError :
                print("\nGracefully exiting!")
                return

        if len(UserInput) != 0 :
                ParseUserInput(UserInput)
                 
        

if __name__ == "__main__" :
        
        mainloop()






















