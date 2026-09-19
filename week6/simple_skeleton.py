class Patient:
    def __init__(self,):
        self.appointments = []

        def add_appointment(self, appointment):
            self.appointments.append(appointment)

        def get_appointments(self):
            return self.appointments

class Practitioner:
    def __init__(self,):
        self.appointments = []

        def add_appointment(self, appointment):
            self.appointments.append(appointment)

        def get_appointments(self):
            return self.appointments

class Appointment:
    def __init__(self, patient, practitioner, status):
        self.patient = patient
        self.practitioner = practitioner
        self.status = status

        patient.add_appointment(self)
        practitioner.add_appointment(self)

        def update_status(self, new_status):
            self.status = new_status

        def cancel(self):
            self.status = "Cancelled"