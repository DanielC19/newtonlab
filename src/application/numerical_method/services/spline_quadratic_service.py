import numpy as np
from src.application.numerical_method.interfaces.interpolation_method import InterpolationMethod
from src.application.shared.utils.plot_spline import plot_spline_quadratic

class SplineQuadraticService(InterpolationMethod):
    def solve(self, x: list[float], y: list[float]) -> dict:
        n = len(x)
        if n < 3:
            return {
                "message_method": "Se necesitan al menos 3 puntos para calcular un spline cuadrático.",
                "is_successful": False,
                "have_solution": False,
                "tramos": [],
            }
        # Ordenar puntos por x
        points = sorted(zip(x, y), key=lambda p: p[0])
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        n = len(x)
        h = [x[i+1] - x[i] for i in range(n-1)]

        # Sistema para coeficientes a, b, c de cada tramo
        # S_i(x) = a_i + b_i*(x-x_i) + c_i*(x-x_i)^2
        a = [y[i] for i in range(n-1)]
        b = [0]*(n-1)
        c = [0]*(n-1)

        # Ecuaciones:
        # 1. S_i(x_{i+1}) = y_{i+1}
        # 2. S_i'(x_{i+1}) = S_{i+1}'(x_{i+1}) para i=0..n-3
        # 3. S_0''(x_0) = 0 (condición natural)

        # Construir sistema lineal
        A = np.zeros((2*(n-1), 2*(n-1)))
        rhs = np.zeros(2*(n-1))

        # Ecuaciones de paso por puntos
        for i in range(n-1):
            A[i, i] = h[i]
            A[i, n-1+i] = h[i]**2
            rhs[i] = y[i+1] - y[i]

        # Ecuaciones de derivadas iguales
        for i in range(n-2):
            A[n-1+i, i] = 1
            A[n-1+i, i+1] = -1
            A[n-1+i, n-1+i] = 2*h[i]
            A[n-1+i, n-1+i+1] = -0
            rhs[n-1+i] = 0

        # Condición natural: segunda derivada en x0 es 0
        # S_0''(x_0) = 2*c_0 = 0
        A[-1, n-1+0] = 2
        rhs[-1] = 0

        # Resolver sistema
        sol = np.linalg.solve(A, rhs)
        b = sol[:n-1]
        c = sol[n-1:]

        tramos = []
        for i in range(n-1):
            tramo = f"{a[i]:.4f} + {b[i]:.4f}*(x - {x[i]:.4f}) + {c[i]:.4f}*(x - {x[i]:.4f})^2"
            tramos.append(tramo)
        plot_spline_quadratic("Spline Cuadrático", list(zip(x, y)), x, y)
        return {
            "is_successful": True,
            "have_solution": True,
            "tramos": tramos,
        }

    def validate_input(self, x_input: str, y_input: str) -> str | list[tuple[float, float]]:
        max_points = 8
        x_list = [value.strip() for value in x_input.split(" ") if value.strip()]
        y_list = [value.strip() for value in y_input.split(" ") if value.strip()]
        if len(x_list) == 0 or len(y_list) == 0:
            return "Error: Las listas de 'x' y 'y' no pueden estar vacías."
        if len(x_list) != len(y_list):
            return "Error: Las listas de 'x' y 'y' deben tener la misma cantidad de elementos."
        try:
            x_values = [float(value) for value in x_list]
            y_values = [float(value) for value in y_list]
        except ValueError:
            return "Error: Todos los valores de 'x' y 'y' deben ser numéricos."
        if len(set(x_values)) != len(x_values):
            return "Error: Los valores de 'x' deben ser únicos."
        if len(x_values) > max_points:
            return f"Error: El número máximo de puntos es {max_points}."
        return [x_values, y_values]
