import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Movilización Lista 4", layout="centered")

# ENCABEZADO
st.markdown(
    """
    <div style="background-color:#004a99;padding:20px;border-radius:10px;border-left: 8px solid #fdb813;">
        <h1 style="color:white;text-align:center;margin:0;">PERONISMO DE TODOS</h1>
        <h3 style="color:#fdb813;text-align:center;margin:0;">Movilización Electoral - Lista 4</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# --- PASO 1: CONEXIÓN OBLIGATORIA ---
st.info("🔌 Paso 1: Haz clic en el botón de abajo para autorizar el acceso al Excel.")
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Forzamos una lectura de prueba para que aparezca el botón de Google
    test_read = conn.read(nrows=1)
except Exception as e:
    st.warning("Esperando conexión con Google Sheets...")

st.markdown("---")

# --- PASO 2: SEGURIDAD (PASSWORD) ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    with st.form("login"):
        st.subheader("🔐 Ingreso de Seguridad")
        usuario = st.text_input("Tu Nombre")
        clave = st.text_input("Contraseña", type="password")
        if st.form_submit_button("INGRESAR"):
            if clave == "lista42026" and usuario != "":
                st.session_state['auth'] = True
                st.session_state['u'] = usuario
                st.rerun()
            else:
                st.error("Nombre o Contraseña incorrectos")
    st.stop()

# --- PASO 3: FORMULARIO DE CARGA ---
st.success(f"Sesión iniciada: {st.session_state['u']}")

with st.form(key="votos", clear_on_submit=True):
    dni = st.text_input("DNI DEL VOTANTE", placeholder="Sin puntos ni espacios")
    if st.form_submit_button("✅ REGISTRAR VOTO"):
        if dni:
            try:
                df = conn.read()
                nuevo = pd.DataFrame([{
                    "DNI": dni, 
                    "Voto": "VOTÓ", 
                    "Responsable": st.session_state['u'], 
                    "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }])
                df_final = pd.concat([df, nuevo], ignore_index=True)
                conn.update(data=df_final)
                st.success(f"¡Registrado con éxito! DNI: {dni}")
                st.balloons()
            except Exception as e:
                st.error("Error al guardar. Asegúrate de haber presionado el botón azul de 'Connect' arriba.")
        else:
            st.warning("Por favor, ingresa un DNI.")

# CERRAR SESIÓN
if st.button("Salir / Cambiar de Chofer"):
    st.session_state['auth'] = False
    st.rerun()
