import streamlit as st
from datetime import date
import math

st.set_page_config(
    page_title="Simulador PYME — Rosental S.A.",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] > .main { background: #f0f2f7; }
[data-testid="block-container"] { padding-top: 0.5rem; padding-bottom: 2rem; }
#MainMenu, header, footer { visibility: hidden; }

.app-header {
    background: linear-gradient(135deg, #0f2d5e 0%, #1a4fa8 100%);
    color: white;
    padding: 16px 28px;
    border-radius: 12px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-header h1 { font-size: 1.25rem; margin: 0; font-weight: 700; }
.app-header p  { font-size: 0.73rem; opacity: 0.68; margin: 3px 0 0; }

/* ── NETO card ── */
.neto-card {
    background: linear-gradient(135deg, #054f37 0%, #059669 100%);
    color: white;
    border-radius: 16px;
    padding: 30px 28px 26px;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 6px 24px rgba(5,150,105,0.28);
}
.neto-card .nc-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.78;
    margin-bottom: 10px;
}
.neto-card .nc-amount {
    font-size: 2.7rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    line-height: 1;
    margin: 0;
}
.neto-card .nc-sub {
    font-size: 0.72rem;
    opacity: 0.65;
    margin-top: 10px;
}

/* ── Breakdown card ── */
.bk-card {
    background: white;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.bk-title {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: 1px solid #f1f5f9;
}
.bk-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    font-size: 0.82rem;
}
.bk-row.sep { border-top: 1px solid #e2e8f0; margin-top: 6px; padding-top: 8px; }
.bk-row.bold { font-weight: 700; color: #0f2d5e; font-size: 0.85rem; }
.bk-row.sgr  { color: #92400e; }
.bk-row.neto-row {
    font-weight: 800;
    color: #065f46;
    font-size: 0.92rem;
    background: #f0fdf4;
    border-radius: 8px;
    padding: 9px 10px;
    margin-top: 8px;
}
.bk-key { color: #6b7280; }
.bk-val { font-weight: 600; font-family: 'Consolas', 'Courier New', monospace; }

/* ── Instrument input card ── */
.inst-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px; height: 20px;
    background: #1a4fa8;
    color: white;
    border-radius: 50%;
    font-size: 0.64rem;
    font-weight: 700;
    margin-right: 7px;
    flex-shrink: 0;
    vertical-align: middle;
}

/* ── Labels ── */
.slabel {
    font-size: 0.63rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    color: #94a3b8;
    margin-bottom: 3px;
}
.whint {
    font-size: 0.67rem;
    color: #adb5bd;
    font-style: italic;
    margin-top: -9px;
    padding-bottom: 2px;
    min-height: 14px;
    line-height: 1.3;
}

/* ── Param card ── */
.pcrd {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 13px 15px;
    height: 100%;
}
.pcrd h4 {
    font-size: 0.67rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #6b7280;
    margin: 0 0 8px;
}
[data-testid="stNumberInput"] input { font-weight: 600; color: #1a4fa8; }
[data-testid="stTabs"] button[data-baseweb="tab"] { font-size: 0.88rem; font-weight: 600; }

/* ── Empty state ── */
.empty-state {
    background: white;
    border: 2px dashed #e2e8f0;
    border-radius: 16px;
    padding: 60px 40px;
    text-align: center;
    color: #94a3b8;
}
.empty-state .es-icon { font-size: 2.8rem; margin-bottom: 12px; }
.empty-state .es-title { font-size: 0.9rem; font-weight: 600; color: #64748b; }
.empty-state .es-sub   { font-size: 0.78rem; margin-top: 6px; }

/* ── Multi-instrument table ── */
.mit { overflow-x: auto; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 8px; }
.mit table { border-collapse: collapse; width: 100%; font-size: 0.77rem; font-family: 'Segoe UI', system-ui, sans-serif; }
.mit th { padding: 7px 9px; font-size: 0.63rem; font-weight: 700; text-transform: uppercase; letter-spacing: .3px; white-space: nowrap; text-align: right; }
.mit th:first-child { text-align: left; }
.mit td { padding: 7px 9px; text-align: right; border-bottom: 1px solid #f0f2f5; white-space: nowrap; }
.mit td:first-child { text-align: left; font-weight: 500; }
.mit tbody tr:hover td { background: #f8faff !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════
def fmt_ars(n, dec=2):
    if n is None or (isinstance(n, float) and (math.isnan(n) or math.isinf(n))):
        return "—"
    s = f"{abs(n):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if n < 0 else "") + s

def numero_a_palabras(n):
    if n is None or (isinstance(n, float) and (math.isnan(n) or math.isinf(n))):
        return ""
    ni = int(abs(n))
    if ni == 0:
        return "cero"
    ONES = ["","uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve",
            "diez","once","doce","trece","catorce","quince","dieciséis","diecisiete",
            "dieciocho","diecinueve","veinte"]
    TENS  = ["","","veinte","treinta","cuarenta","cincuenta","sesenta","setenta","ochenta","noventa"]
    HUNDS = ["","ciento","doscientos","trescientos","cuatrocientos","quinientos",
             "seiscientos","setecientos","ochocientos","novecientos"]
    def lt100(x):
        if x <= 20: return ONES[x]
        d, u = divmod(x, 10)
        if d == 2 and u: return "veinti" + ONES[u]
        return TENS[d] + (" y " + ONES[u] if u else "")
    def lt1000(x):
        if x == 0:   return ""
        if x == 100: return "cien"
        if x < 100:  return lt100(x)
        c, r = divmod(x, 100)
        return HUNDS[c] + (" " + lt100(r) if r else "")
    parts, rem = [], ni
    if rem >= 1_000_000:
        m, rem = divmod(rem, 1_000_000)
        parts.append("un millón" if m == 1 else lt1000(m) + " millones")
    if rem >= 1_000:
        k, rem = divmod(rem, 1_000)
        parts.append("mil" if k == 1 else lt1000(k) + " mil")
    if rem:
        parts.append(lt1000(rem))
    return " ".join(parts)

# ══════════════════════════════════════════════════
# FÓRMULAS (replicadas del Excel exactamente)
# ══════════════════════════════════════════════════
def get_dias(fl, fp):
    if not fl or not fp:
        return 0
    try:
        return (fp - fl).days
    except Exception:
        return 0

def calc_row(fl, fp, vn_usd, tc, tna_pct, p, garantizado):
    dias = get_dias(fl, fp)
    tna  = tna_pct / 100.0
    H = vn_usd * tc
    denom = 1 + tna * dias / 365
    J = H / denom if dias > 0 and denom != 0 else H
    K = H - J
    if dias != 0:
        L = (J * p["der"] if dias > 90 else J * p["der"] / 90 * dias)
    else:
        L = 0.0
    if H != 0:
        ar_base = H * p["com"] / 365 * dias
        M = p["boleto"] if ar_base < p["boleto"] else ar_base
    else:
        M = 0.0
    N = (L + M) * 0.21
    O = L + M + N
    P_col = H - K - O
    Q = H * p["sgr_com"] * (dias - 2) / 365
    R = H * p["sgr_caja"] * 1.21
    S = Q + R
    T = H - K - O - (S if garantizado else 0)
    return dict(dias=dias, H=H, J=J, K=K, L=L, M=M, N=N, O=O, P=P_col, Q=Q, R=R, S=S, T=T)

# ══════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════
def init():
    defaults = {
        "pg_ids": [],
        "pg_next_id": 1,
        "pg_garantizado": True,
        "p_der":      0.0600,
        "p_com":      1.5000,
        "p_boleto":   100.00,
        "p_sgr_com":  2.0000,
        "p_sgr_caja": 0.2000,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

def get_params():
    return {
        "der":      st.session_state.p_der    / 100,
        "com":      st.session_state.p_com    / 100,
        "boleto":   st.session_state.p_boleto,
        "sgr_com":  st.session_state.p_sgr_com  / 100,
        "sgr_caja": st.session_state.p_sgr_caja / 100,
    }

def pg_add():
    iid = st.session_state.pg_next_id
    st.session_state.pg_next_id += 1
    n = len(st.session_state.pg_ids) + 1
    st.session_state.pg_ids.append(iid)
    st.session_state[f"pg_n_{iid}"]   = f"Instrumento {n}"
    st.session_state[f"pg_fl_{iid}"]  = date.today()
    st.session_state[f"pg_fp_{iid}"]  = date.today()
    st.session_state[f"pg_vn_{iid}"]  = 0.0
    st.session_state[f"pg_tc_{iid}"]  = 0.0
    st.session_state[f"pg_tna_{iid}"] = 0.0

def pg_del(iid):
    st.session_state.pg_ids = [x for x in st.session_state.pg_ids if x != iid]
    for k in [f"pg_n_{iid}", f"pg_fl_{iid}", f"pg_fp_{iid}",
              f"pg_vn_{iid}", f"pg_tc_{iid}", f"pg_tna_{iid}"]:
        st.session_state.pop(k, None)

def pg_clear():
    for iid in st.session_state.pg_ids.copy():
        for k in [f"pg_n_{iid}", f"pg_fl_{iid}", f"pg_fp_{iid}",
                  f"pg_vn_{iid}", f"pg_tc_{iid}", f"pg_tna_{iid}"]:
            st.session_state.pop(k, None)
    st.session_state.pg_ids = []
    st.session_state.pg_next_id = 1

# ══════════════════════════════════════════════════
# BREAKDOWN HTML helpers
# ══════════════════════════════════════════════════
def bk_row(key, val, css=""):
    return f'<div class="bk-row {css}"><span class="bk-key">{key}</span><span class="bk-val">$ {fmt_ars(val)}</span></div>'

def single_breakdown(c, nombre, garantizado):
    sgr_block = ""
    if garantizado:
        sgr_block = f"""
        {bk_row("Com. SGR", c['Q'], "sep sgr")}
        {bk_row("Caja de Valores SGR", c['R'], "sgr")}
        {bk_row("Total SGR", c['S'], "sgr bold")}"""
    return f"""
    <div class="bk-card">
      <div class="bk-title">📋 Detalle de Liquidación — {nombre} · {int(c['dias'])} días</div>
      {bk_row("Valor Nominal Pesos", c['H'])}
      {bk_row("Importe Bruto", c['J'])}
      {bk_row("Descuento", c['K'])}
      {bk_row("Der. de Mercado", c['L'], "sep")}
      {bk_row("Arancel Rosental S.A.", c['M'])}
      {bk_row("IVA Gastos", c['N'])}
      {bk_row("Total Gastos", c['O'], "bold")}
      {bk_row("Total Boleto", c['P'], "sep bold")}
      {sgr_block}
      <div class="bk-row neto-row">
        <span>NETO A COBRAR</span>
        <span>$ {fmt_ars(c['T'])}</span>
      </div>
    </div>"""

def multi_table(rows_data, tot, garantizado):
    G  = "#f1f5f9"
    BL = "#dbeafe"
    YL = "#fef9c3"
    GN = "#dcfce7"
    TK = "#1e293b"
    TH = f"background:{G};border-bottom:2px solid #e2e8f0;"
    TS = f"background:{TK};color:#f8fafc;font-weight:700;font-size:0.81rem;"

    sgr_head = ""
    sgr_foot = ""
    if garantizado:
        sgr_head = f"""
        <th style="{TH}background:{YL};color:#92400e;">Com. SGR</th>
        <th style="{TH}background:{YL};color:#92400e;">Caja Val.</th>
        <th style="{TH}background:{YL};color:#92400e;">Tot. SGR</th>"""
        sgr_foot = f"""
        <td style="{TS}color:#fcd34d;">{fmt_ars(tot['Q'])}</td>
        <td style="{TS}color:#fcd34d;">{fmt_ars(tot['R'])}</td>
        <td style="{TS}color:#fcd34d;">{fmt_ars(tot['S'])}</td>"""

    body = ""
    for row in rows_data:
        c = row["calc"]
        sgr_tds = ""
        if garantizado:
            sgr_tds = f"""
            <td style="background:{YL};color:#92400e;">{fmt_ars(c['Q'])}</td>
            <td style="background:{YL};color:#92400e;">{fmt_ars(c['R'])}</td>
            <td style="background:{YL};color:#92400e;font-weight:600;">{fmt_ars(c['S'])}</td>"""
        body += f"""<tr>
          <td style="text-align:left;font-weight:500;">{row['nombre']}</td>
          <td style="background:{G};">{int(c['dias'])}</td>
          <td style="background:{G};">{fmt_ars(c['H'])}</td>
          <td style="background:{G};">{fmt_ars(c['J'])}</td>
          <td style="background:{G};">{fmt_ars(c['K'])}</td>
          <td style="background:{G};">{fmt_ars(c['L'])}</td>
          <td style="background:{G};">{fmt_ars(c['M'])}</td>
          <td style="background:{G};">{fmt_ars(c['N'])}</td>
          <td style="background:{G};">{fmt_ars(c['O'])}</td>
          <td style="background:{BL};color:#1d40af;font-weight:600;">{fmt_ars(c['P'])}</td>
          {sgr_tds}
          <td style="background:{GN};color:#065f46;font-weight:700;">{fmt_ars(c['T'])}</td>
        </tr>"""

    return f"""
    <div class="mit">
    <table>
    <thead><tr>
      <th style="{TH}text-align:left;min-width:120px;">Instrumento</th>
      <th style="{TH}">Días</th>
      <th style="{TH}">VN Pesos</th>
      <th style="{TH}">Imp. Bruto</th>
      <th style="{TH}">Descuento</th>
      <th style="{TH}">Der. Mercado</th>
      <th style="{TH}">Arancel</th>
      <th style="{TH}">IVA Gastos</th>
      <th style="{TH}">Tot. Gastos</th>
      <th style="{TH}background:{BL};color:#1d40af;">Tot. Boleto</th>
      {sgr_head}
      <th style="{TH}background:{GN};color:#065f46;">NETO</th>
    </tr></thead>
    <tbody>{body}</tbody>
    <tfoot><tr>
      <td style="{TS}text-align:left;">▶ TOTALES</td>
      <td style="{TS}color:#94a3b8;">—</td>
      <td style="{TS}">{fmt_ars(tot['H'])}</td>
      <td style="{TS}">{fmt_ars(tot['J'])}</td>
      <td style="{TS}">{fmt_ars(tot['K'])}</td>
      <td style="{TS}">{fmt_ars(tot['L'])}</td>
      <td style="{TS}">{fmt_ars(tot['M'])}</td>
      <td style="{TS}">{fmt_ars(tot['N'])}</td>
      <td style="{TS}">{fmt_ars(tot['O'])}</td>
      <td style="{TS}color:#93c5fd;">{fmt_ars(tot['P'])}</td>
      {sgr_foot}
      <td style="{TS}color:#86efac;font-size:0.86rem;">{fmt_ars(tot['T'])}</td>
    </tr></tfoot>
    </table></div>"""

# ══════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
  <div>
    <h1>📄 Simulador de Financiamiento PYME</h1>
    <p>Rosental S.A. Sociedad de Bolsa</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════
tab_pg, tab_ch = st.tabs(["  📄  Pagarés  ", "  📋  Cheques  "])

# ─────────────────────────────
# TAB: PAGARÉS
# ─────────────────────────────
with tab_pg:

    # Segmento
    col_seg, _ = st.columns([3, 5])
    with col_seg:
        opts = ["✅ Avalado (con SGR)", "🔓 No Garantizado"]
        sel = st.radio("**Segmento**", opts, horizontal=True,
                       index=0 if st.session_state.pg_garantizado else 1,
                       key="_pg_grt")
        st.session_state.pg_garantizado = (sel == opts[0])
    garantizado = st.session_state.pg_garantizado

    # Parameters
    with st.expander("⚙️  Gastos y Aranceles — Parámetros", expanded=False):
        nc = 4 if garantizado else 2
        pcols = st.columns(nc)
        with pcols[0]:
            st.markdown('<div class="pcrd"><h4>📊 Derechos de Mercado</h4>', unsafe_allow_html=True)
            st.number_input("Tasa anual + IVA (%)", min_value=0.0, step=0.01, format="%.4f", key="p_der")
            st.markdown("</div>", unsafe_allow_html=True)
        with pcols[1]:
            st.markdown('<div class="pcrd"><h4>🏢 Arancel Rosental S.A.</h4>', unsafe_allow_html=True)
            st.number_input("Comisión anual + IVA (%)", min_value=0.0, step=0.1, format="%.4f", key="p_com")
            st.number_input("Boleto Mínimo ($)", min_value=0.0, step=10.0, format="%.2f", key="p_boleto")
            st.markdown("</div>", unsafe_allow_html=True)
        if garantizado:
            with pcols[2]:
                st.markdown('<div class="pcrd"><h4>🔒 SGR — Comisión</h4>', unsafe_allow_html=True)
                st.number_input("Tasa anual (%)", min_value=0.0, step=0.1, format="%.4f", key="p_sgr_com")
                st.markdown("</div>", unsafe_allow_html=True)
            with pcols[3]:
                st.markdown('<div class="pcrd"><h4>🏦 SGR — Caja de Valores</h4>', unsafe_allow_html=True)
                st.number_input("Tasa × 1,21 IVA (%)", min_value=0.0, step=0.01, format="%.4f", key="p_sgr_caja")
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.7rem;color:#9ca3af;margin-top:8px;'>(*) TC Com. BNA billete vendedor</p>", unsafe_allow_html=True)

    st.markdown("---")

    # ── MAIN LAYOUT ──
    left_col, right_col = st.columns([2, 3], gap="large")

    # ── LEFT: instrument inputs ──
    with left_col:
        b1, b2 = st.columns([3, 2])
        with b1:
            if st.button("➕  Agregar Instrumento", use_container_width=True, type="primary"):
                pg_add()
                st.rerun()
        with b2:
            if st.session_state.pg_ids:
                if st.button("🗑  Limpiar", use_container_width=True):
                    pg_clear()
                    st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        for idx, iid in enumerate(st.session_state.pg_ids):
            with st.container(border=True):
                hc1, hc2 = st.columns([7, 1])
                with hc1:
                    st.markdown(
                        f'<span class="inst-num">{idx+1}</span>'
                        f'<b style="color:#0f4c81;font-size:0.83rem;vertical-align:middle;">Instrumento {idx+1}</b>',
                        unsafe_allow_html=True,
                    )
                    st.text_input("Nombre", key=f"pg_n_{iid}",
                                  label_visibility="collapsed",
                                  placeholder="Nombre del instrumento…")
                with hc2:
                    st.write("")
                    if st.button("✕", key=f"pg_del_{iid}", help="Borrar instrumento"):
                        pg_del(iid)
                        st.rerun()

                d1, d2 = st.columns(2)
                with d1:
                    st.markdown('<div class="slabel">📅 F. Liquidación</div>', unsafe_allow_html=True)
                    st.date_input("FL", key=f"pg_fl_{iid}", label_visibility="collapsed")
                with d2:
                    st.markdown('<div class="slabel">📅 F. Pago</div>', unsafe_allow_html=True)
                    st.date_input("FP", key=f"pg_fp_{iid}", label_visibility="collapsed")

                v1, v2 = st.columns(2)
                with v1:
                    st.markdown('<div class="slabel">💵 VN USD</div>', unsafe_allow_html=True)
                    vn_v = st.number_input("VN", min_value=0.0, step=1000.0, format="%.2f",
                                           key=f"pg_vn_{iid}", label_visibility="collapsed")
                    if vn_v:
                        st.markdown(f'<div class="whint">{fmt_ars(vn_v)} · <i>{numero_a_palabras(vn_v)}</i></div>',
                                    unsafe_allow_html=True)
                with v2:
                    st.markdown('<div class="slabel">🔄 Tipo de Cambio</div>', unsafe_allow_html=True)
                    tc_v = st.number_input("TC", min_value=0.0, step=10.0, format="%.2f",
                                           key=f"pg_tc_{iid}", label_visibility="collapsed")
                    if tc_v:
                        st.markdown(f'<div class="whint">{fmt_ars(tc_v)} · <i>{numero_a_palabras(tc_v)}</i></div>',
                                    unsafe_allow_html=True)

                st.markdown('<div class="slabel">📈 TNA (%)</div>', unsafe_allow_html=True)
                tna_v = st.number_input("TNA", min_value=0.0, max_value=9999.0, step=0.5, format="%.2f",
                                        key=f"pg_tna_{iid}", label_visibility="collapsed")
                if tna_v:
                    st.markdown(f'<div class="whint"><i>{numero_a_palabras(tna_v)} por ciento</i></div>',
                                unsafe_allow_html=True)

    # ── RIGHT: results ──
    with right_col:
        if not st.session_state.pg_ids:
            st.markdown("""
            <div class="empty-state">
              <div class="es-icon">📄</div>
              <div class="es-title">Agregá un instrumento para ver los resultados</div>
              <div class="es-sub">Usá el botón de la izquierda</div>
            </div>""", unsafe_allow_html=True)
        else:
            params = get_params()
            rows_data = []
            for iid in st.session_state.pg_ids:
                vn  = st.session_state.get(f"pg_vn_{iid}",  0.0)
                tc  = st.session_state.get(f"pg_tc_{iid}",  0.0)
                tna = st.session_state.get(f"pg_tna_{iid}", 0.0)
                fl  = st.session_state.get(f"pg_fl_{iid}",  date.today())
                fp  = st.session_state.get(f"pg_fp_{iid}",  date.today())
                nm  = st.session_state.get(f"pg_n_{iid}",   f"Instrumento {iid}")
                calc = calc_row(fl, fp, vn, tc, tna, params, garantizado)
                rows_data.append({"nombre": nm, "calc": calc})

            tot = {k: sum(r["calc"][k] for r in rows_data)
                   for k in ["H","J","K","L","M","N","O","P","Q","R","S","T"]}
            n_inst = len(rows_data)
            sub_txt = f"{n_inst} instrumento{'s' if n_inst > 1 else ''}"

            # Big NETO card
            st.markdown(f"""
            <div class="neto-card">
              <div class="nc-label">Neto a Cobrar</div>
              <div class="nc-amount">$ {fmt_ars(tot['T'])}</div>
              <div class="nc-sub">{sub_txt}</div>
            </div>""", unsafe_allow_html=True)

            if n_inst == 1:
                # Single instrument: full key-value breakdown
                c = rows_data[0]["calc"]
                st.markdown(single_breakdown(c, rows_data[0]["nombre"], garantizado),
                            unsafe_allow_html=True)
            else:
                # Multiple: compact per-instrument cards + full table below
                for row in rows_data:
                    c = row["calc"]
                    sgr_part = f"&nbsp;&nbsp;·&nbsp;&nbsp; SGR: <b>$ {fmt_ars(c['S'])}</b>" if garantizado else ""
                    st.markdown(f"""
                    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;
                                padding:12px 16px;margin-bottom:8px;font-size:0.81rem;">
                      <b style="color:#0f2d5e;">{row['nombre']}</b>
                      &nbsp;·&nbsp; {int(c['dias'])} días
                      <span style="float:right;font-family:monospace;">
                        Boleto: <b>$ {fmt_ars(c['P'])}</b>
                        {sgr_part}
                        &nbsp;&nbsp;→ <b style="color:#065f46;">$ {fmt_ars(c['T'])}</b>
                      </span>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                st.markdown(multi_table(rows_data, tot, garantizado), unsafe_allow_html=True)

            st.markdown("<p style='font-size:0.69rem;color:#9ca3af;'>(*) TC Com. BNA billete vendedor</p>",
                        unsafe_allow_html=True)

# ─────────────────────────────
# TAB: CHEQUES (próximamente)
# ─────────────────────────────
with tab_ch:
    st.markdown("""
    <div style="text-align:center;padding:90px 0;color:#94a3b8;">
      <div style="font-size:3rem;margin-bottom:16px;">📋</div>
      <div style="font-size:1rem;font-weight:600;color:#64748b;">Cheques — Próximamente</div>
      <div style="font-size:0.8rem;margin-top:8px;">Esta sección estará disponible en breve.</div>
    </div>""", unsafe_allow_html=True)
