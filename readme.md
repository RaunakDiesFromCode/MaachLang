#### (the language is still under development.)

<table align="center">
<td align="center">
  <p style="font:bold">
    <h1 style="text-align: center; ">
    MaachLang
    </h1>

  <h4 style="text-align: center; ">
    MaachLang is a small Bengali-inspired programming language written in Python.
  </h4>

  </p>
</td>
</table>

## Overview

MaachLang is implemented as a simple interpreter. Source code is read as text, tokenized, parsed into an abstract syntax tree, and then executed by the runtime.

The language currently supports variables, numbers, strings, lists, functions, conditionals, loops, and a small built-in standard library.

## How It Works

The public runtime entrypoint is `maach.run(fn, text)`, exposed through the `maach` package.

1. The lexer converts raw source text into tokens.
2. The parser turns those tokens into an abstract syntax tree.
3. The interpreter walks the tree and evaluates the program.
4. Built-in values and functions are loaded into the global symbol table before execution starts.

This is why the shell runners are thin wrappers around the shared interpreter logic.

For a deeper engineering-level walkthrough of the runtime, see [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md).

## How To Run Code

### Run A File

Use the file runner to execute a MaachLang source file:

```bash
python3 FileRunnerShell.py examples/helloworld.maach
```

You can also use the convenience script:

```bash
bash maach.sh examples/helloworld.maach
```

### Start The Interactive Shell

Run the REPL when you want to type code line by line:

```bash
python3 shell.py
```

Type `tham` or `exit` to leave the shell.

### Use The Interpreter From Python

If you want to embed MaachLang in another Python script:

```python
from maach import run

result, error = run("<stdin>", 'bol("Hello World")')
```

## Language Reference

The full list of keywords and built-in functions lives in `guide.md`.

Some of the currently available built-ins are:

- `bol` for printing
- `jigesh_kor` for input
- `sonkha_jigesh_kor` for integer input
- `laga` / `byass_ber_kor` / `atka` for list operations
- `floor`, `ceil`, `round`, `abs`, `sqroot`, `sin`, `cos`, `tan`, `pow` for math helpers

## Example Programs

```python
# Hello world
bol("Hello World")
```

```python
# A basic for loop
ghorao i = 0 theke 5 tarpor
  bol("loop!")
byass
```

```python
# A simple function
kaaj naam(name);
  bol("Hello " + name);
byass;

bol("Name: ")
chol n = jigesh_kor()
naam(n)
```

```python
# Recursive factorial
kaaj fact(n);
  jodi n<=1 tarpor de(1) nahole de(n * fact(n-1))
byass;

bol(fact(5))
```

More runnable examples are available in the `examples/` directory:

- `examples/conditionals.maach` (if/else and boolean logic)
- `examples/while_countdown.maach` (while loop)
- `examples/list_ops.maach` (list values and list helpers)
- `examples/math_showcase.maach` (math built-ins)
- `examples/script_runner.maach` (running one script from another)

## Installation

A formal installation flow is not published yet. For now, clone the repository and run the scripts with Python 3.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
