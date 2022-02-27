from rest_framework import serializers

from main.models import Patient, Referral, User


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = ['url','patient_number', 'next_of_kin', 'address',
                  'date_of_birth', 'age', 'contacts', 'patient_name',
                  'created_by', 'created_at', 'updated_by', 'updated_at']
        read_only_fields = ['age', 'patient_number',
                            'created_by', 'created_at',
                            'updated_by', 'updated_at']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'first_name',
                  'last_name', 'phone_number']
        read_only_fields = ['email', 'username',
                            'first_name', 'last_name', 'phone_number', 'id']


class ReferralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Referral
        fields = ['url', 'patient', 'doctor', 'created_at',
                  'created_by', 'updated_at', 'updated_by']
        read_only_fields = ['created_by', 'updated_at',
                           'updated_by', 'created_at']
