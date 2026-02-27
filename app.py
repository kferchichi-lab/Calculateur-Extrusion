import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Calculateur Extrusion", page_icon="📟")

# CSS pour le style (Correction des barres)
st.markdown("""
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        .container-barre { width: 100%; background-color: #e0e0e0; border-radius: 5px; margin-bottom: 10px; position: relative; height: 25px;}
        .barre-lopin { background-color: #808080; height: 100%; border-radius: 5px; transition: width 0.5s;}
        .barre-limite { background-color: #006400; height: 8px; border-radius: 2px; margin-top: 5px;}
        .label-barre { font-size: 0.8em; color: #555; margin-bottom: 2px;}
    </style>
    """, unsafe_allow_html=True)

# --- ENTÊTE ---
col_logo, col_titre = st.columns([2, 5])
with col_logo:
    st.image("https://scontent.fnbe1-2.fna.fbcdn.net/v/t39.30808-6/408929007_749166663924252_578772537697061170_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=1d70fc&_nc_ohc=outSX1TrNzMQ7kNvwH8dLos&_nc_oc=AdnayidTjVde0oO8dBewwk-Vo1bwbpm9MvDcBijNWzBt6b_52O9jssFyIDcLrqtW-bk&_nc_zt=23&_nc_ht=scontent.fnbe1-2.fna&_nc_gid=mw-_AZkaw4Oh_IX1S6ObVQ&oh=00_AfuIu1RSs4hY2piAZBZvukecG5Pl97xctCOBml-nIqgrIQ&oe=69A62B8A", width=90)

with col_titre:
    st.write("**Tunisie Profilés d'Aluminium**")
    st.subheader("Direction Maintenance et Travaux Neufs")

st.divider()
st.title("📟 Calculateur d'Extrusion")

# --- SECTION 1 : SAISIE DES DONNÉES ---
st.header("📥 Paramètres d'entrée")
col1, col2 = st.columns(2)

with col1:
    type_billette = st.selectbox("Nature de la billette :", ["Primaire", "Recyclée"])
    p_m = st.number_input("P/m du profilé (kg/m)", min_value=0.0, format="%.3f", value=0.0)

with col2:
    n_ecoulements = st.number_input("Nombre d'écoulements", min_value=1, step=1)
    long_demandee = st.number_input("Longueur écoulée demandée (m)", min_value=0.0, format="%.2f", value=0.0)

# --- CONSTANTES ---
POIDS_LINEIQUE_BILLETTE = 110.180  
LIMITE_MAX = 1100.0

# --- SECTION 2 : CALCULS ET AFFICHAGE ---
if st.button("🧮 CALCULER LE LOPIN OPTIMAL"):
    if p_m > 0 and long_demandee > 0:
        # 1. Calcul du culot
        k = 0.1 if type_billette == "Primaire" else 0.16
        long_culot_mm = k * 228

        # 2. Calcul du poids (Correction de la NameError ici)
        poids_lopin = ((p_m * n_ecoulements) * long_demandee) + (POIDS_LINEIQUE_BILLETTE * (long_culot_mm / 1000))
        
        # 3. Calcul de la longueur
        long_lopin_mm = (poids_lopin / POIDS_LINEIQUE_BILLETTE) * 1000
        pourcentage_lopin = min((long_lopin_mm / LIMITE_MAX) * 100, 100)

        if long_lopin_mm > LIMITE_MAX:
            st.error(f"🚨 ALERTE : Lopin trop long ({long_lopin_mm:.2f} mm). La limite est de {LIMITE_MAX} mm.")
        else:
            st.success("✅ Dimension conforme.")
            st.info(f"📏 **VALEUR DU CULOT : {long_culot_mm:.2f} mm**")
            
            res1, res2 = st.columns(2)
            res1.metric("POIDS LOPIN", f"{poids_lopin:.3f} kg")
            res1.metric("LONGUEUR LOPIN", f"{long_lopin_mm:.2f} mm")
            
            with res2:
                st.markdown(f'<div class="label-barre">Lopin : {long_lopin_mm:.2f} mm</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="container-barre"><div class="barre-lopin" style="width: {pourcentage_lopin}%;"></div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="label-barre">Limite Machine : {LIMITE_MAX} mm</div>', unsafe_allow_html=True)
                st.markdown('<div class="barre-limite" style="width: 100%;"></div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Veuillez remplir tous les champs avec des valeurs supérieures à 0.")

st.divider()
st.caption("© 2026 TPR - Système d'Assistance Technique")
