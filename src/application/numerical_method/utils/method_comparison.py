import csv
import io

from src.application.numerical_method.services.bisection_service import BisectionService
from src.application.numerical_method.services.regula_falsi_service import RegulaFalsiService
from src.application.numerical_method.services.fixed_point_service import FixedPointService
from src.application.numerical_method.services.newton_raphson_service import NewtonService
from src.application.numerical_method.services.secant_service import SecantService
from src.application.numerical_method.services.multiple_roots_1_service import MultipleRoots1Service
from src.application.numerical_method.services.multiple_roots_2_service import MultipleRoots2Service
from src.application.numerical_method.services.jacobi_service import JacobiService
from src.application.numerical_method.services.gauss_seidel_service import GaussSeidelService
from src.application.numerical_method.services.sor_service import SORService

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

    # Filtrar solo los métodos convergentes y tienen solución numérica válida
    converged = [
        r for r in results
        if r.get('¿Converge?', r.get('¿Éxito?', False)) in ('Sí', True)
        and r.get('Solución', r.get('Raíz', None)) not in ("-", "", None)
    ]

    # Si hay al menos dos métodos convergentes, buscar los más parecidos
    best_indexes = []
    if len(converged) >= 2:
        # Extraer soluciones numéricas
        def parse_solution(sol):
            # Puede ser lista, float, o string
            if isinstance(sol, list):
                return [float(x) for x in sol]
            try:
                return [float(sol)]
            except Exception:
                # Intentar parsear string tipo "[1.0, 2.0]"
                try:
                    import ast
                    val = ast.literal_eval(sol)
                    if isinstance(val, (list, tuple)):
                        return [float(x) for x in val]
                    return [float(val)]
                except Exception:
                    return []
        parsed = [(i, parse_solution(r.get('Solución', r.get('Raíz', None)))) for i, r in enumerate(converged)]
        # Calcular distancia euclidiana entre todas las combinaciones
        import itertools
        min_dist = float('inf')
        best_pair = None
        for (i1, s1), (i2, s2) in itertools.combinations(parsed, 2):
            if len(s1) == len(s2) and len(s1) > 0:
                dist = sum((a - b) ** 2 for a, b in zip(s1, s2)) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    best_pair = (i1, i2)
        # Seleccionar los dos más parecidos
        if best_pair:
            best_indexes = list(best_pair)
    elif len(converged) == 1:
        best_indexes = [0]

    # De los más parecidos, elegir el de menos iteraciones
    if best_indexes:
        min_iter = float('inf')
        best_idx = None
        for idx in best_indexes:
            iteraciones = converged[idx].get('Iteraciones', float('inf'))
            try:
                iteraciones = int(iteraciones)
            except Exception:
                iteraciones = float('inf')
            if iteraciones < min_iter:
                min_iter = iteraciones
                best_idx = idx
        # Marcar el mejor método
        for i, r in enumerate(results):
            r['¿Mejor?'] = "Sí" if r in converged and converged.index(r) == best_idx else "No"
    else:
        for r in results:
            r['¿Mejor?'] = "No"

    # Generar CSV en memoria (incluyendo columna ¿Mejor?)
    output = io.StringIO()
    # Detectar campos automáticamente
    fieldnames = list(results[0].keys()) if results else []
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)
    return output.getvalue()

