import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Movilización Lista 4", layout="centered")

# --- PASO 1: FORZAR CONEXIÓN CON GOOGLE ---
# Esto se pone antes de cualquier diseño para que el botón no se esconda
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Intentamos una lectura mínima para disparar el botón azul de 'Connect'
    test_df = conn.read(nrows=1)
    st.sidebar.success("✅ Google Sheets Conectado")
except Exception:
    st.warning("⚠️ IMPORTANTE: Haz clic en el botón azul 'Connect to Google Sheets' que aparece aquí abajo para activar el sistema.")
    # El botón aparecerá aquí automáticamente por el comando conn.read()

# --- DISEÑO DEL BANNER ---
st.markdown(
    """
    <div style="background-color:#004a99;padding:20px;border-radius:10px;border-left: 8px solid #fdb813;">
        <h1 style="color:white;text-align:center;margin:0;">PERONISMO DE TODOS</h1>
        <h3 style="color:#fdb813;text-align:center;margin:0;">Movilización Electoral - Lista 4</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# --- PASO 2: SEGURIDAD (CONTRASEÑA) ---
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
                st.error("⚠️ Nombre o Contraseña incorrectos")
    st.stop()

# --- PASO 3: FORMULARIO DE CARGA ---
st.success(f"Sesión iniciada: {st.session_state['u']}")

with st.form(key="votos", clear_on_submit=True):
    dni = st.text_input("DNI DEL VOTANTE", placeholder="Sin puntos ni espacios")
    if st.form_submit_button("✅ REGISTRAR VOTO"):
        if dni:
            try:
                # Leemos la planilla actualizada
                df = conn.read()
                # Creamos el nuevo registro
                nuevo = pd.DataFrame([{
                    "DNI": dni, 
                    "Voto": "VOTÓ", 
                    "Responsable": st.session_state['u'], 
                    "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }])
                # Unimos y subimos
                df_final = pd.concat([df, nuevo], ignore_index=True)
                conn.update(data=df_final)
                st.success(f"¡Registrado con éxito! DNI: {dni}")
                st.balloons()
            except Exception as e:
                st.error("Error al guardar. Asegúrate de haber presionado el botón azul de 'Connect' arriba.")
        else:
            st.warning("Por favor, ingresa un DNI.")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state['auth'] = False
    st.rerun()
