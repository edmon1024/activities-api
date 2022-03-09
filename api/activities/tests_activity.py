from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

import json

from rest_framework.test import APIClient
from rest_framework import status

from activities.models import (
    Property,
    Activity,
    Survey,
)


class ActivityTestCase(TestCase):
    def setUp(self):
        user = User(
            email="edmon.af@gmail.com",
            first_name="Edmundo",
            last_name="Andrade",
            username="eandrade",
        )
        user.set_password("1234567890***")
        user.save()

        self.now = timezone.now()

        p_1 = Property.objects.create(
            title="Propiedad del valle", 
            address="Calle prueba 100", 
            description="Propiedad 1",
        )
        p_1.save()
        p_2 = Property.objects.create(
            title="Propiedad centro", 
            address="Calle prueba 200", 
            description="Propiedad 2",
        )
        p_2.save()
        p_3 = Property.objects.create(
            title="Propiedad buenavista", 
            address="Calle prueba 300", 
            description="Propiedad 3",
            status="disabled",
        )
        p_3.save()

        a_1 = Activity.objects.create(
            property_id=p_1,
            schedule=self.now + datetime.timedelta(days=2),
            title="Actividad 1",
        )
        a_1.save()
        a_2 = Activity.objects.create(
            property_id=p_2,
            schedule=self.now + datetime.timedelta(days=7),
            title="Actividad 2",
        )
        a_2.save()

        s_1 = Survey.objects.create(
            activity=a_1,
            answers={
                "A": 1,
                "B": 2,
            }
        )
        s_1.save()
        s_2 = Survey.objects.create(
            activity=a_2,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s_2.save()

        client = APIClient()

        response = client.post(
            "/api/v1/auth/", {
                "username": "eandrade",
                "password": "1234567890***"
            },
        )

        result = json.loads(response.content)

        self.token = result["token"]
        self.user = user
        self.p_1 = p_1
        self.p_2 = p_2
        self.p_3 = p_3

    def _activities_for_testing(self):
        p_9 = Property.objects.create(
            title="Propiedad buenavista",
            address="Calle prueba 900",
            description="Propiedad 9",
        )
        p_9.save()

        a_9 = Activity.objects.create(
            property_id=p_9,
            schedule=self.now,
            title="Actividad 9",
        )
        a_9.save()

        Survey.objects.create(
            activity=a_9,
            answers={
                "A": 1,
                "B": 2,
            }
        )

        p_10 = Property.objects.create(
            title="Propiedad buenavista",
            address="Calle prueba 1000",
            description="Propiedad 10",
        )
        p_10.save()

        a_10 = Activity.objects.create(
            property_id=p_10,
            schedule=self.now + datetime.timedelta(days=21),
            title="Actividad 10",
        )
        a_10.save()

        Survey.objects.create(
            activity=a_10,
            answers={
                "A": 1,
                "B": 2,
            }
        )

        p_11 = Property.objects.create(
            title="Propiedad buenavista",
            address="Calle prueba 1100",
            description="Propiedad 11",
        )
        p_11.save()

        a_11 = Activity.objects.create(
            property_id=p_11,
            schedule=self.now - datetime.timedelta(days=8),
            title="Actividad 11",
        )
        a_11.save()

        Survey.objects.create(
            activity=a_11,
            answers={
                "A": 1,
                "B": 2,
            }
        )

    def test_list_properties(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)
    
        response = client.get("/api/v1/property/")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(result["count"], 2)
    
        for item in result["results"]:
            self.assertIn("id", item)
            self.assertIn("title", item)
            self.assertIn("address", item)
            self.assertIn("status", item)
            break

    def test_list_activities(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        response = client.get("/api/v1/activity/")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(result["count"], 2)
    
        for item in result["results"]:
            self.assertIn("id", item)
            self.assertIn("schedule", item)
            self.assertIn("title", item)
            self.assertIn("created_at", item)
            self.assertIn("status", item)
            self.assertIn("condition", item)
            self.assertIn("property", item)
            self.assertIn("id", item["property"])
            self.assertIn("title", item["property"])
            self.assertIn("address", item["property"])
            self.assertIn("survey", item)
            break

    def test_create_activity_success(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)
    
        response = client.post(
            "/api/v1/activity/",
            {
              "property_id": self.p_2.id,
              "schedule": self.now + datetime.timedelta(days=4, hours=4),
              "title": "activity 5",
              "survey": {
                "answers": {
                  "test1": "answer1",
                  "test2": "answer2",
                }
              }
            },
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", result)
        self.assertIn("property_id", result)
        self.assertIn("schedule", result)
        self.assertIn("title", result)
        self.assertIn("survey", result)
        self.assertIn("id", result["survey"])
        self.assertIn("answers", result["survey"])
        self.assertIn("condition", result)
        self.assertIn("created_at", result)
    
    def test_reschedule_activity_not_found(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        response = client.patch(
            "/api/v1/activity/10000/reschedule/",
            {
              "schedule": self.now + datetime.timedelta(days=9, hours=1),
            },
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(result["detail"], "Not found.")

    def test_reschedule_activity_success(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad 4",
            address="Calle prueba 400",
            description="Propiedad 4 A",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(days=10, hours=8),
            title="Actividad 4",
        )
        a.save()
        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        response = client.patch(
            f"/api/v1/activity/{a.id}/reschedule/",
            {
              "schedule": self.now + datetime.timedelta(days=1, hours=10),
            },
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", result)
        self.assertIn("schedule", result)

    def test_reschedule_activity_w_property_disabled(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad 5",
            address="Calle prueba 500",
            description="Propiedad 4 A",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(hours=3),
            title="Actividad 5",
            status="cancelled",
        )
        a.save()
        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        response = client.patch(
            f"/api/v1/activity/{a.id}/reschedule/",
            {
              "schedule": self.now + datetime.timedelta(days=6, hours=7),
            },
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result["status"], "Cancelled activities cannot be rescheduled")

    def test_cancelled_activity_success(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad 6",
            address="Calle prueba 600",
            description="Propiedad 6",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(days=4, hours=9),
            title="Actividad 6",
        )
        a.save()

        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        response = client.post(f"/api/v1/activity/{a.id}/cancelled/")

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["status"], "cancelled")

    def test_cancelled_activity_status_cannot_changed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad 7",
            address="Calle prueba 700",
            description="Propiedad 7",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(hours=5),
            title="Actividad 7",
            status="cancelled",
        )
        a.save()

        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        response = client.post(f"/api/v1/activity/{a.id}/cancelled/")

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result["status"], "The status cannot be changed, the activity has cancelled")

    def test_retrieve_survey_success(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad 8",
            address="Calle prueba 800",
            description="Propiedad 8",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now - datetime.timedelta(days=1),
            title="Actividad 8",
        )
        a.save()

        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        response = client.get(f"/api/v1/survey/{s.id}/")

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", result)
        self.assertIn("answers", result)

    def test_retrieve_survey_not_found(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        response = client.get("/api/v1/survey/1000/")

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(result["detail"], "Not found.")

    def test_list_activities_default_filter(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        response = client.get("/api/v1/activity/")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["count"], 3)

        for item in result["results"]:
            self.assertIn("id", item) 
            self.assertIn("schedule", item)
            self.assertIn("title", item)
            self.assertIn("created_at", item)
            self.assertIn("status", item)
            self.assertIn("condition", item)
            self.assertIn("property", item)
            self.assertIn("id", item["property"])
            self.assertIn("title", item["property"])
            self.assertIn("address", item["property"])
            self.assertIn("survey", item)
            break

    def test_list_activities_w_status_unknown_filter(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        response = client.get("/api/v1/activity/?status=unknown")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["count"], 0)
        self.assertEqual(result["results"], [])

    def test_list_activities_w_status_filter(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        response = client.get("/api/v1/activity/?status=active")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["count"], 5)

        for item in result["results"]:
            self.assertIn("id", item)
            self.assertIn("schedule", item)
            self.assertIn("title", item)
            self.assertIn("created_at", item)
            self.assertIn("status", item)
            self.assertIn("condition", item)
            self.assertIn("property", item)
            self.assertIn("id", item["property"])
            self.assertIn("title", item["property"])
            self.assertIn("address", item["property"])
            self.assertIn("survey", item)
            break

    def test_list_activities_w_schedule_range_filter_empty(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        schedule_after = self.now - datetime.timedelta(days=30)
        schedule_after = schedule_after.strftime("%Y-%m-%d %H:%M")

        schedule_before = self.now - datetime.timedelta(days=28)
        schedule_before = schedule_before.strftime("%Y-%m-%d %H:%M")

        response = client.get(f"/api/v1/activity/?schedule_after={schedule_after}&schedule_before={schedule_before}")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["count"], 0)

    def test_list_activities_w_schedule_range_filter_w_data(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        schedule_after = self.now + datetime.timedelta(days=20)
        schedule_after = schedule_after.strftime("%Y-%m-%d %H:%M")

        schedule_before = self.now + datetime.timedelta(days=22)
        schedule_before = schedule_before.strftime("%Y-%m-%d %H:%M")

        response = client.get(f"/api/v1/activity/?schedule_after={schedule_after}&schedule_before={schedule_before}")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["count"], 1)

        for item in result["results"]:
            self.assertIn("id", item)
            self.assertIn("schedule", item)
            self.assertIn("title", item)
            self.assertIn("created_at", item)
            self.assertIn("status", item)
            self.assertIn("condition", item)
            self.assertIn("property", item)
            self.assertIn("id", item["property"])
            self.assertIn("title", item["property"])
            self.assertIn("address", item["property"])
            self.assertIn("survey", item)
            break

    def test_list_activities_w_status_and_schedule_range_filter_empty(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        schedule_after = self.now + datetime.timedelta(days=20)
        schedule_after = schedule_after.strftime("%Y-%m-%d %H:%M")

        schedule_before = self.now + datetime.timedelta(days=22)
        schedule_before = schedule_before.strftime("%Y-%m-%d %H:%M")

        response = client.get(f"/api/v1/activity/?status=cancelled&schedule_after={schedule_after}&schedule_before={schedule_before}")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["count"], 0)

    def test_list_activities_w_status_and_schedule_range_filter_w_data(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        schedule_after = self.now + datetime.timedelta(days=20)
        schedule_after = schedule_after.strftime("%Y-%m-%d %H:%M")

        schedule_before = self.now + datetime.timedelta(days=22)
        schedule_before = schedule_before.strftime("%Y-%m-%d %H:%M")

        response = client.get(f"/api/v1/activity/?status=active&schedule_after={schedule_after}&schedule_before={schedule_before}")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(result["count"], 1)

        for item in result["results"]:
            self.assertIn("id", item)
            self.assertIn("schedule", item)
            self.assertIn("title", item)
            self.assertIn("created_at", item)
            self.assertIn("status", item)
            self.assertIn("condition", item)
            self.assertIn("property", item)
            self.assertIn("id", item["property"])
            self.assertIn("title", item["property"])
            self.assertIn("address", item["property"])
            self.assertIn("survey", item)
            break

    def test_list_activities_w_schedule_range_format_error(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        self._activities_for_testing()

        schedule_after = self.now + datetime.timedelta(days=20)
        schedule_after = schedule_after.strftime("%Y/%m/%d %H:%M")

        schedule_before = self.now + datetime.timedelta(days=22)
        schedule_before = schedule_before.strftime("%Y/%m/%d %H:%M")

        response = client.get(f"/api/v1/activity/?schedule_after={schedule_after}&schedule_before={schedule_before}")

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("schedule", result)
        self.assertEqual(result["schedule"][0], "Enter a valid date/time.")

    def test_create_activity_w_property_disabled(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad A",
            address="Calle prueba A",
            description="Propiedad A",
            status="disabled",
        )
        p.save()

        response = client.post(
            "/api/v1/activity/",
            {
              "property_id": p.id,
              "schedule": self.now + datetime.timedelta(days=10),
              "title": "activity A",
              "survey": {
                "answers": {
                  "testA": "answer A",
                  "testA": "answer B",
                }
              }
            },
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("property_id", result)
        self.assertEqual(result["property_id"], "The activity cannot be created if the property is disabled")

    def test_create_activity_w_schedule_problem(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad A",
            address="Calle prueba A",
            description="Propiedad A",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(days=10, minutes=30),
            title="Actividad 8",
        )
        a.save()

        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        response = client.post(
            "/api/v1/activity/",
            {
              "property_id": p.id,
              "schedule": self.now + datetime.timedelta(days=10),
              "title": "activity A",
              "survey": {
                "answers": {
                  "testA": "answer A",
                  "testA": "answer B",
                }
              }
            },
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(result[0], "Activities cannot be created on the same date and time as another activity")

    def test_create_activity_required_field_missing(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        response = client.post(
            "/api/v1/activity/",
            {},
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("property_id", result)
        self.assertIn("schedule", result)
        self.assertIn("title", result)
        self.assertIn("survey", result)

        self.assertEqual(result["property_id"][0], "This field is required.")
        self.assertEqual(result["schedule"][0], "This field is required.")
        self.assertEqual(result["title"][0], "This field is required.")
        self.assertEqual(result["survey"][0], "This field is required.")

    def test_reschedule_activity_w_schedule_problem(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad A",
            address="Calle prueba A",
            description="Propiedad A",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(days=10, minutes=30),
            title="Actividad 8",
        )
        a.save()

        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        a_1 = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(days=11, minutes=30),
            title="Actividad 9",
        )
        a_1.save()

        s_1 = Survey.objects.create(
            activity=a_1,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s_1.save()

        response = client.patch(
            f"/api/v1/activity/{a_1.id}/reschedule/",
            {
              "schedule": self.now + datetime.timedelta(days=10, minutes=25),
            },
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("schedule",result)
        self.assertEqual(result["schedule"], "Activities cannot be created on the same date and time as another activity")

    def test_reschedule_activity_required_field_missing_schedule(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

        p = Property.objects.create(
            title="Propiedad A",
            address="Calle prueba A",
            description="Propiedad A",
        )
        p.save()

        a = Activity.objects.create(
            property_id=p,
            schedule=self.now + datetime.timedelta(days=10, minutes=30),
            title="Actividad 8",
        )
        a.save()

        s = Survey.objects.create(
            activity=a,
            answers={
                "C": 1,
                "D": 2,
            }
        )
        s.save()

        response = client.patch(f"/api/v1/activity/{a.id}/reschedule/")

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("schedule",result)
        self.assertEqual(result["schedule"], "The field is required")




