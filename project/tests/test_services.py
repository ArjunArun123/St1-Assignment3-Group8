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



class TestPatientRegistration:
    """Test FR-01: Patient registration requirements."""

    def test_register_valid_patient(self, setup_store):
        """Test-FR01-01: Valid patient registration succeeds."""
        store, patient_svc, _, _, _, _ = setup_store
        patient = patient_svc.register_patient("P2", "Jane Doe")
        assert store.find_patient("P2") is patient
        assert patient.name == "Jane Doe"

    def test_register_duplicate_patient_raises_value_error(self, setup_store):
        """Test-FR01-02: Duplicate patient ID raises ValueError."""
        store, patient_svc, _, _, _, _ = setup_store
        with pytest.raises(ValueError):
            patient_svc.register_patient("P1", "Duplicate Name")
        # Original patient must be preserved
        original = store.find_patient("P1")
        assert original.name == "John Doe"


class TestPractitionerRegistration:
    """Test FR-03: Practitioner registration requirements."""

    def test_register_valid_practitioner(self, setup_store):
        """Test-FR03-01: Valid practitioner registration succeeds."""
        store, _, practitioner_svc, _, _, _ = setup_store
        practitioner = practitioner_svc.register_practitioner(
            "PR2", "Dr. Johnson", "Cardiology"
        )
        assert store.find_practitioner("PR2") is practitioner
        assert practitioner.specialty == "Cardiology"

    def test_register_duplicate_practitioner_raises_value_error(self, setup_store):
        """Test-FR03-02: Duplicate practitioner ID raises ValueError."""
        store, _, practitioner_svc, _, _, _ = setup_store
        with pytest.raises(ValueError):
            practitioner_svc.register_practitioner("PR1", "Duplicate", "Other")
        # Original must be preserved
        original = store.find_practitioner("PR1")
        assert original.name == "Dr. Smith"


class TestAppointmentBooking:
    """Test FR-04 and FR-05: Appointment booking and conflict rules."""

    def test_book_valid_appointment(self, setup_store):
        """Test-FR04-01: Valid appointment booking succeeds."""
        store, _, _, appt_svc, _, _ = setup_store
        future_time = datetime(2026, 11, 7, 10, 0)
        appointment = appt_svc.book_appointment("A2", "P1", "PR1", future_time)
        assert store.find_appointment("A2") is appointment
        assert appointment.status is AppointmentStatus.SCHEDULED

    def test_book_appointment_practitioner_conflict(self, setup_store):
        """Test-FR05-01: Same practitioner, same time raises ValueError."""
        store, _, _, appt_svc, _, _ = setup_store
        future_time = datetime(2026, 11, 7, 10, 0)
        appt_svc.book_appointment("A2", "P1", "PR1", future_time)
        with pytest.raises(ValueError):
            appt_svc.book_appointment("A3", "P1", "PR1", future_time)

    def test_book_different_practitioner_same_time_allowed(self, setup_store):
        """Test-FR05-02: Different practitioner, same time is allowed."""
        store, _, practitioner_svc, appt_svc, _, _ = setup_store
        practitioner_svc.register_practitioner("PR2", "Dr. Jones", "General")
        future_time = datetime(2026, 11, 7, 10, 0)
        appt_svc.book_appointment("A2", "P1", "PR1", future_time)
        # Different practitioner should succeed
        appointment2 = appt_svc.book_appointment("A3", "P1", "PR2", future_time)
        assert appointment2.practitioner.practitioner_id == "PR2"

    def test_book_with_unknown_patient_raises_lookup_error(self, setup_store):
        """Test-FR04-02: Unknown patient ID raises LookupError."""
        store, _, _, appt_svc, _, _ = setup_store
        future_time = datetime(2026, 11, 7, 10, 0)
        with pytest.raises(LookupError):
            appt_svc.book_appointment("A2", "UNKNOWN", "PR1", future_time)

    def test_book_with_unknown_practitioner_raises_lookup_error(self, setup_store):
        """Test-FR04-03: Unknown practitioner ID raises LookupError."""
        store, _, _, appt_svc, _, _ = setup_store
        future_time = datetime(2026, 11, 7, 10, 0)
        with pytest.raises(LookupError):
            appt_svc.book_appointment("A2", "P1", "UNKNOWN", future_time)


class TestCancellationGuards:
    """Test FR-06 and FR-07: Cancellation guards and history retention."""

    def test_cancel_completed_appointment_raises_value_error(self, setup_store):
        """Test-FR06-03: Cannot cancel COMPLETED appointment."""
        store, _, _, appt_svc, patient, practitioner = setup_store
        future_time = datetime(2026, 11, 7, 10, 0)
        appt = appt_svc.book_appointment("A2", "P1", "PR1", future_time)
        # Manually set to COMPLETED for testing
        appt._status = AppointmentStatus.COMPLETED
        with pytest.raises(ValueError):
            appt_svc.cancel_appointment("A2")
        assert appt.status is AppointmentStatus.COMPLETED

    def test_cancel_retains_history(self, setup_store):
        """Test-FR07-01: Cancelled appointment remains retrievable."""
        store, _, _, appt_svc, patient, practitioner = setup_store
        future_time = datetime(2026, 11, 7, 10, 0)
        appt = appt_svc.book_appointment("A2", "P1", "PR1", future_time)
        appt_svc.cancel_appointment("A2")
        # Must still be findable
        found = store.find_appointment("A2")
        assert found is appt
        assert found.status is AppointmentStatus.CANCELLED
        # Must appear in list
        all_appointments = store.list_appointments()
        assert appt in all_appointments