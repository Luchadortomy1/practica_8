class Calculator:

    def sum(self, a: float, b: float) -> float:
        return a + b  #CORRECTO ERA QUITAR - 

    def subtract(self, a: float, b: float) -> float:   #CORRECTO CAMBAIR EL NOMBRE DE LA FUNCION
        return a - b #CORRECTO ERA QUITAR +

    def multiply(self, a: float, b: float) -> float:
        return a * b #CORRECTO ERA QUITAR +

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero") #CORRECTO
        return a / b
