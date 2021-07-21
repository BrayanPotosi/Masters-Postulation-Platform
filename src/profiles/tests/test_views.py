import json

# Django
from django.urls import reverse

# Rest Framework
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status

# Mommy
from model_mommy import mommy

# Models
from django.contrib.auth import get_user_model
from profiles.models import Profile, JobStatus, Education
# Views
from profiles.views import profile_form, job_status, EducationProfile


class ProfileFormTestCase(APITestCase, APIRequestFactory):

    def setUp(self):
        self.profile_form_url = reverse('profiles:profile_form')
        self.User = get_user_model()
        self.factory = APIRequestFactory()
        self.view = profile_form
        self.user_object = self.User.objects.create(
            email="adminmaster2@master.com",
            password="test123456"
        )
        Profile.objects.last()

    def test_get_complete_profile_information_if_a_user_us_authenticated(self):
        """A user can access their information once they have
         authenticated with their credentials"""
        request = self.factory.get(self.profile_form_url)
        force_authenticate(request, user=self.user_object)
        response = self.view(request)

        # Profile information request, status code must not be different from 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User registers must be 1
        self.assertEqual(self.User.objects.count(), 1)

        # Data must not be void
        self.assertNotEqual(response.data, None)


class JobStatusTestCase(APITestCase, APIRequestFactory):

    def setUp(self):
        self.job_status_url = reverse('profiles:job_status')
        self.factory = APIRequestFactory()
        self.User = get_user_model()
        self.view = job_status
        # Create User Object
        self.user_object = self.User.objects.create(
            email="adminmaster2@master.com",
            password="test123456"
        )
        # Create Job Status Object
        self.job_status_object = JobStatus.objects.create(
            has_job=True,
            company_name='CompanyName',
            salary=300,
            change_opt=True
        )
        # Data from update the job status object
        self.job_data = {
            "has_job": "true",
            "company_name": "Testing",
            "salary": "100",
            "change_opt": "true"
        }

    def test_get_information_about_a_candidate_current_employment_status(self):
        """A user must be able to obtain his work information if is authenticated"""
        request = self.factory.get(self.job_status_url)
        force_authenticate(request, user=self.user_object)
        response = self.view(request)

        # Job Status request, status code must not be different from 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Data must not be void
        self.assertNotEqual(response.data, None)

    def test_update_their_current_employment_information(self):
        """A user must be able to update his work information if is authenticated"""
        request = self.factory.put(self.job_status_url, self.job_data)
        force_authenticate(request, user=self.user_object)
        response = self.view(request)

        # Job status success update, code must not be different from 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # the object had to be updated
        self.assertEqual(JobStatus.objects.last().company_name, 'Testing')


class EducationTestCase(APITestCase, APIRequestFactory):

    def setUp(self):
        self.education_url = reverse('profiles:EducationProfile')
        self.factory = APIRequestFactory()
        self.User = get_user_model()
        self.view = EducationProfile.as_view()
        self.user_object = self.User.objects.create(
            email="adminmaster@master.com",
            password="test123456"
        )
        self.last_grade = mommy.make('profiles.LastGrade', _fill_optional=True, id=1)
        self.gotten_grade = mommy.make('profiles.GottenGrade', _fill_optional=True, id=1)
        self.education_object = Education.objects.create(
            institution_name='institution_name',
            year_end='2000-08-08',
            last_grade_id=1,
            gotten_grade_id=1
        )

        self.education_data = {
            "institution_name": "testing",
            "year_end": "2000-01-01",
            "last_grade_id": "1",
            "gotten_grade_id": "1"
        }
        self.updated_education_data = {
            "education_id": "1",
            "institution_name": "testing01",
            "year_end": "2012-12-12",
            "last_grade_id": "1",
            "gotten_grade_id": "1"
        }
        self.delete_information_Data = {
            "education_id": "11"
        }

    def test_get_educational_information_of_a_user_authenticated(self):
        """A user must be able of get their educational information if is authenticated"""
        request = self.factory.get(self.education_url)
        force_authenticate(request, user=self.user_object)
        response = self.view(request)

        # The status code of the response must be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_educational_information_in_profile(self):
        """A user must be able of add a new educational experience"""
        request = self.factory.post(self.education_url, self.education_data, format='json')
        force_authenticate(request, user=self.user_object)
        response = self.view(request)

        # The status code of the response must be 200
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # The new record must have education_data values
        self.assertEqual(Education.objects.last().institution_name, 'testing')

    def test_update_educational_information_in_profile(self):
        """A user must be able of update a existing educational experience"""
        request = self.factory.put(self.education_url, self.updated_education_data, format='json')
        force_authenticate(request, user=self.user_object)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_educational_information_in_profile(self):
        request = self.factory.delete(self.education_url, self.delete_information_Data, format='json')
        force_authenticate(request, user=self.user_object)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
