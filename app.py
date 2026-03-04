import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="Movilización Lista 4")

# ENCABEZADO
st.markdown('<div style="background-color:#004a99;padding:20px;border-radius:10px;"><h1 style="color:white;text-align:center;">PERONISMO DE TODOS</h1><h3 style="color:#fdb813;text-align:center;">Movilización Electoral - Lista 4</h3></div>', unsafe_allow_html=True)

# LOGIN
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    with st.form("login"):
        u = st.text_input("Tu Nombre")
        c = st.text_input("Contraseña", type="password")
        if st.form_submit_button("INGRESAR"):
            if c == "lista42026" and u != "":
                st.session_state['auth'] = True
                st.session_state['u'] = u
                st.rerun()
            else: st.error("Clave incorrecta")
    st.stop()

# CONEXIÓN
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    with st.form(key="votos", clear_on_submit=True):
        dni = st.text_input("DNI DEL VOTANTE")
        if st.form_submit_button("✅ REGISTRAR VOTO"):
            if dni:
                df = conn.read()
                nuevo = pd.DataFrame([{"DNI": dni, "Voto": "VOTÓ", "Responsable": st.session_state['u'], "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}])
                df_final = pd.concat([df, nuevo], ignore_index=True)
                conn.update(data=df_final)
                st.success(f"¡Registrado con éxito! DNI: {dni}")
                st.balloons()
            else: st.warning("Falta el DNI")
except Exception as e:
    st.info("Por favor, hacé clic en el botón de abajo para autorizar el acceso a la planilla.")
