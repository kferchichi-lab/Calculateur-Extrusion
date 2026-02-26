import streamlit as st

st.set_page_config(page_title="Calculateur Extrusion", page_icon="📟")

col_logo, col_titre = st.columns([1, 4])

with col_logo:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6q1BtDSDgVnJZFo0hOBfQJoDS6OYiub-qfQ&s", width=120) 

with col_titre:
    st.markdown("Tunisie Profilés d'Aluminium")
    st.subheader("Département Maintenance et Travaux Neufs")

st.markdown("---")
st.title("📟 Calculateur d'Extrusion")
st.markdown("Saisissez les paramètres pour obtenir les réglages machine.")

# --- SECTION 1 : SAISIE DES DONNÉES ---
st.header("📥 Paramètres d'entrée")

col1, col2 = st.columns(2)

with col1:
    type_billette = st.selectbox(
        "Nature de la billette :",
        ["Primaire", "Recyclée"]
    )
    p_m = st.number_input("P/m du profilé (kg/m)", min_value=0.0, format="%.3f")

with col2:
    n_ecoulements = st.number_input("Nombre d'écoulements", min_value=1, step=1)
    long_demandee = st.number_input("Longueur demandée (m)", min_value=0.0, format="%.2f")

st.divider()

# --- SECTION 2 : CALCULS ET AFFICHAGE ---
poids_lineique_billette = 110.180

if st.button("🧮 CALCULER LE LOPIN OPTIMAL"):
    if p_m > 0 and long_demandee > 0:
        # A. CALCUL DU CULOT
        k = 0.1 if type_billette == "Primaire" else 0.16
        long_culot_mm = k * 228
        
        # B. CALCUL DU POIDS ET DE LA LONGUEUR DU LOPIN
        poids_lopin = ((p_m * n_ecoulements) * long_demandee) + (poids_lineique_billette * (long_culot_mm / 1000))
        long_lopin_mm = (poids_lopin / poids_lineique_billette) * 1000
        
        # C. VÉRIFICATION DE LA CONDITION (Limite 1100 mm)
        if long_lopin_mm > 1100:
            st.error("🚨 ALERTE SÉCURITÉ")
            st.markdown(
                f"""
                <div style="background-color: #ff4b4b; padding: 20px; border-radius: 10px; border: 2px solid white;">
                    <h2 style="color: white; margin: 0; text-align: center;">⚠️ LE LOPIN EST TROP LONG ({long_lopin_mm:.2f} mm)</h2>
                    <p style="color: white; text-align: center; font-size: 1.2em; margin-top: 10px;">
                        La limite est de 1100 mm. Merci de ressaisir les données.
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            # D. AFFICHAGE DES RÉSULTATS
            st.markdown("### 📋 Consignes Opérateur")
            st.info(f"📏 **VALEUR DU CULOT : {long_culot_mm:.2f} mm**")
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric(label="POIDS DU LOPIN", value=f"{poids_lopin:.3f} kg")
            with col_res2:
                st.metric(label="LONGUEUR LOPIN OPTIMALE", value=f"{long_lopin_mm:.2f} mm")
            
            st.success("✅ Réglages validés.")
            
    else:
        st.warning("⚠️ Information manquante : Vérifiez le P/m ou la Longueur.")

st.caption(f"© 2026 TPR- Système d'Assistance Technique") 
st.caption("Développé pour l'assistance opérateur en extrusion.")
