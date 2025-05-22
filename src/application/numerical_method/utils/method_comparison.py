import csv
import io

from src.application.numerical_method.services.bisection_service import BisectionService
from src.application.numerical_method.services.regula_falsi_service import RegulaFalsiService
from src.application.numerical_method.services.fixed_point_service import FixedPointService
from src.application.numerical_method.services.newton_raphson_service import NewtonService
from src.application.numerical_method.services.secant_service import SecantService
from src.application.numerical_method.services.multiple_roots_1_service import MultipleRoots1Service
from src.application.numerical_method.services.multiple_roots_2_service import MultipleRoots2Service

def run_all_methods(params):
    # Estandarizar parámetros para todos los métodos
    std_params = {
        "interval_a": params.get("interval_a", params.get("x0", 1)),
        "interval_b": params.get("interval_b", params.get("x0", 1) + 1),
        "x0": params.get("x0", params.get("interval_a", 1)),
        "tolerance": params.get("tolerance", 1e-5),
        "max_iterations": params.get("max_iterations", 100),
        "function_f": params.get("function_f"),
        "precision": params.get("precision", 1),
        "function_g": params.get("function_g", params.get("function_f")),
        "multiplicity": params.get("multiplicity", 1),
    }

    results = []

    # Bisección
    try:
        res = BisectionService().solve(
            std_params["interval_a"], std_params["interval_b"], std_params["tolerance"],
            std_params["max_iterations"], std_params["function_f"], std_params["precision"]
        )
        results.append({
            "Método": "Bisección",
            "Iteraciones": len(res["table"]),
            "Solución": res["root"],
            "¿Converge?": "Sí" if res["have_solution"] else "No"
        })
    except Exception:
        results.append({"Método": "Bisección", "Iteraciones": "-", "Solución": "-", "¿Converge?": "No"})

    # Regla Falsa
    try:
        res = RegulaFalsiService().solve(
            std_params["interval_a"], std_params["interval_b"], std_params["tolerance"],
            std_params["max_iterations"], std_params["function_f"], std_params["precision"]
        )
        results.append({
            "Método": "Regla Falsa",
            "Iteraciones": len(res["table"]),
            "Solución": res["root"],
            "¿Converge?": "Sí" if res["have_solution"] else "No"
        })
    except Exception:
        results.append({"Método": "Regla Falsa", "Iteraciones": "-", "Solución": "-", "¿Converge?": "No"})

    # Punto Fijo
    try:
        res = FixedPointService().solve(
            std_params["x0"], std_params["tolerance"], std_params["max_iterations"],
            std_params["precision"], std_params["function_f"], function_g=std_params["function_g"]
        )
        results.append({
            "Método": "Punto Fijo",
            "Iteraciones": len(res["table"]),
            "Solución": res.get("root", "-"),
            "¿Converge?": "Sí" if res.get("have_solution") else "No"
        })
    except Exception:
        results.append({"Método": "Punto Fijo", "Iteraciones": "-", "Solución": "-", "¿Converge?": "No"})

    # Newton-Raphson
    try:
        res = NewtonService().solve(
            std_params["x0"], std_params["tolerance"], std_params["max_iterations"],
            std_params["precision"], std_params["function_f"]
        )
        results.append({
            "Método": "Newton-Raphson",
            "Iteraciones": len(res["table"]),
            "Solución": res.get("root", "-"),
            "¿Converge?": "Sí" if res.get("have_solution") else "No"
        })
    except Exception:
        results.append({"Método": "Newton-Raphson", "Iteraciones": "-", "Solución": "-", "¿Converge?": "No"})

    # Secante
    try:
        res = SecantService().solve(
            std_params["interval_a"], std_params["tolerance"], std_params["max_iterations"],
            std_params["precision"], std_params["function_f"], interval_b=std_params["interval_b"]
        )
        results.append({
            "Método": "Secante",
            "Iteraciones": len(res["table"]),
            "Solución": res.get("root", "-"),
            "¿Converge?": "Sí" if res.get("have_solution") else "No"
        })
    except Exception:
        results.append({"Método": "Secante", "Iteraciones": "-", "Solución": "-", "¿Converge?": "No"})

    # Raíces Múltiples #1
    try:
        res = MultipleRoots1Service().solve(
            std_params["x0"], std_params["tolerance"], std_params["max_iterations"],
            std_params["precision"], std_params["function_f"], std_params["multiplicity"]
        )
        results.append({
            "Método": "Raíces Múltiples #1",
            "Iteraciones": len(res["table"]),
            "Solución": res.get("root", "-"),
            "¿Converge?": "Sí" if res.get("have_solution") else "No"
        })
    except Exception:
        results.append({"Método": "Raíces Múltiples #1", "Iteraciones": "-", "Solución": "-", "¿Converge?": "No"})

    # Raíces Múltiples #2
    try:
        res = MultipleRoots2Service().solve(
            std_params["x0"], std_params["tolerance"], std_params["max_iterations"],
            std_params["precision"], std_params["function_f"]
        )
        results.append({
            "Método": "Raíces Múltiples #2",
            "Iteraciones": len(res["table"]),
            "Solución": res.get("root", "-"),
            "¿Converge?": "Sí" if res.get("have_solution") else "No"
        })
    except Exception:
        results.append({"Método": "Raíces Múltiples #2", "Iteraciones": "-", "Solución": "-", "¿Converge?": "No"})

    # Filtrar los que convergen
    converged = [r for r in results if r.get('¿Converge?') == 'Sí' and isinstance(r.get('Iteraciones'), int)]
    # Encontrar el mínimo de iteraciones
    best = None
    if converged:
        min_iter = min(r['Iteraciones'] for r in converged)
        # Si hay empate, puedes marcar todos como "Sí" o solo el primero
        for r in results:
            if r.get('¿Converge?') == 'Sí' and r.get('Iteraciones') == min_iter:
                r['¿Mejor?'] = 'Sí'
            else:
                r['¿Mejor?'] = 'No'
    else:
        for r in results:
            r['¿Mejor?'] = 'No'

    # Generar CSV en memoria (sin la columna ¿Mejor?)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Método", "Iteraciones", "Solución", "¿Converge?"])
    writer.writeheader()
    for row in results:
        # Elimina la clave ¿Mejor? si existe
        row.pop("¿Mejor?", None)
        writer.writerow(row)
    return output.getvalue()
