from rest_framework import serializers

from main.models import Admission, Patient, Prescription, Referral, User, Ward

from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.serializers import PasswordResetSerializer


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "url",
            "patient_number",
            "next_of_kin",
            "address",
            "date_of_birth",
            "age",
            "contacts",
            "patient_name",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]
        read_only_fields = [
            "age",
            "patient_number",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]
        read_only_fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]


class ReferralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Referral
        fields = [
            "url",
            "patient",
            "status",
            "doctor",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = ["created_by", "updated_at", "updated_by", "created_at"]


class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prescription
        fields = [
            "url",
            "patient",
            "start_datetime",
            "end_datetime",
            "description",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]


class WardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ward
        fields = ["url", "name"]


class AdmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admission
        fields = [
            "url",
            "ward",
            "patient",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "role",
            "username",
            "phone_number",
        )


# Nested Hyperlinked Model Serialiazers


class AdmissionNestedSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer()
    updated_by = UserSerializer()
    ward = WardSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Admission
        fields = [
            "url",
            "id",
            "ward",
            "patient",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]


class PrescriptionNestedSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer()
    updated_by = UserSerializer()
    patient = PatientSerializer()

    class Meta:
        model = Prescription
        fields = [
            "url",
            "patient",
            "start_datetime",
            "end_datetime",
            "description",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]


class ReferralNestederializer(serializers.HyperlinkedModelSerializer):
    patient = PatientSerializer()
    doctor = UserSerializer()
    created_by = UserSerializer()
    updated_by = UserSerializer()

    class Meta:
        model = Referral
        fields = [
            "url",
            "patient",
            "status",
            "doctor",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = ["created_by", "updated_at", "updated_by", "created_at"]


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {"email_template_name": "password_reset_email.html"}
