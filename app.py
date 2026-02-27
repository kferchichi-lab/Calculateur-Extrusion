import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Calculateur Extrusion", page_icon="📟")

# CSS pour le style et les barres
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
col_logo, col_titre = st.columns([1, 4])

with col_logo:
    st.image(
        "https://scontent.fnbe1-2.fna.fbcdn.net/v/t39.30808-6/408929007_749166663924252_578772537697061170_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=1d70fc&_nc_ohc=outSX1TrNzMQ7kNvwH8dLos&_nc_oc=AdnayidTjVde0oO8dBewwk-Vo1bwbpm9MvDcBijNWzBt6b_52O9jssFyIDcLrqtW-bk&_nc_zt=23&_nc_ht=scontent.fnbe1-2.fna&_nc_gid=mw-_AZkaw4Oh_IX1S6ObVQ&oh=00_AfuIu1RSs4hY2piAZBZvukecG5Pl97xctCOBml-nIqgrIQ&oe=69A62B8A",
        width=120
    )

with col_titre:
    st.markdown("Tunisie Profilés d'Aluminium")
    st.subheader("Direction Maintenance et Travaux Neufs")

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
long_lopin_mm = (poids_lopin / poids_lineique_billette) * 1000
        

LIMITE_MAX = 1100.0
pourcentage_lopin = min((long_lopin_mm / LIMITE_MAX) * 100, 100)
if st.button("🧮 CALCULER LE LOPIN OPTIMAL"):

    if p_m > 0 and long_demandee > 0:

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

            st.markdown("### 📋 Consignes Opérateur")
            st.info(f"📏 **VALEUR DU CULOT : {long_culot_mm:.2f} mm**")

            col_res1, col_res2 = st.columns(2)

            with col_res1:
                st.metric(
                    label="POIDS DU LOPIN",
                    value=f"{poids_lopin:.3f} kg"
                )
                st.metric(
                    label="LONGUEUR LOPIN OPTIMALE",
                    value=f"{long_lopin_mm:.2f} mm"
                )
            with col_res2:
               with col_visu:
                st.markdown("<br>", unsafe_allow_html=True)
                # Barre Grise (Lopin actuel)
                st.markdown(f'<div class="label-barre">Lopin actuel : {long_lopin_mm:.2f} mm</div>', unsafe_allow_html=True)
                st.markdown(f'''
                    <div class="container-barre">
                        <div class="barre-lopin" style="width: {pourcentage_lopin}%;"></div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # Barre Vert Sombre (Limite Cisaille)
                st.markdown(f'<div class="label-barre">Capacité Tapis Cisaille (Limite : {LIMITE_MAX} mm)</div>', unsafe_allow_html=True)
                st.markdown('<div class="barre-limite" style="width: 100%;"></div>', unsafe_allow_html=True)
                
                st.success("✅ Dimension conforme à la capacité machine.")

    else:
        st.warning("⚠️ Information manquante : Vérifiez le P/m ou la Longueur.")

# --- PIED DE PAGE ---
st.caption("© 2026 TPR - Système d'Assistance Technique")
st.caption("Développé pour l'assistance opérateur en extrusion.")
