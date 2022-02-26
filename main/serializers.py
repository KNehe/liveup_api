from rest_framework import serializers

from main.models import Patient, User


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
