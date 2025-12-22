# i13c-lang

A basic compiler for i13c language.

## development

You need to work only with the Makefile.
- `make deps` will install all dependencies
- `make test` will check if all tests are green
- `make lint` will reformat the code
- `make asm` will show the disassembled code

If you installed deps you can use i13c script:
- `i13c lex file.i13c` will tokenize the file
- `i13c ast file.i13c` will produce AST of the file
- `i13c low file.i13c` will produce IR of the file
- `i13c elf file.i13c` will generate a.out
