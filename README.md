# yan85 Architecture Plugin for Binary Ninja
This was a personal project to learn more about Binary Ninja (and maybe acting as a crutch for yan85 challenges on [pwn.college](https://pwn.college/)). This was heavily based off of another architecture plugin by lowbob-rondo ([his plugin](https://librondo.so/BinjaVm/Architecture+Plugin)).

## What is yan85?
yan85 is a custom architecture used in challenges on [pwn.college](https://pwn.college/). The architecture has 3 byte long instructions, with 1 byte representing the opcode and the other 2 for the arguments.

## How to use
You can dump the program code with `scripts/dump.py`. It will ask for the path to the virtual machine binary, the address where the yan85 code starts, the code length, and where beginning yan85 memory address.

Every yan85 challenge is different. Opcodes, syscalls, flags, and more have different values. Before opening a yan85 program, make sure you've defined all of the changing values in `versions/active.py`. Just for reference, I've included some examples in `versions/reverse_engineering` which work for the associated levels in the pwn.college reverse engineering module.

## Problems
Because the stack grows up in this architecture, it seems like Binary Ninja has some trouble with stack based operations, such as when a string is built on the stack. 

Theres also no pattern I've noticed for calling convetion and functions, so most functions will have to be defined manually.
