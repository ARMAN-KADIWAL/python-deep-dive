# Messy Calculator - Before Refactoring
import math

def calc(x, y, z, op):
    if op == "add":
        result = x + y
        if z != 0:
            result = result + z
        return result
    elif op == "subtract" or op == "sub":
        result = x - y
        if z != 0:
            result = result - z
        return result
    elif op == "multiply" or op == "mul":
        result = x * y
        if z != 0:
            result = result * z
        return result
    elif op == "divide" or op == "div":
        if y == 0:
            return "Error: Division by zero"
        result = x / y
        if z != 0:
            if z == 0:
                return "Error: Division by zero"
            result = result / z
        return result
    elif op == "power":
        result = x ** y
        if z != 0:
            result = result ** z
        return result
    elif op == "sqrt":
        if x < 0:
            return "Error: Cannot calculate square root of negative number"
        result = math.sqrt(x)
        return result
    else:
        return "Error: Unknown operation"

def process_data():
    data = [10, 20, 30, 40, 50]
    total = 0
    for i in range(len(data)):
        total = total + data[i]
    avg = total / len(data)
    
    max_val = data[0]
    for i in range(len(data)):
        if data[i] > max_val:
            max_val = data[i]
    
    min_val = data[0]
    for i in range(len(data)):
        if data[i] < min_val:
            min_val = data[i]
    
    print("Total:", total)
    print("Average:", avg)
    print("Maximum:", max_val)
    print("Minimum:", min_val)

def main():
    print("Calculator Results:")
    print(calc(10, 5, 2, "add"))
    print(calc(10, 5, 2, "multiply"))
    print(calc(16, 0, 0, "sqrt"))
    print(calc(10, 0, 0, "divide"))
    
    print("\nData Processing Results:")
    process_data()

if __name__ == "__main__":
    main()
