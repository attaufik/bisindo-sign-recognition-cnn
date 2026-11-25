import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        
        # Don't draw header/footer on cover/first page if desired, or draw minimal
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, 810, "DOKUMENTASI SPESIFIKASI PROYEK: BISINDO AI (BAHASA ISYARAT INDONESIA)")
            self.drawRightString(555, 810, "ARSITEKTUR & BLUEPRINT SKILL")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(40, 804, 555, 804)

            # Footer
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, 30, "Kecerdasan Buatan (Sem 5) • CNN + Flask Microservice • Format Panduan Claude / Gemini Skill")
            self.drawRightString(555, 30, f"Halaman {self._pageNumber} dari {page_count}")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(40, 42, 555, 42)
            
        self.restoreState()

def create_bisindo_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A233A")
    accent_blue = colors.HexColor("#2563EB")
    slate_dark = colors.HexColor("#334155")
    slate_light = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        alignment=0,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=slate_dark,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=slate_dark
    )

    table_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # ==========================
    # COVER / HEADER BANNER
    # ==========================
    banner_data = [
        [
            Paragraph("<font size='10' color='#2563EB'><b>PROYEK KECERDASAN BUATAN (SEMESTER 5)</b></font><br/>"
                      "<b><font size='18' color='#1A233A'>BISINDO AI: Deteksi Alfabet Isyarat Real-Time</font></b><br/>"
                      "<font size='9' color='#64748B'>Dokumentasi Komprehensif Arsitektur Sistem, Dataset, Model Deep Learning CNN, Backend API, Frontend & Spesifikasi Skill AI</font>",
                      body_style)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[515])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 12))

    # Meta Info Card
    meta_data = [
        [
            Paragraph("<b>Identitas Proyek:</b>", body_style),
            Paragraph("BISINDO AI (Bahasa Isyarat Indonesia Recognition)", body_style),
            Paragraph("<b>Model Format:</b>", body_style),
            Paragraph("Keras H5 (<code>model_bisindo_super.h5</code>)", code_style)
        ],
        [
            Paragraph("<b>Domain:</b>", body_style),
            Paragraph("Computer Vision & Deep Learning (CNN)", body_style),
            Paragraph("<b>Ukuran Model:</b>", body_style),
            Paragraph("2.05 MB (537,308 Parameter)", body_style)
        ],
        [
            Paragraph("<b>Total Dataset:</b>", body_style),
            Paragraph("31,319 Citra (26 Kelas Abjad A-Z)", body_style),
            Paragraph("<b>Backend / UI:</b>", body_style),
            Paragraph("Flask Microservice + Tailwind Web App", body_style)
        ],
        [
            Paragraph("<b>Tujuan Dokumen:</b>", body_style),
            Paragraph("Bahan acuan pembuatan Skill / Agent Tool di Gemini oleh Claude", body_style),
            Paragraph("<b>Input Dimensi:</b>", body_style),
            Paragraph("128 x 128 x 3 (RGB Normalized)", code_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[95, 165, 95, 160])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 1. LATAR BELAKANG & TUJUAN
    # ==========================
    story.append(Paragraph("1. Latar Belakang & Deskripsi Proyek", h1_style))
    story.append(Paragraph(
        "<b>BISINDO (Bahasa Isyarat Indonesia)</b> adalah sistem bahasa isyarat alami yang digunakan secara luas "
        "oleh komunitas Tuli di Indonesia. Berbeda dengan SIBI (Sistem Isyarat Bahasa Indonesia) yang sering memakai satu tangan, "
        "BISINDO memiliki keunikan gerak dan konfigurasi tangan yang adaptif dan kaya konteks visual. "
        "Tujuan utama proyek ini adalah mengembangkan sistem cerdas berbasis <b>Deep Learning Convolutional Neural Network (CNN)</b> "
        "yang mampu mendeteksi dan mengklasifikasikan 26 huruf alfabet BISINDO (A hingga Z) secara instan (real-time) menggunakan webcam laptop/komputer "
        "maupun melalui unggah berkas gambar statis.",
        body_style
    ))
    story.append(Paragraph(
        "Sistem ini dibangun secara menyeluruh mulai dari kurasi dataset citra, augmentasi gambar, perancangan model CNN khusus "
        "dengan bobot ringan dan akurasi tinggi, integrasi microservice backend menggunakan Flask API, "
        "hingga antarmuka pengguna interaktif (Web Dashboard) dengan panduan area deteksi (Region of Interest / ROI).",
        body_style
    ))

    # ==========================
    # 2. ARSITEKTUR & WORKFLOW
    # ==========================
    story.append(Paragraph("2. Alur Kerja Sistem (End-to-End Workflow)", h1_style))
    story.append(Paragraph(
        "Sistem berjalan dengan siklus transmisi asinkron antara antarmuka web klien dan peladen Flask secara terus-menerus:",
        body_style
    ))

    flow_data = [
        [
            Paragraph("<b>Tahap</b>", table_header_style),
            Paragraph("<b>Komponen</b>", table_header_style),
            Paragraph("<b>Deskripsi Teknis</b>", table_header_style),
            Paragraph("<b>Output / Data</b>", table_header_style)
        ],
        [
            Paragraph("1. Akuisisi", table_cell_style),
            Paragraph("Webcam / File Upload", table_cell_style),
            Paragraph("Pengguna mengarahkan gestur tangan ke dalam kotak hijau ROI di layar browser (mode live) atau memilih file foto.", table_cell_style),
            Paragraph("Video stream / File buffer", table_cell_code)
        ],
        [
            Paragraph("2. Ekstraksi", table_cell_style),
            Paragraph("HTML5 Canvas & JS", table_cell_style),
            Paragraph("JavaScript mengambil snapshot frame setiap 500 ms (2 FPS) dan mengenkripsi frame menjadi format Base64 DataURL.", table_cell_style),
            Paragraph("<code>data:image/jpeg;base64,...</code>", table_cell_code)
        ],
        [
            Paragraph("3. Transmisi", table_cell_style),
            Paragraph("Fetch API (HTTP POST)", table_cell_style),
            Paragraph("Frame Base64 dikirimkan sebagai payload JSON menuju endpoint <code>/predict_snapshot</code>.", table_cell_style),
            Paragraph("JSON <code>{ image: ... }</code>", table_cell_code)
        ],
        [
            Paragraph("4. Preprocessing", table_cell_style),
            Paragraph("OpenCV + NumPy", table_cell_style),
            Paragraph("Decoding Base64 buffer, konversi BGR ke RGB, resize citra menjadi 128x128 piksel, dan normalisasi nilai piksel (dibagi 255.0).", table_cell_style),
            Paragraph("Tensor Shape: <code>(1, 128, 128, 3)</code>", table_cell_code)
        ],
        [
            Paragraph("5. Inferensi", table_cell_style),
            Paragraph("TensorFlow / Keras", table_cell_style),
            Paragraph("Model CNN <code>model_bisindo_super.h5</code> memproses tensor dan mengeluarkan vektor distribusi probabilitas 26 kelas via Softmax.", table_cell_style),
            Paragraph("26 Softmax Probabilities", table_cell_code)
        ],
        [
            Paragraph("6. Respons & Visual", table_cell_style),
            Paragraph("Flask & Tailwind UI", table_cell_style),
            Paragraph("Mengembalikan huruf terbaik (Argmax) dan persentase keyakinan. DOM frontend diperbarui seketika dengan animasi progress bar.", table_cell_style),
            Paragraph("JSON <code>{'huruf':'A', 'akurasi':'98.5'}</code>", table_cell_code)
        ]
    ]
    flow_table = Table(flow_data, colWidths=[65, 85, 235, 130])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, slate_light]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 3. SPESIFIKASI DATASET
    # ==========================
    story.append(Paragraph("3. Analisis Dataset & Pipeline Augmentasi", h1_style))
    story.append(Paragraph(
        "Dataset proyek terdiri dari kumpulan citra alfabet isyarat BISINDO yang terbagi menjadi dua direktori utama: "
        "<b>Pelatihan (Train)</b> dan <b>Validasi (Val)</b>. Total terdapat <b>31.319 citra</b> yang mencakup seluruh 26 abjad latin:",
        body_style
    ))

    ds_summary = [
        [
            Paragraph("<b>Direktori Dataset</b>", table_header_style),
            Paragraph("<b>Jumlah Gambar</b>", table_header_style),
            Paragraph("<b>Jumlah Kelas</b>", table_header_style),
            Paragraph("<b>Rata-rata per Kelas</b>", table_header_style),
            Paragraph("<b>Rasio Split</b>", table_header_style)
        ],
        [
            Paragraph("<code>images/train/</code>", table_cell_code),
            Paragraph("26.946 citra", table_cell_style),
            Paragraph("26 Kelas (A - Z)", table_cell_style),
            Paragraph("~1.036 citra / huruf", table_cell_style),
            Paragraph("~86.0 %", table_cell_style)
        ],
        [
            Paragraph("<code>images/val/</code>", table_cell_code),
            Paragraph("4.373 citra", table_cell_style),
            Paragraph("26 Kelas (A - Z)", table_cell_style),
            Paragraph("~168 citra / huruf", table_cell_style),
            Paragraph("~14.0 %", table_cell_style)
        ],
        [
            Paragraph("<b>TOTAL KESELURUHAN</b>", table_cell_style),
            Paragraph("<b>31.319 citra</b>", table_cell_style),
            Paragraph("<b>26 Kelas</b>", table_cell_style),
            Paragraph("<b>1.204 citra / huruf</b>", table_cell_style),
            Paragraph("<b>100.0 %</b>", table_cell_style)
        ]
    ]
    ds_table = Table(ds_summary, colWidths=[120, 95, 100, 110, 90])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), accent_blue),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, slate_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E0E7FF")),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Konfigurasi Augmentasi Citra (ImageDataGenerator):</b>", h2_style))
    story.append(Paragraph(
        "Untuk mencegah overfitting serta meningkatkan ketahanan model terhadap variasi pencahayaan, sudut tangan, dan jarak kamera pada lingkungan nyata, "
        "diterapkan teknik augmentasi data dinamis pada pipeline pelatihan:",
        body_style
    ))

    aug_data = [
        [
            Paragraph("<b>Parameter Augmentasi</b>", table_header_style),
            Paragraph("<b>Nilai Konfigurasi</b>", table_header_style),
            Paragraph("<b>Tujuan Fungsional</b>", table_header_style)
        ],
        [
            Paragraph("<code>rescale</code>", table_cell_code),
            Paragraph("<code>1.0 / 255.0</code>", table_cell_code),
            Paragraph("Normalisasi nilai kecerahan piksel dari rentang [0, 255] menjadi rentang desimal [0.0, 1.0].", table_cell_style)
        ],
        [
            Paragraph("<code>rotation_range</code>", table_cell_code),
            Paragraph("15 derajat", table_cell_style),
            Paragraph("Simulasi kemiringan orientasi pergelangan tangan pengguna secara natural.", table_cell_style)
        ],
        [
            Paragraph("<code>width_shift_range</code>", table_cell_code),
            Paragraph("0.1 (10% lebar)", table_cell_style),
            Paragraph("Mengakomodasi pergeseran posisi horizontal tangan dalam area kamera.", table_cell_style)
        ],
        [
            Paragraph("<code>height_shift_range</code>", table_cell_code),
            Paragraph("0.1 (10% tinggi)", table_cell_style),
            Paragraph("Mengakomodasi pergeseran vertikal gestur tangan pengguna.", table_cell_style)
        ],
        [
            Paragraph("<code>zoom_range</code>", table_cell_code),
            Paragraph("0.1 (±10%)", table_cell_style),
            Paragraph("Simulasi variasi jarak tangan terhadap lensa kamera (skala tangan besar/kecil).", table_cell_style)
        ],
        [
            Paragraph("<code>brightness_range</code>", table_cell_code),
            Paragraph("[0.8, 1.2]", table_cell_style),
            Paragraph("Ketahanan model terhadap perbedaan intensitas cahaya ruangan (redup maupun terang).", table_cell_style)
        ],
        [
            Paragraph("<code>fill_mode</code>", table_cell_code),
            Paragraph("'nearest'", table_cell_style),
            Paragraph("Strategi pengisian piksel kosong akibat rotasi atau translasi citra.", table_cell_style)
        ],
        [
            Paragraph("<code>target_size & batch</code>", table_cell_code),
            Paragraph("128 x 128 piksel | Batch: 32", table_cell_code),
            Paragraph("Resolusi kompromi terbaik antara kecepatan inferensi dan ketajaman fitur jari tangan.", table_cell_style)
        ]
    ]
    aug_table = Table(aug_data, colWidths=[130, 130, 255])
    aug_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, slate_light]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(aug_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 4. ARSITEKTUR MODEL CNN
    # ==========================
    story.append(Paragraph("4. Detail Arsitektur Deep Learning (Convolutional Neural Network)", h1_style))
    story.append(Paragraph(
        "Arsitektur jaringan dirancang secara kustom dengan 4 blok konvolusi bertingkat. Fitur penting dari rancangan ini adalah "
        "penggunaan <b>Batch Normalization</b> di setiap blok untuk mempercepat konvergensi gradien, serta penggunaan "
        "<b>GlobalAveragePooling2D</b> sebagai pengganti <code>Flatten()</code> konvensional. Langkah ini memangkas jutaan bobot fully-connected, "
        "sehingga ukuran model sangat ringkas (hanya 2.05 MB) dan memiliki ketahanan tinggi terhadap overfitting.",
        body_style
    ))

    arch_data = [
        [
            Paragraph("<b>Blok / Layer</b>", table_header_style),
            Paragraph("<b>Tipe Lapisan</b>", table_header_style),
            Paragraph("<b>Output Shape</b>", table_header_style),
            Paragraph("<b>Jumlah Parameter</b>", table_header_style),
            Paragraph("<b>Aktivasi & Keterangan</b>", table_header_style)
        ],
        [
            Paragraph("<b>Blok 1</b>", table_cell_style),
            Paragraph("Conv2D (32, 3x3)<br/>BatchNorm<br/>MaxPooling2D (2x2)", table_cell_code),
            Paragraph("(None, 126, 126, 32)<br/>(None, 126, 126, 32)<br/>(None, 63, 63, 32)", table_cell_code),
            Paragraph("896<br/>128<br/>0", table_cell_style),
            Paragraph("Ekstraksi tepi & kontur jari tahap awal. ReLU aktivasi.", table_cell_style)
        ],
        [
            Paragraph("<b>Blok 2</b>", table_cell_style),
            Paragraph("Conv2D (64, 3x3)<br/>BatchNorm<br/>MaxPooling2D (2x2)", table_cell_code),
            Paragraph("(None, 61, 61, 64)<br/>(None, 61, 61, 64)<br/>(None, 30, 30, 64)", table_cell_code),
            Paragraph("18,496<br/>256<br/>0", table_cell_style),
            Paragraph("Deteksi pola bentuk kurva dan sudut lekukan jari tangan.", table_cell_style)
        ],
        [
            Paragraph("<b>Blok 3</b>", table_cell_style),
            Paragraph("Conv2D (128, 3x3)<br/>BatchNorm<br/>MaxPooling2D (2x2)", table_cell_code),
            Paragraph("(None, 28, 28, 128)<br/>(None, 28, 28, 128)<br/>(None, 14, 14, 128)", table_cell_code),
            Paragraph("73,856<br/>512<br/>0", table_cell_style),
            Paragraph("Pengenalan struktur gestur isyarat yang lebih kompleks.", table_cell_style)
        ],
        [
            Paragraph("<b>Blok 4</b>", table_cell_style),
            Paragraph("Conv2D (256, 3x3)<br/>BatchNorm<br/>MaxPooling2D (2x2)", table_cell_code),
            Paragraph("(None, 12, 12, 256)<br/>(None, 12, 12, 256)<br/>(None, 6, 6, 256)", table_cell_code),
            Paragraph("295,168<br/>1,024<br/>0", table_cell_style),
            Paragraph("Kapasitas ekstra untuk representasi 25.000+ data latihan.", table_cell_style)
        ],
        [
            Paragraph("<b>Pooling</b>", table_cell_style),
            Paragraph("GlobalAveragePool2D", table_cell_code),
            Paragraph("(None, 256)", table_cell_code),
            Paragraph("0", table_cell_style),
            Paragraph("Mereduksi seluruh feature map menjadi vektor 256-D tanpa parameter.", table_cell_style)
        ],
        [
            Paragraph("<b>Dense FC</b>", table_cell_style),
            Paragraph("Dense (512 neuron)<br/>BatchNorm<br/>Dropout (0.5)", table_cell_code),
            Paragraph("(None, 512)<br/>(None, 512)<br/>(None, 512)", table_cell_code),
            Paragraph("131,584<br/>2,048<br/>0", table_cell_style),
            Paragraph("Fully-connected classifier. Dropout 50% untuk regularisasi ketat.", table_cell_style)
        ],
        [
            Paragraph("<b>Output</b>", table_cell_style),
            Paragraph("Dense (26 kelas)", table_cell_code),
            Paragraph("(None, 26)", table_cell_code),
            Paragraph("13,338", table_cell_style),
            Paragraph("Aktivasi <b>Softmax</b> untuk probabilitas kelas huruf A sampai Z.", table_cell_style)
        ],
        [
            Paragraph("<b>TOTAL</b>", table_cell_style),
            Paragraph("<b>Model Sequential</b>", table_cell_style),
            Paragraph("<b>Bobot File: 2.05 MB</b>", table_cell_style),
            Paragraph("<b>537,308 Param</b>", table_cell_style),
            Paragraph("Trainable: 535,322 | Non-trainable: 1,984", table_cell_style)
        ]
    ]
    arch_table = Table(arch_data, colWidths=[55, 115, 125, 75, 145])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, slate_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#DBEAFE")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Mekanisme Pelatihan & Callbacks (train_terminal.py):</b>", h2_style))
    story.append(Paragraph(
        "Pelatihan model dilengkapi dua callback proteksi otomatis untuk menjaga kestabilan dan bobot optimal:<br/>"
        "• <b>ReduceLROnPlateau:</b> Memonitor <code>val_accuracy</code> dengan parameter <code>patience=3</code>, <code>factor=0.5</code>, dan batas minimum learning rate <code>min_lr=1e-5</code>. Apabila akurasi validasi tidak meningkat selama 3 epoch beruntun, learning rate dipangkas separuhnya.<br/>"
        "• <b>EarlyStopping:</b> Memonitor <code>val_loss</code> dengan <code>patience=6</code> dan <code>restore_best_weights=True</code>. Pelatihan akan berhenti secara dini bila loss validasi mengalami stagnasi, serta mengembalikan bobot epoch paling prima secara otomatis.<br/>"
        "• <b>Optimizer:</b> Adam | <b>Loss Function:</b> Categorical Crossentropy | <b>Target Epoch:</b> 50 Epochs.",
        body_style
    ))
    story.append(Spacer(1, 14))

    # ==========================
    # 5. BACKEND API FLASK
    # ==========================
    story.append(Paragraph("5. Arsitektur Backend API & Kontrak Data (Flask Microservice)", h1_style))
    story.append(Paragraph(
        "Backend diimplementasikan menggunakan micro-framework <b>Flask</b> (<code>frontend/app.py</code>) dengan integrasi pustaka <b>OpenCV</b> dan <b>TensorFlow Keras</b>. "
        "Server bertindak sebagai model inference engine lokal dengan latency rendah.",
        body_style
    ))

    api_data = [
        [
            Paragraph("<b>Spesifikasi</b>", table_header_style),
            Paragraph("<b>Endpoint 1: Halaman Web</b>", table_header_style),
            Paragraph("<b>Endpoint 2: Prediksi Snapshot</b>", table_header_style)
        ],
        [
            Paragraph("<b>Routing Path</b>", table_cell_style),
            Paragraph("<code>GET /</code>", table_cell_code),
            Paragraph("<code>POST /predict_snapshot</code>", table_cell_code)
        ],
        [
            Paragraph("<b>Fungsi Handler</b>", table_cell_style),
            Paragraph("<code>index()</code>", table_cell_code),
            Paragraph("<code>predict_snapshot()</code>", table_cell_code)
        ],
        [
            Paragraph("<b>Request Header</b>", table_cell_style),
            Paragraph("Standard HTTP GET", table_cell_style),
            Paragraph("<code>Content-Type: application/json</code>", table_cell_code)
        ],
        [
            Paragraph("<b>Request Payload</b>", table_cell_style),
            Paragraph("None (Hanya request URL)", table_cell_style),
            Paragraph("<code>{\n  \"image\": \"data:image/jpeg;base64,/9j/4AAQ...\"\n}</code>", table_cell_code)
        ],
        [
            Paragraph("<b>Tahap Pemrosesan</b>", table_cell_style),
            Paragraph("Merender berkas template <code>templates/index.html</code> ke browser.", table_cell_style),
            Paragraph("1. Parsing string Base64 & pemisahan header DataURL<br/>"
                      "2. Konversi bytes ke array NumPy (<code>np.frombuffer</code>)<br/>"
                      "3. Decoding citra OpenCV (<code>cv2.imdecode</code>)<br/>"
                      "4. Transformasi BGR ke RGB (<code>cv2.cvtColor</code>)<br/>"
                      "5. Resize spasial ke 128x128 piksel (<code>cv2.resize</code>)<br/>"
                      "6. Normalisasi skalar: <code>img / 255.0</code><br/>"
                      "7. Ekspansi batch dimension: shape <code>(1, 128, 128, 3)</code><br/>"
                      "8. Inferensi: <code>model.predict(img_input)</code><br/>"
                      "9. Ekstraksi kelas via <code>np.argmax</code> dan nilai confidence.", table_cell_style)
        ],
        [
            Paragraph("<b>Response Success</b>", table_cell_style),
            Paragraph("HTTP 200 (HTML Web Page)", table_cell_style),
            Paragraph("<code>{\n  \"huruf\": \"B\",\n  \"akurasi\": \"96.74\"\n}</code> (Status 200 OK)", table_cell_code)
        ],
        [
            Paragraph("<b>Response Error</b>", table_cell_style),
            Paragraph("Standard HTTP 404 / 500", table_cell_style),
            Paragraph("<code>{\n  \"error\": \"&lt;Pesan kesalahan sistem&gt;\"\n}</code>", table_cell_code)
        ]
    ]
    api_table = Table(api_data, colWidths=[90, 150, 275])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, slate_light]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(api_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 6. FRONTEND & UI/UX DESIGN
    # ==========================
    story.append(Paragraph("6. Antarmuka Pengguna & Fitur Interaktif (Frontend)", h1_style))
    story.append(Paragraph(
        "Frontend dirancang modern berbasis standar UI/UX modern terinspirasi dari layout desain Figma, menggunakan "
        "<b>TailwindCSS</b> (via CDN) dan tipografi <b>Inter Font Family</b>. Tampilan memiliki struktur dual-pane yang responsif:",
        body_style
    ))

    ui_points = [
        [
            Paragraph("<b>Komponen UI</b>", table_header_style),
            Paragraph("<b>Fitur & Karakteristik Teknis</b>", table_header_style)
        ],
        [
            Paragraph("<b>Sidebar Navigasi</b><br/>(Background <code>#1A233A</code>)", table_cell_style),
            Paragraph("• Logo BISINDO AI dengan icon badge dinamis.<br/>"
                      "• Menu Workspace: Dashboard, Live Detection (Active View), Detection History, BISINDO Alphabet Guide.<br/>"
                      "• Widget status model di pojok bawah: <i>Custom CNN • 26 Alphabets • TensorFlow & Flask</i>.", table_cell_style)
        ],
        [
            Paragraph("<b>Dual-Mode Input Panel</b>", table_cell_style),
            Paragraph("• <b>Mode 1 - Kamera Langsung (Default):</b> Mengakses webcam via WebRTC (<code>navigator.mediaDevices.getUserMedia</code>). Video di-mirror secara horizontal (<code>-scale-x-100</code>) agar menyerupai cermin alami.<br/>"
                      "• <b>Bounding Box ROI (Region of Interest):</b> Kotak hijau putus-putus transparan berukuran 60% x 60% tepat di tengah kanvas video sebagai panduan peletakan gestur tangan agar akurasi maksimal.<br/>"
                      "• <b>Mode 2 - Upload Gambar:</b> Drag-and-drop / klik browser berkas untuk menganalisis gambar format JPG atau PNG dari media penyimpanan.", table_cell_style)
        ],
        [
            Paragraph("<b>Panel Hasil Prediksi</b>", table_cell_style),
            Paragraph("• <b>Tipografi Huruf Super Besar:</b> Menampilkan karakter abjad terdeteksi (A - Z) dalam ukuran font <code>text-8xl</code> hitam tebal.<br/>"
                      "• <b>Confidence Metric:</b> Nilai probabilitas model dalam persentase desimal dua angka di belakang koma (contoh: <code>99.12%</code>).<br/>"
                      "• <b>Dynamic Progress Bar:</b> Bar visual animasi hijau yang memanjang seiring kenaikan tingkat keyakinan prediksi.<br/>"
                      "• <b>Badge Status Deteksi:</b> Indikator hijau berkedip saat kamera aktif dan pendeteksian berjalan lancar.", table_cell_style)
        ],
        [
            Paragraph("<b>Looping Snapshot (JS)</b>", table_cell_style),
            Paragraph("Menggunakan <code>setInterval</code> berkecepatan 500 ms (2 frame per detik) yang menggambar frame video saat itu ke elemen <code>&lt;canvas&gt;</code> tersembunyi, mengubahnya ke JPEG Base64, lalu melakukan asynchronous fetch POST.", table_cell_style)
        ]
    ]
    ui_table = Table(ui_points, colWidths=[140, 375])
    ui_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, slate_light]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ui_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 7. STRUKTUR DIREKTORI PROYEK
    # ==========================
    story.append(Paragraph("7. Struktur Direktori & Berkas Proyek", h1_style))
    story.append(Paragraph(
        "Berikut adalah hierarki lengkap folder dan file di dalam repositori proyek BISINDO:",
        body_style
    ))

    tree_text = """bisindo/
├── train_terminal.py              # Script utama training model CNN menggunakan TensorFlow/Keras
├── frontend/
│   ├── app.py                     # Server backend Flask (routing, API /predict_snapshot, load model)
│   ├── model_bisindo_super.h5     # Bobot model terlatih final (26 kelas, ukuran 2.05 MB)
│   ├── static/
│   │   └── uploads/               # Direktori penyimpanan sementara berkas gambar yang diunggah
│   ├── templates/
│   │   └── index.html             # Tampilan antarmuka pengguna (TailwindCSS, JS Webcam, Live Predict)
│   └── env_gpu/                   # Virtual environment Python lokal
└── images/
    ├── train/                     # Direktori data latihan (26 folder: A/ sampai Z/, total 26.946 file)
    └── val/                       # Direktori data validasi (26 folder: A/ sampai Z/, total 4.373 file)"""

    tree_table = Table([[Paragraph(f"<pre>{tree_text}</pre>", code_style)]], colWidths=[515])
    tree_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tree_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 8. PANDUAN EKSEKUSI
    # ==========================
    story.append(Paragraph("8. Panduan Instalasi & Eksekusi Sistem", h1_style))
    story.append(Paragraph(
        "Langkah-langkah untuk menjalankan sistem klasifikasi bahasa isyarat BISINDO di komputer lokal:",
        body_style
    ))

    run_steps = [
        [
            Paragraph("<b>Tahap</b>", table_header_style),
            Paragraph("<b>Perintah Terminal / PowerShell</b>", table_header_style),
            Paragraph("<b>Hasil / Keterangan</b>", table_header_style)
        ],
        [
            Paragraph("1. Persiapan Dependensi", table_cell_style),
            Paragraph("<code>pip install tensorflow flask opencv-python numpy</code>", table_cell_code),
            Paragraph("Menginstal pustaka pemrosesan citra, deep learning, dan web framework.", table_cell_style)
        ],
        [
            Paragraph("2. Menjalankan Training (Opsional)", table_cell_style),
            Paragraph("<code>python train_terminal.py</code>", table_cell_code),
            Paragraph("Memulai proses pembelajaran 50 epoch pada 26.946 citra dan menghasilkan <code>model_bisindo_super.h5</code>.", table_cell_style)
        ],
        [
            Paragraph("3. Menjalankan Server Web", table_cell_style),
            Paragraph("<code>cd frontend\npython app.py</code>", table_cell_code),
            Paragraph("Memuat model CNN ke memori RAM/GPU dan menjalankan server pada port 5000.", table_cell_style)
        ],
        [
            Paragraph("4. Mengakses Aplikasi", table_cell_style),
            Paragraph("Buka browser: <code>http://127.0.0.1:5000</code>", table_cell_code),
            Paragraph("Izinkan akses kamera (Permission Allow) saat diminta oleh browser.", table_cell_style)
        ]
    ]
    run_table = Table(run_steps, colWidths=[90, 220, 205])
    run_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, slate_light]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(run_table)
    story.append(Spacer(1, 14))

    # ==========================
    # 9. PANDUAN CLAUDE MEMBUAT SKILL KE GEMINI
    # ==========================
    story.append(Paragraph("9. Panduan Khusus Claude: Spesifikasi Pembuatan Skill AI untuk Gemini", h1_style))
    story.append(Paragraph(
        "<i>Bagian ini disusun secara khusus sebagai instruksi teknis bagi Claude untuk menyusun modul AI Skill, Antigravity Custom Skill, "
        "ataupun MCP (Model Context Protocol) Server terstandarisasi untuk Gemini:</i>",
        callout_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>A. Definisi Fungsi & Skema Alat (Tool Definition / Function Calling Schema):</b>", h2_style))
    story.append(Paragraph(
        "Skill yang dibuat oleh Claude di Gemini dapat mengekspos fungsi klasifikasi gambar berikut:",
        body_style
    ))

    schema_text = """{
  "name": "predict_bisindo_alphabet",
  "description": "Mengklasifikasikan abjad Bahasa Isyarat Indonesia (BISINDO) dari citra input (base64 atau file path) ke dalam 26 kelas huruf (A-Z) beserta nilai akurasi keyakinan (confidence percentage).",
  "parameters": {
    "type": "object",
    "properties": {
      "image_base64": {
        "type": "string",
        "description": "String citra terenkode Base64 (dengan atau tanpa prefix data:image/jpeg;base64,)"
      },
      "image_path": {
        "type": "string",
        "description": "Path absolut file gambar lokal jika citra tersimpan di harddisk"
      }
    },
    "required": []
  }
}"""
    schema_table = Table([[Paragraph(f"<pre>{schema_text}</pre>", code_style)]], colWidths=[515])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(schema_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>B. System Instruction / Prompt Context untuk Gemini Agent:</b>", h2_style))
    prompt_text = """Anda adalah BISINDO AI Assistant, asisten ahli bahasa isyarat dan penerjemah Bahasa Isyarat Indonesia (BISINDO).
Karakteristik & Peran Utama:
1. Membantu pengguna mengenali, membaca, dan memverifikasi gestur huruf BISINDO (abjad A sampai Z).
2. Memanfaatkan model Convolutional Neural Network (CNN) khusus 26 kelas yang terlatih pada 31.319 citra isyarat.
3. Memberikan panduan fisik posisi jari dan tangan jika pengguna bertanya bagaimana cara membentuk huruf isyarat BISINDO tertentu.
4. Mampu memproses citra webcam atau berkas gambar melalui pemanggilan tool 'predict_bisindo_alphabet' dan menyajikan hasil berupa huruf dan tingkat kepercayaan (confidence rate).
5. Selalu bersikap inklusif, ramah terhadap komunitas Tuli, dan mengedepankan edukasi bahasa isyarat yang akurat dan mudah dipahami."""

    prompt_table = Table([[Paragraph(prompt_text.replace('\n', '<br/>'), callout_style)]], colWidths=[515])
    prompt_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(prompt_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>C. Skenario & Use Cases yang Didukung oleh Skill:</b>", h2_style))
    story.append(Paragraph(
        "1. <b>Real-Time Verification:</b> Asisten memverifikasi apakah gestur tangan pengguna di depan kamera sudah sesuai dengan standar BISINDO.<br/>"
        "2. <b>Spelling Word Builder:</b> Pengguna mengeja kata huruf demi huruf (finger-spelling), dan sistem menggabungkannya menjadi kata atau kalimat bermakna.<br/>"
        "3. <b>Interactive Sign Quiz:</b> Gemini memberikan tantangan huruf tertentu (misal: 'Tunjukkan huruf R'), lalu mengecek tangkapan kamera pengguna menggunakan model prediksi.<br/>"
        "4. <b>Educational Diagnostics:</b> Bila akurasi rendah (&lt;70%), asisten memberi rekomendasi perbaikan gestur (posisi ibu jari, jarak jari, atau sudut hadap telapak tangan).",
        body_style
    ))

    # ==========================
    # BUILD PDF
    # ==========================
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF berhasil dibuat: {output_filename}")

if __name__ == '__main__':
    out_path = os.path.abspath('BISINDO_AI_Project_Documentation.pdf')
    create_bisindo_pdf(out_path)

