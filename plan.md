# HVB Project Plan
## Ngữ liệu Song ngữ Hán–Việt, Lịch sử Việt Nam

---

## 1. Tổng quan kiến trúc

Pipeline được tách thành **2 phần thực thi độc lập**:

```
┌─────────────────────────────────────────────────────────────┐
│  ocr_segmentation                                              │
│  Trách nhiệm: đọc config, OCR ảnh/PDF, tách câu            │
│  Input : data/config.json + raw files                       │
│  Output: ocr_output/<id>/han.txt + viet.txt                 │
│          processed/<id>/han.json  + viet.json               │
└──────────────────────────┬──────────────────────────────────┘
                           │  (processed/<id>/han.json + viet.json)
┌──────────────────────────▼──────────────────────────────────┐
│  sentence_alignment                                         │
│  Trách nhiệm: dóng hàng câu Hán↔Việt, xuất corpus          │
│  Input : processed/<id>/han.json + viet.json                │
│  Output: corpus/<id>/HVB_corpus.tsv                         │
└─────────────────────────────────────────────────────────────┘
```

**Lý do tách 2 phần:**
- `ocr_segmentation` tốn thời gian xử lý → chạy 1 lần, lưu kết quả
- `sentence_alignment` chạy lại thoải mái khi thử các method khác nhau
- Dễ debug từng phần độc lập

---

## 2. Cấu trúc thư mục

```
nlp-mid/
│
├── data/
│   ├── config.json                        ← TRUNG TÂM: khai báo tất cả tác phẩm
│   │
│   ├── raw/                               ← Files gốc (KHÔNG chỉnh sửa)
│   │   ├── images/                        ← Ảnh scan rời (JPG/PNG)
│   │   ├── pdfs/                          ← File PDF
│   │   └── texts/                         ← File text thuần (.txt)
│   │
│   ├── ocr_output/                        ← Text thô sau OCR, mỗi dòng = 1 bbox/đoạn
│   │   ├── an-nam-chi-luoc/
│   │   │   ├── han.txt
│   │   │   └── viet.txt
│   │   └── dai-viet-su-ky/
│   │       ├── han.txt
│   │       └── viet.txt
│   │
│   ├── processed/                         ← Câu đã tách, dạng JSON có metadata
│   │   ├── an-nam-chi-luoc/
│   │   │   ├── han.json
│   │   │   └── viet.json
│   │   └── dai-viet-su-ky/
│   │       ├── han.json
│   │       └── viet.json
│   │
│   └── corpus/                            ← Output cuối: corpus song ngữ
│       ├── an-nam-chi-luoc/
│       │   └── HVB_corpus.tsv
│       ├── dai-viet-su-ky/
│       │   └── HVB_corpus.tsv
│       └── HVB_corpus_all.tsv             ← Gộp toàn bộ tác phẩm
│
├── src/
│   ├── ocr_segmentation/                     ← PHẦN 1
│   │   ├── run.py                         ← Entrypoint: python src/ocr_segmentation/run.py
│   │   ├── config_loader.py               ← Đọc và validate data/config.json
│   │   ├── pdf_to_images.py               ← PDF → ảnh JPG từng trang (PyMuPDF)
│   │   ├── ocr_engine.py                  ← OCR dispatcher: PaddleOCR (Hán) / pytesseract (Việt) / text-layer
│   │   ├── bbox_sort.py                   ← Sắp xếp bbox: phải→trái, trên→dưới
│   │   └── segmenter.py                   ← Tách câu: HanLP (Hán) + Underthesea (Việt)
│   │
│   ├── sentence_alignment/                ← PHẦN 2
│   │   ├── run.py                         ← Entrypoint: python src/sentence_alignment/run.py
│   │   ├── aligner.py                     ← LaBSE / auto-translate / greedy fallback
│   │   ├── char_aligner.py                ← MED Levenshtein + SinoNom dict (verify OCR)
│   │   └── corpus_builder.py              ← Tổng hợp, gán ID, xuất TSV
│   │
│   └── utils.py                           ← ID generator (HVB_fff.ccc.ppp.ss), file I/O
│
├── dictionaries/
│   ├── SinoNom_Similar.dic                ← S1: Hán tự hình dáng tương đồng
│   ├── QuocNgu_SinoNom.dic                ← S2: Quốc ngữ → Hán Nôm tương ứng
│   └── HanViet.dic                        ← Âm Hán Việt
│
├── configs/
│   └── pipeline.yaml                      ← Cấu hình OCR tool, alignment method, threshold
│
├── requirements.txt
├── .env                                   ← GEMINI_API_KEY — chỉ cần nếu dùng method auto_translate ở Part 2
├── .env.example
├── .gitignore
├── plan.md                                ← File này
└── README.md
```

