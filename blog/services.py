import uuid

import xlwt
from django.forms.models import model_to_dict
from django.http import HttpResponse


class ExportTO:
    def export_excel(self, qs):
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = f"attachment; filename={uuid.uuid4()}.xls"

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("django-try")

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.FAMILY_MODERN = True
        columns = list(model_to_dict(qs[0]).keys())

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows = list(qs.values_list())

        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        ws.save(response)
        return response
