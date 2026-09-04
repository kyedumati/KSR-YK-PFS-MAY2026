class InvalidPinError(Exception):
    """ Invalid pin """
    pass

correct_pin = 1234
def is_pin_valid(entered_pin):
    if entered_pin == correct_pin:
        return True
    else:
        raise InvalidPinError("Invalid pin, please enter correct pin number")

attempt = 0
for i in range(3):
    attempt +=1
    try:
        user_pin = int(input("Enter your pin number: "))
        if is_pin_valid(user_pin):
            print("Pin is valid, please proceeed with the withdraw")
            break
    except InvalidPinError as e:
        print(e)
        if attempt <=3:
           continue
    except ValueError as e:
        print(e)
        break
    except Exception as e:
        print(e)
        break
    except: # this can handle any exception in the python world, even exception cant handle
        print("someoone cancelled the program in between due to techinical failure")




