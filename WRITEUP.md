

Intro
=====
This writeup is divided by sections detailing the individual exercises 
within the synacor challenge. Each section will contain a description of the
problem followed by an account of how I solved it. Anyone reading this 
should have already solved the overall challenge, but the problem 
descriptions may serve as a reminder for those who don't fully remember 
them. If however, the problems are fresh in your head, then you can simply 
skip forward to the solutions.


Implementing the syn virtual machine (Codes 1-4)
================================================
The first item you are tasked with is to create a virtual machine that
implements the given specification.

This virtual machine is very basic, and anyone with rudimentary knowledge
on how computers work should be able to throw something together
relatively quickly. Luckily I had written a Chip-8 emulator before, so I
wasn't completely clueless as to how to proceed.


Navigating the maze (Code 5)
============================
Once you get the virtual machine going, you then run the given binary with
it. What you find is that the binary is actually a text adventure game!
Playing through it, you soon find yourself in a maze with some very bizarre
characteristics. For example, going north repeatedly will eventually take
you where you started. To proceed with the game, you need to navigate your
way out of this maze.

My first thought was I would need to reverse engineer the binary file.
Since I had just written a virtual machine, I figured all of the following
challenges would be ones that required hacking the ROM. 

So I started off by doing a simple "strings" on the binary, but didn't get
anything useful back. Then I tried doing "strings" on a memory dump that I
extracted after the self-tests ran, in case the program decrypted itself. 
Sure enough, I then got some valid results including the room descriptions.

But as I examined the room descriptions I found they were not exactly the
same. They all had subtle differences, which I figured was obviously 
some sort of hint for solving this.

So I went through the maze again, this time actually paying attention to the
text. Luckily, the room descriptions are different enough that you can
uniquely identify each room. Now I could keep track of the rooms in my head
and within 5 minutes I found the exit. All in all, this makes sense to have
as a challenge since attention to detail is an important trait for a
programmer.


Solving the coin puzzle (Code 6)
================================
So after getting through the maze, you find yourself confronted with yet
another puzzle. This time a door that unlocks by solving the equation etched
on it. It essentially is of the form ... and you are given a set of values
to place in the blanks.

I have to admit, I was a little disappointed in how easy this one was. Using
educated guesswork, I was able to solve manually in a few tries.

stub: include a code snippet that solves this (just for fun)


Using the teleporter (Code 7)
=============================
stub: thought I could get by with tracer and hexdump
stub: created a debugger to provide interactivity
stub: created a disassembler to locate where I was in the logic
stub: had seen a hint on reddit mentioning ackermann function
stub: provide definition of verifier function in terms of m, n, and k
stub: tried to come up with a closed form solution by hand
stub: got m = 0, m = 1, and m = 2
stub: using that, optimized the code (crack-better-verifier.c) to use m = 2
      formula, solved in 10 seconds
stub: tried optimizing further, use a loop to calculate m = 3, improved
      solving time to 3 seconds


Conclusion
==========
stub: would like to write a "to syn machine code" compiler (or assembler)
stub: thinking about a connect four game for the syn-vm
stub: look out for more things from this guy (like advent of code)


