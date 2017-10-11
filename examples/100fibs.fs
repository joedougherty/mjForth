: nextfib ( add new fib num to top of stack ) over over + ;
: 100fibs ( produce first 100 fibs ) 1 1 999 1 ?DO nextfib LOOP ;

100fibs 
.
