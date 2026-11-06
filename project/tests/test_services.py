import pytest
from datetime import datetime, timedelta
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Patient, Practitioner, Appointment, AppointmentStatus
from smartcare.services import PatientService, PractitionerService, AppointmentService


@pytest.fixture
def setup_store():
    """Create a fresh store and services for each test."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appointment_svc = AppointmentService(store)

    # Register synthetic data
    patient = patient_svc.register_patient("P1", "John Doe")
    practitioner = practitioner_svc.register_practitioner("PR1", "Dr. Smith", "General")

    return store, patient_svc, practitioner_svc, appointment_svc, patient, practitioner


class TestPatientAndPractitionerSearch:
    def test_find_valid_patient(self, setup_store):
        store, patient_svc, _, _, patient, _ = setup_store
        found = patient_svc.find_patient("P1")
        assert found is patient  # Must be the exact same object

    def test_find_valid_practitioner(self, setup_store):
        store, _, practitioner_svc, _, _, practitioner = setup_store
        found = practitioner_svc.find_practitioner("PR1")
        assert found is practitioner

    def test_find_patient_whitespace_trimmed(self, setup_store):
        store, patient_svc, _, _, patient, _ = setup_store
        found = patient_svc.find_patient("  P1  ")
        assert found is patient

    def test_find_patient_blank_raises_value_error(self, setup_store):
        store, patient_svc, _, _, _, _ = setup_store
        with pytest.raises(ValueError):
            patient_svc.find_patient("   ")

    def test_find_patient_unknown_raises_lookup_error(self, setup_store):
        store, patient_svc, _, _, _, _ = setup_store
        with pytest.raises(LookupError):
            patient_svc.find_patient("UNKNOWN_ID")


class TestAppointmentCancellation:
    def test_cancel_scheduled_appointment(self, setup_store):
        store, _, _, appt_svc, patient, practitioner = setup_store
        # Use a fixed datetime with 0 seconds and 0 microseconds to pass validation
        future_time = datetime(2026, 11, 7, 10, 0)
        appt = appt_svc.book_appointment("A1", "P1", "PR1", future_time)

        cancelled = appt_svc.cancel_appointment("A1")

        assert cancelled is appt  # Must return the exact same object
        assert appt.status == AppointmentStatus.CANCELLED
        assert store.find_appointment("A1") is appt  # Must still be retrievable (FR-07)

    def test_cancel_unknown_appointment_raises_lookup_error(self, setup_store):
        store, _, _, appt_svc, _, _ = setup_store
        with pytest.raises(LookupError):
            appt_svc.cancel_appointment("UNKNOWN_ID")

    def test_cancel_blank_appointment_raises_value_error(self, setup_store):
        store, _, _, appt_svc, _, _ = setup_store
        with pytest.raises(ValueError):
            appt_svc.cancel_appointment("   ")

    def test_cancel_already_cancelled_raises_value_error(self, setup_store):
        store, _, _, appt_svc, patient, practitioner = setup_store
        future_time = datetime(2026, 11, 7, 10, 0)
        appt = appt_svc.book_appointment("A1", "P1", "PR1", future_time)
        appt_svc.cancel_appointment("A1")

        with pytest.raises(ValueError):
            appt_svc.cancel_appointment("A1")

        assert appt.status == AppointmentStatus.CANCELLED  # State unchanged