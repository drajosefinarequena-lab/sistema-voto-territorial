import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Movilización Electoral", page_icon="🗳️")

# BANNER DE ENCABEZADO
st.markdown(
    """
    <div style="background-color:#004a99;padding:20px;border-radius:10px;border-left: 8px solid #fdb813;">
        <h1 style="color:white;text-align:center;margin:0;">PERONISMO DE TODOS</h1>
        <h3 style="color:#fdb813;text-align:center;margin:0;">Movilización Electoral - Lista 4</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SISTEMA DE LOGUEO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    with st.form("login"):
        st.subheader("🔐 Ingreso de Seguridad")
        usuario = st.text_input("Tu Nombre")
        clave = st.text_input("Contraseña", type="password")
        btn_ingresar = st.form_submit_button("INGRESAR")
        
        if btn_ingresar:
            if clave == "lista42026" and usuario != "":
                st.session_state['autenticado'] = True
                st.session_state['usuario_nombre'] = usuario
                st.rerun()
            else:
                st.error("⚠️ Nombre o Contraseña incorrectos")
    st.stop()

st.success(f"Sesión iniciada: {st.session_state['usuario_nombre']}")

# CONEXIÓN A TU PLANILLA ESPECÍFICA
URL_PLANILLA = "https://docs.google.com/spreadsheets/d/1IUFHe5MWTbVHBp2cGzC3gGHN2eP3TpHLiaLt9AXlHDw/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Error técnico de conexión.")

with st.form(key="voto_form", clear_on_submit=True):
    dni = st.text_input("DNI DEL VOTANTE", placeholder="Ej: 20123456")
    submit_button = st.form_submit_button(label="✅ REGISTRAR VOTO")

    if submit_button:
        if not dni:
            st.warning("⚠️ Por favor, ingresa un DNI.")
        else:
            nueva_data = pd.DataFrame([{
                "DNI": dni,
                "Voto": "VOTÓ",
                "Responsable": st.session_state['usuario_nombre'],
                "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }])
            try:
                # Leemos los datos actuales de la planilla
                df_existente = conn.read(spreadsheet=URL_PLANILLA)
                # Unimos con el nuevo voto
                df_final = pd.concat([df_existente, nueva_data], ignore_index=True)
                # Subimos la planilla actualizada
                conn.update(spreadsheet=URL_PLANILLA, data=df_final)
                st.success(f"¡Registrado con éxito! DNI: {dni}")
                st.balloons()
            except Exception as e:
                st.error("Error de escritura. Revisa los permisos en Google Sheets (Cualquier persona -> EDITOR).")

# AUDITORÍA EN LA BARRA LATERAL
if st.sidebar.checkbox("Ver Auditoría"):
    try:
        data = conn.read(spreadsheet=URL_PLANILLA)
        st.sidebar.metric("Total Votos", len(data))
        st.write("### Últimos Registros", data.tail(5))
    except:
        st.sidebar.write("Cargando datos...")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state['autenticado'] = False
    st.rerun()