def compare_matrix_methods_report(A, b, x0, tolerance, max_iterations, relaxation_factor=1.2, precision_type="decimales_correctos"):
    """
    Compara Jacobi, Gauss-Seidel y SOR para el mismo sistema.
    Devuelve el CSV y los datos tabulares.
    """
    results = []

    # Jacobi
    try:
        jacobi_res = JacobiService().solve(
            A, b, x0, tolerance, max_iterations, precision_type
        )
        have_solution = jacobi_res.get("have_solution")
        table = jacobi_res.get("table", {})
        last_iter = table[max(table)] if table else {}
        error_value = last_iter.get("Error", "-") if have_solution else "-"
        results.append({
            "Método": "Jacobi",
            "Iteraciones": len(table),
            "Solución": jacobi_res.get("solution", []) if have_solution else "-",
            "Error": error_value,
            "¿Converge?": "Sí" if have_solution else "No"
        })
    except Exception:
        results.append({"Método": "Jacobi", "Iteraciones": "-", "Solución": "-", "Error": "-", "¿Converge?": "No"})

    # Gauss-Seidel
    try:
        gs_precision = 1 if precision_type == "decimales_correctos" else 0
        gs_res = GaussSeidelService().solve(
            A, b, x0, tolerance, max_iterations, gs_precision
        )
        have_solution = gs_res.get("have_solution")
        table = gs_res.get("table", {})
        last_iter = table[max(table)] if table else {}
        error_value = last_iter.get("Error", "-") if have_solution else "-"
        results.append({
            "Método": "Gauss-Seidel",
            "Iteraciones": len(table),
            "Solución": gs_res.get("solution", []) if have_solution else "-",
            "Error": error_value,
            "¿Converge?": "Sí" if have_solution else "No"
        })
    except Exception:
        results.append({"Método": "Gauss-Seidel", "Iteraciones": "-", "Solución": "-", "Error": "-", "¿Converge?": "No"})

    # SOR
    try:
        sor_precision = 1 if precision_type == "decimales_correctos" else 0
        sor_res = SORService().solve(
            A, b, x0, tolerance, max_iterations, relaxation_factor, sor_precision
        )
        have_solution = sor_res.get("have_solution")
        table = sor_res.get("table", {})
        last_iter = table[max(table)] if table else {}
        error_value = last_iter.get("Error", "-") if have_solution else "-"
        results.append({
            "Método": "SOR",
            "Iteraciones": len(table),
            "Solución": sor_res.get("solution", []) if have_solution else "-",
            "Error": error_value,
            "¿Converge?": "Sí" if have_solution else "No"
        })
    except Exception:
        results.append({"Método": "SOR", "Iteraciones": "-", "Solución": "-", "Error": "-", "¿Converge?": "No"})

    # Selección del mejor método: compara soluciones, elige los más parecidos y de esos el de menor error final (si empate, menor iteraciones)
    converged = [r for r in results if r.get("¿Converge?") == "Sí" and r.get("Solución") not in ("-", "", None)]
    best_indexes = []
    if len(converged) >= 2:
        # Parsear soluciones a listas de floats
        def parse_solution(sol):
            if isinstance(sol, list):
                return [float(x) for x in sol]
            try:
                return [float(sol)]
            except Exception:
                try:
                    import ast
                    val = ast.literal_eval(sol)
                    if isinstance(val, (list, tuple)):
                        return [float(x) for x in val]
                    return [float(val)]
                except Exception:
                    return []
        parsed = [(i, parse_solution(r.get("Solución"))) for i, r in enumerate(converged)]
        import itertools
        min_dist = float("inf")
        best_pair = None
        for (i1, s1), (i2, s2) in itertools.combinations(parsed, 2):
            if len(s1) == len(s2) and len(s1) > 0:
                dist = sum((a - b) ** 2 for a, b in zip(s1, s2)) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    best_pair = (i1, i2)
        if best_pair:
            best_indexes = list(best_pair)
    elif len(converged) == 1:
        best_indexes = [0]

    # De los más parecidos, elegir el de menor error final (si empate, menor iteraciones)
    if best_indexes:
        min_error = float("inf")
        best_idx = None
        for idx in best_indexes:
            r = converged[idx]
            try:
                error = float(r.get("Error", float("inf")))
            except Exception:
                error = float("inf")
            if error < min_error:
                min_error = error
                best_idx = idx
        # Si hay empate en error, elegir menor iteraciones
        if best_idx is not None:
            bests = [idx for idx in best_indexes if
                     abs(float(converged[idx].get("Error", float("inf"))) - min_error) < 1e-12]
            if len(bests) > 1:
                min_iter = min(int(converged[idx].get("Iteraciones", float("inf"))) for idx in bests)
                best_idx = [idx for idx in bests if int(converged[idx].get("Iteraciones", float("inf"))) == min_iter][0]
            best = converged[best_idx]
            for r in results:
                r["¿Mejor?"] = "Sí" if r is best else "No"
        else:
            for r in results:
                r["¿Mejor?"] = "No"
    else:
        for r in results:
            r["¿Mejor?"] = "No"

    # Generar CSV en memoria
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Método", "Iteraciones", "Solución", "Error", "¿Converge?", "¿Mejor?"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)
    csv_content = output.getvalue()

    return csv_content, results
