from rest_framework import serializers

from main.models import Admission, Patient, Prescription, Referral, User, Ward

from dj_rest_auth.serializers import UserDetailsSerializer


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = ['url', 'patient_number', 'next_of_kin', 'address',
                  'date_of_birth', 'age', 'contacts', 'patient_name',
                  'created_by', 'created_at', 'updated_by', 'updated_at']
        read_only_fields = ['age', 'patient_number',
                            'created_by', 'created_at',
                            'updated_by', 'updated_at']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'first_name',
                  'last_name', 'phone_number', 'role']
        read_only_fields = ['email', 'username',
                            'first_name', 'last_name', 'phone_number',
                            'role']


class ReferralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Referral
        fields = ['url', 'patient', 'status', 'doctor', 'created_at',
                  'created_by', 'updated_at', 'updated_by']
        read_only_fields = ['created_by', 'updated_at',
                            'updated_by', 'created_at']


class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prescription
        fields = ['url', 'patient', 'start_datetime', 'end_datetime',
                  'description', 'created_at', 'created_by',
                  'updated_at', 'updated_by']
        read_only_fields = ['created_at', 'created_by',
                            'updated_at', 'updated_by']


class WardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ward
        fields = ['url', 'name']


class AdmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admission
        fields = ['url', 'ward', 'patient', 'created_at',
                  'created_by', 'updated_at', 'updated_by']
        read_only_fields = ['created_at', 'created_by',
                            'updated_at', 'updated_by']


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + \
            ('role', 'username', 'phone_number')
