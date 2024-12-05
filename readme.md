#### (the language is still under development.)

<table align="center">
<td align="center">
  <p style="font:bold">
    <h1 style="text-align: center; ">
    MaachLang
    </h1>

  <h4 style="text-align: center; ">
    MaachLang is simple 'bengali' programming language made with python.
  </h4>
  
  </p>
</td>
</table>

## Installation

A clear installation method will come soon.

## Keywords & Functions

All keywords and functions are present in `guide.md`

## Example Program

```python
  # the below code prints hello world to the screen
  bol("Hello World")
```

```python
  # implementation of a basic for loop

  ghorao i = 0 theke 5 tarpor
    bol("loop!")
  byass
```

```python
  # basic functions
  
  kaaj naam(name);
    bol("Hello " + name);
  byass;
  
  bol("Name: ")
  chol n = jigesh_kor()
  naam(n)
```

```python
  # basic recursion example using factorial
  
  kaaj fact(n);
    jodi n<=1 tarpor de(1) nahole de(n * fact(n-1))
  byass;
  
  bol(fact(5))
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
