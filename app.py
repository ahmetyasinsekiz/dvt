import streamlit as st
from supabase import create_client, Client

# Sayfa Yapılandırması
st.set_page_config(page_title="Ameliyat Sonrası Takip", layout="centered")

# Supabase Bağlantısını Başlatma
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

st.title("🩺 Bilimsel Çalışma Veri Girişi")
st.write("Lütfen günlük antiemboli çorabı sonrası değerlerinizi giriniz.")

# Kullanıcı Bilgileri ve Form
with st.form("survey_form"):
    name = st.text_input("Adınız Soyadınız")
    st.divider()
    
    vas_score = st.slider("VAS Ağrı Skoru (0: Yok, 10: Şiddetli)", 0, 10, 5)
    st.divider()
    
    st.subheader("Bacak Hissiyat Değerlendirmesi")
    st.write("1: Hiç yok, 5: Çok fazla")
    
    weight_sense = st.radio("Bacak Ağırlık Hissi", [1, 2, 3, 4, 5], horizontal=True)
    fatigue_sense = st.radio("Bacak Yorgunluğu", [1, 2, 3, 4, 5], horizontal=True)
    swelling_sense = st.radio("Bacak Şişlik Hissi", [1, 2, 3, 4, 5], horizontal=True)
    
    submit_button = st.form_submit_button("Verileri Kaydet")

if submit_button:
    if name:
        # Veritabanına gönderilecek veriyi hazırlama (Tarih veritabanı tarafından otomatik atanır)
        data = {
            "katilimci": name,
            "vas_skoru": vas_score,
            "bacak_agirlik": weight_sense,
            "bacak_yorgunluk": fatigue_sense,
            "bacak_sislik": swelling_sense
        }
        
        # Veriyi Supabase'e yazma
        try:
            response = supabase.table("anket_verileri").insert(data).execute()
            st.success("Verileriniz başarıyla kaydedildi. Teşekkür ederiz!")
            st.balloons()
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.error("Lütfen isminizi giriniz.")