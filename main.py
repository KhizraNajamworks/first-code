print("WELCOME TO YOUR CALCULATOR ")
while True:
    print("1. Add(+)")
    print("2. subtract(-)")
    print("3. multiply(*)")
    print("4. divide(/)")
    print("5. EXIT PROGRAM")

    choice = input("select your operation(1-5)")
    if choice == '5':
        print("program is exited.THANKYOU FOR USING")
        break
    if choice in ('1', '2', '3', '4'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == '1':
            result = num1 + num2
            print(f"RESULT{num1} + {num2} = {result}")

        elif choice == '2':
            result = num1 - num2
            print(f"RESULT{num1} - {num2}={result}")

        elif choice == '3':
            result = num1 * num2
            print(f"RESULT{num1} * {num2}={result}")

        elif choice == '4':
            if num2==0:
                print("dude you cannot divide by zero cause yk the result is gonna be jus zero")
            else:
                result = num1 / num2
                print(f"RESULT{num1} / {num2}={result}")
        else:
            print("invalid input dude . pls enter stuff from 1-5")