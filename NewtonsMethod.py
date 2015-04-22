# NewtonsMethod.py
# by Kurt D kurtd5105@gmail.com
# Description: Uses sympy to calculate the derivative of the given equation and uses Newton's method
#              to find the x-intercept of the equation. It does not help in special cases, it only 
#              removes the necessity to perform Newton's method many times to find a solution.

from sympy import *
from decimal import *
import re

x = symbols('x')

class InvalidSyntaxError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# formatInput
# Description: Formats the user input to be compatible with sympify
def formatInput(unformattedInput):
    if unformattedInput.find("/0") != -1:
        raise InvalidSyntaxError(None)
    # Replaces nx with n*x and the caret exponentiation to python exponentiation
    return re.sub("(?<=\d)x", "*x", unformattedInput.replace('^', '**'))

# derive
# Description: Uses sympy to compute the derivative of the equation
def derive(equation):
    try:
        return diff(equation, x)
    except:
        raise InvalidSyntaxError(None)

# getContinue
# Description: Gets whether or not the user has another equation to enter
def getContinue():
    userInput = raw_input("Do you have another equation(y/n)? ")
    
    while True:
        if userInput.lower() == 'n':
            return False
        elif userInput.lower() == 'y':
            return True
        
        userInput = raw_input("Do you have another equation, please enter y or n: ")

# getGuess
# Description: Gets the user guess on what the intercept should be.
def getGuess():
    userInput = raw_input("What is your guess value? ")

    while True:
        try:
            userInput = float(userInput)
            return userInput
        except:
            userInput = raw_input("Please enter an integer guess value: ")

# newtonMethod
# Description: Performs Newton's method on an equation and using its derivative
def newtonMethod(guess, equation, derivative):
    result = 0
    count = 1

    # Round to 6 decimal places
    guess = Decimal(guess).quantize(Decimal('1.000000'))

    # Do newton's method, subbing in x into the sympy equations and rounding to 6 places
    try:
        # Try to calculate the first value and print it out
        result = Decimal(guess - Decimal( equation(guess)/derivative(guess) )).quantize(Decimal('1.000000'))
        print "x1 = {}".format(result)
    except TypeError:
        print "Invalid syntax, equation does not work with lambdas."
        return
    except ZeroDivisionError:
        print "Divide by 0 error."
        return
    except:
        if equation(guess) == 0 and derivative(guess) == 0:
            print "The result is x{} = {}.".format(count, "0.000000")
        else:
            print "An unknown error occurred."
        return
        
    # While the rounded result from last iteration isn't the same as the current result, do Newton's method
    while result != guess:
        # Stop calculating if there have been too many iterations
        if count > 1000:
            print "Centering on a solution failed."
            return

        # Attempt to do Newton's method, exceptions will be caught when thrown and the user will be notified
        try:
            guess = result
            # Calculate the result for the given iteration of Newton's method
            result = Decimal(guess - Decimal( equation(guess)/derivative(guess) )).quantize(Decimal('1.000000'))
            count += 1
        except TypeError:
            print "Invalid syntax."
            return
        except ZeroDivisionError:
            print "Divide by 0 error."
            return
        except:
            # Divide by zero error thrown for some reason as a generic error or not as ZeroDivisionError
            if equation(guess) == 0 and derivative(guess) == 0:
                print "The result is x{} = {}.".format(count, "0.000000")
            # At this point the error source is unknown but is still likely the user's fault
            else:
                print "An unknown error occurred."
            return
        print "x{} = {}".format(count, result)

    print "The result is x{} = {}.".format(count-1, result)

# strToLambda
# Description: Turns the sympy equation into a lambda with respect to x
def strToLambda(equation):
    return lambdify(x, sympify(equation), "math")

if __name__ == "__main__":
    question = True
    while question:
        userInput = raw_input("Enter an equation: ")

        # Attempt to format the user input, if an error occurs ask the user if they would like to try again
        try:
            formattedInput = formatInput(userInput)
            derivative = derive(formattedInput)
        except InvalidSyntaxError:
            print "Invalid syntax."
            question = getContinue()
            continue

        print "Derivative: {}".format(derivative)

        equation = strToLambda(formattedInput)
        derivative = strToLambda(derivative)

        guess = getGuess()
        
        newtonMethod(guess, equation, derivative)

        question = getContinue()