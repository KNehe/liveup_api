from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from main.choices import DOCTOR, RECEPTIONIST, STUDENT_CLINICIAN
from main.models import User


class LoginTestCase(APITestCase):
    def setUp(self) -> None:
        self.dummy_user = {
            "email": "knehe@gmail.com",
            "phone_number": "+256554332456",
            "role": STUDENT_CLINICIAN,
            "username": "nehe8kk",
            "first_name": "nehe",
            "last_name": "nehe",
            "password": "#$23msnAB#$&",
        }

    def test_should_login_user(self):
        User.objects.create_user(**self.dummy_user)

        response = self.client.post(reverse("rest_login"), self.dummy_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("user").get("email"), self.dummy_user["email"]
        )
        self.assertEqual(response.data.get("user").get("role"), self.dummy_user["role"])
        self.assertIsNotNone(response.data.get("access_token"))
        self.assertIsNotNone(response.data.get("refresh_token"))

    def test_should_not_login_user_when_password_is_missing(self):
        User.objects.create_user(**self.dummy_user)

        self.dummy_user["password"] = ""

        response = self.client.post(reverse("rest_login"), self.dummy_user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("password")[0], "This field may not be blank."
        )
        self.assertEqual(response.data.get("password")[0].code, "blank")

    def test_should_not_login_user_when_email_is_missing(self):
        User.objects.create_user(**self.dummy_user)

        del self.dummy_user["email"]

        response = self.client.post(reverse("rest_login"), self.dummy_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("non_field_errors")[0],
            "Unable to log in with provided credentials.",
        )
        self.assertEqual(response.data.get("non_field_errors")[0].code, "invalid")

    def test_should_not_login_user_when_user_not_registered(self):
        response = self.client.post(reverse("rest_login"), self.dummy_user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("non_field_errors")[0],
            "Unable to log in with provided credentials.",
        )
        self.assertEqual(response.data.get("non_field_errors")[0].code, "invalid")


class PatientViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.dummy_user = {
            "email": "knehe@gmail.com",
            "phone_number": "+256554332456",
            "role": STUDENT_CLINICIAN,
            "username": "nehe8kk",
            "first_name": "nehe",
            "last_name": "nehe",
            "password": "#$23msnAB#$&",
        }
        self.patient = {
            "next_of_kin": "next_of_kin",
            "address": "address",
            "date_of_birth": "2022-02-25",
            "contacts": "+256 774 332 423",
            "patient_name": "John Doe",
        }

    def authenticate(self):
        User.objects.create_user(**self.dummy_user)

        response = self.client.post(reverse("rest_login"), self.dummy_user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data.get('access_token')}"
        )

    def test_should_register_patient(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("next_of_kin"), self.patient["next_of_kin"])
        self.assertEqual(response.data.get("address"), self.patient["address"])
        self.assertEqual(
            response.data.get("date_of_birth"), self.patient["date_of_birth"]
        )
        self.assertEqual(
            response.data.get("patient_name"), self.patient["patient_name"]
        )
        self.assertEqual(response.data.get("contacts"), self.patient["contacts"])
        self.assertIsNotNone(response.data.get("created_by"))
        self.assertIsNotNone(response.data.get("created_at"))
        self.assertIsNotNone(response.data.get("url"))
        self.assertIsNone(response.data.get("updated_by"))
        self.assertIsNone(response.data.get("updated_at"))

    def test_should_register_patient_if_user_not_authorized(self):
        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_should_register_patient_if_required_data_missing(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.patient["next_of_kin"] = ""
        self.patient["address"] = ""
        self.patient["date_of_birth"] = ""
        self.patient["patient_name"] = ""
        self.patient["contacts"] = ""

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("next_of_kin")[0], "This field may not be blank."
        )
        self.assertEqual(
            response.data.get("address")[0], "This field may not be blank."
        )
        self.assertEqual(
            response.data.get("date_of_birth")[0],
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )
        self.assertEqual(
            response.data.get("patient_name")[0], "This field may not be blank."
        )
        self.assertEqual(
            response.data.get("contacts")[0], "This field may not be blank."
        )

    def test_should_register_patient_if_not_authenticated(self):
        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_should_update_patient(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.patient["patient_name"] = "new name"
        self.patient["next_of_kin"] = "new next of kin name"

        patient_id = response.data.get("url").split("/")[-2]

        response2 = self.client.patch(
            reverse("patient-detail", kwargs={"pk": patient_id}), self.patient
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data.get("next_of_kin"), self.patient["next_of_kin"])
        self.assertEqual(
            response2.data.get("patient_name"), self.patient["patient_name"]
        )
        self.assertEqual(response2.data.get("url"), response.data.get("url"))

    def test_should_not_update_patient_if_not_found(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.patient["patient_name"] = "new name"
        self.patient["next_of_kin"] = "new next of kin name"

        patient_id = 212  # not registered patient id

        response2 = self.client.patch(
            reverse("patient-detail", kwargs={"pk": patient_id}), self.patient
        )

        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.data.get("detail"), "Not found.")

    def test_should_not_update_patient_if_not_authorized(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.patient["patient_name"] = "new name"
        self.patient["next_of_kin"] = "new next of kin name"

        self.dummy_user["role"] = STUDENT_CLINICIAN
        self.dummy_user["email"] = "rando@gmail.com"
        self.dummy_user["username"] = "randohaha"

        self.authenticate()

        patient_id = response.data.get("url").split("/")[-2]

        response2 = self.client.patch(
            reverse("patient-detail", kwargs={"pk": patient_id}), self.patient
        )

        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response2.data.get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_should_not_update_patient_if_not_authenticated(self):
        response = self.client.patch(
            reverse("patient-detail", kwargs={"pk": 1}), self.patient
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_should_retrieve_a_patient(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        patient_id = response.data.get("url").split("/")[-2]

        response2 = self.client.get(
            reverse("patient-detail", kwargs={"pk": patient_id}), self.patient
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data.get("next_of_kin"), self.patient["next_of_kin"])
        self.assertEqual(
            response2.data.get("patient_name"), self.patient["patient_name"]
        )
        self.assertEqual(response2.data.get("url"), response.data.get("url"))

    def test_should_not_retrieve_patient_if_not_authorized(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.dummy_user["role"] = STUDENT_CLINICIAN
        self.dummy_user["email"] = "rando@gmail.com"
        self.dummy_user["username"] = "randohaha"

        self.authenticate()

        patient_id = response.data.get("url").split("/")[-2]

        response2 = self.client.get(
            reverse("patient-detail", kwargs={"pk": patient_id}), self.patient
        )

        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response2.data.get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_should_not_retrieve_patient_if_not_authenticated(self):
        response = self.client.get(
            reverse("patient-detail", kwargs={"pk": 1}), self.patient
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_should_get_all_patients(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("patient-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertIsNone(response.data.get("next"))
        self.assertIsNone(response.data.get("previous"))
        self.assertEqual(len(response.data.get("results")), 1)

    def test_should_not_get_all_patients_if_not_authorized(self):
        self.dummy_user["role"] = RECEPTIONIST

        self.authenticate()

        self.client.post(reverse("patient-list"), self.patient)

        self.dummy_user["role"] = STUDENT_CLINICIAN
        self.dummy_user["email"] = "rando@gmail.com"
        self.dummy_user["username"] = "randohaha"

        self.authenticate()

        response = self.client.get(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_should_not_get_all_patients_if_not_authorized(self):
        response = self.client.get(reverse("patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )


class UserViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.dummy_user = {
            "email": "knehe@gmail.com",
            "phone_number": "+256554332456",
            "role": STUDENT_CLINICIAN,
            "username": "nehe8kk",
            "first_name": "nehe",
            "last_name": "nehe",
            "password": "#$23msnAB#$&",
        }

    def authenticate(self):
        User.objects.create_user(**self.dummy_user)

        response = self.client.post(reverse("rest_login"), self.dummy_user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data.get('access_token')}"
        )

    def test_should_get_all_users(self):
        self.authenticate()

        response = self.client.get(reverse("user-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertIsNone(response.data.get("next"))
        self.assertIsNone(response.data.get("previous"))
        self.assertEqual(len(response.data.get("results")), 1)

    def test_should_not_get_all_users_when_not_athenticated(self):
        response = self.client.get(reverse("user-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_should_not_get_one_user(self):
        self.authenticate()

        user_id = 12212  # unknown user id
        response = self.client.get(reverse("user-detail", kwargs={"pk": user_id}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_get_one_user(self):
        self.authenticate()

        self.dummy_user["email"] = "email@gmail.com"
        self.dummy_user["username"] = "username"

        user_id = User.objects.create_user(**self.dummy_user).id
        response = self.client.get(reverse("user-detail", kwargs={"pk": user_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), self.dummy_user["email"])
        self.assertEqual(response.data.get("first_name"), self.dummy_user["first_name"])


class ReceptionistPatientViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.dummy_user = {
            "email": "knehe@gmail.com",
            "phone_number": "+256554332456",
            "role": RECEPTIONIST,
            "username": "nehe8kk",
            "first_name": "nehe",
            "last_name": "nehe",
            "password": "#$23msnAB#$&",
        }
        self.patient = {
            "next_of_kin": "next_of_kin",
            "address": "address",
            "date_of_birth": "2022-02-25",
            "contacts": "+256 774 332 423",
            "patient_name": "John Doe",
        }

    def authenticate(self):
        User.objects.create_user(**self.dummy_user)

        response = self.client.post(reverse("rest_login"), self.dummy_user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data.get('access_token')}"
        )

    def test_should_get_patients_registered_by_receptionist(self):
        self.authenticate()

        self.client.post(reverse("patient-list"), self.patient)

        response = self.client.get(reverse("registered-patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertIsNone(response.data.get("next"))
        self.assertIsNone(response.data.get("previous"))
        self.assertEqual(len(response.data.get("results")), 1)

    def test_should_not_get_patients_registered_by_receptionist_when_not_authenticated(
        self,
    ):
        response = self.client.get(reverse("registered-patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_should_not_get_patients_registered_by_receptionist_when_not_authorized(
        self,
    ):
        self.dummy_user["role"] = STUDENT_CLINICIAN

        self.authenticate()

        response = self.client.get(reverse("registered-patient-list"), self.patient)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_should_get_one_registered_patient(self):
        self.authenticate()

        response = self.client.post(reverse("patient-list"), self.patient)

        patient_id = response.data.get("url").split("/")[-2]

        response = self.client.get(reverse("patient-detail", kwargs={"pk": patient_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("patient_number"))
        self.assertIsNotNone(response.data.get("patient_name"))
        self.assertIsNotNone(response.data.get("next_of_kin"))
        self.assertIsNotNone(response.data.get("date_of_birth"))

    def test_should_not_get_one_unknown_patient(self):
        self.authenticate()

        patient_id = 12212  # unknown patient id
        response = self.client.get(reverse("patient-detail", kwargs={"pk": patient_id}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_get_one_registered_patient(self):
        self.dummy_user["role"] = STUDENT_CLINICIAN
        self.authenticate()

        response = self.client.get(reverse("patient-detail", kwargs={"pk": 22}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("detail"),
            "You do not have permission to perform this action.",
        )


class ReferralViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.dummy_user = {
            "email": "knehe@gmail.com",
            "phone_number": "+256554332456",
            "role": RECEPTIONIST,
            "username": "nehe8kk",
            "first_name": "nehe",
            "last_name": "nehe",
            "password": "#$23msnAB#$&",
        }
        self.patient = {
            "next_of_kin": "next_of_kin",
            "address": "address",
            "date_of_birth": "2022-02-25",
            "contacts": "+256 774 332 423",
            "patient_name": "John Doe",
        }

    def authenticate(self):
        User.objects.create_user(**self.dummy_user)

        response = self.client.post(reverse("rest_login"), self.dummy_user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data.get('access_token')}"
        )

    def create_doctor(self):
        self.dummy_user["email"] = "doctor@gmail.com"
        self.dummy_user["username"] = "doctor1"
        self.dummy_user["role"] = DOCTOR

        doc = User.objects.create_user(**self.dummy_user)
        return doc

    def create_second_doctor(self):
        self.dummy_user["email"] = "doctor2@gmail.com"
        self.dummy_user["username"] = "doctor2"
        self.dummy_user["role"] = DOCTOR

        doc = User.objects.create_user(**self.dummy_user)
        return doc

    def test_should_refer_patient(self):
        self.authenticate()

        patient_response = self.client.post(reverse("patient-list"), self.patient)

        doctor_id = self.create_doctor().id

        doc_response = self.client.get(reverse("user-detail", kwargs={"pk": doctor_id}))

        response = self.client.post(
            reverse("referral-list"),
            {
                "doctor": doc_response.data.get("url"),
                "patient": patient_response.data.get("url"),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("status"), "Not seen")
        self.assertEqual(response.data.get("doctor"), doc_response.data.get("url"))
        self.assertIsNotNone(response.data.get("created_by"))
        self.assertIsNotNone(response.data.get("created_at"))
        self.assertIsNone(response.data.get("updated_at"))
        self.assertIsNone(response.data.get("updated_by"))

    def test_should_not_refer_patient_when_not_authenticated(self):

        response = self.client.post(
            reverse("referral-list"),
            {
                "doctor": "will not be checked",
                "patient": "will not be checked",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_should_not_refer_patient_with_invalid_urls(self):
        self.authenticate()

        response = self.client.post(
            reverse("referral-list"),
            {
                "doctor": "bad_url",
                "patient": "invalid_url",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("patient")[0], "Invalid hyperlink - No URL match."
        )
        self.assertEqual(
            response.data.get("doctor")[0], "Invalid hyperlink - No URL match."
        )

    def test_should_update_referral_data(self):
        self.authenticate()

        patient_response = self.client.post(reverse("patient-list"), self.patient)

        doctor_id = self.create_doctor().id
        doc_response = self.client.get(reverse("user-detail", kwargs={"pk": doctor_id}))

        response = self.client.post(
            reverse("referral-list"),
            {
                "doctor": doc_response.data.get("url"),
                "patient": patient_response.data.get("url"),
            },
        )

        doctor_id = self.create_second_doctor().id

        doc_response = self.client.get(reverse("user-detail", kwargs={"pk": doctor_id}))

        refferal_id = response.data.get("url").split("/")[-2]

        response2 = self.client.patch(
            reverse("referral-detail", kwargs={"pk": refferal_id}),
            {"doctor": doc_response.data.get("url")},
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data.get("status"), "Not seen")
        self.assertNotEqual(response.data.get("doctor"), response2.data.get("doctor"))
        self.assertIsNotNone(response2.data.get("updated_at"))
        self.assertIsNotNone(response2.data.get("updated_by"))

    def test_should_not_update_referral_data_when_not_authenticated(self):
        response = self.client.patch(
            reverse("referral-detail", kwargs={"pk": 22}),
            {"doctor": "will not vause trouble"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Authentication credentials were not provided.",
        )

    def test_should_not_update_referral_data_with_invalid_urls(self):
        self.authenticate()

        patient_response = self.client.post(reverse("patient-list"), self.patient)

        doctor_id = self.create_doctor().id
        doc_response = self.client.get(reverse("user-detail", kwargs={"pk": doctor_id}))

        response = self.client.post(
            reverse("referral-list"),
            {
                "doctor": doc_response.data.get("url"),
                "patient": patient_response.data.get("url"),
            },
        )

        doctor_id = self.create_second_doctor().id

        doc_response = self.client.get(reverse("user-detail", kwargs={"pk": doctor_id}))

        refferal_id = response.data.get("url").split("/")[-2]

        response2 = self.client.patch(
            reverse("referral-detail", kwargs={"pk": refferal_id}),
            {"doctor": "invalid_url", "patient": "invalid_url"},
        )

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response2.data.get("patient")[0], "Invalid hyperlink - No URL match."
        )
        self.assertEqual(
            response2.data.get("doctor")[0], "Invalid hyperlink - No URL match."
        )


# IF YOU'RE HAVE REACHED HERE, THANKS FOR READING MY TESTS
# I DID NOT TEST ALL VIEWS BECAUSE THIS PROJECT WAS MEANT FOR LEARNING
# I THINK THE REST OF THE TEST LOGIC FOR NON-TESTED VIEWS WILL BE VERY SIMILAR and I'VE UNDERSTOOD ENOUGH
# IN PRODUCTION IT'D BE WISE TO TEST ALL
# FEEL FREE TO CLONE AND CONTINUE IF INTERESTED
