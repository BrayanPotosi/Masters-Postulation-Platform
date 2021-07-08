import pandas as pd
import datetime
import math
import os

# Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.http import FileResponse

# Rest_framework
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework import serializers, status, authentication, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Utilities
from utils.dataframe_to_excel import Dataframe2Excel
from utils.constants import CONSTANTS
from utils.responses import Responses

# Reportlab
from arrow import utcnow, get
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, green, white
from reportlab.pdfgen import canvas
from io import BytesIO

# Models
from profiles.models import Profile
from .models import Score

# Serializers
from .serializers import CandidatesListSerializer, CandidateDetailSerializer, AdminDetailSerializer, ScoreSerializer
from profiles.serializers import UserSerializer

User = get_user_model()


class UpdateScore(UpdateAPIView):
    """Update the score of a candidate's profile"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            profile_obj = Profile.objects.get(pk=request.data.get('profile_id'))
            if instance.id == profile_obj.score.id:
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    response = serializer.save()
                    response = ScoreSerializer(response)
                    return Responses.make_response(data=response.data, authorization=True)
                    # return self.update(request, *args, **kwargs)
            raise Exception
        except:
            return Responses.make_response(error=True, message="Server error", 
                                           status=status.HTTP_500_INTERNAL_SERVER_ERROR, authorization=True)


class GetCandidateDetails(RetrieveUpdateAPIView):
    """Get the Profile detail of an Candidate user"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CandidateDetailSerializer
    lookup_field = 'user'
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        new_object = self.get_object()
        serializer = CandidateDetailSerializer(new_object)
        return Responses.make_response(data=serializer.data, authorization=True)


class GetAdminDetails(RetrieveUpdateAPIView):
    """Get the User detail of an Admin user"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AdminDetailSerializer
    queryset = User.objects.filter(is_staff=True)

    def get(self, request, *args, **kwargs):
        new_object = self.get_object()
        serializer = AdminDetailSerializer(new_object)
        return Responses.make_response(data=serializer.data, authorization=True)



class AdministratorsView(ListAPIView):
    """Get the list of administrators"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.filter(is_staff=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        total_administrators = queryset.count()
        data = {
            "count": total_administrators,
            "data": serializer.data
        }
        return Responses.make_response(data=data, authorization=True)



class PDFReport(object):

    def __init__(self, table_candidates, table_administrators, pdf_name):
        super(PDFReport, self).__init__()
        self.table_candidates = table_candidates
        self.table_administrators = table_administrators
        self.pdf_name = pdf_name

        self.styles = getSampleStyleSheet()

    @staticmethod
    def _footer(canvas, pdf_file_arg):
        canvas.saveState()
        styles = getSampleStyleSheet()

        align = ParagraphStyle(name="align", alignment=TA_RIGHT,
                                    parent=styles["Normal"])

        # Header
        header_name = Paragraph("", styles["Normal"])
        width, high = header_name.wrap(pdf_file_arg.width, pdf_file_arg.topMargin)
        header_name.drawOn(canvas, pdf_file_arg.leftMargin, 736)

        date = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
        report_date = date.replace("-", "de")

        header_date = Paragraph(report_date, align)
        width, high = header_date.wrap(pdf_file_arg.width, pdf_file_arg.topMargin)
        header_date.drawOn(canvas, pdf_file_arg.leftMargin, 736)

        # footer
        footer_down = Paragraph("", styles["Normal"])
        width, high = footer_down.wrap(pdf_file_arg.width, pdf_file_arg.bottomMargin)
        footer_down.drawOn(canvas, pdf_file_arg.leftMargin, 15 * mm + (0.2 * inch))

        # Format canvas
        canvas.restoreState()

    def convert_data(self, data):
        header_style = ParagraphStyle(name="header_style", alignment=TA_LEFT,
                                      fontSize=10, textColor=white,
                                      fontName="Helvetica-Bold",
                                      parent=self.styles["Normal"])

        normal_style = self.styles["Normal"]
        normal_style.alignment = TA_LEFT

        keys_name, names = zip(*[[k, n] for k, n in data['header']])

        header = [Paragraph(name, header_style) for name in names]
        new_data = [tuple(header)]

        for date in data['data']:
            new_data.append([Paragraph(str(date[keys_name]), normal_style) for keys_name in keys_name])

        return new_data

    def export(self):
        title_align = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=black,
                                          parent=self.styles["Heading1"])

        self.width, self.high = letter

        convert_data = self.convert_data(self.table_candidates)
        convert_data2 = self.convert_data(self.table_administrators)

        table_data = Table(convert_data, colWidths=(self.width - 100) / len(self.table_candidates['header']), hAlign="CENTER")
        table_data.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), green),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),
            ("BOX", (0, 0), (-1, -1), 0.25, black),
        ]))

        table_data2 = Table(convert_data2, colWidths=(self.width - 100) / len(self.table_administrators['header']), hAlign="CENTER")
        table_data2.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), green),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),
            ("BOX", (0, 0), (-1, -1), 0.25, black),
        ]))


        history = []
        history.append(Paragraph(self.table_candidates['title'], title_align))
        history.append(Spacer(1, 0.16 * inch))
        history.append(table_data)
        history.append(Spacer(2, 0.5 * inch))
        history.append(Paragraph(self.table_administrators['title'], title_align))
        history.append(Spacer(2, 0.5 * inch))
        history.append(table_data2)

        buffer = BytesIO()
        pdf_file_arg = SimpleDocTemplate(buffer, leftMargin=50, rightMargin=50, pagesize=letter,
                                         title='Report Up Program')

        pdf_file_arg.build(history, onFirstPage=self._footer,
                         onLaterPages=self._footer,
                         canvasmaker=PagesNumeration)
        buffer.seek(0)
        pdf: BytesIO = buffer
        return pdf


