: range ( Produce a list of ints by to, from *exclusive* ) [ ] concat concat [ ] swap i ?DO i concat LOOP ;
: range_c ( Produce a list of ints by [ to from ] *exclusive* ) [ ] swap i ?DO i concat LOOP ;
: square ( Multiply a number by itself ) dup * ;
