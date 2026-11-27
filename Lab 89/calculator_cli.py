#!/usr/bin/env python3
"""
Mathematical Calculator CLI - Demonstrates type conversion and validation
"""

import argparse
import math

def calculate_area(shape, **kwargs):
    """Calculate area based on shape and parameters"""
    if shape == 'rectangle':
        return kwargs['width'] * kwargs['height']
    elif shape == 'circle':
        return math.pi * (kwargs['radius'] ** 2)
    elif shape == 'triangle':
        return 0.5 * kwargs['base'] * kwargs['height']
    else:
        return 0

def positive_float(value):
    """Custom type function to ensure positive float values"""
    try:
        fvalue = float(value)
        if fvalue <= 0:
            raise argparse.ArgumentTypeError(f"'{value}' must be a positive number")
        return fvalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid number")

def main():
    parser = argparse.ArgumentParser(description='Mathematical Calculator CLI')
    
    # Add subcommands for different operations
    subparsers = parser.add_subparsers(dest='operation', help='Mathematical operations')
    
    # Basic arithmetic
    arithmetic_parser = subparsers.add_parser('arithmetic', help='Basic arithmetic operations')
    arithmetic_parser.add_argument('--add', nargs='+', type=float, help='Add numbers')
    arithmetic_parser.add_argument('--multiply', nargs='+', type=float, help='Multiply numbers')
    arithmetic_parser.add_argument('--power', nargs=2, type=float, help='Calculate power (base exponent)')
    
    # Area calculations
    area_parser = subparsers.add_parser('area', help='Calculate area of shapes')
    area_parser.add_argument('shape', choices=['rectangle', 'circle', 'triangle'])
    
    # Rectangle arguments
    area_parser.add_argument('--width', type=positive_float, help='Width (for rectangle)')
    area_parser.add_argument('--height', type=positive_float, help='Height (for rectangle/triangle)')
    
    # Circle arguments
    area_parser.add_argument('--radius', type=positive_float, help='Radius (for circle)')
    
    # Triangle arguments
    area_parser.add_argument('--base', type=positive_float, help='Base (for triangle)')
    
    # Statistics
    stats_parser = subparsers.add_parser('stats', help='Statistical calculations')
    stats_parser.add_argument('numbers', nargs='+', type=float, help='List of numbers')
    stats_parser.add_argument('--precision', type=int, default=2, help='Decimal precision')
    
    args = parser.parse_args()
    
    if not args.operation:
        parser.print_help()
        return
    
    print("\n" + "=" * 40)
    print("CALCULATOR RESULTS")
    print("=" * 40)
    
    if args.operation == 'arithmetic':
        if args.add:
            result = sum(args.add)
            print(f"Addition: {' + '.join(map(str, args.add))} = {result}")
        
        if args.multiply:
            result = 1
            for num in args.multiply:
                result *= num
            print(f"Multiplication: {' × '.join(map(str, args.multiply))} = {result}")
        
        if args.power:
            base, exponent = args.power
            result = base ** exponent
            print(f"Power: {base}^{exponent} = {result}")
    
    elif args.operation == 'area':
        if args.shape == 'rectangle':
            if not (args.width and args.height):
                print("Error: Rectangle requires --width and --height")
                return
            area = calculate_area('rectangle', width=args.width, height=args.height)
            print(f"Rectangle area (width={args.width}, height={args.height}): {area:.2f}")
        
        elif args.shape == 'circle':
            if not args.radius:
                print("Error: Circle requires --radius")
                return
            area = calculate_area('circle', radius=args.radius)
            print(f"Circle area (radius={args.radius}): {area:.2f}")
        
        elif args.shape == 'triangle':
            if not (args.base and args.height):
                print("Error: Triangle requires --base and --height")
                return
            area = calculate_area('triangle', base=args.base, height=args.height)
            print(f"Triangle area (base={args.base}, height={args.height}): {area:.2f}")
    
    elif args.operation == 'stats':
        numbers = args.numbers
        precision = args.precision
        
        mean = sum(numbers) / len(numbers)
        sorted_nums = sorted(numbers)
        median = sorted_nums[len(sorted_nums)//2] if len(sorted_nums) % 2 == 1 else \
                 (sorted_nums[len(sorted_nums)//2-1] + sorted_nums[len(sorted_nums)//2]) / 2
        
        print(f"Numbers: {numbers}")
        print(f"Count: {len(numbers)}")
        print(f"Sum: {sum(numbers):.{precision}f}")
        print(f"Mean: {mean:.{precision}f}")
        print(f"Median: {median:.{precision}f}")
        print(f"Min: {min(numbers):.{precision}f}")
        print(f"Max: {max(numbers):.{precision}f}")

if __name__ == '__main__':
    main()
