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

### Integer/Float Math ###
    
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

### (Joy-style) Combinators ###

| Combinator | Stack Result                              |
|------------|-------------------------------------------|
| i          | `[ 1 2 ] i => 1 2`                        |
| concat     | `[ 1 2 ] [ 3 4 ] concat => [ 1 2 3 4 ]`   |
| dip        | `[ 1 2 ] [ 3 4 ] dip => 3 4 [ 1 2 ]`      |
| cons       | `[ 1 2 ] [ 3 4 ] cons => [ [ 1 2 ] 3 4 ]` |
| unit       | `[ 1 2 3 ] unit => [ [ 1 2 3 ] ]`         |

(More on combinators [here](http://www.kevinalbrecht.com/code/joy-mirror/j06prg.html))

## Notes ##

[\*] Must be used with the context of a colon definition.


