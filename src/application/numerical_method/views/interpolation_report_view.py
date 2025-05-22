import csv
import io
from django.http import HttpResponse
from django.views import View
from src.application.numerical_method.services.lagrange_service import LagrangeService
from src.application.numerical_method.services.vandermonde_service import VandermondeService
from src.application.numerical_method.services.newton_interpol_service import NewtonInterpolService
from src.application.numerical_method.services.spline_linear_service import SplineLinearService
from src.application.numerical_method.services.spline_cubic_service import SplineCubicService
from src.application.numerical_method.services.spline_quadratic_service import SplineQuadraticService

class InterpolationReportView(View):
    def post(self, request, *args, **kwargs):
        x_input = request.POST.get("x", "")
        y_input = request.POST.get("y", "")
        file_format = request.POST.get("file_format", "csv")

        # Ejecutar todos los métodos
        methods = [
            ("Lagrange", LagrangeService()),
            ("Vandermonde", VandermondeService()),
            ("Newton", NewtonInterpolService()),
            ("Spline Lineal", SplineLinearService()),
            ("Spline Cuadrático", SplineQuadraticService()),
            ("Spline Cúbico", SplineCubicService()),
        ]
        results = []
        for name, service in methods:
            valid = service.validate_input(x_input, y_input)
            if isinstance(valid, str):
                result = valid
            else:
                x, y = valid
                response = service.solve(x, y)
                if name in ["Spline Lineal", "Spline Cuadrático", "Spline Cúbico"]:
                    if response.get("is_successful"):
                        tramos = response.get("tramos", [])
                        result = "\n".join(tramos) if tramos else ""
                    else:
                        result = response.get("message_method", "")
                else:
                    result = response.get("polynomial") or response.get("message_method")
            results.append((name, result))

        if file_format == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Método de Interpolación", "Resultado"])
            writer.writerow(["Datos de entrada X", x_input])
            writer.writerow(["Datos de entrada Y", y_input])
            writer.writerow([])
            for name, result in results:
                writer.writerow([f"--- {name} ---", ""])
                for line in str(result).splitlines():
                    writer.writerow(["", line])
                writer.writerow([])
            response = HttpResponse(output.getvalue(), content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="informe_interpolacion.csv"'
            return response
        else:
            return HttpResponse("Formato PDF no implementado.", status=501)
