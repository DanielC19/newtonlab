import csv
from io import StringIO
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Importa los servicios de los métodos
from src.application.numerical_method.services.bisection_service import BisectionService
from src.application.numerical_method.services.regula_falsi_service import RegulaFalsiService
from src.application.numerical_method.services.fixed_point_service import FixedPointService
from src.application.numerical_method.services.newton_raphson_service import NewtonService
from src.application.numerical_method.services.secant_service import SecantService
from src.application.numerical_method.services.multiple_roots_1_service import MultipleRoots1Service
from src.application.numerical_method.services.multiple_roots_2_service import MultipleRoots2Service

@method_decorator(csrf_exempt, name='dispatch')
def csv_report_view(request):
    if request.method == "POST":
        # Estandariza los parámetros de entrada
        interval_a = float(request.POST.get("interval_a", 1))
        interval_b = float(request.POST.get("interval_b", 2))
        x0 = float(request.POST.get("x0", interval_a))
        tolerance = float(request.POST.get("tolerance", 0.001))
        max_iterations = int(request.POST.get("max_iterations", 100))
        function_f = request.POST.get("function_f", "x**2-2")
        precision = int(request.POST.get("precision", 1))
        multiplicity = int(request.POST.get("multiplicity", 2))
        function_g = request.POST.get("function_g", "x")

        # Ejecuta cada método y recopila resultados
        results = []

        # Bisección
        bisection = BisectionService().solve(interval_a, interval_b, tolerance, max_iterations, function_f, precision)
        results.append({
            "Método": "Bisección",
            "Iteraciones": len(bisection["table"]),
            "Raíz": bisection.get("root", ""),
            "Error final": list(bisection["table"].values())[-1]["error"] if bisection["table"] else "",
            "¿Éxito?": bisection.get("have_solution", False),
        })

        # Regla Falsa
        regula = RegulaFalsiService().solve(interval_a, interval_b, tolerance, max_iterations, function_f, precision)
        results.append({
            "Método": "Regla Falsa",
            "Iteraciones": len(regula["table"]),
            "Raíz": regula.get("root", ""),
            "Error final": list(regula["table"].values())[-1]["error"] if regula["table"] else "",
            "¿Éxito?": regula.get("have_solution", False),
        })

        # Punto Fijo
        fixed = FixedPointService().solve(x0, tolerance, max_iterations, precision, function_f, function_g=function_g)
        results.append({
            "Método": "Punto Fijo",
            "Iteraciones": len(fixed["table"]),
            "Raíz": fixed.get("root", ""),
            "Error final": list(fixed["table"].values())[-1]["error"] if fixed["table"] else "",
            "¿Éxito?": fixed.get("have_solution", False),
        })

        # Newton-Raphson
        newton = NewtonService().solve(x0, tolerance, max_iterations, precision, function_f)
        results.append({
            "Método": "Newton-Raphson",
            "Iteraciones": len(newton["table"]),
            "Raíz": newton.get("root", ""),
            "Error final": list(newton["table"].values())[-1]["error"] if newton["table"] else "",
            "¿Éxito?": newton.get("have_solution", False),
        })

        # Secante
        secant = SecantService().solve(interval_a, interval_b, tolerance, max_iterations, function_f, precision)
        results.append({
            "Método": "Secante",
            "Iteraciones": len(secant["table"]),
            "Raíz": secant.get("root", ""),
            "Error final": list(secant["table"].values())[-1]["error"] if secant["table"] else "",
            "¿Éxito?": secant.get("have_solution", False),
        })

        # Raíces Múltiples #1
        multiple1 = MultipleRoots1Service().solve(x0, tolerance, max_iterations, precision, function_f, multiplicity)
        results.append({
            "Método": "Raíces Múltiples #1",
            "Iteraciones": len(multiple1["table"]),
            "Raíz": multiple1.get("root", ""),
            "Error final": list(multiple1["table"].values())[-1]["error"] if multiple1["table"] else "",
            "¿Éxito?": multiple1.get("have_solution", False),
        })

        # Raíces Múltiples #2
        multiple2 = MultipleRoots2Service().solve(x0, tolerance, max_iterations, precision, function_f)
        results.append({
            "Método": "Raíces Múltiples #2",
            "Iteraciones": len(multiple2["table"]),
            "Raíz": multiple2.get("root", ""),
            "Error final": list(multiple2["table"].values())[-1]["error"] if multiple2["table"] else "",
            "¿Éxito?": multiple2.get("have_solution", False),
        })

        # Selecciona el mejor método (menor error final y éxito)
        best = min(
            (r for r in results if r["¿Éxito?"] and r["Error final"] not in ("", None)),
            key=lambda r: abs(r["Error final"]),
            default=None,
        )
        for r in results:
            r["¿Mejor método?"] = "Sí" if best and r["Método"] == best["Método"] else "No"

        # Genera el CSV
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=comparacion_metodos.csv"
        return response
    return HttpResponse("Método no permitido", status=405)
