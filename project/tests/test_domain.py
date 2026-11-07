"""Tests for domain objects: Patient, Practitioner, and Appointment."""
import pytest
from datetime import datetime
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


class TestPatientDomain:
    """Test Patient domain object construction and validation."""

    def test_patient_valid_construction_and_trimming(self):
        """Test-DOM-01: Valid patient with whitespace in ID is trimmed."""
        patient = Patient("  P001  ", "John Doe")
        assert patient.patient_id == "P001"
        assert patient.name == "John Doe"

    def test_patient_blank_id_rejected(self):
        """Test-DOM-02: Blank patient ID raises ValueError."""
        with pytest.raises(ValueError):
            Patient("   ", "John Doe")

    def test_patient_blank_name_rejected(self):
        """Test-DOM-02b: Blank patient name raises ValueError."""
        with pytest.raises(ValueError):
            Patient("P001", "  ")


class TestPractitionerDomain:
    """Test Practitioner domain object construction and validation."""

    def test_practitioner_valid_construction(self):
        """Test-DOM-03: Valid practitioner construction retains all fields."""
        practitioner = Practitioner("DR001", "Dr. Smith", "General")
        assert practitioner.practitioner_id == "DR001"
        assert practitioner.name == "Dr. Smith"
        assert practitioner.specialty == "General"

    def test_practitioner_blank_id_rejected(self):
        """Test-DOM-04: Blank practitioner ID raises ValueError."""
        with pytest.raises(ValueError):
            Practitioner("   ", "Dr. Smith", "General")

    def test_practitioner_blank_specialty_rejected(self):
        """Test-DOM-04b: Blank specialty raises ValueError."""
        with pytest.raises(ValueError):
            Practitioner("DR001", "Dr. Smith", "  ")


class TestAppointmentDomain:
    """Test Appointment domain object and status transitions."""

    def test_appointment_initial_status_scheduled(self):
        """Test-DOM-05: New appointment starts as SCHEDULED."""
        patient = Patient("P001", "John Doe")
        practitioner = Practitioner("DR001", "Dr. Smith", "General")
        appointment = Appointment(
            "A001", patient, practitioner, datetime(2026, 11, 15, 10, 0)
        )
        assert appointment.status is AppointmentStatus.SCHEDULED

    def test_appointment_cancellation_changes_status(self):
        """Test-DOM-06: Cancellation changes status to CANCELLED."""
        patient = Patient("P001", "John Doe")
        practitioner = Practitioner("DR001", "Dr. Smith", "General")
        appointment = Appointment(
            "A001", patient, practitioner, datetime(2026, 11, 15, 10, 0)
        )
        appointment.cancel()
        assert appointment.status is AppointmentStatus.CANCELLED

    def test_appointment_repeated_cancellation_rejected(self):
        """Test-DOM-07: Repeated cancellation raises ValueError."""
        patient = Patient("P001", "John Doe")
        practitioner = Practitioner("DR001", "Dr. Smith", "General")
        appointment = Appointment(
            "A001", patient, practitioner, datetime(2026, 11, 15, 10, 0)
        )
        appointment.cancel()
        with pytest.raises(ValueError):
            appointment.cancel()
        assert appointment.status is AppointmentStatus.CANCELLED

    def test_appointment_completed_cancellation_guard(self):
        """Test-DOM-08: Cannot cancel COMPLETED appointment."""
        patient = Patient("P001", "John Doe")
        practitioner = Practitioner("DR001", "Dr. Smith", "General")
        appointment = Appointment(
            "A001",
            patient,
            practitioner,
            datetime(2026, 11, 15, 10, 0),
            status=AppointmentStatus.COMPLETED,
        )
        with pytest.raises(ValueError):
            appointment.cancel()
        assert appointment.status is AppointmentStatus.COMPLETED

    def test_appointment_whitespace_id_trimmed(self):
        """Test-DOM-09: Appointment ID whitespace is trimmed."""
        patient = Patient("P001", "John Doe")
        practitioner = Practitioner("DR001", "Dr. Smith", "General")
        appointment = Appointment(
            "  A001  ", patient, practitioner, datetime(2026, 11, 15, 10, 0)
        )
        assert appointment.appointment_id == "A001"