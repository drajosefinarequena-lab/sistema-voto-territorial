import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# CONFIGURACIÓN VISUAL
st.set_page_config(page_title="Movilización Lista 4", page_icon="🗳️")

st.markdown(
    """
    <div style="background-color:#004a99;padding:20px;border-radius:10px;border-left: 8px solid #fdb813;">
        <h1 style="color:white;text-align:center;margin:0;">PERONISMO DE TODOS</h1>
        <h3 style="color:#fdb813;text-align:center;margin:0;">Movilización Electoral - Lista 4</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SEGURIDAD ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    with st.form("login"):
        st.subheader("🔐 Ingreso de Seguridad")
        usuario = st.text_input("Nombre del Responsable")
        clave = st.text_input("Contraseña", type="password")
        if st.form_submit_button("INGRESAR"):
            if clave == "lista42026" and usuario != "":
                st.session_state['autenticado'] = True
                st.session_state['usuario_nombre'] = usuario
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.stop()

# --- CONEXIÓN ---
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form(key="voto_form", clear_on_submit=True):
    dni = st.text_input("DNI DEL VOTANTE")
    if st.form_submit_button(label="✅ REGISTRAR VOTO"):
        if dni:
            nueva_data = pd.DataFrame([{
                "DNI": dni,
                "Voto": "VOTÓ",
                "Responsable": st.session_state['usuario_nombre'],
                "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }])
            try:
                # Al usar los Secrets, no hace falta poner la URL aquí
                df_existente = conn.read()
                df_final = pd.concat([df_existente, nueva_data], ignore_index=True)
                conn.update(data=df_final)
                st.success(f"Registrado: {dni}")
                st.balloons()
            except Exception as e:
                st.error("Error de permisos. Revisá los Secrets y que el Excel sea Editor.")
        else:
            st.warning("Falta el DNI")

# AUDITORÍA
if st.sidebar.checkbox("Ver Auditoría"):
    try:
        data = conn.read()
        st.sidebar.metric("Total", len(data))
        st.write(data.tail(5))
    except:
        st.sidebar.write("Sin datos.")
