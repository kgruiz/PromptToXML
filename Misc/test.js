class Calculator {
    constructor() {
        this.result = 0;
    }

    Add(a, b) {
        this.result = a + b;
        return this.result;
    }

    Subtract(a, b) {
        this.result = a - b;
        return this.result;
    }

    Multiply(a, b) {
        this.result = a * b;
        return this.result;
    }

    Divide(a, b) {
        if (b === 0) {
            throw new Error('Division by zero is not allowed.');
        }
        this.result = a / b;
        return this.result;
    }

    Clear() {
        this.result = 0;
    }

    GetResult() {
        return this.result;
    }
}

class AdvancedCalculator extends Calculator {
    Power(base, exponent) {
        this.result = Math.pow(base, exponent);
        return this.result;
    }

    SquareRoot(number) {
        if (number < 0) {
            throw new Error('Square root of negative number is not allowed.');
        }
        this.result = Math.sqrt(number);
        return this.result;
    }

    Logarithm(number) {
        if (number <= 0) {
            throw new Error('Logarithm of non-positive number is not allowed.');
        }
        this.result = Math.log(number);
        return this.result;
    }
}

function main() {
    const calc = new AdvancedCalculator();
    console.log('Add: ', calc.Add(10, 5));
    console.log('Subtract: ', calc.Subtract(10, 5));
    console.log('Multiply: ', calc.Multiply(10, 5));
    console.log('Divide: ', calc.Divide(10, 5));
    console.log('Power: ', calc.Power(2, 3));
    console.log('SquareRoot: ', calc.SquareRoot(16));
    console.log('Logarithm: ', calc.Logarithm(10));
    calc.Clear();
    console.log('Result after clear: ', calc.GetResult());
}

main();