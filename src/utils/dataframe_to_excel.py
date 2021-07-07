# Pandas
import pandas as pd
import io

# Django
from django.http import HttpResponse

# Rest Framework
from rest_framework import status

# Utilities
from utils.responses import Responses
from utils.constants import CONSTANTS


class Dataframe2Excel:

    def df2xlsx(data, name="report"):
        try:
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            for key, df_value in data.items():
                df_value.to_excel(writer, sheet_name=f'Sheet_{key}')
            writer.save()
            output.seek(0)
            # xlsx_data = output.getvalue()
            file_name = f'{name}.xlsx'
            response = HttpResponse(output,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
        except:
            return Responses.make_response(error=True, message=CONSTANTS.get('error_2xlsx'),
                                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
