"""Tests for Stage 9 pure query functions."""
import pytest
from datetime import datetime
from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.queries import appointment_sort_key, select_appointments


def make_appointment(appt_id, practitioner_id, time, status=AppointmentStatus.SCHEDULED):
    """Helper to create appointments for testing."""
    patient = Patient("P1", "Test Patient")
    practitioner = Practitioner(practitioner_id, "Dr. Test", "General")
    return Appointment(appt_id, patient, practitioner, time, status)


class TestAppointmentSortKey:
    def test_sort_key_returns_datetime_and_id(self):
        appt = make_appointment("A1", "DR1", datetime(2026, 1, 1, 10, 0))
        assert appointment_sort_key(appt) == (datetime(2026, 1, 1, 10, 0), "A1")


class TestSelectAppointments:
    def test_select_by_practitioner(self):
        appt1 = make_appointment("A1", "DR1", datetime(2026, 1, 1, 10, 0))
        appt2 = make_appointment("A2", "DR2", datetime(2026, 1, 1, 10, 0))
        result = select_appointments([appt1, appt2], "DR1")

        assert len(result) == 1
        assert result[0] is appt1  # QRY-01: Select only requested practitioner

    def test_select_by_status(self):
        appt1 = make_appointment("A1", "DR1", datetime(2026, 1, 1, 10, 0), AppointmentStatus.SCHEDULED)
        appt2 = make_appointment("A2", "DR1", datetime(2026, 1, 1, 11, 0), AppointmentStatus.CANCELLED)

        result = select_appointments([appt1, appt2], "DR1", AppointmentStatus.SCHEDULED)

        assert len(result) == 1
        assert result[0] is appt1  # QRY-02: Explicit status filters apply

    def test_select_omitted_status_includes_all(self):
        appt1 = make_appointment("A1", "DR1", datetime(2026, 1, 1, 10, 0), AppointmentStatus.SCHEDULED)
        appt2 = make_appointment("A2", "DR1", datetime(2026, 1, 1, 11, 0), AppointmentStatus.CANCELLED)

        result = select_appointments([appt1, appt2], "DR1")

        assert len(result) == 2  # QRY-02: Omitted status includes all

    def test_select_sorts_by_datetime_then_id(self):
        appt1 = make_appointment("A2", "DR1", datetime(2026, 1, 1, 10, 0))
        appt2 = make_appointment("A1", "DR1", datetime(2026, 1, 1, 10, 0))  # Same time, lower ID
        appt3 = make_appointment("A3", "DR1", datetime(2026, 1, 1, 9, 0))  # Earlier time

        result = select_appointments([appt1, appt2, appt3], "DR1")

        assert result[0] is appt3  # 9:00 comes first
        assert result[1] is appt2  # 10:00, ID A1 comes before A2
        assert result[2] is appt1  # 10:00, ID A2

    def test_select_returns_new_list_purity(self):
        appt1 = make_appointment("A1", "DR1", datetime(2026, 1, 1, 10, 0))
        source = [appt1]

        result = select_appointments(source, "DR1")

        assert result is not source  # FP-02: Return a distinct list container
        assert result[0] is appt1  # But contains the same objects

    def test_select_known_practitioner_no_matches(self):
        appt1 = make_appointment("A1", "DR2", datetime(2026, 1, 1, 10, 0))

        result = select_appointments([appt1], "DR1")

        assert result == []  # QRY-04: Known practitioner with no matches gives empty list