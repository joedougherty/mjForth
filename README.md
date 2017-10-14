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
* 1-
* 1+
* &lt;
* &gt;

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

### Global variables (Memory) ###

Declare a variable.

`variable v`

Set the value.

`1000 v !`

Get its value and push on top of the data stack.

`v @`
