from datetime import date, datetime
from enum import Enum


def required(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required")
    return value.strip()


class Patient:
    def __init__(self, patient_id: str, name: str,
                 date_of_birth: str, contact_details: str) -> None:
        self.patient_id = required(patient_id, "Patient ID")
        self.name = required(name, "Patient name")
        self.date_of_birth = required(date_of_birth, "Birth date")
        try:
            birth = date.fromisoformat(self.date_of_birth)
        except ValueError as error:
            raise ValueError("Birth date must be YYYY-MM-DD") from error
        if birth.strftime("%Y-%m-%d") != self.date_of_birth:
            raise ValueError("Birth date must be YYYY-MM-DD")
        if birth > date.today():
            raise ValueError("Birth date cannot be in the future")
        self.contact_details = required(contact_details, "Contact details")
        self._appointments: list[Appointment] = []

    def add_appointment(self, appointment: Appointment) -> None:
        if appointment.patient is not self:
            raise ValueError("Appointment belongs to another patient")
        self._appointments.append(appointment)

    def get_appointments(self) -> tuple[Appointment, ...]:
        return tuple(self._appointments)


class Practitioner:
    def __init__(self, practitioner_id: str, name: str,
                 specialty: str, contact_details: str) -> None:
        self.practitioner_id = required(practitioner_id, "Practitioner ID")
        self.name = required(name, "Practitioner name")
        self.specialty = required(specialty, "Specialty")
        self.contact_details = required(contact_details, "Contact details")
        self._appointments: list[Appointment] = []

    def add_appointment(self, appointment: Appointment) -> None:
        if appointment.practitioner is not self:
            raise ValueError("Appointment belongs to another practitioner")
        self._appointments.append(appointment)

    def get_appointments(self) -> tuple[Appointment, ...]:
        return tuple(self._appointments)


class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    CANCELLED = "Cancelled"


class Appointment:
    def __init__(self, appointment_id: str, patient: Patient,
                 practitioner: Practitioner, date_time: str) -> None:
        self.appointment_id = required(appointment_id, "Appointment ID")
        if not isinstance(patient, Patient) or not isinstance(practitioner, Practitioner):
            raise TypeError("A valid patient and practitioner are required")
        self.patient = patient
        self.practitioner = practitioner
        try:
            moment = datetime.strptime(required(date_time, "Time"), "%Y-%m-%d %H:%M")
        except ValueError as error:
            raise ValueError("Time must be YYYY-MM-DD HH:MM") from error
        if moment.strftime("%Y-%m-%d %H:%M") != date_time:
            raise ValueError("Time must be YYYY-MM-DD HH:MM")
        self.date_time = moment.strftime("%Y-%m-%d %H:%M")

        for old in patient.get_appointments() + practitioner.get_appointments():
            if old.date_time == self.date_time and old.status is AppointmentStatus.SCHEDULED:
                raise ValueError("Patient or practitioner is already booked")

        self._status = AppointmentStatus.SCHEDULED
        patient.add_appointment(self)
        practitioner.add_appointment(self)

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    def update_status(self, new_status: AppointmentStatus) -> None:
        if new_status is not AppointmentStatus.CANCELLED:
            raise ValueError("Only cancellation is supported")
        if self._status is AppointmentStatus.CANCELLED:
            raise ValueError("Appointment is already cancelled")
        self._status = new_status

    def cancel(self) -> None:
        self.update_status(AppointmentStatus.CANCELLED)

    def __str__(self) -> str:
        return (f"{self.appointment_id}: {self.patient.name} with "
                f"{self.practitioner.name} at {self.date_time} [{self.status.value}]")


def main() -> None:
    patients: dict[str, Patient] = {
        "P001": Patient("P001", "Alice Smith", "1990-05-01", "0400 000 001")}
    practitioners: dict[str, Practitioner] = {
        "G001": Practitioner("G001", "Dr. John Doe", "GP", "Clinic")}
    appointments: dict[str, Appointment] = {}

    print("Welcome to SmartCare. Try patient P001 and practitioner G001.")
    while True:
        try:
            print("\n1 Add patient  2 Add practitioner  3 Book  4 List  5 Cancel  0 Exit")
            choice = input("Choice: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                pid = input("Patient ID: ").strip()
                name = input("Name: ").strip()
                dob = input("Birth date (YYYY-MM-DD): ").strip()
                contact = input("Contact: ").strip()
                if pid in patients:
                    raise ValueError("Patient ID already exists")
                patients[pid] = Patient(pid, name, dob, contact)
                print(f"Patient added: {patients[pid].name} ({pid})")
            elif choice == "2":
                gid = input("Practitioner ID: ").strip()
                name = input("Name: ").strip()
                specialty = input("Specialty: ").strip()
                contact = input("Contact: ").strip()
                if gid in practitioners:
                    raise ValueError("Practitioner ID already exists")
                practitioners[gid] = Practitioner(gid, name, specialty, contact)
                print(f"Practitioner added: {practitioners[gid].name} ({gid})")
            elif choice == "3":
                patient_choices = ", ".join(f"{p.patient_id} ({p.name})" for p in patients.values())
                gp_choices = ", ".join(f"{g.practitioner_id} ({g.name})" for g in practitioners.values())
                print(f"Patients: {patient_choices}")
                print(f"Practitioners: {gp_choices}")
                aid = input("Appointment ID: ").strip()
                pid = input("Patient ID: ").strip()
                gid = input("Practitioner ID: ").strip()
                booking_time = input("Time (YYYY-MM-DD HH:MM): ").strip()
                if aid in appointments:
                    raise ValueError("Appointment ID already exists")
                if pid not in patients or gid not in practitioners:
                    raise ValueError("Patient or practitioner ID not found")
                appointments[aid] = Appointment(aid, patients[pid], practitioners[gid], booking_time)
                print(f"Booked: {appointments[aid]}")
            elif choice == "4":
                if not appointments:
                    print("No appointments yet.")
                for appointment in appointments.values():
                    print(f"  {appointment}")
            elif choice == "5":
                aid = input("Appointment ID: ").strip()
                if aid not in appointments:
                    raise ValueError("Appointment ID not found")
                appointments[aid].cancel()
                print(f"Cancelled: {appointments[aid]}")
            else:
                print("Choose a number from the menu.")
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")
        except EOFError:
            break


if __name__ == "__main__":
    main()
