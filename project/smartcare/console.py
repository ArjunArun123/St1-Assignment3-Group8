"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)
from smartcare.domain import Appointment, AppointmentStatus

def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Stage 9: implement the register/find/book/cancel/list/exit menu."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    while True:
        print("\n--- SmartCare Menu ---")
        print("1. Register Patient")
        print("2. Register Practitioner")
        print("3. Book Appointment")
        print("4. Cancel Appointment")
        print("5. List Practitioner Appointments")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            pid = input("Patient ID: ").strip()
            name = input("Name: ").strip()
            try:
                patients.register_patient(pid, name)
                print(f"Patient {pid} registered.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            prid = input("Practitioner ID: ").strip()
            name = input("Name: ").strip()
            spec = input("Specialty: ").strip()
            try:
                practitioners.register_practitioner(prid, name, spec)
                print(f"Practitioner {prid} registered.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            aid = input("Appointment ID: ").strip()
            pid = input("Patient ID: ").strip()
            prid = input("Practitioner ID: ").strip()
            time_str = input("Date/Time (YYYY-MM-DD HH:MM): ").strip()
            try:
                dt = parse_date_time(time_str)
                appt = appointments.book_appointment(aid, pid, prid, dt)
                print(f"Booked: {format_appointment(appt)}")
            except (ValueError, LookupError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            aid = input("Appointment ID to cancel: ").strip()
            try:
                appt = appointments.cancel_appointment(aid)
                print(f"Cancelled: {format_appointment(appt)}")
            except (ValueError, LookupError) as e:
                print(f"Error: {e}")

        elif choice == "5":
            prid = input("Practitioner ID: ").strip()
            status_str = input("Status (SCHEDULED/CANCELLED/COMPLETED) or leave blank for all: ").strip()
            status = None
            if status_str:
                try:
                    status = AppointmentStatus[status_str.upper()]
                except KeyError:
                    print("Error: Invalid status. Use SCHEDULED, CANCELLED, or COMPLETED.")
                    continue
            try:
                appts = appointments.list_practitioner_appointments(prid, status)
                if not appts:
                    print("No appointments found.")
                else:
                    for a in appts:
                        print(format_appointment(a))
            except (ValueError, LookupError) as e:
                print(f"Error: {e}")

        elif choice == "6":
            print("Exiting SmartCare. Session data lost.")
            break
        else:
            print("Error: Invalid menu choice.")
