import streamlit as st

# Configuration de l'onglet du navigateur
st.set_page_config(page_title="Calculateur Extrusion", page_icon="⚙️")

# Titre principal
st.title("🏗️ Assistant de Calcul Extrusion")
st.markdown("Ce calculateur permet de définir la longueur de culot et de lopin optimale.")

# --- SECTION 1 : CALCUL DU CULOT ---
st.header("1. Type de Billette")
type_billette = st.selectbox(
    "Quelle est la nature de la billette ?",
    ["Primaire", "Recyclée"]
)

# Application de la règle k : 0.1 si primaire, 0.16 si recyclée
k = 0.1 if type_billette == "Primaire" else 0.16

# Calcul du culot (Fixé par votre formule : k * 228)
long_culot_mm = k * 228

# Affichage du résultat du culot
st.success(f"📏 **Longueur de culot minimal : {long_culot_mm:.2f} mm**")

st.divider() # Ligne de séparation

# --- SECTION 2 : CALCUL DU LOPIN ---
st.header("2. Paramètres de Production")

# Organisation en deux colonnes pour une meilleure lisibilité
col1, col2 = st.columns(2)

with col1:
    p_m = st.number_input("Poids au mètre (P/m) du profilé (kg/m)", min_value=0.0, format="%.3f")
    n_ecoulements = st.number_input("Nombre d'écoulements", min_value=1, step=1)

with col2:
    long_demandee = st.number_input("Longueur écoulée demandée (m)", min_value=0.0, format="%.2f")
    # Constante fixe
    poids_lineique_billette = 110.180

# --- SECTION 3 : RÉSULTATS FINAUX ---
st.markdown("### Résultat du calcul")

if st.button("CALCULER LE LOPIN OPTIMAL"):
    if p_m > 0 and long_demandee > 0:
        # 1. Calcul du poids du lopin (en kg)
        # On convertit long_culot_mm en mètres pour la formule
        poids_lopin = ((p_m * n_ecoulements) * long_demandee) + (poids_lineique_billette * (long_culot_mm / 1000))
        
        # 2. Calcul de la longueur du lopin (conversion m en mm)
        long_lopin_mm = (poids_lopin / poids_lineique_billette) * 1000
        
        # Affichage des résultats
        st.write("---")
        st.metric(label="POIDS TOTAL DU LOPIN", value=f"{poids_lopin:.3f} kg")
        st.metric(label="LONGUEUR LOPIN À RÉGLER", value=f"{long_lopin_mm:.2f} mm")
        
        st.info("💡 Note : Pensez à vérifier la température de la billette avant le filage.")
    else:
        st.warning("⚠️ Veuillez entrer les valeurs de P/m et de Longueur demandée.")

# Bas de page
st.caption("Développé pour l'assistance opérateur en extrusion.")
