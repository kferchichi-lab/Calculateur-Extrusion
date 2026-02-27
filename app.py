import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Calculateur Extrusion", page_icon="📟", layout="wide")

# --- BARRE LATÉRALE (CHOIX DE LA PRESSE) ---
with st.sidebar:
    st.header("⚙️ Configuration Machine")
    # Le paramètre index=None permet d'avoir un champ vide au départ avec une petite croix "x"
    presse_choisie = st.selectbox(
        "Sélectionnez la Presse :",
        ["Presse 4", "Presse 6", "Presse 7"],
        index=None,
        placeholder="Choisir une presse..."
    )
    
    if presse_choisie:
        st.success(f"Connecté à : **{presse_choisie}**")
    else:
        st.warning("Veuillez sélectionner une presse pour commencer.")

# --- ENTÊTE ---
col_logo, col_titre = st.columns([1, 4])

with col_logo:
    st.image(
        "https://scontent.fnbe1-2.fna.fbcdn.net/v/t39.30808-6/408929007_749166663924252_578772537697061170_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=1d70fc&_nc_ohc=outSX1TrNzMQ7kNvwH8dLos&_nc_oc=AdnayidTjVde0oO8dBewwk-Vo1bwbpm9MvDcBijNWzBt6b_52O9jssFyIDcLrqtW-bk&_nc_zt=23&_nc_ht=scontent.fnbe1-2.fna&_nc_gid=mw-_AZkaw4Oh_IX1S6ObVQ&oh=00_AfuIu1RSs4hY2piAZBZvukecG5Pl97xctCOBml-nIqgrIQ&oe=69A62B8A",
        width=120
    )

with col_titre:
    st.markdown("### Tunisie Profilés d'Aluminium")
    st.subheader("Direction Maintenance et Travaux Neufs")

st.markdown("---")

# Affichage du titre dynamique
if presse_choisie:
    st.title(f"📟 Calculateur d'Extrusion - {presse_choisie}")
else:
    st.title("📟 Calculateur d'Extrusion")

# --- CONDITION : BLOQUER LE RESTE SI AUCUNE PRESSE N'EST CHOISIE ---
if not presse_choisie:
    st.info("👈 Veuillez sélectionner une presse dans la barre latérale pour activer le calculateur.")
    st.stop() # Arrête l'exécution ici tant que la presse n'est pas choisie

# --- SECTION 1 : SAISIE DES DONNÉES ---
st.header("📥 Paramètres d'entrée")

col1, col2 = st.columns(2)

with col1:
    type_billette = st.selectbox(
        "Nature de la billette :",
        ["Primaire", "Recyclée"]
    )
    p_m = st.number_input(
        "P/m du profilé (kg/m)",
        value=None,
        format="%.3f",
        placeholder="Ex: 1.25"
    )

with col2:
    n_ecoulements = st.number_input(
        "Nombre d'écoulements",
        min_value=1,
        step=1
    )
    long_demandee = st.number_input(
        "Longueur écoulée demandée (m)",
        value=None,
        format="%.2f",
        placeholder="Ex: 47"
    )

st.divider()

# --- SECTION 2 : CALCULS ET AFFICHAGE ---
poids_lineique_billette = 110.180  # kg/m

if st.button("🧮 CALCULER LE LOPIN OPTIMAL"):

    if p_m and long_demandee: # Vérifie que les valeurs ne sont pas None

        k = 0.1 if type_billette == "Primaire" else 0.16
        long_culot_mm = k * 228

        poids_lopin = (
            (p_m * n_ecoulements) * long_demandee
            + (poids_lineique_billette * (long_culot_mm / 1000))
        )

        long_lopin_mm = (poids_lopin / poids_lineique_billette) * 1000

        if long_lopin_mm > 1100:
            st.error("🚨 ALERTE SÉCURITÉ")
            st.markdown(
                f"""
                <div style="background-color: #ff4b4b; padding: 20px; 
                            border-radius: 10px; border: 2px solid white;">
                    <h2 style="color: white; margin: 0; text-align: center;">
                        ⚠️ LE LOPIN EST TROP LONG ({long_lopin_mm:.2f} mm)
                    </h2>
                    <p style="color: white; text-align: center; 
                              font-size: 1.2em; margin-top: 10px;">
                        La limite est de 1100 mm. Merci de ressaisir les données.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"### 📋 Consignes Opérateur - {presse_choisie}")
            st.info(f"📏 **VALEUR DU CULOT : {long_culot_mm:.2f} mm**")

            col_res1, col_res2 = st.columns(2)

            with col_res1:
                st.metric(
                    label="POIDS DU LOPIN",
                    value=f"{poids_lopin:.3f} kg"
                )

            with col_res2:
                st.metric(
                    label="LONGUEUR LOPIN OPTIMALE",
                    value=f"{long_lopin_mm:.2f} mm"
                )

            st.success(f"✅ Réglages validés pour la {presse_choisie}.")
    else:
        st.warning("⚠️ Information manquante : Vérifiez le P/m ou la Longueur.")

# --- PIED DE PAGE ---
st.caption("© 2026 TPR - Système d'Assistance Technique")
st.caption(f"Développé pour l'assistance opérateur en extrusion.")
