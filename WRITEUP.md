

Intro
=====
This writeup is divided into sections detailing the individual exercises 
within the synacor challenge. Each section will contain a description of 
the problem followed by an account of how I solved it. Anyone reading this 
should have already solved the overall challenge, but the problem 
descriptions may serve as a reminder for those who don't fully remember 
them. If however, the problems are fresh in your head, then you can simply 
skip forward to the solutions.


Implementing the syn virtual machine (Codes 1-4)
================================================
### Problem
The first item you are tasked with is to create a virtual machine that
implements the given specification.

### Solution
This virtual machine is very basic, and anyone with rudimentary knowledge
on how computers work should be able to throw something together
relatively quickly. Luckily I had written a Chip-8 emulator before, so I
wasn't completely clueless as to how to proceed.


Navigating the maze (Code 5)
============================
### Problem
Once you get the virtual machine going, you then run the given binary with
it. What you find is that the binary is actually a text adventure game!
Playing through it, you soon find yourself in a maze with some very bizarre
characteristics. For example, going north repeatedly will eventually take
you where you started. To proceed with the game, you need to navigate your
way out of this maze.

### Solution
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

So I went through the maze again, this time actually paying attention to 
the text. Luckily, the room descriptions are different enough that you can
uniquely identify each room. Now I could keep track of the rooms in my head
and within 5 minutes I found the exit. All in all, this makes sense to have
as a challenge since attention to detail is an important trait for a
programmer.


Solving the coin puzzle (Code 6)
================================
### Problem
So after getting through the maze, you find yourself confronted with yet
another puzzle. This time an equation like so.

_ + _ * _^2 + _^3 - _ = 399

You are then given 5 values with which to fill out the blanks with.

### Solution
I have to admit, I was a little disappointed in how easy this one was. 
Using educated guesswork, I was able to solve manually in a few tries.

Just for fun though, here is some python code that will solve it
automatically.

```
from itertools import permutations

for a, b, c, d, e in permutations([2, 3, 5, 7, 9]):
    if a + b * c**2 + d**3 - e == 399:
        print(a, b, c, d, e)
```


Using the teleporter (Code 7)
=============================
### Problem
After solving the equation, you then come across a teleporter. You also
obtain a book describing how to operate your new teleportation device. It
mentions something about an 8th register needing to be set to a non-zero
value. Doing this then activates a verification routine, for the teleporter
requires a very specific value, and if that value is not met, you may rip
the space time continuum (or something like that). The only issue is that
your teleporter is rather low-tech and will take about a billion years to
run through the verification algorithm.

### Problem
Though the previous problem was a bit lackluster, this one more than makes
up for it. The teleporter is definitely the most interesting (and most
difficult) exercise in the entire challenge.

At first, I thought this was just going to be a simple equality check. (I
guess I wasn't really understanding the whole take a billion years to
verify thing.) So I tried getting by with nothing more than a trace routine
which would print off all the instructions my vm executed. This however,
was not enough, and I began work on a debugger. This allowed me to interact
more with the program, but I was still having trouble visualizing where
exactly I was in the overall logic. One disassembler later, and I had what
I needed to start solving the problem.

Now I have to admit that unfortunately (or maybe fortunately) I stumbled
upon a hint on reddit mentioning the Ackermann function. So knowing that,
and using my newly crafted tools, I was able to piece together what was
happening.

Essentially, the value in the R7 register is actually a key for decrypting
the next game code, and the verification routine is verifying that you have
the correct value for that key. So to get through this, one has to extract
the verification algorithm, optimize it, figure out the correct key, put
that key in R7, and then force the vm to skip the verification routine.

Okay, so the algorithm is a modified version of the Ackermann function. The
definition is as follows.

```
A(m, n) =
  n + 1               if m = 0
  A(m-1, k)           if m > 0 and n = 0
  A(m-1, A(m, n-1))   if m > 0 and n > 0

where k is some constant
```

The program is setting m to 4, n to 1, and k to the value in R7, and then
checking that the result is 6. This will only happen with the correct key
value.

