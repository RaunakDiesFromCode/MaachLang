import basic

while True:
    text = input("calc> ")

    if text.strip() == "": continue

    elif text == "tham" or text == "exit":
        break

    result, error = basic.run('<AjobFile>',text)

    if error:
        print(error.as_string())
    else:
        print(result)
