import basic

print("MaachLang v1.0.0 ~ running <ShellFile>\nType 'tham' to exit\n")
while True:
    text = input("🐟> ")

    if text.strip() == "":
        continue

    elif text == "tham" or text == "exit":
        print("Goodbye!\n-\n©2024 Raunak")
        break

    result, error = basic.run("<ShellFile>", text)

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
