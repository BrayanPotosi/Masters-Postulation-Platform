import math
import pandas as pd 

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import serializers, status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, UpdateAPIView

from profiles.models import Profile
from .serializers import CandidatesListSerializer, CandidateDetailSerializer, AdminDetailSerializer, ScoreSerializer
from profiles.serializers import UserSerializer
from utils.responses import Responses
from .models import Score

from utils.constants import CONSTANTS
from utils.dataframe_to_excel import Dataframe2Excel

# pdf utils
import datetime
import os
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


User = get_user_model()

"""Update the score of a candidate's profile"""
class UpdateScore(UpdateAPIView):
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
                    return Responses.make_response(data=response.data)
                    # return self.update(request, *args, **kwargs)
            raise Exception
        except:
            return Responses.make_response(error=True, message="Server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""Get the Profile detail of an Candidate user"""
class GetCandidateDetails(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = CandidateDetailSerializer
    lookup_field = 'user'
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CandidateDetailSerializer(obj)
        return Responses.make_response(data=serializer.data)
        

"""Get the User detail of an Admin user"""
class GetAdminDetails(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = AdminDetailSerializer
    queryset = User.objects.filter(is_staff=True)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = AdminDetailSerializer(obj)
        return Responses.make_response(data=serializer.data)


class AdministratorsView(ListAPIView):
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
        return Responses.make_response(data=data)


@api_view(['GET'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def candidates_view(request):
    ITEMS_PER_PAGE = 2
    items_per_page = ITEMS_PER_PAGE
    page_num = request.query_params.get('page')    
    items_pp_query = request.query_params.get('ippage')
    sort_option = request.query_params.get('sort')
    export_excel = request.query_params.get('2xlsx')

    order = 'total_score'
    if sort_option == 'desc':
        order = '-total_score'
        
    try:
        if items_pp_query is not None:
            items_per_page = items_pp_query

        profile_list = Profile.objects.order_by(order)
        total_candidates = profile_list.count()

        """Getting ready the data to export to excel format, only if 
            param '2xlsx' is equal to '1'. """
        if export_excel=='1':

            admin_list = User.objects.filter(is_staff=True)
            admin_count = admin_list.count()
            candidate_count = total_candidates

            users_count = {
                'User type': ['Admin', 'Candidate'],
                'Count':[admin_count, candidate_count]
            }

            candidate_obj = {
                'username':[],
                'email':[],
                'Name':[],
                'Location':[],
                'score':[],
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
                'email':[],
                'First_name': [],
                'Last_name':[]
            }
            for admin  in admin_list:
                admin_obj['email'].append(admin.email)
                admin_obj['First_name'].append(admin.first_name)
                admin_obj['Last_name'].append(admin.last_name)

            # profile_list_df = pd.DataFrame(profile_list.values())
            profile_list_df = pd.DataFrame.from_dict(candidate_obj)
            admin_list_df = pd.DataFrame.from_dict(admin_obj)
            count_users_df = pd.DataFrame.from_dict(users_count)

            data = {
                "candidate":profile_list_df,
                "admin": admin_list_df,
                "count":count_users_df,
            }
            return Dataframe2Excel.df2xlsx(data=data, name='Report_Up_Program')
            # profile_list_df.to_excel("output.xlsx")

        elif export_excel == '2':

            current_date = datetime.date.today().strftime('%d/%m/%Y')
            order = request.query_params.get('order')

            candidates = User.objects.filter(is_superuser=False)
            administrators = User.objects.filter(is_superuser=True)
            total_candidates = len(candidates)
            total_administrators = len(administrators)
            total_users = total_candidates + total_administrators

            buffer = BytesIO()

            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer, pagesize=A4)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.

            p.setLineWidth(.2)
            p.setFont('Helvetica', 22)
            p.drawString(30, 750, 'PPM')

            p.setFont('Helvetica', 12)
            p.drawString(30, 735, 'Report')

            p.setFont('Helvetica-Bold', 12)
            p.drawString(480, 750, current_date)
            p.line(460, 747, 560, 747)

            # Candidates_table
            candidates_table = [
                {"Id": '1', 'first_name': 'Nombre', 'last_name': 'Apellido'}
            ]

            # Table header
            styles = getSampleStyleSheet()
            styleBH = styles['Normal']
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 10

            number = Paragraph('''Id''', styleBH)
            first_name = Paragraph('''Nombre''', styleBH)
            last_name = Paragraph('''Apellido''', styleBH)

            data = []
            data.append([number, first_name, last_name])

            # table
            styleN = styles['BodyText']
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7

            high = 650

            for candidate in candidates:
                print('///////////////////////////////////////////////////////////', candidate)
                this_candidate = [candidate['id'], candidate['first_name'], candidate['last_name']]
                data.append(this_candidate)
                high = high - 18

            # table size
            width, height = A4
            table = Table(data, colWidths=[1.9 * cm, 9.5 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm])
            table.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ]))

            # pdf size

            table.wrapOn(p, width, height)
            table.drawOn(p, 30, high)

            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()

            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='Report_Up_Program.pdf')

        paginator = Paginator(profile_list,items_per_page)
        try:
            profile_list = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            profile_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            profile_list = paginator.page(paginator.num_pages)
        data_serializer = CandidatesListSerializer(profile_list, many=True)
        total_pages = math.ceil(total_candidates/int(items_per_page))
        data = {
                "pages":total_pages,   
                "count": total_candidates,
                "data": data_serializer.data
                }
        return Responses.make_response(data=data)
    except ValueError:
        return Responses.make_response(error=True, 
                                        message=CONSTANTS.get('error_server'),
                                        status=status.HTTP_400_BAD_REQUEST)
