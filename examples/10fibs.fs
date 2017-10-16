: nextfib ( add new fib num to top of stack ) over over + ;
: 10fibs ( produce first 10 fibs ) 1 1 9 1 ?DO nextfib LOOP ;

10fibs 
