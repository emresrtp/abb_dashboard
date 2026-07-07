import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, os, math, requests
import google.generativeai as genai

ABB_LOGO_B64 = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IiNmZjAwMGYiIHZpZXdCb3g9Ii0xIC0xIDg4LjIgMzUiPgogIDxwYXRoIGQ9Ik00NyAzM2gyYzYtLjMgMTAuMi01IDEwLjItMTAuNiAwLTEuOS0uNC0zLjgtMS4zLTUuM0g0N1YzM3oiPjwvcGF0aD4KICA8cmVjdCB3aWR0aD0iMTAiIGhlaWdodD0iMTYiIHg9IjM2IiB5PSIxNyI+PC9yZWN0PgogIDxwYXRoIGQ9Ik01Ny4zIDE2Yy0xLTEuNC0yLjQtMi41LTMuOS0zLjMgMS44LTEuMyAzLTMuNCAzLTUuNyAwLTMuOS0zLjEtNy03LTdINDd2MTZoMTAuM3oiPjwvcGF0aD4KICA8cmVjdCB3aWR0aD0iMTAiIGhlaWdodD0iMTYiIHg9IjM2Ij48L3JlY3Q+CiAgPHBhdGggZD0iTTc0IDMzaDJjNi0uMyAxMC4yLTUgMTAuMi0xMC42IDAtMS45LS40LTMuOC0xLjMtNS4zSDc0VjMzeiI+PC9wYXRoPgogIDxyZWN0IHdpZHRoPSIxMCIgaGVpZ2h0PSIxNiIgeD0iNjMiIHk9IjE3Ij48L3JlY3Q+CiAgPHBhdGggZD0iTTg0LjMgMTZjLTEtMS40LTIuNC0yLjUtMy45LTMuMyAxLjgtMS4zIDMtMy40IDMtNS43IDAtMy45LTMuMS03LTctN0g3NHYxNmgxMC4zeiI+PC9wYXRoPgogIDxyZWN0IHdpZHRoPSIxMCIgaGVpZ2h0PSIxNiIgeD0iNjMiPjwvcmVjdD4KICA8cG9seWdvbiBwb2ludHM9IjUuNywxNyAwLDMzIDguMywzMyAxMC43LDI2IDE2LDI2IDE2LDE3Ij48L3BvbHlnb24+CiAgPHBvbHlnb24gcG9pbnRzPSIxNiwwIDExLjcsMCA2LDE2IDE2LDE2Ij48L3BvbHlnb24+CiAgPHBvbHlnb24gcG9pbnRzPSIxNywyNiAyMi4zLDI2IDI0LjcsMzMgMzMsMzMgMjcuMywxNyAxNywxNyI+PC9wb2x5Z29uPgogIDxwb2x5Z29uIHBvaW50cz0iMjcsMTYgMjEuMywwIDE3LDAgMTcsMTYiPjwvcG9seWdvbj4KPC9zdmc+Cg=="

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ABB | Firma Veritabanı",
    page_icon="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IiNmZjAwMGYiIHZpZXdCb3g9Ii0xIC0xIDg4LjIgMzUiPgogIDxwYXRoIGQ9Ik00NyAzM2gyYzYtLjMgMTAuMi01IDEwLjItMTAuNiAwLTEuOS0uNC0zLjgtMS4zLTUuM0g0N1YzM3oiPjwvcGF0aD4KICA8cmVjdCB3aWR0aD0iMTAiIGhlaWdodD0iMTYiIHg9IjM2IiB5PSIxNyI+PC9yZWN0PgogIDxwYXRoIGQ9Ik01Ny4zIDE2Yy0xLTEuNC0yLjQtMi41LTMuOS0zLjMgMS44LTEuMyAzLTMuNCAzLTUuNyAwLTMuOS0zLjEtNy03LTdINDd2MTZoMTAuM3oiPjwvcGF0aD4KICA8cmVjdCB3aWR0aD0iMTAiIGhlaWdodD0iMTYiIHg9IjM2Ij48L3JlY3Q+CiAgPHBhdGggZD0iTTc0IDMzaDJjNi0uMyAxMC4yLTUgMTAuMi0xMC42IDAtMS45LS40LTMuOC0xLjMtNS4zSDc0VjMzeiI+PC9wYXRoPgogIDxyZWN0IHdpZHRoPSIxMCIgaGVpZ2h0PSIxNiIgeD0iNjMiIHk9IjE3Ij48L3JlY3Q+CiAgPHBhdGggZD0iTTg0LjMgMTZjLTEtMS40LTIuNC0yLjUtMy45LTMuMyAxLjgtMS4zIDMtMy40IDMtNS43IDAtMy45LTMuMS03LTctN0g3NHYxNmgxMC4zeiI+PC9wYXRoPgogIDxyZWN0IHdpZHRoPSIxMCIgaGVpZ2h0PSIxNiIgeD0iNjMiPjwvcmVjdD4KICA8cG9seWdvbiBwb2ludHM9IjUuNywxNyAwLDMzIDguMywzMyAxMC43LDI2IDE2LDI2IDE2LDE3Ij48L3BvbHlnb24+CiAgPHBvbHlnb24gcG9pbnRzPSIxNiwwIDExLjcsMCA2LDE2IDE2LDE2Ij48L3BvbHlnb24+CiAgPHBvbHlnb24gcG9pbnRzPSIxNywyNiAyMi4zLDI2IDI0LjcsMzMgMzMsMzMgMjcuMywxNyAxNywxNyI+PC9wb2x5Z29uPgogIDxwb2x5Z29uIHBvaW50cz0iMjcsMTYgMjEuMywwIDE3LDAgMTcsMTYiPjwvcG9seWdvbj4KPC9zdmc+Cg==",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', Arial, sans-serif !important; }