---

## 3. `data/config.json` — Khai báo tác phẩm

Mỗi tác phẩm là 1 entry trong `works[]`. Mỗi tác phẩm có thể có nhiều `resources`
(bản Hán và bản Việt, mỗi bản có thể ở format khác nhau).

```json
{
  "works": [
    {
      "id": "an-nam-chi-luoc",
      "name": "An Nam Chí Lược",
      "resources": [
        {
          "lang": "han",
          "format": "pdf",
          "path": "data/raw/pdfs/an-nam-chi-luoc-han.pdf",
          "pages": null
        },
        {
          "lang": "viet",
          "format": "text",
          "path": "data/raw/texts/an-nam-chi-luoc-viet.txt",
          "pages": null
        }
      ]
    },
    {
      "id": "dai-viet-su-ky",
      "name": "Đại Việt Sử Ký Toàn Thư",
      "resources": [
        {
          "lang": "han",
          "format": "images",
          "path": "data/raw/images/dai-viet-su-ky/",
          "pages": null
        },
        {
          "lang": "viet",
          "format": "pdf",
          "path": "data/raw/pdfs/dai-viet-su-ky-viet.pdf",
          "pages": null
        }
      ]
    },
    {
      "id": "viet-su-luoc",
      "name": "Việt Sử Lược",
      "resources": [
        {
          "lang": "han",
          "format": "pdf",
          "path": "data/raw/pdfs/viet-su-luoc.pdf",
          "pages": "1-80"
        },
        {
          "lang": "viet",
          "format": "pdf",
          "path": "data/raw/pdfs/viet-su-luoc.pdf",
          "pages": "81-150"
        }
      ]
    }
  ]
}
```

**Giải thích các field:**

| Field | Kiểu | Ý nghĩa |
|-------|------|---------|
| `id` | string | Slug không dấu → tên thư mục output |
| `name` | string | Tên đầy đủ để hiển thị |
| `lang` | `"han"` \| `"viet"` | Ngôn ngữ của resource |
| `format` | `"pdf"` \| `"images"` \| `"text"` \| `"mixed_page"` | Loại file đầu vào |
| `path` | string | Relative path từ root repo đến file hoặc thư mục ảnh |
| `pages` | `null` \| `"1-80"` \| `"1,3,5"` | `null` = tất cả trang; dùng khi Hán/Việt lẫn trong 1 PDF |

---

## 4. Xử lý tình huống Hán + Việt lẫn lộn

### Tình huống A — 2 file riêng biệt (đơn giản nhất)
```json
{ "lang": "han",  "format": "pdf",  "path": "data/raw/pdfs/han.pdf",   "pages": null },
{ "lang": "viet", "format": "text", "path": "data/raw/texts/viet.txt",  "pages": null }
```

### Tình huống B — Nửa đầu PDF là Hán, nửa sau là Việt
```json
{ "lang": "han",  "format": "pdf", "path": "data/raw/pdfs/book.pdf", "pages": "1-80"   },
{ "lang": "viet", "format": "pdf", "path": "data/raw/pdfs/book.pdf", "pages": "81-150" }
```

### Tình huống C — Trang xen kẽ (lẻ=Hán, chẵn=Việt)
```json
{ "lang": "han",  "format": "pdf", "path": "data/raw/pdfs/book.pdf", "pages": "1,3,5,7" },
{ "lang": "viet", "format": "pdf", "path": "data/raw/pdfs/book.pdf", "pages": "2,4,6,8" }
```

### Tình huống D — Cùng 1 trang có cả Hán lẫn Việt (2 cột hoặc trên/dưới)
```json
{ "lang": "han",  "format": "mixed_page", "path": "data/raw/pdfs/book.pdf", "pages": null },
{ "lang": "viet", "format": "mixed_page", "path": "data/raw/pdfs/book.pdf", "pages": null }
```
→ `ocr_engine.py` crop ảnh theo vùng (dựa vào tọa độ pixel hoặc tỷ lệ cố định),
  rồi áp **PaddleOCR** cho vùng Hán và **pytesseract** cho vùng Việt.
  Tọa độ crop có thể cấu hình thêm field `region` trong config nếu cần.

---

## 5. `ocr_segmentation` — Chi tiết

### Mục tiêu
Với mỗi tác phẩm trong `config.json`, xử lý từng resource và xuất:
- `ocr_output/<id>/han.txt` và/hoặc `viet.txt`
- `processed/<id>/han.json` và/hoặc `viet.json`

