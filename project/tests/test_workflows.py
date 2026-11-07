"""End-to-end workflow tests for Stage 9."""
import pytest
from datetime import datetime
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import PatientService, PractitionerService, AppointmentService


@pytest.fixture
def clinic():
    """Create a fresh store and all services for workflow tests."""
    store = SmartCareDataStore()
    return {
        "store": store,
        "patients": PatientService(store),
        "practitioners": PractitionerService(store),
        "appointments": AppointmentService(store),
    }


def test_full_booking_and_cancellation_workflow(clinic):
    """UI-01: Verify full lifecycle: register, book, list, cancel, and free slot."""
    # 1. Register participants
    clinic["patients"].register_patient("P1", "Alice")
    clinic["practitioners"].register_practitioner("DR1", "Dr. Bob", "General")

    # 2. Book appointment
    time = datetime(2026, 11, 10, 10, 0)
    appt = clinic["appointments"].book_appointment("A1", "P1", "DR1", time)
    assert appt.status is AppointmentStatus.SCHEDULED

    # 3. List appointments (should show 1 scheduled)
    listed = clinic["appointments"].list_practitioner_appointments("DR1")
    assert len(listed) == 1
    assert listed[0] is appt

    # 4. Cancel appointment
    cancelled = clinic["appointments"].cancel_appointment("A1")
    assert cancelled.status is AppointmentStatus.CANCELLED

    # 5. Verify history retained and slot freed
    history = clinic["appointments"].list_practitioner_appointments("DR1")
    assert len(history) == 1
    assert history[0].status is AppointmentStatus.CANCELLED

    # 6. Book another at the same time (should succeed because slot is freed)
    appt2 = clinic["appointments"].book_appointment("A2", "P1", "DR1", time)
    assert appt2.status is AppointmentStatus.SCHEDULED


def test_invalid_input_recovery_workflow(clinic):
    """UI-02: Verify system recovers from invalid inputs without crashing."""
    # Try to book with unknown patient
    with pytest.raises(LookupError):
        clinic["appointments"].book_appointment("A1", "UNKNOWN", "DR1", datetime(2026, 11, 10, 10, 0))

    # Try to list unknown practitioner
    with pytest.raises(LookupError):
        clinic["appointments"].list_practitioner_appointments("UNKNOWN")

    # Try to cancel unknown appointment
    with pytest.raises(LookupError):
        clinic["appointments"].cancel_appointment("UNKNOWN")

    # Try to book with invalid status filter in listing (handled by service)
    # Note: The service raises ValueError for invalid types, but enum conversion happens in console.