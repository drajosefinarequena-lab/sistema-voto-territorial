import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Movilización Electoral",
    page_icon="🗳️",
    layout="centered"
)

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

st.write("") 

# CONEXIÓN A GOOGLE SHEETS
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Error de conexión. Verifica las credenciales.")

# CUERPO DE LA APP
st.info("Registro rápido de votantes en territorio")

with st.form(key="voto_form", clear_on_submit=True):
    dni = st.text_input("DNI DEL VOTANTE", placeholder="Ej: 20123456")
    responsable = st.selectbox(
        "RESPONSABLE DE CARGA", 
        ["Seleccione su nombre", "Juan Perez", "Maria Garcia", "Pedro Rodriguez", "Equipo 1", "Equipo 2"]
    )
    submit_button = st.form_submit_button(label="✅ REGISTRAR VOTO")

    if submit_button:
        if not dni or responsable == "Seleccione su nombre":
            st.warning("⚠️ Por favor, completa el DNI y selecciona tu nombre.")
        else:
            nueva_data = pd.DataFrame([{
                "DNI": dni,
                "Voto": "VOTÓ",
                "Responsable": responsable,
                "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }])
            try:
                existing_data = conn.read()
                updated_df = pd.concat([existing_data, nueva_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"¡Registrado con éxito! DNI: {dni}")
                st.balloons()
            except Exception as e:
                st.error("Error al guardar. Revisa que el Excel esté compartido como Editor.")

# --- PANEL DE AUDITORÍA ---
st.sidebar.title("Panel de Control")

if st.sidebar.checkbox("Ver Auditoría en Vivo"):
    st.sidebar.markdown("---")
    try:
        data_audit = conn.read()
        if not data_audit.empty:
            st.sidebar.metric("Total de Votos", len(data_audit))
            st.write("### Últimos Registros")
            st.dataframe(data_audit.tail(5))
            st.write("### Votos por Responsable")
            st.bar_chart(data_audit['Responsable'].value_counts())
        else:
            st.sidebar.write("Aún no hay datos.")
    except Exception as e:
        st.sidebar.write("Error al cargar auditoría.")

st.markdown("---")
st.caption("Sistema Territorial - Peronismo de Todos © 2026")