### Flow

```
data/config.json
      │
      ▼ config_loader.py — đọc, validate, resolve paths
      │
      ├─ format = "pdf"        → pdf_to_images.py → ảnh tạm trong RAM/temp
      ├─ format = "images"     → đọc thẳng từ thư mục
      ├─ format = "text"       → skip OCR, đọc file text gốc
      └─ format = "mixed_page" → pdf_to_images.py → ảnh tạm
      │
      ▼ ocr_engine.py
      ├─ lang = "han",  format ≠ text → PaddleOCR (lang="ch", nhận diện Hán tự theo cột)
      ├─ lang = "viet", format ≠ text → pytesseract (lang="vie", nhận diện tiếng Việt có dấu)
      │                               hoặc extract text-layer PDF nếu PDF có sẵn text (không cần OCR)
      ├─ format = "text"              → đọc thẳng, không OCR
      └─ format = "mixed_page"        → crop ảnh theo vùng (trên/dưới hoặc trái/phải)
                                        rồi áp PaddleOCR cho vùng Hán, pytesseract cho vùng Việt
      │
      ▼ bbox_sort.py (chỉ áp dụng cho Hán)
        Sắp xếp bbox: phải → trái, trên → dưới
      │
      ▼ Ghi ocr_output/<id>/han.txt hoặc viet.txt
        (mỗi dòng = 1 bbox hoặc 1 đoạn văn)
      │
      ▼ segmenter.py
      ├─ lang = "han"  → HanLP sentence tokenizer
      └─ lang = "viet" → Underthesea sent_tokenize
      │
      ▼ Ghi processed/<id>/han.json hoặc viet.json
```

### Cách chạy
```bash
# Toàn bộ tác phẩm trong config
python src/ocr_segmentation/run.py

# Chỉ 1 tác phẩm
python src/ocr_segmentation/run.py --work-id an-nam-chi-luoc

# Chỉ 1 ngôn ngữ của 1 tác phẩm
python src/ocr_segmentation/run.py --work-id an-nam-chi-luoc --lang han
```

---

## 6. `sentence_alignment` — Chi tiết

### Mục tiêu
Đọc `processed/<id>/han.json` + `viet.json`, dóng hàng câu Hán ↔ Việt, xuất corpus TSV.

### Flow

```
processed/<id>/han.json  +  viet.json
      │
      ▼ aligner.py — chọn 1 trong 3 method:
      │
      ├─ Method 1: LaBSE cosine similarity       (khuyên dùng, cần sentence-transformers)
      ├─ Method 2: Auto-translate Hán→Việt        (Gemini API + TF-IDF so sánh)
      └─ Method 3: Greedy length ratio            (fallback, không cần thư viện ngoài)
      │
      ▼ (optional) char_aligner.py
        MED Levenshtein + SinoNom_Similar.dic + QuocNgu_SinoNom.dic
        → verify từng ký tự OCR, đánh dấu: đúng (đen) / sửa (xanh) / sai (đỏ)
      │
      ▼ corpus_builder.py
        Gán ID theo chuẩn HVB_fff.ccc.ppp.ss
        Xuất corpus/<id>/HVB_corpus.tsv
      │
      ▼ (sau khi xử lý hết tất cả works)
        Gộp → corpus/HVB_corpus_all.tsv
```

### Cách chạy
```bash
# Toàn bộ tác phẩm, method mặc định (LaBSE)
python src/sentence_alignment/run.py

# Chỉ 1 tác phẩm
python src/sentence_alignment/run.py --work-id an-nam-chi-luoc

# Chọn method
python src/sentence_alignment/run.py --method labse
python src/sentence_alignment/run.py --method auto_translate
python src/sentence_alignment/run.py --method greedy
```

---

## 7. Format output

### `ocr_output/<id>/han.txt`
Mỗi dòng = text của 1 bbox (cột chữ), theo thứ tự đọc đã sort:
```
越南立國之始
歷代君王相繼
北屬千年之久
```

### `ocr_output/<id>/viet.txt`
Mỗi dòng = 1 đoạn/câu Việt:
```
Thuở nước Việt Nam mới dựng nước.
Các đời vua nối nhau trị vì.
Nghìn năm bị phương Bắc đô hộ.
```

### `processed/<id>/han.json`
```json
{
  "work_id": "an-nam-chi-luoc",
  "lang": "han",
  "total_sentences": 3,
  "sentences": [
    { "idx": 0, "text": "越南立國之始" },
    { "idx": 1, "text": "歷代君王相繼" },
    { "idx": 2, "text": "北屬千年之久" }
  ]
}
```

