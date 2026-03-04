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

st.write("") # Espacio en blanco

# CONEXIÓN A GOOGLE SHEETS
# Nota: La conexión se configura en Streamlit Cloud con las Secrets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Error de conexión. Verifica las credenciales de Google Sheets.")

# CUERPO DE LA APP
st.info("Registro rápido de votantes en territorio")

with st.form(key="voto_form", clear_on_submit=True):
    # Ingreso de datos
    dni = st.text_input("DNI DEL VOTANTE", placeholder="Ej: 20123456")
    
    # Lista de Responsables/Choferes
    # Puedes cambiar los nombres en la lista de abajo
    responsable = st.selectbox(
        "RESPONSABLE DE CARGA", 
        ["Seleccione su nombre", "Juan Perez", "Maria Garcia", "Pedro Rodriguez", "Equipo 1", "Equipo 2"]
    )
    
    # Botón principal
    submit_button = st.form_submit_button(label="✅ REGISTRAR VOTO")

    if submit_button:
        if not dni or responsable == "Seleccione su nombre":
            st.warning("⚠️ Por favor, completa el DNI y selecciona tu nombre.")
        else:
            # Crear los datos a enviar
            nueva_data = pd.DataFrame([{
                "DNI": dni,
                "Voto": "VOTÓ",
                "Responsable": responsable,
                "Fecha_Hora": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }])
            
            # Leer datos actuales y agregar la nueva fila
            try:
                existing_data = conn.read()
                updated_df = pd.concat([existing_data, nueva_data], ignore_index=True)
                
                # Actualizar la planilla
                conn.update(data=updated_df)
                st.success(f"¡Registrado con éxito! DNI: {dni}")
                st.balloons() # Animación de festejo
            except Exception as e:
                st.error("No se pudo guardar en el Excel. Revisa los permisos.")

# --- PANEL DE AUDITORÍA (En la barra lateral) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Logo_del_Partido_Justicialista.png/200px-Logo_del_Partido_Justicialista.png", width=100)
st.sidebar.title("Panel de Control")

if st.sidebar.checkbox("Ver Auditoría en Vivo"):
    st.sidebar.markdown("---")
    try:
        data_audit = conn.read()
        total_votos = len(data_audit)
        st.sidebar.metric("Total de Votos", total_votos)
        
        st.write("### Últimos Movimientos")
        st.dataframe(data_audit.tail(10), use_container_width=True)
        
        # Gráfico rápido
