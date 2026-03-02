#BUNU ÇALIŞTIRMANIN YOLU CMD AÇ VE "streamlit run information_solver.py" YAZ.

import ollama
import json
import streamlit as st
import PyPDF2
import os
import datetime
from fpdf import FPDF
import re


# --- AYARLAR ---
BASIC_MODEL_NAME = "info-solver"
COMPLEX_MODEL_NAME ="info-solver-complex"
JSON_MODEL_NAME ="info-solver-json"
CHUNK_SIZE = 1500


# Sayfa Ayarları

st.set_page_config(page_title = "INFORMATION SOLVER", layout = "centered")
st.title("🧠Information Solver")
st.markdown("PDF dosayısını yükle. Analiz ile özet çıkartılsın")


# Chunking the text

def chunk_text(text, chunk_size):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0,len(words), chunk_size)]

# Kademeli hafızada finalize_chunks'dan gelecek öz ile eşleşen kademe burada olacak.

### İLK ÖZET
def summarize_chunks(chunks, model_name): 
    summaries = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, chunk in enumerate(chunks):
        status_text.text(f"Par.a {i+1}/{len(chunks)} analiz ediliyor...")

        prompt = chunk

        response = ollama.chat (model = model_name, messages =[
            {'role': 'user',
             'content': prompt
             }
        ])
        summaries.append(response['message']['content'])
        progress_bar.progress((i+1)/len(chunks))

    status_text.text("Tüm parçalar analiz edildi. Parçalar birleştirilip, son sentez oluşturuluyor...")
    return "\n\n".join(summaries)

### ORTA ÖZET
# Bunun işi okunabilir formatta kullanıcıyı bilgilendirecek özü içermektir.
# Daha sonra kademeli bir hafıza için json ile eşleşecek ilk öz bu
def finalize_chunks(combined, model_name): 
    prompt = combined                       
    response = ollama.chat(model=model_name, messages=[
        {'role':'user', 'content': prompt}
    ])
    return response

### SON ÖZET
# Bu tamamen anahtar kelimeler içerir bu en rahat hafızadan çekilebilir formatı içerir. Mind map için keywordsler buradan gelir.

def finalize_json(combined, model_name):
    prompt = combined
    response = ollama.chat(model=model_name, messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']




# Dosya Yükleyici
uploaded_file = st.file_uploader("Bir PDF Dosyası Seçin", type="pdf")
document_text = ""

if uploaded_file is not None:
    with st.spinner("PDF Ayrıştırılıyor..."):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                document_text += extracted + "\n"

    st.success(f"PDF Başarıyla Okundu. (Yaklaşık {len(document_text.split())} kelime.)")

if st.button("Metni Aşamalı Analiz Et ve Özetle"):
    if not document_text:
        st.warning("Lütfen önce bir PDF yükleyin.")
    else:
        with st.spinner("Information Solver Çalışıyor..."):
            try:
                # 1. Metni Parçala
                chunks = chunk_text(document_text, CHUNK_SIZE)
                
                # 2. Parçaları Özetle (Large Map)
                combined_summaries = summarize_chunks(chunks, BASIC_MODEL_NAME)
                
                with st.expander("Ara Özetleri Gör (Geliştirici Detayı)"):
                    st.write(combined_summaries)
            
                # 3. Orta Özeti Çıkar(Middle Map)
                final = finalize_chunks(combined_summaries, COMPLEX_MODEL_NAME)
                st.subheader("Bütüncül Analiz Sonucu (Tek Parça):")
                st.write(final['message']['content'])

                # 4. Son Özeti Çıkar(Final Map)(JSON)
                raw_json = finalize_json(combined_summaries, JSON_MODEL_NAME )
                st.subheader("JSON:")
                st.write(raw_json)

####-------------------------------------####

# JSON AND DATA CREATION

                # 1. Final JSON'u temizle ve Sözlüğe (Dictionary) çevir (SIĞ KATMAN)
                clean_json = raw_json.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:]
                if clean_json.endswith("```"):
                    clean_json = clean_json[:-3]
                
                shallow_data = json.loads(clean_json) # Keywords ve Essence burada
                
                # 2. Orta Özeti metin olarak al (DERİN KATMAN)
                deep_text = final['message']['content'] 

                # --- YENİ EKLENEN PDF KAYIT BÖLÜMÜ ---
                pdf_folder = "PDFs"
                os.makedirs(pdf_folder, exist_ok=True)
                
                # JSON'dan 'name' değerini al, yoksa varsayılan isim ver
                raw_name = shallow_data.get("name", "Analiz")
                # Windows/Linux dosya adlandırma kurallarını bozan karakterleri temizle
                safe_name = re.sub(r'[\\/*?:"<>|]', "", raw_name) 
                pdf_path = os.path.join(pdf_folder, f"{safe_name}.pdf")

                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    
                    # Not: FPDF standart fontları ş,ğ,ı gibi Türkçe karakterlerde hata verebilir.
                    # Hata almamak için metni latin-1 formatına zorluyoruz (İleride kursu bitirince buraya UTF-8 font eklersin!)
                    safe_text = deep_text.encode('latin-1', 'replace').decode('latin-1')
                    
                    pdf.multi_cell(0, 10, txt=safe_text)
                    pdf.output(pdf_path)
                    st.success(f"📄 Bütüncül Analiz başarıyla PDF olarak kaydedildi: `{pdf_path}`")
                except Exception as e:
                    st.error(f"PDF oluşturulurken bir hata meydana geldi: {e}")
                # --------------------------------------

                # 3. MASTER MEMORY OBJECT (İki katmanı birbirine MAP eden ana yapı)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                document_id = f"doc_{timestamp}"

                master_memory = {
                    "document_id": document_id,
                    "shallow_layer": shallow_data,      # Vektör araması ilk buraya bakacak
                    "deep_layer": {
                        "structured_summary": deep_text # Derine inmek isterse burayı okuyacak
                    }
                }

                st.subheader("Master Memory Map:")
                st.json(master_memory)

                # 4. Tam Otomatik Klasör ve Dosya İşlemleri (Arka Plan Kaydı)
                output_folder = "Memory_Bank"
                os.makedirs(output_folder, exist_ok=True)
                
                file_name = f"{document_id}.json"
                file_path = os.path.join(output_folder, file_name)
                
                # 5. Fiziksel Dosyaya Sessizce Yazdır
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(master_memory, f, ensure_ascii=False, indent=4)
                
                st.success(f"✅ DEUS İki Kademeli Hafıza Haritası Başarıyla Kaydedildi! \nDosya Konumu: `{file_path}`")

            except json.JSONDecodeError:
                st.error("JSON Ayrıştırma Hatası! Model geçerli bir yapı üretmedi.")
                st.code(raw_json)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
   

                