### `processed/<id>/viet.json`
```json
{
  "work_id": "an-nam-chi-luoc",
  "lang": "viet",
  "total_sentences": 3,
  "sentences": [
    { "idx": 0, "text": "Thuở nước Việt Nam mới dựng nước." },
    { "idx": 1, "text": "Các đời vua nối nhau trị vì." },
    { "idx": 2, "text": "Nghìn năm bị phương Bắc đô hộ." }
  ]
}
```

### `corpus/<id>/HVB_corpus.tsv`
```tsv
id                    han_text          viet_text                              align_score
HVB_001.001.001.01    越南立國之始       Thuở nước Việt Nam mới dựng nước.     0.92
HVB_001.001.001.02    歷代君王相繼       Các đời vua nối nhau trị vì.          0.88
HVB_001.001.001.03    北屬千年之久       Nghìn năm bị phương Bắc đô hộ.        0.85
```

**ID format:** `HVB_fff.ccc.ppp.ss`
- `HVB` = do GV cấp
- `fff` = file index (tác phẩm thứ mấy)
- `ccc` = chapter/chương
- `ppp` = page/trang
- `ss`  = sentence index trong trang

---

## 8. Thư viện sử dụng

| Thư viện | Module | Mục đích | Ghi chú |
|----------|--------|----------|---------|
| `pymupdf` | `ocr_segmentation` | PDF → ảnh JPG | Không cần Poppler/GPU |
| `paddleocr` | `ocr_segmentation` | OCR chữ Hán/Nôm | `lang="ch"`, CPU OK (~3-5s/ảnh) |
| `paddlepaddle` | `ocr_segmentation` | Runtime của PaddleOCR | Dùng bản CPU, không cần GPU |
| `pytesseract` | `ocr_segmentation` | OCR tiếng Việt có dấu | Cần cài Tesseract engine riêng + gói `vie` |
| `Pillow` | `ocr_segmentation` | Xử lý/crop ảnh | |
| `underthesea` | `ocr_segmentation` | Tách câu tiếng Việt | CPU only |
| `hanlp` | `ocr_segmentation` | Tách câu tiếng Hán | Model ~500MB, CPU OK |
| `sentence-transformers` | `sentence_alignment` | LaBSE alignment | Model ~1.8GB, CPU OK |
| `google-generativeai` | `sentence_alignment` | Auto-translate method (optional) | Chỉ cần nếu dùng method 2 |
| `python-dotenv` | `sentence_alignment` | Đọc GEMINI_API_KEY (optional) | Chỉ cần nếu dùng method 2 |
| `pyyaml` | Cả 2 | Đọc `pipeline.yaml` | |
| `tqdm` | Cả 2 | Progress bar | |

**Cài đặt:**
```bash
# Thư viện Python
pip install pymupdf paddleocr paddlepaddle pytesseract \
            underthesea sentence-transformers \
            pyyaml tqdm Pillow

pip install hanlp   # cài riêng vì nặng (~500MB model)

# Tesseract OCR engine (cần cài riêng ngoài pip):
# Windows: tải installer tại https://github.com/UB-Mannheim/tesseract/wiki
#           sau đó tải thêm gói ngôn ngữ "vie" (tiếng Việt)
# Linux:   sudo apt install tesseract-ocr tesseract-ocr-vie
# macOS:   brew install tesseract && brew install tesseract-lang
```

---

## 9. Setup & Thứ tự thực hiện

```
Bước 1: Điền data/config.json với đường dẫn tác phẩm thực tế

Bước 2: Cài Tesseract engine (cho pytesseract tiếng Việt)
         Windows → tải https://github.com/UB-Mannheim/tesseract/wiki
                   tích chọn "Vietnamese" khi cài
         Linux   → sudo apt install tesseract-ocr tesseract-ocr-vie

Bước 3: pip install -r requirements.txt

Bước 4: (Optional) Nếu dùng method auto_translate ở Part 2:
         Lấy Gemini API key tại https://aistudio.google.com/app/apikey
         Copy .env.example → .env, điền GEMINI_API_KEY=...

Bước 5: python src/ocr_segmentation/run.py
         → Kiểm tra ocr_output/<id>/ và processed/<id>/

Bước 6: python src/sentence_alignment/run.py
         → Kiểm tra corpus/<id>/HVB_corpus.tsv

Bước 7: Review thủ công corpus, sửa lỗi alignment nếu cần
         Có thể chạy lại Bước 6 với method khác mà không mất kết quả OCR
```

