from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main.views import ClinicianAssignedPatientsViewSet, PatientViewSet, PrescriptionViewSet,\
    ReceptionistPatientView, ReferralViewSet, UserViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'users', UserViewSet)
router.register(r'referrals', ReferralViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'receptionist-patients',
                ReceptionistPatientView,
                'registered-patient')
router.register(r'assigned-patients',
                ClinicianAssignedPatientsViewSet,
                basename='assigned-patient')

urlpatterns = [
    path('browsable-api-auth/', include('rest_framework.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('', include(router.urls))
]
