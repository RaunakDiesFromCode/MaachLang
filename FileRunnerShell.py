import sys
import basic

# Ensure a file argument is provided
if len(sys.argv) != 2:
    print("Usage: python3 FileRunnerShell.py <filename.maach>")
    sys.exit(1)

filename = sys.argv[1]

print("MaachLang v1.0.0 ~ running", filename, "\n")


result, error = basic.run(
    filename, (f'Maach("{filename}")')
)  # Assuming basic.run() can use filename here.

if error:
    print(error.as_string())
elif result:
    if len(result.elements) == 1:
        print(repr(result.elements[0]))
    else:
        print(repr(result))
