from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main.views import PatientViewSet,\
    ReceptionistPatientView, ReferralViewSet, UserViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'users', UserViewSet)
router.register(r'receptionist-patients',
                ReceptionistPatientView,
                'registered-patient-detail')
router.register(r'referrals', ReferralViewSet)

urlpatterns = [
    path('browsable-api-auth/', include('rest_framework.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('', include(router.urls))
]
