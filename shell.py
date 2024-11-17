import basic

while True:
    text = input("calc> ")
    result, error = basic.run('AjobFile',text)

    if error:
        print(error.as_string())
    else:
        print(result)
