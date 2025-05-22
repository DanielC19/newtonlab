from django.http import HttpResponse
from django.views import View
from src.application.numerical_method.utils.method_comparison import compare_matrix_methods_report

class MatrixComparisonReportView(View):
    def get(self, request):
        matrix_a_raw = request.GET.get("matrix_a", "")
        vector_b_raw = request.GET.get("vector_b", "")
        initial_guess_raw = request.GET.get("initial_guess", "")
        tolerance = float(request.GET.get("tolerance"))
        max_iterations = int(request.GET.get("max_iterations"))
        relaxation_factor = float(request.GET.get("relaxation_factor", 1.2))
        precision_type = request.GET.get("precision_type", "decimales_correctos")
        matrix_size = int(request.GET.get("matrix_size", 2))

        A = [
            [float(num) for num in row.strip().split()]
            for row in matrix_a_raw.split(";") if row.strip()
        ]
        b = [float(num) for num in vector_b_raw.strip().split()]
        x0 = [float(num) for num in initial_guess_raw.strip().split()]

        csv_content, _ = compare_matrix_methods_report(
            A, b, x0, tolerance, max_iterations, relaxation_factor, precision_type
        )

        response = HttpResponse(csv_content, content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=comparacion_metodos.csv"
        return response
