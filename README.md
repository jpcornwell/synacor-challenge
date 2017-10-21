
Synacor-Challenge
=================

The Synacor Challenge is a story driven collection of programming exercises
and logic puzzles provided by the company Synacor.

I would say that the problems inside it range from beginner to intermediate
difficulty, but overall it is a fun experience.

This repository contains some code and a writeup of my playthrough of this
challenge.  


Documentation
=============


Syn-VM
------

The virtual machine is the file syn-vm.py. Run it with the -h option to see
how to use it. For simply running a program, call the script with the
desired binary file as input, like so.

```
./syn-vm.py challenge.bin
```


Save/Load
---------

Syn-VM will allow you to save and load the machine state so that you can
jump back into a session where ever you left off.

The save feature is a little hackish. You need to wait for the VM to
request input, and then type in "debug: save". This will then create a
file in your directory called "save.state" that you can then use to load
from.

To load use the -l option.

```
./syn-vm.py -l foo.state
```


Tracer
------

Syn-VM includes tracer functionality for debugging purposes. Specify the
-t option, and it will create a file called "trace.out" in your directory
that contains the exact instructions that were executed by the VM for that
session.

```
./syn-vm.py -t program.bin
```


Debugger
--------

Syn-VM has an interactive debugger that you can use. With it you can go
through instructions step by step, set and remove breakpoints, and change
register values.

In order to keep the debugger output separate from the normal VM output,
the VM output will be redirected to a file called "display.out" when in
debug mode. The recommended workflow is to use two terminals and run the
two following commands in them. (First command going to the first terminal,
second command going to the second terminal.)

```
./syn-vm.py -d program.bin
tail -f display.out
```

The commands you can run from the debug menu are these.

|Command                   |Description                              |
|--------------------------|-----------------------------------------|
|step                      |Step through one instruction             |
|continue                  |Continue execution to the next breakpoint|
|set break \<addr>         |Set a breakpoint at the given address    |
|remove break \<addr>      |Remove a breakpoint at the given address |
|display breaks            |Display a list of the active breakpoints |
|set register \<#> \<value>|Set the # register to the given value    |


Utils
-----

### Crack Programs
These are programs to crack the key for the teleporter game-code. Simply
compile and run them. The inputs are hard coded in.

### Disassembler
This will try to disassemble syn-vm machine code to an assembly-like
readable format. It doesn't do anything special for differentiating
between code and data within a binary, but it should work well enough for 
most situations.

```
./disassembler.py program.bin
```

### Print Dump
This is just a quick script that I wrote for printing a hexdump-like
printout to the screen of a syn-vm binary. The reasoning was that hexdump
was giving me addresses per byte, and I wanted addresses to be per word,
so that I didn't have to constantly convert between the two when looking
at a trace or disassembly. There probably is an option in hexdump to give 
me what I wanted, but this was quicker.

```
./print_dump.py program.bin
```
