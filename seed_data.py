"""Script pour peupler la base de données avec des données de démo."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medibook.settings')
django.setup()

from accounts.models import User
from doctors.models import Specialite, Medecin
from patients.models import ProfilPatient

# Spécialités
specialites_data = [
    ("Médecine générale", "Prise en charge globale des patients"),
    ("Cardiologie", "Maladies du cœur et du système cardiovasculaire"),
    ("Dermatologie", "Maladies de la peau, des cheveux et des ongles"),
    ("Pédiatrie", "Médecine de l'enfant et de l'adolescent"),
    ("Gynécologie", "Santé de la femme"),
    ("Ophtalmologie", "Maladies des yeux et de la vision"),
    ("Dentisterie", "Soins dentaires et bucco-dentaires"),
    ("ORL", "Oreille, nez, gorge"),
    ("Neurologie", "Maladies du système nerveux"),
    ("Radiologie", "Imagerie médicale"),
]

for nom, desc in specialites_data:
    Specialite.objects.get_or_create(nom=nom, defaults={'description': desc})
print(f"OK {len(specialites_data)} spécialités créées")

# Superuser admin
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@medibook.dz',
        password='Admin@2025',
        first_name='Admin',
        last_name='MediBook',
        role='admin'
    )
    print("OK Superuser admin créé (admin / Admin@2025)")

# Patients de démo
patients_data = [
    ('patient1', 'Marie', 'Dupont', 'patient1@medibook.dz'),
    ('patient2', 'Ahmed', 'Benali', 'patient2@medibook.dz'),
]

for username, first, last, email in patients_data:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, password='Patient@2025',
            first_name=first, last_name=last, email=email, role='patient'
        )
        ProfilPatient.objects.create(utilisateur=user)
print("OK Patients de démo créés (password: Patient@2025)")

# Médecins de démo
medecins_data = [
    ('dr_martin', 'Jean', 'Martin', 'dr.martin@medibook.dz', 'Cardiologie', 15),
    ('dr_amrani', 'Fatima', 'Amrani', 'dr.amrani@medibook.dz', 'Dermatologie', 8),
    ('dr_boudiaf', 'Karim', 'Boudiaf', 'dr.boudiaf@medibook.dz', 'Pédiatrie', 12),
]

for username, first, last, email, specialite_nom, exp in medecins_data:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, password='Medecin@2025',
            first_name=first, last_name=last, email=email, role='medecin'
        )
        specialite = Specialite.objects.get(nom=specialite_nom)
        medecin = Medecin.objects.create(
            utilisateur=user,
            telephone_pro='+213 555 00 00 00',
            adresse_cabinet='Centre Médical, Alger',
            description=f"Médecin spécialisé en {specialite_nom} avec {exp} ans d'expérience.",
            annees_experience=exp,
            tarif_consultation=2000,
            est_actif=True,
        )
        medecin.specialites.add(specialite)
print("OK Médecins de démo créés (password: Medecin@2025)")

print("\n=== Donnees de demo creees avec succes ! ===")
print("Admin : admin / Admin@2025")
print("Patient : patient1 / Patient@2025")
print("Medecin : dr_martin / Medecin@2025")
