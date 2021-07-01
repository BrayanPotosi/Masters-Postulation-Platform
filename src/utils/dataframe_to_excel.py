import io
import pandas as pd
from django.http import HttpResponse

class Dataframe2Excel():

    def df2xlsx(df, name="report"):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        output.seek(0)
        # xlsx_data = output.getvalue()
        file_name = f'{name}.xlsx'
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response