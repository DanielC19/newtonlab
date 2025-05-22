from django.views import View
from django.http import HttpResponse
from src.application.numerical_method.utils.method_comparison import run_all_methods

class DownloadCSVReportView(View):
    def get(self, request, *args, **kwargs):
        # Recoge los parámetros de la URL (GET)
        params = {
            "interval_a": request.GET.get("interval_a"),
            "interval_b": request.GET.get("interval_b"),
            "x0": request.GET.get("x0"),
            "tolerance": request.GET.get("tolerance"),
            "max_iterations": request.GET.get("max_iterations"),
            "function_f": request.GET.get("function_f"),
            "function_g": request.GET.get("function_g"),
            "precision": request.GET.get("precision"),
            "multiplicity": request.GET.get("multiplicity"),
        }
        # Convierte a float/int donde corresponda
        for k in ["interval_a", "interval_b", "x0", "tolerance"]:
            if params[k] is not None:
                try:
                    params[k] = float(params[k])
                except Exception:
                    pass
        for k in ["max_iterations", "precision", "multiplicity"]:
            if params[k] is not None:
                try:
                    params[k] = int(params[k])
                except Exception:
                    pass
        # Elimina None
        params = {k: v for k, v in params.items() if v is not None}
        csv_content = run_all_methods(params)
        response = HttpResponse(csv_content, content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=comparacion_metodos.csv"
        return response
