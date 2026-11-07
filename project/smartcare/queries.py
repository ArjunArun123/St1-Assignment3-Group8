"""Stage 9 contracts for pure collection processing."""
from datetime import datetime
from smartcare.domain import Appointment, AppointmentStatus


def appointment_sort_key(appointment: Appointment) -> tuple[datetime, str]:
    """Return the date/time and appointment ID ordering key without side effects."""
    return (appointment.date_time, appointment.appointment_id)


def select_appointments(
    appointments: list[Appointment],
    practitioner_id: str,
    status: AppointmentStatus | None = None,
) -> list[Appointment]:
    """Return a new list for this practitioner, optionally filtered by status.
    Order by date/time then appointment ID using appointment_sort_key.
    Do not mutate the source list/objects or perform input/output.
    """
    result = []
    for appt in appointments:
        # Filter by practitioner
        if appt.practitioner.practitioner_id == practitioner_id:
            # Filter by status (if provided)
            if status is None or appt.status == status:
                result.append(appt)

    # Sort the new list using the reusable key
    result.sort(key=appointment_sort_key)
    return result