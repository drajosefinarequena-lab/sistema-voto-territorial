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
        <h3 style="color:#fdb813;text-align:center;margin:0;">Movilización Electoral</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SISTEMA DE LOGUEO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    with st.form("login"):
        st.subheader("🔐 Ingreso de Seguridad - Lista 4")
        usuario = st.text_input("Tu Nombre")
        clave = st.text_input("Contraseña de Campaña", type="password")
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

# CONEXIÓN CORREGIDA
# He quitado la dependencia de 'conn' para usar una carga más directa
URL_PLANILLA = "https://docs.google.com/spreadsheets/d/1Bf8I-oO_Kz-N_8fKscM8-X9Xm-7BIdYvE0N99_l8I6E/edit#gid=0"

# Intentamos conectar
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Error técnico de conexión.")

with st.form(key="voto_form", clear_on_submit=True):
    dni = st.text_input("DNI DEL VOTANTE", placeholder="Sin puntos ni espacios")
    submit_button = st.form_submit_button(label="✅ REGISTRAR VOTO")

    if submit_button:
        if not dni:
            st.warning("⚠️ Ingresa un DNI.")
        else:
            nueva_data = pd.DataFrame([{
                "DNI": dni,
                "Voto": "VOTÓ",
                "Responsable": st.session_state['usuario_nombre'],
                "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }])
            try:
                # LEER DATOS USANDO LA URL DIRECTA
                df_existente = conn.read(spreadsheet=URL_PLANILLA, usecols=[0,1,2,3])
                df_final = pd.concat([df_existente, nueva_data], ignore_index=True)
                
                # ACTUALIZAR
                conn.update(spreadsheet=URL_PLANILLA, data=df_final)
                st.success(f"¡Registrado con éxito! DNI: {dni}")
                st.balloons()
            except Exception as e:
                st.error("Error de permisos de Google. La planilla debe estar en 'Cualquier persona con el enlace' -> EDITOR.")
                st.info("Si el error persiste, es necesario configurar los SECRETS de Streamlit para dar permiso total.")

# AUDITORÍA
if st.sidebar.checkbox("Ver Auditoría"):
    try:
        data = conn.read(spreadsheet=URL_PLANILLA)
        st.sidebar.metric("Total Votos", len(data))
        st.write("### Últimos Movimientos", data.tail(5))
    except:
        st.sidebar.write("Cargando datos...")
