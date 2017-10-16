## The Players ##

* Data stack
* Literals
* Words 

## What to do with input? ## 

All input flows through `consume_tokens`. `consume_tokens` expects a list of tokens.
(Input is first "formatted" by running it through `tokenize`.)


Example:
========

    # SOURCE: ($ROOTDIR/mjForth.py | 212)
    def consume_tokens(input_list):
        while input_list:
            term = input_list.pop(0)
            handle_term(term, input_list)


`handle_term` routes the given word to the correct action. There are a small number of possible routes:


Input Types Routing:
===================

Types of input to deal with:
    
* Terminating Branches:

    * literals (ints, true, false)
    * Built-in words
    * word definition
    * see
    * variable declaration (in globally-accessible Memory)
    * variable store/fetch 

* Non-terminating Branches:

    * do loop
    * while loop
    * User-defined words
    * conditional (IF ... ENDIF / IF ... ELSE .. ENDIF )

Eval/Apply:
==========

[Substitution Model](https://mitpress.mit.edu/sicp/full-text/sicp/book/node10.html)

    "To apply a compound procedure to arguments, 
     evaluate the body of the procedure with each 
     formal parameter replaced by the corresponding argument."

Our case is a bit different. To apply a word, evaluate the words it is composed of. We don't need to worry about parameters.

We can use the substitution model to investigate how this might go down. 

Consider this small program that pushes the first 10 Fibonacci numbers onto the stack.

    : nextfib ( add new fib num to top of stack ) over over + ;
    : 10fibs ( produce first 10 fibs ) 9 1 ?DO nextfib LOOP ;

    1 1
    10fib
    .s

What happens when `10fib` is called? 

    9   # Push 9 
    1   # Push 1
    
    ?DO # Get the two top-most values and run a loop from 1 to 9
        
    # All the calls to nextfib
    over over + 
    over over + 
    over over +
    over over +
    over over +
    over over +
    over over +
    over over +
    over over +

Let's say we wanted to alter this program to produce the first 50 values. Sure, we could alter the ?DO params in `main`, but we could also write a new word to take care of this.

    : 50fibs ( -- ) 5 1 ?DO 10fibs LOOP ;
 
