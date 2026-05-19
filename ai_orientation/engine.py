from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

SPECIALITES_KEYWORDS = {
    "Cardiologie": (
        "coeur palpitations douleur thoracique essoufflement tachycardie hypertension "
        "poitrine cardiologue arythmie infarctus angine"
    ),
    "Dermatologie": (
        "peau bouton acné eczéma psoriasis démangeaison rougeur allergie éruption "
        "cicatrice grain beauté verrue champignon tache"
    ),
    "Pédiatrie": (
        "enfant bébé nourrisson fièvre enfants vaccination croissance développement "
        "pédiatre pédiatrique pediatrie"
    ),
    "Gynécologie": (
        "règles cycle menstruel grossesse contraception utérus ovaires sein gynécologue "
        "menstruation ménopause maternité accouchement"
    ),
    "Ophtalmologie": (
        "yeux vision vue lunettes myopie hypermétropie cataracte glaucome rétine "
        "ophtalmologue opticien brûlure oculaire"
    ),
    "Dentisterie": (
        "dent dentaire carie gencive mâchoire douleur dentaire couronne plombage "
        "orthodontie dentiste extraction"
    ),
    "ORL": (
        "oreille gorge nez sinusite otite rhinite allergique rhume angine amygdale "
        "audition acouphène vertiges ORL"
    ),
    "Neurologie": (
        "migraine maux de tête céphalée épilepsie convulsion tremblements paralysie "
        "sclérose Alzheimer Parkinson mémoire vertige neurologie"
    ),
    "Radiologie": (
        "radio scanner IRM échographie imagerie radiographie os fracture"
    ),
    "Médecine générale": (
        "fièvre fatigue grippe infection rhume toux angine médecin généraliste "
        "consultation malaise mal être douleur générale"
    ),
}


def recommander_specialite(motif_patient, n_resultats=3):
    corpus = list(SPECIALITES_KEYWORDS.values())
    noms = list(SPECIALITES_KEYWORDS.keys())

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus)

    motif_vec = vectorizer.transform([motif_patient])
    similarites = cosine_similarity(motif_vec, tfidf_matrix).flatten()

    top_indices = np.argsort(similarites)[::-1][:n_resultats]
    resultats = [
        {'specialite': noms[i], 'score': round(float(similarites[i]), 3)}
        for i in top_indices
        if similarites[i] > 0
    ]
    if not resultats:
        resultats = [{'specialite': 'Médecine générale', 'score': 0}]
    return resultats
