## mjForth ##

An experimental Forth interpreter. Seeks to emulate a subset of [gforth](https://www.gnu.org/software/gforth/).

### Stack Manipulations ###

* drop
* swap 
* dup
* over
* rot
* nip 
* tuck

### Integer Math ###
    
* \+
* \-
* \*
* /
* mod
* 0=
* 0>
* 1-
* 1+
* =
* &lt;
* &gt;
* negate
* abs
* min
* max

### Colon Definitions ###

Define words!

` : newword ( describe the stack effect here ) dup over swap ; `

Use `see` to view the definition of a word.

### Booleans ###
    
* `true`
* `false`

### Conditional Branching [\*] ###

`IF ... ENDIF`

`IF ... ELSE ... ENDIF`

### Counted (?DO) Loops [\*] ###

`10 1 ?DO i ... LOOP`

### While Loops ###

`BEGIN ... WHILE ... REPEAT`

### Recursion ###

`: fac_rec ( n -- n! ) dup 0> IF dup 1- fac_rec * ELSE drop 1 ENDIF ;`

### Global Variables (Memory) ###

Declare a variable.

`variable v`

Set the value.

`1000 v !`

Get its value and push on top of the data stack.

`v @`

## Notes ##

[\*] Must be used with the context of a colon definition.