.stApp { background-color: #f4f6f9; }
.topbar {
    background: #1a1a2e; color: #fff;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px; height: 60px; border-radius: 0 0 8px 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,.3); margin-bottom: 22px;
}
.topbar-title { font-size: 1rem; font-weight: 600; color: #eee; margin-left: 14px; }
.topbar-right { font-size: .78rem; color: #aaa; }
[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e0e0e0 !important; }
[data-testid="stSidebar"] * { color: #222 !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label {
    color: #666 !important; font-size: .75rem !important;
    text-transform: uppercase; letter-spacing: 1px; font-weight: 700 !important;
}
.stat-card {
    background: #fff; border-radius: 10px; padding: 16px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,.07); border-left: 4px solid #FF000F; margin-bottom: 6px;
}
.stat-card .val { font-size: 1.9rem; font-weight: 800; color: #FF000F; line-height: 1; }
.stat-card .lbl { font-size: .72rem; color: #888; text-transform: uppercase; letter-spacing: .8px; margin-top: 4px; font-weight: 600; }
.stat-card-blue { border-left-color: #6764f6 !important; }
.stat-card-blue .val { color: #6764f6 !important; }
.sec-title {
    font-size: .78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #444;
    border-bottom: 2px solid #FF000F; padding-bottom: 6px; margin: 4px 0 12px;
}
.tbl-wrap { background: #fff; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,.07); overflow: hidden; margin-top: 4px; }
.tbl-wrap table { width: 100%; border-collapse: collapse; font-size: .82rem; }
.tbl-wrap thead th {
    background: #1a2740; color: #cdd6e8;
    padding: 10px 12px; text-align: left; font-size: .72rem;
    text-transform: uppercase; letter-spacing: .5px; white-space: nowrap;
}
.tbl-wrap tbody tr { border-bottom: 1px solid #f0f0f0; transition: background .12s; }
.tbl-wrap tbody tr:last-child { border-bottom: none; }
.tbl-wrap tbody tr:hover { background: #fafafa; }
.tbl-wrap td { padding: 9px 12px; vertical-align: middle; color: #222; }
.tbl-wrap td .firma-name { font-weight: 700; color: #1a1a2e; font-size: .84rem; }
.badge-cat { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: .7rem; font-weight: 600; background: #ffdccd; color: #FF000F; }
.badge-city { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: .7rem; font-weight: 600; background: #e8f4fd; color: #1565c0; }
.web-link { color: #FF000F; text-decoration: none; font-size: .79rem; font-weight: 600; }
.web-link:hover { text-decoration: underline; }
.prod-cell { max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: .74rem; color: #777; }
.pager-info { font-size: .78rem; color: #888; text-align: center; margin-top: 6px; }
.inter-panel {
    background: #f9f9ff; border-radius: 10px;
    border: 1px solid #e4e7ff; padding: 16px 20px; margin-top: 10px;
}
.ai-box {
    background: linear-gradient(135deg,#f0f2ff,#e8e4ff);
    border-left: 4px solid #6764f6; border-radius: 8px;
    padding: 14px; font-size: .82rem; color: #222; margin-top: 10px; line-height: 1.7;
}
.note-saved {
    background: #fffbf0; border: 1px solid #f5c542;
    border-radius: 7px; padding: 10px 13px; font-size: .8rem; color: #555; margin: 8px 0;
}
.del-warning {
    background: #fff5f5; border: 1px solid #ffcdd2; border-radius: 8px;
    padding: 14px 18px; font-size: .84rem; color: #c62828; margin: 10px 0;
}
.edit-panel {
    background: #f8faff; border: 1px solid #dde5ff; border-radius: 8px;
    padding: 16px 18px; margin-top: 8px;
}
.map-hint {
    font-size: .74rem; color: #888; text-align: center;
    padding: 6px; background: #f8f8f8; border-radius: 6px; margin-bottom: 8px;
}
.stButton > button {
    background-color: #FF000F !important; color: #fff !important;
    border: none !important; border-radius: 5px !important;
    font-weight: 600 !important; font-size: .82rem !important;
    padding: 6px 16px !important; transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .85 !important; }
.stLinkButton a {
    background-color: #1a2740 !important; color: #fff !important;
    border: none !important; border-radius: 5px !important;
    font-weight: 600 !important; font-size: .82rem !important;
    padding: 6px 14px !important;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── TÜRKİYE İL KOORDİNATLARI ─────────────────────────────────────────────────
CITY_COORDS = {
    "Adana": (37.0000, 35.3213), "Adıyaman": (37.7648, 38.2786),
    "Afyonkarahisar": (38.7507, 30.5567), "Ağrı": (39.7191, 43.0503),
    "Amasya": (40.6499, 35.8353), "Ankara": (39.9334, 32.8597),
    "Antalya": (36.8969, 30.7133), "Artvin": (41.1828, 41.8183),
    "Aydın": (37.8560, 27.8416), "Balıkesir": (39.6484, 27.8826),
    "Bilecik": (40.1506, 29.9792), "Bingöl": (38.8854, 40.4983),
    "Bitlis": (38.4006, 42.1232), "Bolu": (40.7360, 31.6060),
    "Burdur": (37.7260, 30.2881), "Bursa": (40.1826, 29.0665),
    "Çanakkale": (40.1553, 26.4142), "Çankırı": (40.6013, 33.6134),
    "Çorum": (40.5506, 34.9556), "Denizli": (37.7765, 29.0864),
    "Diyarbakır": (37.9144, 40.2306), "Edirne": (41.6818, 26.5623),
    "Elazığ": (38.6810, 39.2264), "Erzincan": (39.7500, 39.5000),
    "Erzurum": (39.9000, 41.2700), "Eskişehir": (39.7767, 30.5206),
    "Gaziantep": (37.0662, 37.3833), "Giresun": (40.9128, 38.3895),
    "Gümüşhane": (40.4386, 39.4814), "Hakkari": (37.5744, 43.7408),
    "Hatay": (36.4018, 36.3498), "Isparta": (37.7648, 30.5566),
    "İçel": (36.8000, 34.6333), "Mersin": (36.8000, 34.6333),
    "İstanbul": (41.0082, 28.9784), "İzmir": (38.4192, 27.1287),
    "Kars": (40.6013, 43.0975), "Kastamonu": (41.3887, 33.7827),
    "Kayseri": (38.7312, 35.4787), "Kırklareli": (41.7333, 27.2167),
    "Kırıklareli": (41.7333, 27.2167), "Kırşehir": (39.1425, 34.1709),
    "Kocaeli": (40.8533, 29.8815), "Konya": (37.8714, 32.4846),
    "Kütahya": (39.4167, 29.9833), "Malatya": (38.3552, 38.3095),
    "Manisa": (38.6191, 27.4289), "Kahramanmaraş": (37.5858, 36.9371),
    "Mardin": (37.3212, 40.7245), "Muğla": (37.2153, 28.3636),
    "Muş": (38.9462, 41.7539), "Nevşehir": (38.6939, 34.6857),
    "Niğde": (37.9667, 34.6833), "Ordu": (40.9862, 37.8797),
    "Rize": (41.0201, 40.5234), "Sakarya": (40.6940, 30.4358),
    "Samsun": (41.2867, 36.3300), "Siirt": (37.9333, 41.9500),
    "Sinop": (42.0231, 35.1531), "Sivas": (39.7477, 37.0179),
    "Tekirdağ": (41.4564, 27.5152), "Tokat": (40.3167, 36.5500),
    "Trabzon": (41.0015, 39.7178), "Tunceli": (39.1079, 39.5480),
    "Şanlıurfa": (37.1591, 38.7969), "Uşak": (38.6823, 29.4082),
    "Van": (38.4891, 43.4089), "Yozgat": (39.8181, 34.8147),
    "Zonguldak": (41.4564, 31.7987), "Aksaray": (38.3687, 34.0370),
    "Bayburt": (40.2552, 40.2249), "Karaman": (37.1759, 33.2287),
    "Kilis": (36.7184, 37.1212), "Osmaniye": (37.0742, 36.2466),
    "Düzce": (40.8438, 31.1565), "Batman": (37.8812, 41.1351),
    "Şırnak": (37.5164, 42.4611), "Bartın": (41.6344, 32.3375),
    "Ardahan": (41.1105, 42.7022), "Iğdır": (39.9167, 44.0333),
    "Yalova": (40.6500, 29.2667),
}

# ── GeoJSON YÜKLE ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_turkey_geojson():
    """Türkiye il sınırları GeoJSON - GitHub'dan çek"""
    url = "https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception:
        return None

# ── NOTES ────────────────────────────────────────────────────────────────────
NOTES_FILE = "firma_notes.json"
DATA_FILE  = "yeniListe.xlsx"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

# ── DATA ─────────────────────────────────────────────────────────────────────
def load_data_raw():
    df = pd.read_excel(DATA_FILE)
    df["Website"]            = df["Website"].fillna("")
    df["Sektör"]             = df["Sektör"].fillna("Belirtilmemiş")
    df["İlçe"]               = df["İlçe"].fillna("")
    df["Extracted_Products"] = df["Extracted_Products"].fillna("")
    df["İl"]                 = df["İl"].str.strip()
    df = df.reset_index(drop=True)
    return df

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

# ── AI SUMMARY ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=86400)
def ai_summary_gemini(firma, sektor, il, ilce, products, website):
    """Gemini API ile firma özeti — sonuçlar cache'lenir"""
    loc = f"{ilce} / {il}" if ilce else il
    prompt = f"""Türkçe, kısa ve net yanıt ver. Markdown kullanma.

Firma: {firma}
Sektör: {sektor}
Konum: {loc}
Ürünler/Hizmetler: {products if products else "Bilgi yok"}
Website: {website if website else "Yok"}

Şu 3 başlıkta kısaca yaz (her biri 1-2 cümle):
1. Genel Üretim: Bu firma ne üretir / ne iş yapar?
2. Şirket Büyüklüğü: Tahmini ölçeği nedir? (KOBİ / orta / büyük)
3. ABB Fırsatı: ABB hangi ürün/çözümü önerebilir?"""
    import time
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if "quota" in str(e).lower() or "429" in str(e):
            time.sleep(5)
            try:
                response = gemini_model.generate_content(prompt)
                return response.text.strip()
            except:
                return "⚠️ API limiti doldu. Lütfen biraz bekleyip tekrar deneyin."
        return f"Hata: {str(e)}"

def ai_summary(row):
    """Gemini varsa Gemini, yoksa template özet"""
    firma    = str(row["FİRMA"])
    sektor   = str(row["Sektör"])
    il       = str(row["İl"])
    ilce     = str(row["İlçe"])
    products = str(row["Extracted_Products"])
    website  = str(row["Website"])

    if GEMINI_OK:
        return ai_summary_gemini(firma, sektor, il, ilce, products, website)

    # Fallback: template
    loc = f"{ilce} / {il}" if ilce else il
    lines = [f"<b>{firma}</b>, {loc} bölgesinde faaliyet gösteren bir <b>{sektor}</b> firmasıdır.<br><br>"]
    if products and products != "nan":
        items = [p.strip() for p in products.split(",")[:5]]
        lines.append(f"<b>🏭 Öne Çıkan Ürünler:</b> {', '.join(items)}" +
                     ("..." if len(products.split(",")) > 5 else "") + "<br><br>")
    lines.append(
        f"<b>💡 ABB Fırsatı:</b> {sektor} sektöründe faaliyet gösteren bu firma, "
        f"ABB'nin endüstriyel otomasyon ve enerji çözümleriyle örtüşen fırsatlar sunabilir.")
    return "".join(lines)

# ── HARİTA FONKSİYONU ─────────────────────────────────────────────────────────
def make_turkey_map(city_counts_df, geojson=None, selected_cities=None):
    """Türkiye bubble haritası — opsiyonel choropleth"""
    # Koordinat ekle
    city_counts_df = city_counts_df.copy()
    city_counts_df["lat"] = city_counts_df["İl"].map(lambda x: CITY_COORDS.get(x, (None,None))[0])
    city_counts_df["lon"] = city_counts_df["İl"].map(lambda x: CITY_COORDS.get(x, (None,None))[1])
    city_counts_df = city_counts_df.dropna(subset=["lat","lon"])

    if geojson:
        # GeoJSON ile Choropleth + Bubble katmanı
        # GeoJSON property key bul
        try:
            prop_key = list(geojson["features"][0]["properties"].keys())[0]
            # il isimlerini geojson key ile eşleştir
            geojson_cities = [f["properties"][prop_key] for f in geojson["features"]]

            # city_counts normalize
            all_cities_geo = pd.DataFrame({"İl": geojson_cities})
            merged = all_cities_geo.merge(city_counts_df, on="İl", how="left")
            merged["Sayı"] = merged["Sayı"].fillna(0)

            fig = go.Figure()

            # Choropleth layer
            fig.add_trace(go.Choropleth(
                geojson=geojson,
                featureidkey=f"properties.{prop_key}",
                locations=merged["İl"],
                z=merged["Sayı"],
                colorscale=[[0,"#fff0ee"],[0.3,"#ff957e"],[0.6,"#FF4444"],[1.0,"#FF000F"]],
                showscale=True,
                colorbar=dict(title="Firma Sayısı", thickness=12, len=0.6),
                hovertemplate="<b>%{location}</b><br>Firma: %{z:.0f}<extra></extra>",
                marker_line_color="#fff",
                marker_line_width=0.8,
            ))

            # Bubble layer (yalnızca veri olan iller)
            fig.add_trace(go.Scattergeo(
                lat=city_counts_df["lat"],
                lon=city_counts_df["lon"],
                text=city_counts_df.apply(
                    lambda r: f"{r['İl']}<br>{r['Sayı']} firma", axis=1),
                customdata=city_counts_df["İl"],
                mode="markers+text",
                textposition="top center",
                textfont=dict(size=9, color="#1a1a2e"),
                marker=dict(
                    size=city_counts_df["Sayı"] ** 0.55 * 4,
                    color="#FF000F",
                    opacity=0.75,
                    line=dict(color="#fff", width=1),
                ),
                hovertemplate="%{customdata}: %{text}<extra></extra>",
                showlegend=False,
            ))

        except Exception:
            geojson = None  # fallback

    if not geojson:
        # Sadece bubble map
        fig = px.scatter_geo(
            city_counts_df,
            lat="lat", lon="lon",
            size="Sayı",
            color="Sayı",
            hover_name="İl",
            hover_data={"Sayı": True, "lat": False, "lon": False},
            text="İl",
            color_continuous_scale=[[0,"#ffdccd"],[0.4,"#ff957e"],[1,"#FF000F"]],
            size_max=55,
            custom_data=["İl"],
        )
        fig.update_traces(
            textposition="top center",
            textfont=dict(size=9, color="#1a1a2e"),
            hovertemplate="<b>%{customdata[0]}</b><br>%{marker.size:.0f} firma<extra></extra>",
        )

    fig.update_layout(
        geo=dict(
            scope="asia",
            center=dict(lat=39.0, lon=35.5),
            projection_scale=4.8,
            showland=True, landcolor="#f0f0e8",
            showocean=True, oceancolor="#e8f4fd",
            showlakes=True, lakecolor="#e8f4fd",
            showcountries=True, countrycolor="#ccc",
            showcoastlines=True, coastlinecolor="#bbb",
            showsubunits=True, subunitcolor="#ddd",
            bgcolor="#f4f6f9",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="#f4f6f9",
        height=480,
        clickmode="event+select",
        font=dict(family="Segoe UI, Arial"),
        coloraxis_colorbar=dict(title="Firma Sayısı"),
    )
    # Seçili iller (map click + sidebar) farklı renkte vurgula
    if selected_cities:
        valid = [(c, CITY_COORDS[c]) for c in selected_cities if c in CITY_COORDS]
        if valid:
            fig.add_trace(go.Scattergeo(
                lat=[v[1][0] for v in valid],
                lon=[v[1][1] for v in valid],
                text=[v[0] for v in valid],
                customdata=[v[0] for v in valid],
                mode="markers+text",
                textposition="bottom center",
                textfont=dict(size=10, color="#6764f6", family="Arial Black"),
                marker=dict(
                    size=22, color="rgba(103,100,246,0.25)",
                    line=dict(color="#6764f6", width=2.5),
                    symbol="circle",
                ),
                name="Seçili",
                hovertemplate="<b>%{text}</b> — seçili<extra></extra>",
                showlegend=False,
            ))
    return fig

# ── GEMİNİ INIT ──────────────────────────────────────────────────────────────
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash-8b")
    GEMINI_OK = True
except Exception:
    GEMINI_OK = False

# ── SESSION INIT ─────────────────────────────────────────────────────────────
if "df_data"   not in st.session_state: st.session_state.df_data   = load_data_raw()
if "notes"     not in st.session_state: st.session_state.notes     = load_notes()
if "ai_open"   not in st.session_state: st.session_state.ai_open   = {}
if "page"      not in st.session_state: st.session_state.page      = 1
if "del_conf"  not in st.session_state: st.session_state.del_conf  = None
if "saved_ok"  not in st.session_state: st.session_state.saved_ok  = False
if "show_map"            not in st.session_state: st.session_state.show_map            = False
if "map_filter_cities"   not in st.session_state: st.session_state.map_filter_cities   = []
if "last_map_sel_hash"   not in st.session_state: st.session_state.last_map_sel_hash   = ""

df = st.session_state.df_data

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:14px 0 12px; border-bottom:1px solid #e0e0e0; margin-bottom:16px;
                display:flex; align-items:center; gap:10px;">
        <img src="data:image/svg+xml;base64,{ABB_LOGO_B64}" style="height:32px; border-radius:2px;">
        <span style="font-size:.78rem;color:#888;font-weight:700;letter-spacing:1px;
                     text-transform:uppercase;">Firma Veritabanı</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("**🔍 FİRMA / ÜRÜN ARA**")
    search = st.text_input("", placeholder="Arama...", label_visibility="collapsed")

    st.markdown("**🏙 ŞEHİR**")
    all_cities  = sorted(df["İl"].dropna().unique().tolist())
    sel_cities  = st.multiselect("", options=all_cities, default=[],
                                 placeholder="Tüm şehirler...", label_visibility="collapsed")

    st.markdown("**📂 KATEGORİ**")
    all_sectors = sorted(df["Sektör"].dropna().unique().tolist())
    sel_sectors = st.multiselect("", options=all_sectors, default=[],
                                 placeholder="Tüm kategoriler...", label_visibility="collapsed")

    st.markdown("---")
    if st.button("💾 Değişiklikleri Excel'e Kaydet", key="save_excel"):
        save_data(st.session_state.df_data)
        st.success("Excel kaydedildi!")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:.72rem;color:#aaa;text-align:center;line-height:1.9;">
        © 2024 ABB Ltd. Türkiye<br>
        <span style="color:#FF000F;">●</span> Gıda &amp; İçecek Firma Veritabanı
    </div>""", unsafe_allow_html=True)

# ── FILTER ───────────────────────────────────────────────────────────────────
df = st.session_state.df_data
fdf = df.copy()
combined_cities = list(set(sel_cities + st.session_state.map_filter_cities))
if combined_cities:  fdf = fdf[fdf["İl"].isin(combined_cities)]
if sel_sectors:      fdf = fdf[fdf["Sektör"].isin(sel_sectors)]
if search:
    mask = (fdf["FİRMA"].str.contains(search, case=False, na=False) |
            fdf["Extracted_Products"].str.contains(search, case=False, na=False))
    fdf = fdf[mask]

cur_filter = f"{combined_cities}|{sel_sectors}|{search}"
if st.session_state.get("_prev_f","") != cur_filter:
    st.session_state.page   = 1
    st.session_state._prev_f = cur_filter

# ── TOPBAR ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div style="display:flex;align-items:center;">
    <img src="data:image/svg+xml;base64,{ABB_LOGO_B64}" style="height:38px;border-radius:3px;">
    <span class="topbar-title">Gıda &amp; İçecek Firma Veritabanı</span>
  </div>
  <div class="topbar-right">Türkiye Pazar Analizi &nbsp;·&nbsp; {len(df)} Kayıt</div>
</div>""", unsafe_allow_html=True)

if st.session_state.saved_ok:
    st.success("✅ Değişiklikler kaydedildi!")
    st.session_state.saved_ok = False

# ── KPI CARDS ────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
cards = [
    (k1, len(fdf), f"/{len(df)} toplam", "Toplam Firma", ""),
    (k2, fdf["İl"].nunique(), f"/{df['İl'].nunique()} il", "Aktif Şehir", "stat-card-blue"),
    (k3, fdf["Sektör"].nunique(), f"/{df['Sektör'].nunique()} kategori", "Kategori", ""),
    (k4, len(st.session_state.notes), "kayıtlı not", "Notlarım", "stat-card-blue"),
]
for col, val, sub, lbl, cls in cards:
    with col:
        st.markdown(f"""
        <div class="stat-card {cls}">
            <div class="val">{val}</div>
            <div class="lbl">{lbl}</div>
            <div style="font-size:.7rem;color:#bbb;margin-top:2px;">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CHARTS + HARİTA ──────────────────────────────────────────────────────────
city_counts = fdf["İl"].value_counts().reset_index()
city_counts.columns = ["İl", "Sayı"]

cc1, cc2 = st.columns(2)

with cc1:
    st.markdown('<div class="sec-title">📍 Şehir Bazlı Dağılım (Top 12)</div>', unsafe_allow_html=True)
    st.markdown('<div class="map-hint">👆 Grafiğin altındaki butona tıklayarak Türkiye haritasını açabilirsiniz</div>',
                unsafe_allow_html=True)

    city_top = city_counts.head(12)
    fig1 = px.bar(city_top, x="Sayı", y="İl", orientation="h", text="Sayı",
                  color="Sayı", color_continuous_scale=[[0,"#ffdccd"],[0.5,"#ff957e"],[1,"#FF000F"]])
    fig1.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff", height=360,
                       margin=dict(l=0,r=30,t=4,b=0), coloraxis_showscale=False,
                       yaxis=dict(categoryorder="total ascending"),
                       font=dict(family="Segoe UI, Arial"))
    fig1.update_traces(textposition="outside", textfont_size=10)
    st.plotly_chart(fig1, key="chart1")

    # Harita toggle butonu
    map_label = "🗺️ Türkiye Haritasını Kapat" if st.session_state.show_map else "🗺️ Türkiye Haritasını Aç"
    if st.button(map_label, key="map_toggle"):
        st.session_state.show_map = not st.session_state.show_map
        st.rerun()

with cc2:
    st.markdown('<div class="sec-title">🏭 Kategori Dağılımı (Top 12)</div>', unsafe_allow_html=True)
    sec_c = fdf["Sektör"].value_counts().head(12).reset_index()
    sec_c.columns = ["Sektör","Sayı"]
    fig2 = px.bar(sec_c, x="Sayı", y="Sektör", orientation="h", text="Sayı",
                  color="Sayı", color_continuous_scale=[[0,"#e4e7ff"],[0.5,"#93a1ff"],[1,"#6764f6"]])
    fig2.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff", height=360,
                       margin=dict(l=0,r=30,t=4,b=0), coloraxis_showscale=False,
                       yaxis=dict(categoryorder="total ascending"),
                       font=dict(family="Segoe UI, Arial"))
    fig2.update_traces(textposition="outside", textfont_size=10)
    st.plotly_chart(fig2, key="chart2")

# ── TÜRKİYE HARİTASI ─────────────────────────────────────────────────────────
if st.session_state.show_map:
    st.markdown("---")
    st.markdown('<div class="sec-title">🗺️ Türkiye Firma Yoğunluk Haritası</div>', unsafe_allow_html=True)

    with st.spinner("Harita yükleniyor..."):
        geojson = load_turkey_geojson()

    if geojson:
        st.markdown(
            '<div class="map-hint">✅ İl sınırları yüklendi — renkli choropleth + bubble gösterim</div>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="map-hint">⚠️ GeoJSON yüklenemedi — bubble harita gösteriliyor</div>',
            unsafe_allow_html=True)

    all_sel = list(set(sel_cities + st.session_state.map_filter_cities))
    fig_map = make_turkey_map(city_counts, geojson, selected_cities=all_sel)

    # Seçili iller chip'leri
    if st.session_state.map_filter_cities:
        chips_html = "".join([
            f'<span style="background:#6764f6;color:#fff;padding:3px 12px;'
            f'border-radius:20px;font-size:.76rem;font-weight:700;margin:2px;'
            f'display:inline-block;">📍 {c}</span>'
            for c in st.session_state.map_filter_cities
        ])
        st.markdown(
            f'<div style="background:#f0f2ff;border:1px solid #e4e7ff;border-radius:8px;'            f'padding:8px 12px;margin-bottom:8px;">'            f'<span style="font-size:.74rem;color:#6764f6;font-weight:700;margin-right:8px;">'            f'🗺️ HARİTADAN SEÇİLEN İLLER:</span>{chips_html}</div>',
            unsafe_allow_html=True)
        if st.button("✖ Harita Seçimlerini Temizle", key="clear_map_sel"):
            st.session_state.map_filter_cities = []
            st.session_state.last_map_sel_hash = ""
            st.rerun()

    # Haritayı çiz — tıklama yakala
    map_event = st.plotly_chart(
        fig_map,
        key="turkey_map",
        on_select="rerun",
        selection_mode=["points"],
    )

    # Tıklama işle
    if map_event and map_event.selection and map_event.selection.points:
        sel_hash = str(sorted([str(p) for p in map_event.selection.points]))
        if sel_hash != st.session_state.last_map_sel_hash:
            st.session_state.last_map_sel_hash = sel_hash
            for pt in map_event.selection.points:
                city = (
                    pt.get("location") or
                    (pt.get("customdata") if isinstance(pt.get("customdata"), str) else None) or
                    str(pt.get("text", "")).split("<br>")[0]
                ).strip()
                if city and city in CITY_COORDS:
                    if city in st.session_state.map_filter_cities:
                        st.session_state.map_filter_cities.remove(city)
                    else:
                        st.session_state.map_filter_cities.append(city)
            st.rerun()

    # İl detay tablosu
    st.markdown('<div class="sec-title">📋 İl Bazlı Firma Sayıları</div>', unsafe_allow_html=True)
    city_tbl = city_counts.copy()
    city_tbl["Oran (%)"] = (city_tbl["Sayı"] / city_tbl["Sayı"].sum() * 100).round(1)
    city_tbl.columns = ["İl", "Firma Sayısı", "Oran (%)"]
    st.dataframe(city_tbl, hide_index=True, height=300,
                 column_config={
                     "Firma Sayısı": st.column_config.ProgressColumn(
                         "Firma Sayısı", format="%d", min_value=0, max_value=int(city_tbl["Firma Sayısı"].max())),
                     "Oran (%)": st.column_config.NumberColumn("Oran (%)", format="%.1f%%"),
                 })

# ── TABLE ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f'<div class="sec-title">🏢 Firma Listesi — {len(fdf)} firma</div>', unsafe_allow_html=True)

ITEMS       = 20
total_pages = max(1, math.ceil(len(fdf) / ITEMS))
s           = (st.session_state.page - 1) * ITEMS
page_df     = fdf.iloc[s: s + ITEMS].reset_index(drop=False)

rows_html = ""
for _, row in page_df.iterrows():
    url = row["Website"]
    if url and not str(url).startswith("http"):
        url = "https://" + str(url)
    web_cell  = (f'<a class="web-link" href="{url}" target="_blank">🔗 Aç</a>'
                 if url else '<span style="color:#ccc;font-size:.74rem;">—</span>')
    prod      = str(row["Extracted_Products"])
    prod_cell = f'<div class="prod-cell" title="{prod}">{prod[:70] + "..." if len(prod)>70 else (prod or "—")}</div>'
    rows_html += f"""
    <tr>
        <td><div class="firma-name">{row['FİRMA']}</div></td>
        <td><span class="badge-cat">{row['Sektör']}</span></td>
        <td><span class="badge-city">{row['İl']}</span></td>
        <td style="font-size:.77rem;color:#888;">{row['İlçe']}</td>
        <td>{web_cell}</td>
        <td>{prod_cell}</td>
    </tr>"""

st.markdown(f"""
<div class="tbl-wrap"><table>
<thead><tr>
    <th>Firma Adı</th><th>Kategori</th><th>Şehir</th>
    <th>İlçe</th><th>Website</th><th>Ürünler</th>
</tr></thead>
<tbody>{rows_html}</tbody>
</table></div>""", unsafe_allow_html=True)

# ── INTERACTION PANEL ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
firma_names = page_df["FİRMA"].tolist()
sel = st.selectbox(
    "📌 İşlem yapmak istediğiniz firmayı seçin:",
    options=["— Firma seçin —"] + firma_names,
    key="firma_sel"
)

if sel != "— Firma seçin —":
    row_series = page_df[page_df["FİRMA"] == sel].iloc[0]
    orig_index = row_series["index"]
    firma_key  = str(row_series["FİRMA"])
    ai_key     = f"ai_{firma_key}"

    st.markdown('<div class="inter-panel">', unsafe_allow_html=True)

    ic1, ic2, ic3 = st.columns([3, 1, 1])
    with ic1:
        st.markdown(f"""
        <div style="font-weight:700;font-size:.95rem;color:#1a1a2e;">{row_series['FİRMA']}</div>
        <div style="margin-top:5px;">
            <span class="badge-cat">{row_series['Sektör']}</span>
            <span class="badge-city" style="margin-left:5px;">{row_series['İl']}</span>
        </div>""", unsafe_allow_html=True)
    with ic2:
        url = row_series["Website"]
        if url and not str(url).startswith("http"):
            url = "https://" + str(url)
        if url:
            st.link_button("🌐 Website", url=url)
        else:
            st.button("🌐 Website Yok", disabled=True, key="no_web")
    with ic3:
        lbl = "🤖 Kapat" if st.session_state.ai_open.get(ai_key) else "🤖 AI Özeti"
        if st.button(lbl, key="ai_btn"):
            st.session_state.ai_open[ai_key] = not st.session_state.ai_open.get(ai_key, False)
            st.rerun()

    if st.session_state.ai_open.get(ai_key):
        st.markdown(
            f'<div class="ai-box"><b style="color:#6764f6;font-size:.72rem;letter-spacing:1px;">'
            f'🤖 AI ÖZET</b><br><br>{ai_summary(row_series)}</div>',
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_note, tab_edit, tab_del = st.tabs(["📝 Not Ekle", "✏️ Bilgileri Düzenle", "🗑️ Firmayı Sil"])

    with tab_note:
        existing = st.session_state.notes.get(firma_key, "")
        if existing:
            st.markdown(f'<div class="note-saved">📌 <b>Kayıtlı Not:</b> {existing}</div>',
                        unsafe_allow_html=True)
        nc1, nc2, nc3 = st.columns([5, 1, 1])
        with nc1:
            new_note = st.text_area("Not:", value=existing, height=80,
                                    placeholder="Bu firma hakkında not...",
                                    label_visibility="collapsed", key=f"ta_{firma_key}")
        with nc2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Kaydet", key="save_note"):
                st.session_state.notes[firma_key] = new_note
                save_notes(st.session_state.notes)
                st.success("Kaydedildi!")
        with nc3:
            st.markdown("<br>", unsafe_allow_html=True)
            if existing and st.button("🗑️ Sil", key="del_note"):
                del st.session_state.notes[firma_key]
                save_notes(st.session_state.notes)
                st.rerun()

    with tab_edit:
        st.markdown('<div class="edit-panel">', unsafe_allow_html=True)
        with st.form("edit_form"):
            ef1, ef2 = st.columns(2)
            with ef1:
                e_firma   = st.text_input("🏢 Firma Adı",  value=str(row_series["FİRMA"]))
                e_sektor  = st.text_input("🏭 Kategori",   value=str(row_series["Sektör"]))
                e_website = st.text_input("🌐 Website",    value=str(row_series["Website"]))
            with ef2:
                e_il      = st.text_input("📍 İl",         value=str(row_series["İl"]))
                e_ilce    = st.text_input("🗺️ İlçe",       value=str(row_series["İlçe"]))
                e_prods   = st.text_area("📦 Ürünler",     value=str(row_series["Extracted_Products"]), height=68)
            submitted = st.form_submit_button("✅ Değişiklikleri Kaydet")
            if submitted:
                st.session_state.df_data.at[orig_index, "FİRMA"]              = e_firma
                st.session_state.df_data.at[orig_index, "Sektör"]             = e_sektor
                st.session_state.df_data.at[orig_index, "Website"]            = e_website
                st.session_state.df_data.at[orig_index, "İl"]                 = e_il.strip()
                st.session_state.df_data.at[orig_index, "İlçe"]               = e_ilce
                st.session_state.df_data.at[orig_index, "Extracted_Products"] = e_prods
                st.session_state.saved_ok = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_del:
        st.markdown(f"""
        <div class="del-warning">
            ⚠️ &nbsp;<b>{row_series['FİRMA']}</b> firmasını silmek üzeresiniz.<br>
            <span style="font-size:.78rem;">Bu işlem geri alınamaz.</span>
        </div>""", unsafe_allow_html=True)
        if st.session_state.del_conf != firma_key:
            if st.button("🗑️ Evet, Bu Firmayı Sil", key="ask_del"):
                st.session_state.del_conf = firma_key
                st.rerun()
        else:
            dc1, dc2 = st.columns(2)
            with dc1:
                if st.button("⛔ ONAYLA — Sil", key="confirm_del"):
                    st.session_state.df_data = st.session_state.df_data.drop(index=orig_index).reset_index(drop=True)
                    if firma_key in st.session_state.notes:
                        del st.session_state.notes[firma_key]
                        save_notes(st.session_state.notes)
                    st.session_state.del_conf = None
                    st.session_state.page = 1
                    st.success(f"{firma_key} silindi.")
                    st.rerun()
            with dc2:
                if st.button("↩️ Vazgeç", key="cancel_del"):
                    st.session_state.del_conf = None
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── PAGINATION ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
p1, p2, p3, p4, p5 = st.columns([1,1,2,1,1])
with p1:
    if st.button("« İlk", key="pg_first", disabled=(st.session_state.page<=1)):
        st.session_state.page=1; st.rerun()
with p2:
    if st.button("‹ Önceki", key="pg_prev", disabled=(st.session_state.page<=1)):
        st.session_state.page-=1; st.rerun()
with p3:
    st.markdown(
        f'<div class="pager-info">Sayfa <b>{st.session_state.page}</b> / {total_pages}'
        f' &nbsp;·&nbsp; {len(fdf)} firma</div>', unsafe_allow_html=True)
with p4:
    if st.button("Sonraki ›", key="pg_next", disabled=(st.session_state.page>=total_pages)):
        st.session_state.page+=1; st.rerun()
with p5:
    if st.button("Son »", key="pg_last", disabled=(st.session_state.page>=total_pages)):
        st.session_state.page=total_pages; st.rerun()

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#aaa;font-size:.75rem;padding:10px 0;
            display:flex;align-items:center;justify-content:center;gap:10px;">
    <img src="data:image/svg+xml;base64,{ABB_LOGO_B64}" style="height:22px;border-radius:2px;opacity:.7;">
    <span>Gıda &amp; İçecek Firma Veritabanı &nbsp;·&nbsp; Türkiye Pazar Analizi &nbsp;·&nbsp; © 2024 ABB Ltd.</span>
</div>""", unsafe_allow_html=True)