class PagesNumeration(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        pages_number = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(pages_number)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, pages_count):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Página {} de {}".format(self._pageNumber, pages_count))


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def candidates_view(request):
    ITEMS_PER_PAGE = 2
    items_per_page = ITEMS_PER_PAGE
    page_num = request.query_params.get('page')
    items_pp_query = request.query_params.get('ippage')
    sort_option = request.query_params.get('sort')
    format_export = request.query_params.get('2xlsx')
    order = 'total_score'

    if sort_option == 'desc':
        order = '-total_score'

    try:
        if items_pp_query is not None:
            items_per_page = items_pp_query

        profile_list = Profile.objects.order_by(order)
        total_candidates = profile_list.count()
        admin_list = User.objects.filter(is_staff=True)
        admin_count = admin_list.count()
        candidate_count = total_candidates
        total_users = total_candidates + admin_count

        # Getting ready the data to export to excel format, only if param '2xlsx' is equal to '1'.
        if format_export == '1':

            users_count = {
                'User type': ['Admin', 'Candidate'],
                'Count': [admin_count, candidate_count]
            }

            candidate_obj = {
                'username': [],
                'email': [],
                'Name': [],
                'Location': [],
                'score': [],
                'total_score': []
            }

            for candidate in profile_list:
                candidate_obj['username'].append(candidate.user.username)
                candidate_obj['email'].append(candidate.user.email)
                candidate_obj['Name'].append(candidate.user.first_name)
                candidate_obj['Location'].append(candidate.Address)
                candidate_obj['score'].append(candidate.score)
                candidate_obj['total_score'].append(candidate.total_score)

            admin_obj = {
                'email': [],
                'First_name': [],
                'Last_name': []
            }

            for admin in admin_list:
                admin_obj['email'].append(admin.email)
                admin_obj['First_name'].append(admin.first_name)
                admin_obj['Last_name'].append(admin.last_name)

            # profile_list_df = pd.DataFrame(profile_list.values())
            profile_list_df = pd.DataFrame.from_dict(candidate_obj)
            admin_list_df = pd.DataFrame.from_dict(admin_obj)
            count_users_df = pd.DataFrame.from_dict(users_count)

            data = {
                "candidate": profile_list_df,
                "admin": admin_list_df,
                "count": count_users_df,
            }

            return Dataframe2Excel.df2xlsx(data=data, name='Report_Up_Program')
            # profile_list_df.to_excel("output.xlsx")

        # Getting ready the data to export to PDF format, only if param '2xlsx' is equal to '2'.
        elif format_export == '2':

            buffer = BytesIO()

            tittle = "LISTADO DE CANDIDATOS"

            header_candidate = (
                ("ID", "ID"),
                ("Username", "Username"),
                ("Email", "Email"),
                ("Name", "Name"),
                ("Location", "Location"),
                ("Total_score", "Total_score"),
            )

            data_candidate = []

            for candidate in profile_list:
                this_candidate = {"ID": candidate.user.id,
                                  "Username": candidate.user.username,
                                  "Email": candidate.user.email,
                                  "Name": candidate.user.first_name,
                                  "Location": candidate.Address,
                                  "Total_score": candidate.total_score
                                  }
                data_candidate.append(this_candidate)

            tittle2 = "LISTADO DE ADMINISTRADORES"

            header_admin = (
                ("Email", "ID"),
                ("First Name", "Username"),
                ("Last Name", "Last Name"),
            )

            data_admin = []

            for admin in admin_list:
                this_admin = {"Email": admin.email,
                              "First Name": admin.first_name,
                              "Last Name": admin.last_name,
                              }
                data_admin.append(this_admin)

            pdf_name = "Report_Up_Program.pdf"

            table_candidates = {
                "header": header_candidate,
                "data": data_candidate,
                "title": tittle
            }

            table_administrators = {
                "header": header_admin,
                "data": data_admin,
                "title": tittle2
            }

            pdf_file = PDFReport(table_candidates, table_administrators, pdf_name).export()

            return FileResponse(pdf_file, as_attachment=True, filename='Report_Up_Program.pdf')

        paginator = Paginator(profile_list, items_per_page)
        try:
            profile_list = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            profile_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            profile_list = paginator.page(paginator.num_pages)
        data_serializer = CandidatesListSerializer(profile_list, many=True)
        total_pages = math.ceil(total_candidates / int(items_per_page))
        data = {
            "pages": total_pages,
            "count": total_candidates,
            "data": data_serializer.data
        }
        return Responses.make_response(data=data)
    except ValueError:
        return Responses.make_response(error=True,
                                       message=CONSTANTS.get('error_server'),
                                       status=status.HTTP_400_BAD_REQUEST, authorization=True)
