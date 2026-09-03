# Stage 1 – SmartCare Prototype

print("Welcome to SmartCare: Community Clinic Appointment Booking System!")

# First Appointment
patient1_name = 'Alice Smith'
practitioner1_name = 'Dr. John Doe'
appointment1_time = '2024-07-20 10:00 AM'
print(f"Patient: {patient1_name} | Practitioner: {practitioner1_name} | Time: {appointment1_time}")

# Second Appointment
patient2_name = 'Bob Johnson'
practitioner2_name = 'Dr. Jane Roe'
appointment2_time = '2024-07-20 11:30 AM'
print(f"Patient: {patient2_name} | Practitioner: {practitioner2_name} | Time: {appointment2_time}")

# Enhanced Version – Lists, Dictionaries, Functions

appointments = []

def book_appointment(patient_name, practitioner_name, appointment_time):
    # Controlled improvement: prevent overlapping appointments
    for appt in appointments:
        if appt["time"] == appointment_time:
            raise ValueError("Appointment time is already booked")

    if not patient_name:
        raise ValueError("Patient name cannot be empty")

    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }
    appointments.append(appointment)

def display_appointments():
    if not appointments:
        print("No appointments recorded.")
        return
    for appointment in appointments:
        print(f"Patient: {appointment['patient']} | Practitioner: {appointment['practitioner']} | Time: {appointment['time']}")

print("\nWelcome to SmartCare: The Clinical Appointment Booking System!")

# Example bookings
book_appointment('Alice Smith', 'Dr. John Doe', '2024-07-20 11:30 AM')
book_appointment('Bob Johnson', 'Dr. Jane Roe', '2024-07-20 11:30 AM')

display_appointments()
