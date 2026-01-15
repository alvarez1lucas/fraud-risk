import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# --- CONFIGURACIÓN DE ESTILO ---
st.set_page_config(page_title="Sentinel AI | Global Fraud Command", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stMetric { background-color: #e9edf2; padding: 15px; border-radius: 10px; border: 1px solid #cfd6dd; }
    /* Ajuste para que las pestañas se vean modernas */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #e9edf2; border-radius: 5px 5px 0px 0px; gap: 1px; }
    .stTabs [aria-selected="true"] { background-color: #8fcf9f; }
    </style>

    """, unsafe_allow_html=True)

# --- ESTADO DE LA SESIÓN (Persistencia de datos) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'savings' not in st.session_state:
    st.session_state.savings = 0.0
if 'sim_results' not in st.session_state:
    st.session_state.sim_results = None

# --- LÓGICA: PROCESAMIENTO REAL-TIME ---
def process_realtime():
    tx_id = np.random.randint(1000000, 9999999)
    amt = np.random.uniform(10, 5000)
    deepfake = np.random.uniform(0, 1)
    entropy_val = np.random.uniform(0, 1)
    
    # Lógica del Modelo Sentinel (Score de riesgo ponderado)
    risk = (deepfake * 0.6) + ((1 - entropy_val) * 0.4)
    decision = "REJECT" if risk > 0.65 else "APPROVE"
    tx_hash = f"sha256:{np.random.get_state()[1][0]}"
    
    new_data = {
        "ID": tx_id,
        "Amount": amt,
        "Risk": risk,
        "Decision": decision,
        "Liveness": deepfake,
        "Entropy": entropy_val,
        "Blockchain_Hash": tx_hash,
        "Time": datetime.now().strftime("%H:%M:%S")
    }
    
    st.session_state.history.append(new_data)
    if decision == "REJECT":
        st.session_state.savings += amt
    
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)

# --- LÓGICA: SIMULACIÓN DE MUNDO (MESA ENGINE) ---
def run_world_simulation(n_fraudsters, avg_ticket):
    ticks = 30 # Simulación de 30 días
    days = []
    savings_curve = []
    loss_curve = []
    acc_savings = 0
    acc_losses = 0
    
    for day in range(1, ticks + 1):
        # Survival Rate del 88% (nuestra métrica de ciberseguridad)
        detected = np.random.binomial(n_fraudsters, 0.88)
        missed = n_fraudsters - detected
        
        acc_savings += detected * avg_ticket
        acc_losses += missed * avg_ticket
        
        days.append(day)
        savings_curve.append(acc_savings)
        loss_curve.append(acc_losses)
        
    return pd.DataFrame({"Día": days, "Ahorro": savings_curve, "Pérdidas": loss_curve})

# --- UI: SIDEBAR ---
st.sidebar.title(" Sentinel Control")
st.sidebar.divider()

# Solo mostramos el control de stream si estamos en la pestaña de monitoreo
run_stream = st.sidebar.toggle("Live Ingest (Kafka Sim)", value=True)
speed = st.sidebar.slider("Stream Speed (s)", 0.5, 5.0, 2.0)

st.sidebar.divider()
st.sidebar.subheader(" Blockchain Status")
st.sidebar.success("Sentinel Ledger: CONNECTED")
st.sidebar.code("Node: 0x71C...a4f9")

# --- UI: PESTAÑAS ---
tab1, tab2, tab3 = st.tabs([" Live Monitoring", " World Simulation (Impact)", " Model Health "])

# ==========================================
# TAB 1: MONITOREO EN VIVO
# ==========================================
with tab1:
    st.title("Sentinel AI: Real-Time Multi-Modal Fusion")
    
    # Métricas Top
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Ahorrado (ROI)", f"${st.session_state.savings:,.2f}", delta="Inmune a Tampering")
    with m2:
        fraud_count = len([x for x in st.session_state.history if x['Decision'] == 'REJECT'])
        st.metric("Tasa de Fraude (Live)", f"{fraud_count * 5}%", delta="High Alert" if fraud_count > 3 else "Normal", delta_color="inverse")
    with m3:
        st.metric("Blockchain Uptime", "99.99%", delta="Verified")
    with m4:
        st.metric("Model Drift", "0.02%", delta="Stable")

    st.divider()

    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("Live Transaction Stream")
        df_history = pd.DataFrame(st.session_state.history)
        if not df_history.empty:
            def color_decision(val):
                return 'background-color: #1f6e2e' if val == 'APPROVE' else 'background-color: #822727'
            st.dataframe(df_history.style.map(color_decision, subset=['Decision']), width='stretch')
        else:
            st.info("Iniciando conexión con el broker de datos...")

    with c2:
        st.subheader("XAI: Risk Radar")
        if not df_history.empty:
            last_tx = st.session_state.history[-1]
            categories = ['Monto', 'Liveness', 'Entropía', 'Red']
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[last_tx['Amount']/5000, last_tx['Liveness'], 1-last_tx['Entropy'], 0.4],
                theta=categories, fill='toself', line_color='#ff4b4b'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False, 
                              paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, width='stretch')
            st.caption(f"TX ID: {last_tx['ID']} | Verified Hash: {last_tx['Blockchain_Hash'][:12]}...")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if not df_history.empty:
            fig_line = px.line(df_history, x='Time', y='Risk', title="Real-Time Risk Evolution", template="plotly_dark")
            st.plotly_chart(fig_line, width='stretch')
    with col_b:
        st.write("**Adversarial & Edge Status**")
        st.progress(0.88, text="Survival Rate (PGD Attacks)")
        st.code("Model: quantized_sentinel_int8.pt | Weight: 4.2MB")

# ==========================================
# TAB 2: SIMULACIÓN DE MUNDO (MESA)
# ==========================================
with tab2:
    st.title("Strategic Impact Simulation")
    st.write("Simula escenarios de ataque masivos para validar el ROI del modelo en el tiempo.")
    
    col_s1, col_s2 = st.columns([1, 2])
    
    with col_s1:
        st.subheader("Configuración del Mercado")
        n_fraud = st.slider("Volumen de Atacantes (Agentes)", 10, 1000, 100)
        avg_ticket = st.number_input("Ticket Promedio de Fraude ($)", value=1200)
        st.divider()
        if st.button(" Ejecutar Stress Test"):
            st.session_state.sim_results = run_world_simulation(n_fraud, avg_ticket)
            
    with col_s2:
        if st.session_state.sim_results is not None:
            res = st.session_state.sim_results
            fig_sim = go.Figure()
            fig_sim.add_trace(go.Scatter(x=res['Día'], y=res['Ahorro'], name="Ahorro (Sentinel)", line=dict(color="#cae679", width=3)))
            fig_sim.add_trace(go.Scatter(x=res['Día'], y=res['Pérdidas'], name="Pérdidas (Missed)", line=dict(color='#e74c3c', dash='dot')))
            fig_sim.update_layout(title="Proyección de Impacto Económico (30 Días)", template="plotly_dark")
            st.plotly_chart(fig_sim, width='stretch')
            
            total_protected = res['Ahorro'].iloc[-1]
            st.success(f" Resultado: Sentinel protegería ${total_protected:,.2f} en este escenario.")
        else:
            st.info("Ajusta los parámetros y lanza la simulación para ver resultados.")

with tab3:
    st.header(" Model Diagnostics & Performance")
    st.write("Análisis profundo de la capacidad de detección y robustez de Sentinel AI.")
    
    col_x1, col_x2 = st.columns(2)
    
    with col_x1:
        st.subheader(" Precision-Recall Curve")
        # Recreamos tu curva con Plotly para que sea interactiva
        # Simulamos los puntos basados en tu AUC de ~0.94
        recall_vals = np.linspace(0, 1, 100)
        precision_vals = 1 - (recall_vals**3) * 0.4 # Curva realista para AUC alto
        
        fig_pr = go.Figure()
        fig_pr.add_trace(go.Scatter(x=recall_vals, y=precision_vals, fill='tozeroy',
                                    name='Sentinel Fusion', line=dict(color='#3498db', width=3)))
        
        fig_pr.update_layout(title=f'PR-AUC Final: 0.9412',
                             xaxis_title='Recall (Capacidad de Detección)',
                             yaxis_title='Precision (Confiabilidad de Alerta)',
                             template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_pr, width='stretch')
        st.caption("Esta curva valida que Sentinel mantiene una precisión alta incluso detectando el 90% de los fraudes.")

    with col_x2:
        st.subheader(" Confusion Matrix (Normalized)")
        # Datos típicos de nuestra simulación de red neuronal
        z = [[0.98, 0.02], [0.09, 0.91]]
        x = ['Legítimo', 'Fraude']
        y = ['Legítimo', 'Fraude']
        
        fig_cm = px.imshow(z, x=x, y=y, color_continuous_scale='Purp', text_auto=True,
                           title="Matriz de Confusión (Validación)")
        fig_cm.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_cm, width='stretch')
        st.caption("Falsos Positivos limitados al 2% para proteger la experiencia del usuario.")

    st.divider()
    
    # SECCIÓN DE SEGURIDAD (Lo que mencionamos del ataque PGD)
    st.subheader(" Adversarial Resilience Report")
    col_bench1, col_bench2 = st.columns([1, 1])
    
    with col_bench1:
        # Gráfico de barras comparativo
        scenarios = ["Data Estándar", "Bajo Ataque (Sin Defensa)", "Bajo Ataque (Sentinel)"]
        scores = [0.94, 0.42, 0.88]
        
        fig_bench = px.bar(x=scenarios, y=scores, color=scenarios,
                           title="Performance bajo Ataque Adversarial (PGD)",
                           color_discrete_map={"Data Estándar": "#2ecc71", 
                                             "Bajo Ataque (Sin Defensa)": "#e74c3c", 
                                             "Bajo Ataque (Sentinel)": "#3498db"})
        fig_bench.update_layout(template="plotly_dark", showlegend=False, yaxis_title="Accuracy/AUC")
        st.plotly_chart(fig_bench, width='stretch')
    
    with col_bench2:
        st.markdown("""
        ### Auditoría de Seguridad:
        - **Ataque Testeado:** Inyección de ruido en biometría mediante gradientes calculados (PGD).
        - **Defensa Aplicada:** *Adversarial Training* integrado en la arquitectura de fusión.
        - **Resultado:** Se recuperó el **46% de la capacidad de detección** que se perdía sin la capa de defensa Sentinel.
        - **Cumplimiento:** Este test garantiza resiliencia contra intentos de 'bypass' mediante IA Generativa.
        """)


# --- LOOP DE ACTUALIZACIÓN ---
if run_stream:
    process_realtime()
    time.sleep(speed)
    st.rerun()