I was hoping to come up with an elegant closed form solution that I could
then solve by hand, but was not successful. I got to m = 0, 1, and 2, but
then after that it got too complicated.

```
A(0, n) = n + 1
A(1, n) = k + n + 1
A(2, n) = n(k+1) + 2k + 1
```

Figuring out these formulas was not in vain though. I then wrote a program
(crack-better-verifier.c) that defined A recursively, but for m = 2, fell
back to the closed form solution I came up with. This reduced the
recursion enough that the program could solve for k in about 10 seconds.

That got me the answer, but it was kind of slow. I then optimized further
(crack-even-better-verifier.c) by having the function use a looping
construct to solve for when m = 3. This got me down to about 3 seconds.

The loop construct is possible because using the closed form solutions
we can simplify m = 3 to the following.

```
A(3, n) =
  A(2, k)          = K^2 + 3k + 1                   if n = 0
  A(2, A(3, n-1))  = A(3, n-1) * (k+1) + 2k + 1     if n > 0
```


Unlocking the vault (Code 8)
=============================
### Problem
There is now one last puzzle to solve. After teleporting successfully to
a beach, you continue on and find a locked vault with a very elaborate
locking mechanism. Before the vault lies a grid of rooms, with markings on
the floor like so.

```
 *      8      -      1
 4      *     11      *
 +      4      -     18
22      -      9      *
```

You start off at the lower left and are given a value of 22. As you walk
around the grid, depending on what rooms you enter, your value will change.
For example, walking on a plus sign followed by a four means that your
given value will increment by four. You can only go up, down, left, and
right, so you will always alternate between operator and operand. The goal
is then to end at the upper right with a value of 30, in a minimal amount 
of moves. Also, the extreme lower left room cannot be re-entered, and the
extreme upper right room can only be entered once.

### Solution
So this was another interesting challenge. I figured that the overall path
wouldn't be too long, so I decided to brute force it using find_path.py.

To simplify the program, I only actually work with rooms that have
operands in them. I then create the relationship between these rooms by 
going through each of them and listing the possible routes to the next 
available room along with how that route will adjust the current value.

Once that is properly modeled, I then use a recursive function that will
go through all the possible paths that don't exceed a specified number of
steps. If it ever gets to the goal room with a value of 30, it will print
the path and exit. Finally, to help whittle down the search space, I back 
up if the value ever falls below 0 or gets ridiulously big.

To solve, I then call that function repeatedly, starting with a path length
of 0 and incrementing the number of steps until I get a path that works.
Since the correct path is only 6 steps long, I can get the answer in about
30 milliseconds.

One optimization I had thought of, but ended up not needing, was to go
through the grid backwards. Basically you would start with a value of 30
and need to get to 22, but the operators would include division instead of
multiplication. Also, the operator would have to apply the operand as the
number of the room you came from, not the number of the room you went to.
The advantage of this though, is that you could potentially cut off entire
branches because you know that if you perform a division and end up with a
non-whole number, then it isn't a valid path.

It could be a fun challenge to come up with a variation of this grid such
that a brute force solution going forward is computationally impractical,
but a solution going  backwards and trimming the immediately invalid
branches is computationally trivial.


Conclusion
==========
So all in all, this was an awesome challenge to go through. I really like
when challenge authors take the time to add some story elements into the
mix. I am also looking forward to starting the Advent of Code challenges
which appear to be similar.

One thing I find interesting is that the implementation of the challenges
was probably quite involved. I would definitely love to see
a writeup from the actual author as to how he made this challenge and what
techniques he employed to try to prevent unwanted reverse engineering. In
fact, another thing that is so awesome about this challenge is that trying
to hack the ROM and access the game codes directly without solving the
problems could serve as a fun meta challenge to all of this.

I am extremely glad to have stumbled on this because doing the synacor
challenge has gotten me back into the habit of working fun type projects 
on the side. I already have a large list of other challenges to go work,
and I would love to maybe try my hand at making some myself.

As a further exercise for this particular challenge, after having a bit
more assembly programming under my belt, I wouldn't mind coming back and
writing some programs for syn-vm. Maybe a connect four game would be cool.


