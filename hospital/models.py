from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)


class InvoiceRecords(models.Model):
    InvoiceNumber = models.IntegerField(primary_key=True)
    DateDue = models.DateField()
    amountDue = models.DecimalField(max_digits=10, decimal_places=2)
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)

class Lab(models.Model):
    testID = models.IntegerField(primary_key=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    labName = models.CharField(max_length=15)

class Pharmacy(models.Model):
    medicineID = models.IntegerField(primary_key=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    expiryDate = models.DateField()

class PatientHistory(models.Model):
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)
    Illness = models.CharField(max_length=15)
    treatmentHistory = models.CharField(max_length=40)
    progressNotes = models.CharField(max_length=40)
    familyHistory = models.CharField(max_length=40)

class Department(models.Model):
    Dnumber = models.IntegerField(primary_key=True)
    Dname = models.CharField(max_length=15)
    Dmanager = models.IntegerField()

class InPatient(models.Model):
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE, primary_key=True)
    diagnosis = models.CharField(max_length=15)
    admissionDate = models.DateField()
    dischargeDate = models.DateField()
    NurseID = models.ForeignKey('Nurse', on_delete=models.CASCADE)
    RoomID = models.ForeignKey('Rooms', on_delete=models.CASCADE)

class OutPatient(models.Model):
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE, primary_key=True)
    nextAppointment = models.DateField()
    prognosis = models.CharField(max_length=15)

class Staff(models.Model):
    StaffID = models.IntegerField(primary_key=True)
    Sname = models.CharField(max_length=15)
    Address = models.CharField(max_length=40)
    Phone = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]{10}$')])

class Doctor(models.Model):
    StaffID = models.ForeignKey('Staff', on_delete=models.CASCADE, primary_key=True)
    Speciality = models.CharField(max_length=15)
    Qualification = models.CharField(max_length=15)
    licenseNum = models.CharField(max_length=15)

class Nurse(models.Model):
    StaffID = models.ForeignKey('Staff', on_delete=models.CASCADE, primary_key=True)
    WardID = models.ForeignKey('Ward', on_delete=models.CASCADE)

class Wardboy(models.Model):
    StaffID = models.ForeignKey('Staff', on_delete=models.CASCADE, primary_key=True)
    WardID = models.ForeignKey('Ward', on_delete=models.CASCADE)

class VisitingDoctor(models.Model):
    StaffID = models.ForeignKey('Staff', on_delete=models.CASCADE, primary_key=True)
    VisitingDays = models.CharField(max_length=7)

class InHouseDoctor(models.Model):
    StaffID = models.ForeignKey('Staff', on_delete=models.CASCADE, primary_key=True)

class Rooms(models.Model):
    roomID = models.IntegerField(primary_key=True)
    roomType = models.CharField(max_length=10)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class Ward(models.Model):
    roomID = models.ForeignKey('Rooms', on_delete=models.CASCADE, primary_key=True)
    WType = models.CharField(max_length=1)
    WNumber = models.IntegerField()

class OperationTheatre(models.Model):
    roomID = models.ForeignKey('Rooms', on_delete=models.CASCADE, primary_key=True)
    OTCost = models.DecimalField(max_digits=10, decimal_places=2)
    OTNumber = models.IntegerField()
    BookingTime = models.TimeField()

class ICU(models.Model):
    roomID = models.ForeignKey('Rooms', on_delete=models.CASCADE, primary_key=True)
    ICUNumber = models.IntegerField()
    CareDescription = models.CharField(max_length=30)

class RequestedTests(models.Model):
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)
    testID = models.ForeignKey('Lab', on_delete=models.CASCADE)
    date = models.DateField()
    Result = models.CharField(max_length=30, null=True)

class InvoicePatient(models.Model):
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)
    InvoiceNumber = models.ForeignKey('InvoiceRecords', on_delete=models.CASCADE)

class Prescriptions(models.Model):
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)
    medicineID = models.ForeignKey('Pharmacy', on_delete=models.CASCADE)
    quantity = models.IntegerField()

class PatientPatientHistory(models.Model):
    PatientID = models.ForeignKey('Patient', on_delete=models.CASCADE)
    Illness = models.CharField(max_length=15)
