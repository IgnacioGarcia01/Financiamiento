import html as _html
import math
from datetime import date, timedelta

import streamlit as st

st.set_page_config(
    page_title="Simulador PYME — Rosental S.A.",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"]>.main{background:#f0f2f7}
[data-testid="block-container"]{padding-top:.5rem;padding-bottom:2rem}
#MainMenu,header,footer{visibility:hidden}
[data-testid="stNumberInput"] label svg,
[data-testid="stTextInput"] label svg,
[data-testid="stDateInput"] label svg,
[data-testid="stNumberInput"] label a,
[data-testid="stTextInput"] label a,
[data-testid="stDateInput"] label a{display:none!important}
.app-header{background:linear-gradient(135deg,#0f2d5e,#1a4fa8);color:white;padding:16px 28px;border-radius:12px;margin-bottom:12px}
.app-header h1{font-size:1.25rem;margin:0;font-weight:700}
.app-header p{font-size:.73rem;opacity:.68;margin:3px 0 0}
.rcrd{color:white;border-radius:20px;padding:50px 40px 42px;text-align:center;margin-bottom:18px}
.rcrd.blue{background:linear-gradient(135deg,#0f2d5e,#1a4fa8)}
.rcrd.indigo{background:linear-gradient(135deg,#312e81,#4338ca)}
.rc-label{font-size:.76rem;font-weight:700;text-transform:uppercase;letter-spacing:2.8px;opacity:.72;margin-bottom:16px}
.rc-amount{font-size:4.6rem;font-weight:800;line-height:1}
.rc-words{font-size:.82rem;opacity:.74;font-style:italic;margin-top:12px}
.rc-sub2{font-size:.83rem;opacity:.84;margin-top:10px;font-weight:600}
.rc-sub{font-size:.72rem;opacity:.56;margin-top:6px}
.bk-card{background:white;border-radius:12px;border:1px solid #e2e8f0;padding:18px 20px;margin-bottom:14px}
.bk-card.total{border:2px solid #c7d7f0;background:#f8fbff}
.bk-title{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#64748b;padding-bottom:10px;margin-bottom:10px;border-bottom:1px solid #f1f5f9}
.bk-title.total-title{font-size:.8rem;color:#0f2d5e;font-weight:800}
.bk-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;font-size:.82rem}
.bk-row.sep{border-top:1px solid #e2e8f0;margin-top:6px;padding-top:8px}
.bk-row.bold{font-weight:700;color:#0f2d5e}
.bk-row.sgr{color:#92400e}
.bk-row.neto{font-weight:800;color:#1a4fa8;font-size:.92rem;background:#eff6ff;border-radius:8px;padding:9px 10px;margin-top:8px}
.bk-row.vn-result{font-weight:800;color:#312e81;font-size:.92rem;background:#eef2ff;border-radius:8px;padding:9px 10px;margin-bottom:8px}
.bk-key{color:#6b7280}
.bk-val{font-weight:600;font-family:Consolas,monospace}
.inst-num{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;background:#1a4fa8;color:white;border-radius:50%;font-size:.72rem;font-weight:700;margin-right:9px}
.slabel{font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:#475569;margin-bottom:4px}
.whint{font-size:.69rem;color:#adb5bd;font-style:italic;margin-top:-9px;padding-bottom:2px;min-height:14px}
.date-hint{font-size:.7rem;color:#3b82f6;font-style:italic;margin-top:4px;text-align:center}
.inverse-hint{font-size:.72rem;color:#64748b;margin-top:8px}
.pcrd{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px 18px;height:100%}
.pcrd h4{font-size:.9rem;font-weight:700;color:#1e3a5f;margin:0 0 3px}
.p-sub{font-size:.7rem;color:#94a3b8;margin-bottom:12px;font-style:italic}
.p-sub-label{font-size:.7rem;font-weight:600;text-transform:uppercase;color:#94a3b8;margin:10px 0 3px}
[data-testid="stNumberInput"] input{font-weight:600;color:#1a4fa8;font-size:.95rem}
div[role="radiogroup"]{background:#e8edf5;padding:4px;border-radius:10px;gap:3px;display:flex}
div[role="radiogroup"]>label{flex:1 1 auto;padding:8px 12px;border-radius:8px;font-size:.84rem;font-weight:600;text-align:center;color:#64748b;margin:0!important;white-space:nowrap;min-width:max-content}
div[role="radiogroup"]>label:has(input:checked){background:white;color:#0f2d5e;box-shadow:0 1px 5px rgba(15,45,94,.16)}
div[role="radiogroup"]>label>div:first-child{display:none!important}
[data-testid="stVerticalBlockBorderWrapper"]{border:1.5px solid #c7d7f0!important;border-radius:14px!important;background:white;box-shadow:0 2px 10px rgba(15,45,94,.07);margin-bottom:10px}
.modo-bar{background:#f1f5f9;border-radius:12px;padding:14px 18px;margin-bottom:12px}
.empty-state{background:white;border:2px dashed #e2e8f0;border-radius:16px;padding:60px 40px;text-align:center;color:#94a3b8}
.es-icon{font-size:2.8rem}
.es-title{font-size:.9rem;font-weight:600;color:#64748b}
.es-sub{font-size:.78rem;margin-top:6px}
</style>
""",
    unsafe_allow_html=True,
)

FERIADOS_ARGENTINA_2026 = {
    date(2026, 8, 17),
    date(2026, 10, 12),
    date(2026, 11, 23),
    date(2026, 12, 7),
    date(2026, 12, 8),
    date(2026, 12, 25),
}


def fmt_ars(n, dec=2):
    if n is None or isinstance(n, float) and (math.isnan(n) or math.isinf(n)):
        return "—"
    s = f"{abs(n):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if n < 0 else "") + s


def numero_a_palabras(n):
    if n is None or isinstance(n, float) and (math.isnan(n) or math.isinf(n)):
        return ""
    n = int(abs(n))
    if n == 0:
        return "cero"
    o = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte"]
    t = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
    h = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]

    def a100(x):
        if x <= 20:
            return o[x]
        d, u = divmod(x, 10)
        return ("veinti" + o[u]) if d == 2 and u else t[d] + (" y " + o[u] if u else "")

    def a1000(x):
        if x == 0:
            return ""
        if x == 100:
            return "cien"
        if x < 100:
            return a100(x)
        c, r = divmod(x, 100)
        return h[c] + (" " + a100(r) if r else "")

    p = []
    if n >= 1_000_000:
        m, n = divmod(n, 1_000_000)
        p.append("un millón" if m == 1 else a1000(m) + " millones")
    if n >= 1_000:
        k, n = divmod(n, 1_000)
        p.append("mil" if k == 1 else a1000(k) + " mil")
    if n:
        p.append(a1000(n))
    return " ".join(p)


def _dias(fl, fp):
    try:
        return max(0, (fp - fl).days)
    except (TypeError, AttributeError):
        return 0


def _sumar_dias_habiles(fecha, cantidad):
    r = fecha
    n = 0
    while n < cantidad:
        r += timedelta(days=1)
        if r.weekday() < 5 and r not in FERIADOS_ARGENTINA_2026:
            n += 1
    return r


def calc_pagare(fl, fp, vn_usd, tc, tna_pct, p, garantizado):
    d = _dias(fl, fp)
    t = tna_pct / 100
    vn = vn_usd * tc
    ib = vn / (1 + t * d / 365) if d > 0 else vn
    desc = vn - ib
    der = 0 if d == 0 else ib * p["der"] if d > 90 else ib * p["der"] * d / 90
    ar = 0 if vn == 0 else max(p["boleto"], vn * p["com"] * d / 365)
    iva = (der + ar) * 0.21
    g = der + ar + iva
    sc = vn * p["sgr_com"] * d / 365
    cv = vn * p["sgr_caja"] * 1.21
    sgr = sc + cv if garantizado else 0
    return dict(dias=d, vn_pesos=vn, importe_bruto=ib, descuento=desc, der_mercado=der, arancel=ar, iva_gastos=iva, total_gastos=g, sgr_com=sc, sgr_caja=cv, total_sgr=sgr, neto=ib - g - sgr)


def calc_cheque(fl, fp, vn, tna_pct, p, garantizado):
    d = _dias(fl, fp)
    dd = _dias(fl, _sumar_dias_habiles(fp, 2))
    t = tna_pct / 100
    ib = vn / (1 + t * dd / 365) if dd > 0 else vn
    desc = vn - ib
    der = 0 if d == 0 else ib * p["der"] if d > 90 else ib * p["der"] * d / 90
    ar = 0 if vn == 0 else max(p["boleto"], vn * p["com"] * d / 365)
    iva = (der + ar) * 0.21
    g = der + ar + iva
    sc = vn * p["sgr_com"] * d / 365
    cv = vn * p["sgr_caja"] * 1.21
    sgr = sc + cv if garantizado else 0
    return dict(dias=d, dias_descuento=dd, importe_bruto=ib, descuento=desc, der_mercado=der, arancel=ar, iva_gastos=iva, total_gastos=g, sgr_com=sc, sgr_caja=cv, total_sgr=sgr, neto=ib - g - sgr)


def _vn_desde_neto(fn, target, args, idx):
    if target <= 0:
        return 0.0
    a = list(args)
    lo = 0.0
    hi = max(target * 1.1, 1.0)
    for _ in range(60):
        a[idx] = hi
        if fn(*a)["neto"] >= target:
            break
        hi *= 2
    else:
        return 0.0
    for _ in range(70):
        mid = (lo + hi) / 2
        a[idx] = mid
        if fn(*a)["neto"] < target:
            lo = mid
        else:
            hi = mid
    return hi


def vn_from_neto_pg(target, fl, fp, tc, tna, p, g):
    return _vn_desde_neto(calc_pagare, target, [fl, fp, 0.0, tc, tna, p, g], 2)


def vn_from_neto_ch(target, fl, fp, tna, p, g):
    return _vn_desde_neto(calc_cheque, target, [fl, fp, 0.0, tna, p, g], 2)


def init():
    defaults = {
        "pg_ids": [], "pg_next_id": 1, "pg_garantizado": True, "pg_modo": "directo",
        "p_pg_der": 0.06, "p_pg_com": 1.5, "p_pg_boleto": 100.0, "p_pg_sgr_com": 2.0, "p_pg_sgr_caja": 0.05,
        "ch_ids": [], "ch_next_id": 1, "ch_garantizado": True, "ch_modo": "directo",
        "p_ch_der": 0.06, "p_ch_com": 1.0, "p_ch_boleto": 300.0, "p_ch_sgr_com": 3.85, "p_ch_sgr_caja": 0.05,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init()


def params(p):
    return {
        "der": st.session_state[f"p_{p}_der"] / 100,
        "com": st.session_state[f"p_{p}_com"] / 100,
        "boleto": st.session_state[f"p_{p}_boleto"],
        "sgr_com": st.session_state[f"p_{p}_sgr_com"] / 100,
        "sgr_caja": st.session_state[f"p_{p}_sgr_caja"] / 100,
    }


def acindar(p):
    st.session_state[f"p_{p}_sgr_caja"] = 0.4


def fechas(p, i):
    if st.session_state.get(f"{p}_mode_{i}", "plazo") == "plazo":
        fl = date.today() + timedelta(days=1 if st.session_state.get(f"{p}_t1_{i}", False) else 0)
        return fl, fl + timedelta(days=int(st.session_state.get(f"{p}_plazo_{i}", 30)))
    return st.session_state.get(f"{p}_fl_{i}", date.today()), st.session_state.get(f"{p}_fp_{i}", date.today())


def add_inst(p, tc=True):
    i = st.session_state[f"{p}_next_id"]
    st.session_state[f"{p}_next_id"] += 1
    st.session_state[f"{p}_ids"].append(i)
    n = len(st.session_state[f"{p}_ids"])
    vals = {
        f"{p}_n_{i}": f"Instrumento {n}",
        f"{p}_mode_{i}": "plazo",
        f"{p}_plazo_{i}": 30,
        f"{p}_t1_{i}": False,
        f"{p}_fl_{i}": date.today(),
        f"{p}_fp_{i}": date.today(),
        f"{p}_vn_{i}": 0.0,
        f"{p}_tna_{i}": 0.0,
        f"{p}_neto_{i}": 0.0,
    }
    if tc:
        vals[f"{p}_tc_{i}"] = 0.0
    st.session_state.update(vals)


def del_inst(p, i, tc=True):
    st.session_state[f"{p}_ids"] = [x for x in st.session_state[f"{p}_ids"] if x != i]
    for s in ("n", "mode", "plazo", "t1", "fl", "fp", "vn", "tna", "neto", "pct") + (("tc",) if tc else ()):
        st.session_state.pop(f"{p}_{s}_{i}", None)


def clear_inst(p, tc=True):
    for i in st.session_state[f"{p}_ids"].copy():
        del_inst(p, i, tc)
    st.session_state[f"{p}_next_id"] = 1


def row(k, v, css=""):
    return f'<div class="bk-row {css}"><span class="bk-key">{k}</span><span class="bk-val">$ {fmt_ars(v)}</span></div>'


def card(amount, label, words, sub1="", sub2="", color="blue"):
    return f'<div class="rcrd {color}"><div class="rc-label">{label}</div><div class="rc-amount">{amount}</div>{f"<div class=rc-words>{words}</div>" if words else ""}{f"<div class=rc-sub2>{sub1}</div>" if sub1 else ""}{f"<div class=rc-sub>{sub2}</div>" if sub2 else ""}</div>'


def body(c, g, cheque=False, inverso=False, vnu=None, vna=None, total=False):
    s = ""
    if not cheque:
        s += row("Valor Nominal Pesos", c.get("vn_pesos", 0))
    s += row("Importe Bruto", c["importe_bruto"])
    s += row("Descuento", c["descuento"])
    s += row("Der. de Mercado", c["der_mercado"], "sep")
    s += row("Comisión", c["arancel"])
    s += row("IVA Gastos", c["iva_gastos"])
    s += row("Total Gastos", c["total_gastos"], "bold")
    if g:
        s += row("Com. SGR", c["sgr_com"], "sep sgr")
        s += row("Caja de Valores SGR", c["sgr_caja"], "sgr")
        s += row("Total SGR", c["total_sgr"], "sgr bold")
    vn = ""
    if inverso and vnu is not None:
        vn = f'<div class="bk-row vn-result"><span>VALOR NOMINAL</span><span>U$S {fmt_ars(vnu)}</span></div>'
    elif inverso and vna is not None:
        vn = f'<div class="bk-row vn-result"><span>VALOR NOMINAL</span><span>$ {fmt_ars(vna)}</span></div>'
    return vn + s + f'<div class="bk-row neto"><span>{"NETO TOTAL" if total else "NETO A COBRAR"}</span><span>$ {fmt_ars(c["neto"])}</span></div>'


def breakdown(c, n, g, cheque=False, inverso=False, vnu=None, vna=None, total=False):
    title = "Resumen Total" if total else f'Detalle — {_html.escape(str(n))} · {int(c["dias"])} días'
    return f'<div class="bk-card {"total" if total else ""}"><div class="bk-title {"total-title" if total else ""}">{title}</div>{body(c, g, cheque, inverso, vnu, vna, total)}</div>'


def render_params(p, g, tc=True):
    cols = st.columns(4 if g else 2)
    sub_com = "Predeterminado: 1,50% · Boleto mín. $ 100" if p == "pg" else "Predeterminado: 1,00% · Boleto mín. $ 300"
    with cols[0]:
        st.markdown('<div class="pcrd"><h4>Derechos de Mercado</h4><div class="p-sub">Predeterminado: 0,06%</div><div class="p-sub-label">Tasa anual + IVA (%)</div>', unsafe_allow_html=True)
        st.number_input("_", key=f"p_{p}_der", min_value=0.0, step=0.01, format="%.4f", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="pcrd"><h4>Comisión Rosental S.A.</h4><div class="p-sub">{sub_com}</div><div class="p-sub-label">Comisión anual + IVA (%)</div>', unsafe_allow_html=True)
        st.number_input("__", key=f"p_{p}_com", min_value=0.0, step=0.1, format="%.4f", label_visibility="collapsed")
        st.markdown('<div class="p-sub-label">Boleto Mínimo ($)</div>', unsafe_allow_html=True)
        st.number_input("___", key=f"p_{p}_boleto", min_value=0.0, step=10.0, format="%.2f", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    if g:
        with cols[2]:
            st.markdown('<div class="pcrd"><h4>SGR — Comisión</h4><div class="p-sub">&nbsp;</div><div class="p-sub-label">Tasa anual (%)</div>', unsafe_allow_html=True)
            st.number_input("____", key=f"p_{p}_sgr_com", min_value=0.0, step=0.1, format="%.4f", label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown('<div class="pcrd"><h4>SGR — Caja de Valores</h4><div class="p-sub">Predeterminado: 0,05%</div><div class="p-sub-label">Tasa × 1,21 IVA (%)</div>', unsafe_allow_html=True)
            st.number_input("_____", key=f"p_{p}_sgr_caja", min_value=0.0, step=0.01, format="%.4f", label_visibility="collapsed")
            st.button("Acindar", key=f"{p}_acindar", use_container_width=True, on_click=acindar, args=(p,))
            st.markdown("</div>", unsafe_allow_html=True)
    if tc:
        st.caption("(*) TC: Tipo de Cambio BNA billete vendedor")


def instrument(p, idx, i, modo, tc=True):
    with st.container(border=True):
        a, b = st.columns([7, 1])
        with a:
            st.markdown(f'<span class="inst-num">{idx + 1}</span><b style="color:#0f4c81">Instrumento {idx + 1}</b>', unsafe_allow_html=True)
            st.text_input("_nm", key=f"{p}_n_{i}", label_visibility="collapsed", placeholder="Nombre del instrumento…")
        with b:
            st.write("")
            if st.button("✕", key=f"{p}_del_{i}"):
                del_inst(p, i, tc)
                st.rerun()
        if modo == "inverso":
            st.markdown('<div class="slabel">Neto a cobrar objetivo ($)</div>', unsafe_allow_html=True)
            v = st.number_input("_neto", key=f"{p}_neto_{i}", min_value=0.0, step=100000.0, format="%.2f", label_visibility="collapsed")
            if v:
                st.markdown(f'<div class="whint">{fmt_ars(v)} · <i>{numero_a_palabras(v)} pesos</i></div>', unsafe_allow_html=True)
        opts = ["Por plazo", "Por fechas"]
        cur = st.session_state.get(f"{p}_mode_{i}", "plazo")
        sel = st.radio("_mo", opts, index=0 if cur == "plazo" else 1, horizontal=True, key=f"{p}_mode_radio_{i}", label_visibility="collapsed")
        st.session_state[f"{p}_mode_{i}"] = "plazo" if sel == opts[0] else "fecha"
        if st.session_state[f"{p}_mode_{i}"] == "plazo":
            x, y = st.columns([3, 2])
            with x:
                st.markdown('<div class="slabel">Plazo (días)</div>', unsafe_allow_html=True)
                pl = st.number_input("_pl", min_value=1, max_value=1825, step=1, key=f"{p}_plazo_{i}", label_visibility="collapsed")
            with y:
                st.markdown('<div class="slabel">Liquidación</div>', unsafe_allow_html=True)
                t1 = st.toggle("T+1 (mañana)", key=f"{p}_t1_{i}")
            fl = date.today() + timedelta(days=1 if t1 else 0)
            fp = fl + timedelta(days=int(pl))
            st.markdown(f'<div class="date-hint">Liq: <b>{fl:%d/%m/%Y}</b> → Pago: <b>{fp:%d/%m/%Y}</b></div>', unsafe_allow_html=True)
        else:
            x, y = st.columns(2)
            with x:
                st.markdown('<div class="slabel">Fecha Liquidación</div>', unsafe_allow_html=True)
                st.date_input("_fl", key=f"{p}_fl_{i}", label_visibility="collapsed")
            with y:
                st.markdown('<div class="slabel">Fecha Pago</div>', unsafe_allow_html=True)
                st.date_input("_fp", key=f"{p}_fp_{i}", label_visibility="collapsed")
        if modo == "directo":
            x, y = st.columns(2) if tc else (st.container(), None)
            with x:
                st.markdown(f'<div class="slabel">{"VN USD" if tc else "VN ($)"}</div>', unsafe_allow_html=True)
                st.number_input("_vn", key=f"{p}_vn_{i}", min_value=0.0, step=1000.0, format="%.2f", label_visibility="collapsed")
            if tc:
                with y:
                    st.markdown('<div class="slabel">Tipo de Cambio</div>', unsafe_allow_html=True)
                    st.number_input("_tc", key=f"{p}_tc_{i}", min_value=0.0, step=10.0, format="%.2f", label_visibility="collapsed")
        elif tc:
            st.markdown('<div class="slabel">Tipo de Cambio</div>', unsafe_allow_html=True)
            st.number_input("_tc2", key=f"{p}_tc_{i}", min_value=0.0, step=10.0, format="%.2f", label_visibility="collapsed")
        st.markdown('<div class="slabel">TNA (%)</div>', unsafe_allow_html=True)
        st.number_input("_tna", key=f"{p}_tna_{i}", min_value=0.0, max_value=9999.0, step=0.5, format="%.2f", label_visibility="collapsed")


def results(p, g, modo, tc=True):
    ids = st.session_state[f"{p}_ids"]
    if not ids:
        st.markdown('<div class="empty-state"><div class="es-icon">📄</div><div class="es-title">Agregá un instrumento para ver los resultados</div><div class="es-sub">Usá el botón de la izquierda</div></div>', unsafe_allow_html=True)
        return
    pa = params(p)
    data = []
    cheque = not tc
    obj = sum(st.session_state.get(f"{p}_neto_{i}", 0.0) for i in ids)
    for i in ids:
        n = st.session_state.get(f"{p}_n_{i}", f"Instrumento {i}")
        tna = st.session_state.get(f"{p}_tna_{i}", 0.0)
        fl, fp = fechas(p, i)
        if modo == "directo":
            vn = st.session_state.get(f"{p}_vn_{i}", 0.0)
            tipo = st.session_state.get(f"{p}_tc_{i}", 0.0) if tc else 1.0
            c = calc_pagare(fl, fp, vn, tipo, tna, pa, g) if tc else calc_cheque(fl, fp, vn, tna, pa, g)
            r = {"nombre": n, "calc": c}
            if tc:
                r.update(vn_usd=vn, vn_pesos=c["vn_pesos"])
        else:
            target = st.session_state.get(f"{p}_neto_{i}", 0.0)
            tipo = st.session_state.get(f"{p}_tc_{i}", 0.0) if tc else 1.0
            if tc:
                vn = vn_from_neto_pg(target, fl, fp, tipo, tna, pa, g)
                c = calc_pagare(fl, fp, vn, tipo, tna, pa, g)
                r = {"nombre": n, "calc": c, "vn_usd": vn, "vn_pesos": c["vn_pesos"]}
            else:
                vn = vn_from_neto_ch(target, fl, fp, tna, pa, g)
                c = calc_cheque(fl, fp, vn, tna, pa, g)
                r = {"nombre": n, "calc": c, "vn_ars": vn}
        data.append(r)
    keys = ["importe_bruto", "descuento", "der_mercado", "arancel", "iva_gastos", "total_gastos", "sgr_com", "sgr_caja", "total_sgr", "neto"]
    if tc:
        keys = ["vn_pesos"] + keys
    tot = {k: sum(r["calc"].get(k, 0) for r in data) for k in keys}
    n = len(ids)
    txt = f"{n} instrumento{'s' if n > 1 else ''}"
    if modo == "directo":
        w = numero_a_palabras(tot["neto"])
        st.markdown(card(f'$ {fmt_ars(tot["neto"])}', "Neto a Cobrar", f"{w} pesos" if w and w != "cero" else "", sub2=txt), unsafe_allow_html=True)
    else:
        if tc:
            tot["vn_usd"] = sum(r["vn_usd"] for r in data)
            amount = f'U$S {fmt_ars(tot["vn_usd"])}'
            sub1 = f'≈ $ {fmt_ars(tot["vn_pesos"])} pesos'
            w = numero_a_palabras(tot["vn_usd"])
        else:
            tot["vn_ars"] = sum(r["vn_ars"] for r in data)
            amount = f'$ {fmt_ars(tot["vn_ars"])}'
            sub1 = ""
            w = numero_a_palabras(tot["vn_ars"])
        st.markdown(card(amount, "Valor Nominal", f'{w} {"dólares" if tc else "pesos"}' if w and w != "cero" else "", sub1, f"Neto objetivo total: $ {fmt_ars(obj)} · {txt}", "indigo"), unsafe_allow_html=True)
    for r in data:
        st.markdown(breakdown(r["calc"], r["nombre"], g, cheque, modo == "inverso", r.get("vn_usd") if modo == "inverso" else None, r.get("vn_ars") if modo == "inverso" else None), unsafe_allow_html=True)
    if n > 1:
        st.markdown(breakdown(tot, "", g, cheque, modo == "inverso", tot.get("vn_usd"), tot.get("vn_ars"), True), unsafe_allow_html=True)


def tab(p, tc=True):
    c, _ = st.columns([4, 4])
    with c:
        opts = ["Avalado", "No Garantizado"]
        s = st.radio("**Segmento**", opts, index=0 if st.session_state[f"{p}_garantizado"] else 1, horizontal=True, key=f"_{p}_grt")
        st.session_state[f"{p}_garantizado"] = s == opts[0]
    g = st.session_state[f"{p}_garantizado"]
    with st.expander("Parámetros", expanded=False):
        render_params(p, g, tc)
    st.markdown("---")
    st.markdown('<div class="modo-bar">', unsafe_allow_html=True)
    opts = ["VN → Neto", "Neto → VN"]
    s = st.radio("**Modo de cálculo**", opts, index=0 if st.session_state[f"{p}_modo"] == "directo" else 1, horizontal=True, key=f"_{p}_modo")
    st.session_state[f"{p}_modo"] = "directo" if s == opts[0] else "inverso"
    modo = st.session_state[f"{p}_modo"]
    if modo == "inverso":
        st.markdown('<div class="inverse-hint">Ingresá el neto objetivo dentro de cada instrumento. El neto total será la suma de esos importes.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    l, r = st.columns([2, 3], gap="large")
    with l:
        a, b = st.columns([3, 2])
        with a:
            if st.button("➕  Agregar Instrumento", use_container_width=True, type="primary", key=f"_{p}_add"):
                add_inst(p, tc)
                st.rerun()
        with b:
            if st.session_state[f"{p}_ids"] and st.button("🗑  Limpiar", use_container_width=True, key=f"_{p}_clr"):
                clear_inst(p, tc)
                st.rerun()
        for j, i in enumerate(st.session_state[f"{p}_ids"]):
            instrument(p, j, i, modo, tc)
    with r:
        results(p, g, modo, tc)


st.markdown('<div class="app-header"><h1>Simulador de Financiamiento PYME</h1><p>Rosental Inversiones</p></div>', unsafe_allow_html=True)
a, b = st.tabs(["  Pagarés DLK  ", "  Cheques  "])
with a:
    tab("pg", True)
with b:
    tab("ch", False)
