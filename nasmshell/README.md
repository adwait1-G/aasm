# nasmshell

This is a interactive assembler and disassembler which uses nasm at it's core. 
It is a a very basic python wrapper around the nasm and ndisasm tools. 

You can use this tool if you quickly want assembly or disassembly of some Payload. 

## How do you install and run it?

1. Install **nasm** and **ndisasm** : 

        $ sudo apt-get install nasm

* With this command, you will get both the tools - nasm and ndisasm

2. Clone this Repository : 

        $ git clone https://github.com/adwait1-G/aasm.git

3. Enter the **nasmshell** directory : 

        $ cd aasm/nasmshell

4. Give executable permissions to the python script **nasmshell.py** : 

        aasm/nasmshell$ chmod u+x nasmshell.py

5. Run it : 

        aasm/nasmshell$ ./nasmshell.py
        nasmshell>>>
        nasmshell>>>
        nasmshell>>>

6. You are good to go :)


## How do you use it?

1. It is very simple. There are only 2 commands in nasmshell. They are **asm** and **disasm**. 

2. Examples for **asm** : 

    a. Simple single instructions can be assembled. 

        nasmshell>>> asm xor eax, ebx
        1                                  section .text
        2                                          global _start
        3
        4                                  _start :
        5 00000000 31D8                    xor eax, ebx

    b. If you want machine code of multiple instructions at the same time, you can do separate the commands by a **;** : 

        nasmshell>>> asm xor eax, ebx; inc r15; mov al, byte[rsi]
        1                                  section .text
        2                                          global _start
        3
        4                                  _start :
        5 00000000 31D8                    xor eax, ebx
        6 00000002 49FFC7                   inc r15
        7 00000005 8A06                     mov al, byte[rsi]


3. Examples for **disasm** : This is a work under progress!













