"""Focused regression tests for Stage 8 defects F8-01 and F8-02."""
import pytest
from datetime import datetime
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import PatientService, PractitionerService, AppointmentService


def test_f8_01_same_practitioner_conflict_and_different_allowed():
    """F8-01 Regression: Same practitioner at same time must conflict; different must be allowed."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appt_svc = AppointmentService(store)

    patient = patient_svc.register_patient("P001", "Test Patient")
    dr1 = practitioner_svc.register_practitioner("DR001", "Dr. One", "General")
    dr2 = practitioner_svc.register_practitioner("DR002", "Dr. Two", "General")

    time = datetime(2026, 11, 10, 10, 0)

    # Book first appointment for DR001
    appt_svc.book_appointment("A001", "P001", "DR001", time)

    # 1. Same practitioner (DR001) at same time MUST raise ValueError
    with pytest.raises(ValueError):
        appt_svc.book_appointment("A002", "P001", "DR001", time)

    # 2. Different practitioner (DR002) at same time MUST succeed
    appt2 = appt_svc.book_appointment("A003", "P001", "DR002", time)
    assert appt2.practitioner.practitioner_id == "DR002"


def test_f8_02_cancelled_appointment_is_retained_and_found():
    """F8-02 Regression: Cancelled appointments must remain retrievable via lookup (FR-07)."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appt_svc = AppointmentService(store)

    patient = patient_svc.register_patient("P001", "Test Patient")
    dr1 = practitioner_svc.register_practitioner("DR001", "Dr. One", "General")

    time = datetime(2026, 11, 10, 10, 0)
    appt = appt_svc.book_appointment("A001", "P001", "DR001", time)

    # Cancel the appointment
    appt_svc.cancel_appointment("A001")

    # The appointment MUST still be findable by ID in the store
    found = store.find_appointment("A001")
    assert found is appt
    assert found.status is AppointmentStatus.CANCELLED