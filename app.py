import streamlit as st
from datetime import date, timedelta
import math
import html as _html

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

[data-testid="stNumberInput"] label svg,
[data-testid="stTextInput"]   label svg,
[data-testid="stDateInput"]   label svg,
[data-testid="stNumberInput"] label a,
[data-testid="stTextInput"]   label a,
[data-testid="stDateInput"]   label a { display: none !important; }

.app-header {
    background: linear-gradient(135deg, #0f2d5e 0%, #1a4fa8 100%);
    color: white; padding: 16px 28px; border-radius: 12px; margin-bottom: 12px;
    display: flex; align-items: center; justify-content: space-between;
}
.app-header h1 { font-size: 1.25rem; margin: 0; font-weight: 700; }
.app-header p  { font-size: 0.73rem; opacity: 0.68; margin: 3px 0 0; }

/* ── Recuadro de resultado ── */
.rcrd {
    color: white; border-radius: 16px; padding: 34px 30px 28px;
    text-align: center; margin-bottom: 18px;
}
.rcrd.blue   { background: linear-gradient(135deg, #0f2d5e 0%, #1a4fa8 100%);
               box-shadow: 0 6px 28px rgba(15,45,94,0.28); }
.rcrd.indigo { background: linear-gradient(135deg, #312e81 0%, #4338ca 100%);
               box-shadow: 0 6px 28px rgba(67,56,202,0.28); }
.rcrd .rc-label {
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2.2px; opacity: 0.72; margin-bottom: 12px;
}
.rcrd .rc-amount {
    font-size: 3.2rem; font-weight: 800; letter-spacing: -0.5px; line-height: 1; margin: 0;
}
.rcrd .rc-words { font-size: 0.71rem; opacity: 0.68; font-style: italic; margin-top: 8px; line-height: 1.4; }
.rcrd .rc-sub2  { font-size: 0.75rem; opacity: 0.78; margin-top: 6px; font-weight: 600; }
.rcrd .rc-sub   { font-size: 0.67rem; opacity: 0.52; margin-top: 6px; }

/* ── Neto Objetivo card ── */
.nobj { background: #eff6ff; border: 2px solid #93c5fd; border-radius: 12px; padding: 14px 16px; margin-bottom: 12px; }
.nobj .nobj-label { font-size: 0.66rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #1a4fa8; margin-bottom: 6px; }

/* ── Breakdown ── */
.bk-card { background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 18px 20px; margin-bottom: 14px; }
.bk-title { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b;
            padding-bottom: 10px; margin-bottom: 10px; border-bottom: 1px solid #f1f5f9; }
.bk-row { display: flex; justify-content: space-between; align-items: center; padding: 4px 0; font-size: 0.82rem; }
.bk-row.sep   { border-top: 1px solid #e2e8f0; margin-top: 6px; padding-top: 8px; }
.bk-row.bold  { font-weight: 700; color: #0f2d5e; font-size: 0.85rem; }
.bk-row.sgr   { color: #92400e; }
.bk-row.neto  { font-weight: 800; color: #1a4fa8; font-size: 0.92rem;
                background: #eff6ff; border-radius: 8px; padding: 9px 10px; margin-top: 8px; }
.bk-row.vn-result { font-weight: 800; color: #312e81; font-size: 0.92rem;
                    background: #eef2ff; border-radius: 8px; padding: 9px 10px; margin-bottom: 8px; }
.bk-key { color: #6b7280; }
.bk-val { font-weight: 600; font-family: 'Consolas', 'Courier New', monospace; }

/* ── Instrument badge ── */
.inst-num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 20px; height: 20px; background: #1a4fa8; color: white;
    border-radius: 50%; font-size: 0.64rem; font-weight: 700;
    margin-right: 7px; flex-shrink: 0; vertical-align: middle;
}
.slabel { font-size: 0.63rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px; color: #94a3b8; margin-bottom: 3px; }
.whint  { font-size: 0.67rem; color: #adb5bd; font-style: italic; margin-top: -9px; padding-bottom: 2px; min-height: 14px; line-height: 1.3; }
.date-hint { font-size: 0.67rem; color: #93c5fd; font-style: italic; margin-top: 4px; text-align: center; }

/* ── Param card ── */
.pcrd { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 13px 15px; height: 100%; }
.pcrd h4 { font-size: 0.67rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #6b7280; margin: 0 0 8px; }
[data-testid="stNumberInput"] input { font-weight: 600; color: #1a4fa8; }
[data-testid="stTabs"] button[data-baseweb="tab"] { font-size: 0.86rem; font-weight: 600; }

/* ── Modo inverso toggle ── */
.modo-bar { background: #f1f5f9; border-radius: 10px; padding: 12px 16px; margin-bottom: 12px; }

/* ── Empty state ── */
.empty-state { background: white; border: 2px dashed #e2e8f0; border-radius: 16px; padding: 60px 40px; text-align: center; color: #94a3b8; }
.empty-state .es-icon  { font-size: 2.8rem; margin-bottom: 12px; }
.empty-state .es-title { font-size: 0.9rem; font-weight: 600; color: #64748b; }
.empty-state .es-sub   { font-size: 0.78rem; margin-top: 6px; }

/* ── Multi table ── */
.mit { overflow-x: auto; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 8px; }
.mit table { border-collapse: collapse; width: 100%; font-size: 0.76rem; font-family: 'Segoe UI', system-ui, sans-serif; }
.mit th { padding: 7px 9px; font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: .3px; white-space: nowrap; text-align: right; }
.mit th:first-child { text-align: left; }
.mit td { padding: 7px 9px; text-align: right; border-bottom: 1px solid #f0f2f5; white-space: nowrap; }
.mit td:first-child { text-align: left; font-weight: 500; }
.mit tbody tr:hover td { background: #f8faff !important; }

/* ── Próximamente ── */
.prox { text-align:center; padding:90px 0; color:#94a3b8; }
.prox .prox-icon  { font-size:3rem; margin-bottom:16px; }
.prox .prox-title { font-size:1rem; font-weight:600; color:#64748b; }
.prox .prox-sub   { font-size:0.8rem; margin-top:8px; }
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
    if ni == 0: return "cero"
    ONES = ["","uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve",
            "diez","once","doce","trece","catorce","quince","dieciséis","diecisiete",
            "dieciocho","diecinueve","veinte"]
    TENS  = ["","","veinte","treinta","cuarenta","cincuenta","sesenta","setenta","ochenta","noventa"]
    HUNDS = ["","ciento","doscientos","trescientos","cuatrocientos","quinientos",
             "seiscientos","setecientos","ochocientos","novecientos"]
    def lt100(x):
        if x <= 20: return ONES[x]
        d, u = divmod(x, 10)
        return ("veinti" + ONES[u]) if (d == 2 and u) else (TENS[d] + (" y " + ONES[u] if u else ""))
    def lt1000(x):
        if x == 0: return ""
        if x == 100: return "cien"
        if x < 100: return lt100(x)
        c, r = divmod(x, 100)
        return HUNDS[c] + (" " + lt100(r) if r else "")
    parts, rem = [], ni
    if rem >= 1_000_000:
        m, rem = divmod(rem, 1_000_000)
        parts.append("un millón" if m == 1 else lt1000(m) + " millones")
    if rem >= 1_000:
        k, rem = divmod(rem, 1_000)
        parts.append("mil" if k == 1 else lt1000(k) + " mil")
    if rem: parts.append(lt1000(rem))
    return " ".join(parts)

# ══════════════════════════════════════════════════
# FÓRMULAS
# ══════════════════════════════════════════════════
def _dias(fl, fp):
    try: return max(0, (fp - fl).days)
    except: return 0

def calc_pagare(fl, fp, vn_usd, tc, tna_pct, p, garantizado):
    """Cálculo pagaré USD. Retorna dict con claves nombradas."""
    dias = _dias(fl, fp)
    tna  = tna_pct / 100.0
    H = vn_usd * tc                                                   # VN pesos
    denom = 1 + tna * dias / 365
    J = H / denom if dias > 0 and denom != 0 else H                   # Importe bruto
    K = H - J                                                          # Descuento
    # Derechos mercado (sobre Importe Bruto)
    if dias == 0:    L = 0.0
    elif dias > 90:  L = J * p["der"]
    else:            L = J * p["der"] / 90 * dias
    # Arancel (sobre VN pesos)
    if H == 0:       M = 0.0
    else:
        ar = H * p["com"] / 365 * dias
        M  = p["boleto"] if ar < p["boleto"] else ar
    N   = (L + M) * 0.21                                              # IVA gastos
    O   = L + M + N                                                    # Total gastos
    Q   = H * p["sgr_com"]   * max(0, dias - 2) / 365                # Com SGR
    R   = H * p["sgr_caja"]  * 1.21                                   # Caja Val SGR
    sgr = (Q + R) if garantizado else 0.0
    T   = J - O - sgr                                                  # NETO
    return dict(dias=dias, vn_pesos=H, importe_bruto=J, descuento=K,
                der_mercado=L, arancel=M, iva_gastos=N, total_gastos=O,
                sgr_com=Q, sgr_caja=R, total_sgr=sgr, neto=T)

def calc_cheque(fl, fp, vn, tna_pct, p, garantizado):
    """Cálculo cheque ARS (sin TC). Retorna dict con claves nombradas."""
    dias = _dias(fl, fp)
    tna  = tna_pct / 100.0
    denom = 1 + tna * dias / 365
    I = vn / denom if dias > 0 and denom != 0 else vn                 # Importe bruto
    J = vn - I                                                         # Descuento
    # Derechos mercado (sobre Importe Bruto; ≤90 días → trimestral)
    if dias == 0:    L = 0.0
    elif dias > 90:  L = I * p["der"]
    else:            L = I * p["der"] / 90 * dias
    # Arancel (sobre VN)
    if vn == 0:      M = 0.0
    else:
        ar = vn * p["com"] / 365 * dias
        M  = p["boleto"] if ar < p["boleto"] else ar
    N   = (L + M) * 0.21                                              # IVA gastos
    O   = L + M + N                                                    # Total gastos
    P_c = vn * p["sgr_com"]  * max(0, dias - 3) / 365                # Com SGR (dias-3)
    Q_c = vn * p["sgr_caja"] * 1.21                                   # Caja Val SGR
    sgr = (P_c + Q_c) if garantizado else 0.0
    S   = I - O - sgr                                                  # NETO
    return dict(dias=dias, importe_bruto=I, descuento=J,
                der_mercado=L, arancel=M, iva_gastos=N, total_gastos=O,
                sgr_com=P_c, sgr_caja=Q_c, total_sgr=sgr, neto=S)

def _inv_newton(calc_fn, target, args_template, vn_idx):
    """Two-step Newton scaling: find args[vn_idx] so calc_fn(*args)['neto'] == target."""
    if target <= 0: return 0.0
    a = list(args_template)
    a[vn_idx] = max(target * 1.05, 1.0)
    c = calc_fn(*a)
    if c["neto"] <= 0: return 0.0
    vn1 = a[vn_idx] * target / c["neto"]
    a[vn_idx] = vn1
    c2 = calc_fn(*a)
    if c2["neto"] <= 0: return max(0.0, vn1)
    return max(0.0, vn1 * target / c2["neto"])

def vn_from_neto_pg(target, fl, fp, tc, tna_pct, p, garantizado):
    return _inv_newton(calc_pagare, target,
                       [fl, fp, 0.0, tc, tna_pct, p, garantizado], vn_idx=2)

def vn_from_neto_ch(target, fl, fp, tna_pct, p, garantizado):
    return _inv_newton(calc_cheque, target,
                       [fl, fp, 0.0, tna_pct, p, garantizado], vn_idx=2)

# ══════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════
def init():
    defaults = {
        # Pagarés
        "pg_ids": [], "pg_next_id": 1,
        "pg_garantizado": True,
        "pg_modo": "directo",          # "directo" | "inverso"
        "pg_neto_obj": 0.0,
        "p_pg_der":      0.0600,
        "p_pg_com":      1.5000,
        "p_pg_boleto":   100.00,
        "p_pg_sgr_com":  2.0000,
        "p_pg_sgr_caja": 0.2000,
        # Cheques
        "ch_ids": [], "ch_next_id": 1,
        "ch_garantizado": True,
        "ch_modo": "directo",
        "ch_neto_obj": 0.0,
        "p_ch_der":      0.0600,
        "p_ch_com":      1.0000,
        "p_ch_boleto":   300.00,
        "p_ch_sgr_com":  3.8500,
        "p_ch_sgr_caja": 0.2000,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

def get_params(pfx):
    return {
        "der":      st.session_state[f"p_{pfx}_der"]      / 100,
        "com":      st.session_state[f"p_{pfx}_com"]      / 100,
        "boleto":   st.session_state[f"p_{pfx}_boleto"],
        "sgr_com":  st.session_state[f"p_{pfx}_sgr_com"]  / 100,
        "sgr_caja": st.session_state[f"p_{pfx}_sgr_caja"] / 100,
    }

def resolve_dates(pfx, iid):
    mode = st.session_state.get(f"{pfx}_mode_{iid}", "plazo")
    if mode == "plazo":
        dias  = int(st.session_state.get(f"{pfx}_plazo_{iid}", 30))
        is_t1 = st.session_state.get(f"{pfx}_t1_{iid}", False)
        fl = date.today() + timedelta(days=(1 if is_t1 else 0))
        fp = fl + timedelta(days=dias)
    else:
        fl = st.session_state.get(f"{pfx}_fl_{iid}", date.today())
        fp = st.session_state.get(f"{pfx}_fp_{iid}", date.today())
    return fl, fp

def _add_inst(pfx, has_tc=True):
    iid = st.session_state[f"{pfx}_next_id"]
    st.session_state[f"{pfx}_next_id"] += 1
    n = len(st.session_state[f"{pfx}_ids"]) + 1
    st.session_state[f"{pfx}_ids"].append(iid)
    st.session_state[f"{pfx}_n_{iid}"]     = f"Instrumento {n}"
    st.session_state[f"{pfx}_mode_{iid}"]  = "plazo"
    st.session_state[f"{pfx}_plazo_{iid}"] = 30
    st.session_state[f"{pfx}_t1_{iid}"]    = False
    st.session_state[f"{pfx}_fl_{iid}"]    = date.today()
    st.session_state[f"{pfx}_fp_{iid}"]    = date.today()
    if has_tc:
        st.session_state[f"{pfx}_tc_{iid}"] = 0.0
        st.session_state[f"{pfx}_vn_{iid}"] = 0.0
    else:
        st.session_state[f"{pfx}_vn_{iid}"] = 0.0
    st.session_state[f"{pfx}_tna_{iid}"]   = 0.0
    st.session_state[f"{pfx}_pct_{iid}"]   = 0.0

def _del_inst(pfx, iid, has_tc=True):
    st.session_state[f"{pfx}_ids"] = [x for x in st.session_state[f"{pfx}_ids"] if x != iid]
    keys = [f"{pfx}_n_{iid}", f"{pfx}_mode_{iid}", f"{pfx}_plazo_{iid}", f"{pfx}_t1_{iid}",
            f"{pfx}_fl_{iid}", f"{pfx}_fp_{iid}", f"{pfx}_vn_{iid}",
            f"{pfx}_tna_{iid}", f"{pfx}_pct_{iid}"]
    if has_tc: keys.append(f"{pfx}_tc_{iid}")
    for k in keys: st.session_state.pop(k, None)

def _clear_inst(pfx, has_tc=True):
    for iid in st.session_state[f"{pfx}_ids"].copy():
        _del_inst(pfx, iid, has_tc)
    st.session_state[f"{pfx}_ids"] = []
    st.session_state[f"{pfx}_next_id"] = 1

# ══════════════════════════════════════════════════
# HTML BUILDERS
# ══════════════════════════════════════════════════
def bk_row(key, val, css="", prefix="$"):
    v = fmt_ars(val)
    return (f'<div class="bk-row {css}">'
            f'<span class="bk-key">{key}</span>'
            f'<span class="bk-val">{prefix} {v}</span>'
            f'</div>')

def result_card_html(amount_str, label, words, sub1="", sub2="", color="blue"):
    w_html = f'<div class="rc-words">{words}</div>' if words else ""
    s1_html = f'<div class="rc-sub2">{sub1}</div>' if sub1 else ""
    s2_html = f'<div class="rc-sub">{sub2}</div>' if sub2 else ""
    return (f'<div class="rcrd {color}">'
            f'<div class="rc-label">{label}</div>'
            f'<div class="rc-amount">{amount_str}</div>'
            f'{w_html}{s1_html}{s2_html}'
            f'</div>')

def breakdown_html(c, nombre, garantizado, is_cheque=False, is_inverso=False, vn_usd=None):
    safe_nm = _html.escape(str(nombre))
    rows = ""
    if not is_cheque:
        rows += bk_row("Valor Nominal Pesos", c["vn_pesos"])
    rows += bk_row("Importe Bruto",    c["importe_bruto"])
    rows += bk_row("Descuento",        c["descuento"])
    rows += bk_row("Der. de Mercado",  c["der_mercado"],  "sep")
    rows += bk_row("Arancel",          c["arancel"])
    rows += bk_row("IVA Gastos",       c["iva_gastos"])
    rows += bk_row("Total Gastos",     c["total_gastos"], "bold")
    if garantizado:
        rows += bk_row("Com. SGR",          c["sgr_com"],  "sep sgr")
        rows += bk_row("Caja de Valores SGR", c["sgr_caja"], "sgr")
        rows += bk_row("Total SGR",         c["total_sgr"],"sgr bold")
    # VN result row (only in inverse mode)
    vn_row = ""
    if is_inverso and vn_usd is not None:
        vn_row = (f'<div class="bk-row vn-result">'
                  f'<span>VALOR NOMINAL</span>'
                  f'<span>U$S {fmt_ars(vn_usd)}</span>'
                  f'</div>')
    neto_row = (f'<div class="bk-row neto">'
                f'<span>NETO A COBRAR</span>'
                f'<span>$ {fmt_ars(c["neto"])}</span>'
                f'</div>')
    title = f'📋 Detalle — {safe_nm} · {int(c["dias"])} días'
    return (f'<div class="bk-card">'
            f'<div class="bk-title">{title}</div>'
            f'{vn_row}{rows}{neto_row}'
            f'</div>')

def multi_table_html(rows_data, tot, garantizado, is_cheque=False, is_inverso=False):
    G  = "#f1f5f9"; BL = "#dbeafe"; YL = "#fef9c3"; TK = "#1e293b"
    TH = f"background:{G};border-bottom:2px solid #e2e8f0;"
    TS = f"background:{TK};color:#f8fafc;font-weight:700;font-size:0.80rem;"

    # Column defs: (label, key, bg, color, bold)
    cols = []
    if is_inverso and not is_cheque:
        cols.append(("VN USD", "vn_usd",   "#eef2ff", "#312e81", True))
    if is_inverso and is_cheque:
        cols.append(("VN ARS", "vn_ars",   "#eef2ff", "#312e81", True))
    if not is_cheque:
        cols.append(("VN Pesos",    "vn_pesos",    G,   None,  False))
    cols += [
        ("Imp. Bruto",  "importe_bruto", G,   None,  False),
        ("Descuento",   "descuento",     G,   None,  False),
        ("Der. Mercado","der_mercado",   G,   None,  False),
        ("Arancel",     "arancel",       G,   None,  False),
        ("IVA Gastos",  "iva_gastos",    G,   None,  False),
        ("Tot. Gastos", "total_gastos",  G,   None,  False),
    ]
    if garantizado:
        cols += [
            ("Com. SGR",   "sgr_com",  YL, "#92400e", False),
            ("Caja Val.",  "sgr_caja", YL, "#92400e", False),
            ("Tot. SGR",   "total_sgr",YL, "#92400e", True),
        ]
    cols.append(("NETO", "neto", BL, "#1d40af", True))

    # Header
    thead = '<tr>'
    thead += f'<th style="{TH}text-align:left;min-width:120px;">Instrumento</th>'
    thead += f'<th style="{TH}">Días</th>'
    if is_inverso:
        thead += f'<th style="{TH}">%</th>'
    for lbl, key, bg, clr, bold in cols:
        color_s = f"color:{clr};" if clr else ""
        thead += f'<th style="{TH}background:{bg};{color_s}">{lbl}</th>'
    thead += '</tr>'

    # Body
    tbody = ""
    for row in rows_data:
        c   = row["calc"]
        safe_nm = _html.escape(str(row["nombre"]))
        pct = row.get("pct", None)
        tr  = f'<tr><td style="text-align:left;font-weight:500;">{safe_nm}</td>'
        tr += f'<td style="background:{G};">{int(c["dias"])}</td>'
        if is_inverso:
            tr += f'<td style="background:{G};">{fmt_ars(pct, 1) if pct is not None else "—"}%</td>'
        for lbl, key, bg, clr, bold in cols:
            clr_s  = f"color:{clr};"  if clr  else ""
            bold_s = "font-weight:700;" if bold else ""
            val = row.get(key, c.get(key, 0))  # VN fields stored separately in row
            tr += f'<td style="background:{bg};{clr_s}{bold_s}">{fmt_ars(val)}</td>'
        tr += '</tr>'
        tbody += tr

    # Totals
    tfoot = '<tr>'
    tfoot += f'<td style="{TS}text-align:left;">▶ TOTALES</td>'
    tfoot += f'<td style="{TS}color:#94a3b8;">—</td>'
    if is_inverso:
        tfoot += f'<td style="{TS}">100%</td>'
    for lbl, key, bg, clr, bold in cols:
        clr_s = f"color:{clr};" if clr else ""
        val = tot.get(key, 0)
        tfoot += f'<td style="{TS}{clr_s}">{fmt_ars(val)}</td>'
    tfoot += '</tr>'

    return (f'<div class="mit"><table>'
            f'<thead>{thead}</thead>'
            f'<tbody>{tbody}</tbody>'
            f'<tfoot>{tfoot}</tfoot>'
            f'</table></div>')

# ══════════════════════════════════════════════════
# PARAMS EXPANDER (shared)
# ══════════════════════════════════════════════════
def render_params(pfx, garantizado):
    nc = 4 if garantizado else 2
    pc = st.columns(nc)
    with pc[0]:
        st.markdown('<div class="pcrd"><h4>📊 Derechos de Mercado</h4>', unsafe_allow_html=True)
        st.markdown('<div class="slabel">Tasa anual + IVA (%)</div>', unsafe_allow_html=True)
        st.number_input("_", key=f"p_{pfx}_der", min_value=0.0, step=0.01, format="%.4f",
                        label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    with pc[1]:
        st.markdown('<div class="pcrd"><h4>🏢 Arancel Rosental S.A.</h4>', unsafe_allow_html=True)
        st.markdown('<div class="slabel">Comisión anual + IVA (%)</div>', unsafe_allow_html=True)
        st.number_input("__", key=f"p_{pfx}_com", min_value=0.0, step=0.1, format="%.4f",
                        label_visibility="collapsed")
        st.markdown('<div class="slabel" style="margin-top:6px;">Boleto Mínimo ($)</div>', unsafe_allow_html=True)
        st.number_input("___", key=f"p_{pfx}_boleto", min_value=0.0, step=10.0, format="%.2f",
                        label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    if garantizado:
        with pc[2]:
            st.markdown('<div class="pcrd"><h4>🔒 SGR — Comisión</h4>', unsafe_allow_html=True)
            st.markdown('<div class="slabel">Tasa anual (%)</div>', unsafe_allow_html=True)
            st.number_input("____", key=f"p_{pfx}_sgr_com", min_value=0.0, step=0.1, format="%.4f",
                            label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
        with pc[3]:
            st.markdown('<div class="pcrd"><h4>🏦 SGR — Caja de Valores</h4>', unsafe_allow_html=True)
            st.markdown('<div class="slabel">Tasa × 1,21 IVA (%)</div>', unsafe_allow_html=True)
            st.number_input("_____", key=f"p_{pfx}_sgr_caja", min_value=0.0, step=0.01, format="%.4f",
                            label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem;color:#9ca3af;margin-top:8px;'>(*) TC Com. BNA billete vendedor</p>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# INSTRUMENT CARD (shared renderer)
# ══════════════════════════════════════════════════
def render_inst_card(pfx, idx, iid, modo_calc, n_inst, has_tc=True):
    """Renderiza la card de inputs de un instrumento."""
    with st.container(border=True):
        hc1, hc2 = st.columns([7, 1])
        with hc1:
            st.markdown(
                f'<span class="inst-num">{idx+1}</span>'
                f'<b style="color:#0f4c81;font-size:0.83rem;vertical-align:middle;">'
                f'Instrumento {idx+1}</b>',
                unsafe_allow_html=True,
            )
            st.text_input("_nm", key=f"{pfx}_n_{iid}", label_visibility="collapsed",
                          placeholder="Nombre del instrumento…")
        with hc2:
            st.write("")
            if st.button("✕", key=f"{pfx}_del_{iid}", help="Borrar"):
                _del_inst(pfx, iid, has_tc)
                st.rerun()

        # % en modo inverso con >1 instrumentos
        if modo_calc == "inverso" and n_inst > 1:
            st.markdown('<div class="slabel">% del Neto Total</div>', unsafe_allow_html=True)
            st.number_input("_pct", key=f"{pfx}_pct_{iid}", min_value=0.0, max_value=100.0,
                            step=1.0, format="%.1f", label_visibility="collapsed")

        # Modo plazo / fecha
        mode_opts = ["📅 Por plazo", "📆 Por fechas"]
        cur = "plazo" if st.session_state.get(f"{pfx}_mode_{iid}", "plazo") == "plazo" else "fecha"
        m_sel = st.radio("_mo", mode_opts, index=0 if cur == "plazo" else 1,
                         horizontal=True, key=f"{pfx}_mode_radio_{iid}",
                         label_visibility="collapsed")
        st.session_state[f"{pfx}_mode_{iid}"] = "plazo" if m_sel == mode_opts[0] else "fecha"

        if st.session_state[f"{pfx}_mode_{iid}"] == "plazo":
            pa, pb = st.columns([3, 2])
            with pa:
                st.markdown('<div class="slabel">⏱ Plazo (días)</div>', unsafe_allow_html=True)
                plazo_v = st.number_input("_pl", min_value=1, max_value=1825, step=1,
                                          key=f"{pfx}_plazo_{iid}", label_visibility="collapsed")
            with pb:
                st.markdown('<div class="slabel">📅 Liquidación</div>', unsafe_allow_html=True)
                is_t1 = st.toggle("T+1 (mañana)", key=f"{pfx}_t1_{iid}")
            fl_p = date.today() + timedelta(days=(1 if is_t1 else 0))
            fp_p = fl_p + timedelta(days=int(plazo_v))
            st.markdown(
                f'<div class="date-hint">Liq: <b>{fl_p.strftime("%d/%m/%Y")}</b>'
                f' → Pago: <b>{fp_p.strftime("%d/%m/%Y")}</b></div>',
                unsafe_allow_html=True,
            )
        else:
            d1, d2 = st.columns(2)
            with d1:
                st.markdown('<div class="slabel">📅 F. Liquidación</div>', unsafe_allow_html=True)
                st.date_input("_fl", key=f"{pfx}_fl_{iid}", label_visibility="collapsed")
            with d2:
                st.markdown('<div class="slabel">📅 F. Pago</div>', unsafe_allow_html=True)
                st.date_input("_fp", key=f"{pfx}_fp_{iid}", label_visibility="collapsed")

        # VN (solo en modo directo)
        if modo_calc == "directo":
            v1, v2 = (st.columns(2) if has_tc else (st.container(), None))
            with v1:
                lbl_vn = "💵 VN USD" if has_tc else "💵 VN ($)"
                st.markdown(f'<div class="slabel">{lbl_vn}</div>', unsafe_allow_html=True)
                vn_v = st.number_input("_vn", min_value=0.0, step=1000.0, format="%.2f",
                                       key=f"{pfx}_vn_{iid}", label_visibility="collapsed")
                if vn_v:
                    st.markdown(f'<div class="whint">{fmt_ars(vn_v)} · <i>{numero_a_palabras(vn_v)}</i></div>',
                                unsafe_allow_html=True)
            if has_tc and v2 is not None:
                with v2:
                    st.markdown('<div class="slabel">🔄 Tipo de Cambio</div>', unsafe_allow_html=True)
                    tc_v = st.number_input("_tc", min_value=0.0, step=10.0, format="%.2f",
                                           key=f"{pfx}_tc_{iid}", label_visibility="collapsed")
                    if tc_v:
                        st.markdown(f'<div class="whint">{fmt_ars(tc_v)} · <i>{numero_a_palabras(tc_v)}</i></div>',
                                    unsafe_allow_html=True)
        else:
            # Inverso: TC sí se necesita para convertir, pero VN es calculado
            if has_tc:
                st.markdown('<div class="slabel">🔄 Tipo de Cambio</div>', unsafe_allow_html=True)
                tc_v = st.number_input("_tc2", min_value=0.0, step=10.0, format="%.2f",
                                       key=f"{pfx}_tc_{iid}", label_visibility="collapsed")
                if tc_v:
                    st.markdown(f'<div class="whint">{fmt_ars(tc_v)} · <i>{numero_a_palabras(tc_v)}</i></div>',
                                unsafe_allow_html=True)

        # TNA
        st.markdown('<div class="slabel">📈 TNA (%)</div>', unsafe_allow_html=True)
        tna_v = st.number_input("_tna", min_value=0.0, max_value=9999.0, step=0.5, format="%.2f",
                                key=f"{pfx}_tna_{iid}", label_visibility="collapsed")
        if tna_v:
            st.markdown(f'<div class="whint"><i>{numero_a_palabras(tna_v)} por ciento</i></div>',
                        unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# RESULTS COLUMN
# ══════════════════════════════════════════════════
def render_results(pfx, garantizado, modo_calc, has_tc=True):
    ids = st.session_state[f"{pfx}_ids"]
    if not ids:
        st.markdown("""<div class="empty-state">
          <div class="es-icon">📄</div>
          <div class="es-title">Agregá un instrumento para ver los resultados</div>
          <div class="es-sub">Usá el botón de la izquierda</div>
        </div>""", unsafe_allow_html=True)
        return

    p      = get_params(pfx)
    neto_obj = st.session_state.get(f"{pfx}_neto_obj", 0.0)
    rows_data = []
    n_inst  = len(ids)
    is_ch   = not has_tc

    for iid in ids:
        nm  = st.session_state.get(f"{pfx}_n_{iid}", f"Instrumento {iid}")
        tna = st.session_state.get(f"{pfx}_tna_{iid}", 0.0)
        pct = st.session_state.get(f"{pfx}_pct_{iid}", 0.0)
        fl, fp = resolve_dates(pfx, iid)

        if modo_calc == "directo":
            vn   = st.session_state.get(f"{pfx}_vn_{iid}", 0.0)
            tc   = st.session_state.get(f"{pfx}_tc_{iid}", 0.0) if has_tc else 1.0
            calc_fn = calc_pagare if has_tc else calc_cheque
            args = (fl, fp, vn, tc, tna, p, garantizado) if has_tc else (fl, fp, vn, tna, p, garantizado)
            c = calc_fn(*args)
            row = dict(nombre=nm, calc=c, pct=pct)
            if not is_ch:
                row["vn_usd"]  = vn
                row["vn_pesos"] = c["vn_pesos"]
        else:
            tc = st.session_state.get(f"{pfx}_tc_{iid}", 0.0) if has_tc else 1.0
            target_i = neto_obj * (pct / 100.0) if n_inst > 1 else neto_obj
            if has_tc:
                vn_usd = vn_from_neto_pg(target_i, fl, fp, tc, tna, p, garantizado)
                c = calc_pagare(fl, fp, vn_usd, tc, tna, p, garantizado)
                row = dict(nombre=nm, calc=c, pct=pct, vn_usd=vn_usd, vn_pesos=c["vn_pesos"])
            else:
                vn_ars = vn_from_neto_ch(target_i, fl, fp, tna, p, garantizado)
                c = calc_cheque(fl, fp, vn_ars, tna, p, garantizado)
                row = dict(nombre=nm, calc=c, pct=pct, vn_ars=vn_ars)

        rows_data.append(row)

    # Validation for inverse mode with percentages
    if modo_calc == "inverso" and n_inst > 1:
        total_pct = sum(st.session_state.get(f"{pfx}_pct_{iid}", 0.0) for iid in ids)
        if abs(total_pct - 100.0) > 0.01:
            st.warning(f"Los porcentajes suman {fmt_ars(total_pct, 1)}%. Deben sumar exactamente 100%.")
            return

    # Totals
    keys_sum = ["importe_bruto","descuento","der_mercado","arancel","iva_gastos",
                "total_gastos","sgr_com","sgr_caja","total_sgr","neto"]
    if not is_ch: keys_sum = ["vn_pesos"] + keys_sum
    tot = {k: sum(r["calc"].get(k, 0) for r in rows_data) for k in keys_sum}
    # VN totals for inverse
    if modo_calc == "inverso":
        if has_tc:
            tot["vn_usd"]   = sum(r.get("vn_usd", 0) for r in rows_data)
            tot["vn_pesos"] = sum(r.get("vn_pesos", 0) for r in rows_data)
        else:
            tot["vn_ars"] = sum(r.get("vn_ars", 0) for r in rows_data)

    # ── Big result card ──
    sub_txt = f"{n_inst} instrumento{'s' if n_inst > 1 else ''}"
    if modo_calc == "directo":
        amount  = f"$ {fmt_ars(tot['neto'])}"
        words   = numero_a_palabras(tot['neto'])
        words_s = f"{words} pesos" if words and words != "cero" else ""
        st.markdown(result_card_html(amount, "Neto a Cobrar", words_s, sub2=sub_txt, color="blue"),
                    unsafe_allow_html=True)
    else:
        if has_tc:
            vn_show   = tot["vn_usd"]
            vn_ars    = tot.get("vn_pesos", 0)
            amount    = f"U$S {fmt_ars(vn_show)}"
            words     = numero_a_palabras(vn_show)
            words_s   = f"{words} dólares" if words and words != "cero" else ""
            sub1      = f"≈ $ {fmt_ars(vn_ars)} pesos"
            sub2      = f"Neto objetivo: $ {fmt_ars(neto_obj)} · {sub_txt}"
        else:
            vn_show   = tot["vn_ars"]
            amount    = f"$ {fmt_ars(vn_show)}"
            words     = numero_a_palabras(vn_show)
            words_s   = f"{words} pesos" if words and words != "cero" else ""
            sub1      = ""
            sub2      = f"Neto objetivo: $ {fmt_ars(neto_obj)} · {sub_txt}"
        st.markdown(result_card_html(amount, "Valor Nominal", words_s, sub1=sub1, sub2=sub2, color="indigo"),
                    unsafe_allow_html=True)

    if n_inst == 1:
        row = rows_data[0]
        vn_usd_arg = row.get("vn_usd") if (modo_calc == "inverso" and has_tc) else None
        st.markdown(breakdown_html(row["calc"], row["nombre"], garantizado,
                                   is_cheque=is_ch,
                                   is_inverso=(modo_calc == "inverso"),
                                   vn_usd=vn_usd_arg),
                    unsafe_allow_html=True)
    else:
        for row in rows_data:
            c = row["calc"]
            safe_nm = _html.escape(str(row["nombre"]))
            if modo_calc == "inverso" and has_tc:
                vn_ref = f'VN: <b>U$S {fmt_ars(row.get("vn_usd",0))}</b> &nbsp;·&nbsp; '
            elif modo_calc == "inverso":
                vn_ref = f'VN: <b>$ {fmt_ars(row.get("vn_ars",0))}</b> &nbsp;·&nbsp; '
            else:
                vn_ref = ""
            st.markdown(
                f'<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;'
                f'padding:11px 16px;margin-bottom:7px;font-size:0.80rem;">'
                f'<b style="color:#0f2d5e;">{safe_nm}</b> · {int(c["dias"])} días'
                f'<span style="float:right;font-family:monospace;">'
                f'{vn_ref}NETO → <b style="color:#1a4fa8;">$ {fmt_ars(c["neto"])}</b>'
                f'</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        st.markdown(multi_table_html(rows_data, tot, garantizado,
                                     is_cheque=is_ch,
                                     is_inverso=(modo_calc == "inverso")),
                    unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.69rem;color:#9ca3af;'>(*) TC Com. BNA billete vendedor</p>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TAB RENDERER (shared for pg and ch)
# ══════════════════════════════════════════════════
def render_tab(pfx, has_tc=True):
    grt_key  = f"{pfx}_garantizado"
    modo_key = f"{pfx}_modo"
    nobj_key = f"{pfx}_neto_obj"

    # ── Segmento ──
    col_seg, _ = st.columns([3, 5])
    with col_seg:
        opts = ["✅ Avalado (con SGR)", "🔓 No Garantizado"]
        sel  = st.radio("**Segmento**", opts, horizontal=True,
                        index=0 if st.session_state[grt_key] else 1,
                        key=f"_{pfx}_grt")
        st.session_state[grt_key] = (sel == opts[0])
    garantizado = st.session_state[grt_key]

    # ── Parámetros ──
    with st.expander("⚙️  Gastos y Aranceles — Parámetros", expanded=False):
        render_params(pfx, garantizado)

    st.markdown("---")

    # ── Modo de cálculo ──
    st.markdown('<div class="modo-bar">', unsafe_allow_html=True)
    mc_opts = ["🔢  VN → Neto (directo)", "🔄  Neto → VN (inverso)"]
    mc_sel  = st.radio("**Modo de cálculo**", mc_opts, horizontal=True,
                       index=0 if st.session_state[modo_key] == "directo" else 1,
                       key=f"_{pfx}_modo")
    st.session_state[modo_key] = "directo" if mc_sel == mc_opts[0] else "inverso"
    modo_calc = st.session_state[modo_key]

    if modo_calc == "inverso":
        st.markdown('<div class="nobj"><div class="nobj-label">🎯 Neto a Cobrar Objetivo</div>',
                    unsafe_allow_html=True)
        nobj_v = st.number_input("_nobj", key=nobj_key, min_value=0.0, step=100000.0,
                                 format="%.2f", label_visibility="collapsed")
        if nobj_v:
            st.markdown(f'<div class="whint">{fmt_ars(nobj_v)} · <i>{numero_a_palabras(nobj_v)} pesos</i></div>',
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Layout principal ──
    left_col, right_col = st.columns([2, 3], gap="large")

    with left_col:
        b1, b2 = st.columns([3, 2])
        with b1:
            if st.button("➕  Agregar Instrumento", use_container_width=True, type="primary",
                         key=f"_{pfx}_add"):
                _add_inst(pfx, has_tc)
                st.rerun()
        with b2:
            if st.session_state[f"{pfx}_ids"]:
                if st.button("🗑  Limpiar", use_container_width=True, key=f"_{pfx}_clr"):
                    _clear_inst(pfx, has_tc)
                    st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        n_inst = len(st.session_state[f"{pfx}_ids"])
        for idx, iid in enumerate(st.session_state[f"{pfx}_ids"]):
            render_inst_card(pfx, idx, iid, modo_calc, n_inst, has_tc)

    with right_col:
        render_results(pfx, garantizado, modo_calc, has_tc)

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
tab_pg, tab_ch, tab_hd, tab_cmp = st.tabs([
    "  📄  Pagarés  ",
    "  📋  Cheques  ",
    "  💵  Pagaré Hard Dollar  ",
    "  ⚖️  Comparación  ",
])

with tab_pg:
    render_tab("pg", has_tc=True)

with tab_ch:
    render_tab("ch", has_tc=False)

with tab_hd:
    st.markdown("""<div class="prox">
      <div class="prox-icon">💵</div>
      <div class="prox-title">Pagaré Hard Dollar — Próximamente</div>
      <div class="prox-sub">Simulador de pagarés liquidados en dólares billete.</div>
    </div>""", unsafe_allow_html=True)

with tab_cmp:
    st.markdown("""<div class="prox">
      <div class="prox-icon">⚖️</div>
      <div class="prox-title">Comparación — Próximamente</div>
      <div class="prox-sub">Comparación de condiciones entre distintos instrumentos y segmentos.</div>
    </div>""", unsafe_allow_html=True)
