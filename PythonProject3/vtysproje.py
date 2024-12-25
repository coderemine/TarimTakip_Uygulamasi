import customtkinter as ctk
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime, timedelta
import pyodbc
from tkinter import messagebox


# Kullanıcı veritabanı
USER_DB = "users.db"
FAILED_ATTEMPTS = {}
LOCK_DURATION = timedelta(minutes=1)

# Veritabanı bağlantı bilgileri
DB_CONFIG = {
    'driver': 'SQL Server',
    'server': 'DESKTOP-D11L7UA\\SQLEXPRESS',
    'database': 'TARIMTAKIP',
    'trusted_connection': 'yes'  # Windows Authentication
}

# Veritabanı bağlantı fonksiyonu
def get_db_connection():
    try:
        conn_str = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"Trusted_Connection=yes;"
        )
        print(f"Bağlantı dizesi: {conn_str}")  # Debug için
        return pyodbc.connect(conn_str)
    except pyodbc.Error as e:
        print(f"Bağlantı hatası: {str(e)}")
        raise

# Kullanıcı tablosunu oluştur
def initialize_user_db():
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    # İlk kullanıcıyı ekle
    cursor.execute("SELECT * FROM users WHERE username = 'vtys'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('vtys', hash_password('proje')))
        conn.commit()
    conn.close()

# Şifreyi hash'le
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Kullanıcı kaydet
def save_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Kullanıcı adı zaten varsa
    finally:
        conn.close()

# Kullanıcı doğrula
def validate_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Tema ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# Tablo sütunları
tables_columns = {
    "Ciftlikler": ["Ciftlik_No", "Ciftlik_Adi", "Ciftlik_Sahibi"],
    "UrunBilgi": ["Urun_ID", "Urun_Adi", "Urun_Turu"],
    "Hasat": ["Hasat_No", "Ciftlik_No", "Ciftlik_Adi", "Urun_ID", "Urun_Adi", "Hasat_Tarihi", "Hasat_Miktari"],
    "Satislar": ["Satis_No", "Urun_ID", "Musteri_ID", "Satis_Tarihi", "Satis_Miktari", "Toplam_Tutar"],
    "Lojistik": ["Lojistik_ID", "Satis_No", "Kargo_No", "Teslimat_Tarihi", "Teslimat_Durumu", "Tasima_ID"]
}

# Her tablonun IDENTITY sütunlarını belirt
identity_columns = {
    "Ciftlikler": "Ciftlik_No",
    "UrunBilgi": "Urun_ID",
    "Hasat": "Hasat_No",
    "Satislar": "Satis_No",
    "Lojistik": "Lojistik_ID"
}

# Tablo renkleri
table_colors = {
    "Ciftlikler": "#6A9E67",
    "UrunBilgi": "#5479A3",
    "Hasat": "#B97C4E",
    "Satislar": "#B85A5A",
    "Lojistik": "#E1D589"
}

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TARIMTAKIP")
        self.geometry("1000x700")
        
        # Ana pencere arka plan rengi
        self.configure(fg_color="#E8F3E8")  # Açık yeşil arka plan
        
        initialize_user_db()
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_window()
        
        # Üst menü çerçevesi - Gradient arka plan ile
        top_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", height=70)
        top_frame.pack(fill="x", padx=20, pady=(10, 0))
        top_frame.pack_propagate(False)
        
        # Logo ve isim için sol kısım
        logo_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        logo_frame.pack(side="left", pady=10)
        
        # Üst menü başlığı
        header_label = ctk.CTkLabel(
            logo_frame,
            text="TARIMTAKIP",
            font=("Arial Bold", 24),
            text_color="#2B7539"
        )
        header_label.pack(side="left")
        
        # Sağ üst köşedeki butonlar için frame
        auth_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        auth_frame.pack(side="right", pady=15, padx=10)
        
        # Giriş Yap butonu - Yeni tasarım
        login_btn = ctk.CTkButton(
            auth_frame, 
            text="Giriş Yap",
            width=120,
            height=35,
            command=self.show_login_screen,
            fg_color="#2B7539",
            hover_color="#1E5228",
            font=("Arial Bold", 12),
            corner_radius=8
        )
        login_btn.pack(side="left", padx=5)
        
        # Kayıt Ol butonu - Yeni tasarım
        register_btn = ctk.CTkButton(
            auth_frame, 
            text="Kayıt Ol",
            width=120,
            height=35,
            command=self.show_register_screen,
            fg_color="#28666E",
            hover_color="#1B474D",
            font=("Arial Bold", 12),
            corner_radius=8
        )
        register_btn.pack(side="left", padx=5)
        
        # Ana içerik için orta frame
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(expand=True, pady=(30, 0))
        
        # Ana başlık - Gölgeli efekt için iki label
        title_shadow = ctk.CTkLabel(
            center_frame, 
            text="TARIMTAKIP",
            font=("Arial Bold", 58),
            text_color="#1E5228"
        )
        title_shadow.pack(pady=(0, 10))
        
        # Alt başlık - Modernize edildi
        subtitle_label = ctk.CTkLabel(
            center_frame,
            text="Tarım Ürünleri Takip Sistemi",
            font=("Arial", 26),
            text_color="#2B7539"
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Açıklama metni - Daha şık font
        description_label = ctk.CTkLabel(
            center_frame,
            text="Tarımsal üretim süreçlerinizi kolayca yönetin",
            font=("Arial", 16),
            text_color="#333333"
        )
        description_label.pack(pady=(0, 40))
        
        # Özellikler için ana frame
        features_main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
        features_main_frame.pack(fill="x", padx=40, pady=(0, 30))
        
        # Özellikler başlığı
        features_title = ctk.CTkLabel(
            features_main_frame,
            text="Özellikler",
            font=("Arial Bold", 20),
            text_color="#1E5228"
        )
        features_title.pack(pady=(20, 15))
        
        # Özellikler için iç frame
        features_frame = ctk.CTkFrame(features_main_frame, fg_color="transparent")
        features_frame.pack(padx=20, pady=(0, 20))
        
        # Özellikler listesi - Modern ikonlar ve renkler
        features = [
            ("🌾", "Çiftlik Yönetimi", "Çiftliklerinizi tek noktadan yönetin", "#1E5228"),
            ("🌱", "Ürün Takibi", "Ürünlerinizi detaylı şekilde takip edin", "#2B7539"),
            ("🌿", "Hasat Kaydı", "Hasat verilerinizi düzenli tutun", "#346751"),
            ("💰", "Satış Takibi", "Satışlarınızı anlık takip edin", "#28666E"),
            ("🚛", "Lojistik Yönetimi", "Sevkiyatlarınızı optimize edin", "#1D5C63")
        ]
        
        # Özellikler grid layout
        for i, (icon, title, desc, color) in enumerate(features):
            feature_frame = ctk.CTkFrame(features_frame, fg_color="transparent")
            feature_frame.pack(side="left", padx=15)
            
            # İkon
            icon_label = ctk.CTkLabel(
                feature_frame,
                text=icon,
                font=("Arial", 24),
                text_color=color
            )
            icon_label.pack()
            
            # Başlık
            title_label = ctk.CTkLabel(
                feature_frame,
                text=title,
                font=("Arial Bold", 14),
                text_color=color
            )
            title_label.pack(pady=(5, 2))
            
            # Açıklama
            desc_label = ctk.CTkLabel(
                feature_frame,
                text=desc,
                font=("Arial", 11),
                text_color="#666666",
                wraplength=150
            )
            desc_label.pack()

    # Giriş Ekranı
    def show_login_screen(self):
        self.clear_window()
        self.geometry("400x600")
        
        # Ana container frame
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)  # Dikey ve yatay olarak ortala
        
        # Login frame
        login_frame = ctk.CTkFrame(container, fg_color="#ffffff", corner_radius=15)
        login_frame.pack(padx=20, pady=20)
        
        # İçerik
        self.label = ctk.CTkLabel(login_frame, text="Giriş Yap", font=("Arial Bold", 24))
        self.label.pack(pady=20)

        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Kullanıcı Adı", width=250)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Şifre", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(
            login_frame, 
            text="Giriş Yap", 
            command=self.check_login,
            fg_color="#2B7539",
            hover_color="#1E5228",
            width=250
        )
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(
            login_frame,
            text="Kayıt Ol",
            command=self.show_register_screen,
            fg_color="#28666E",
            hover_color="#1B474D",
            width=250
        )
        self.register_button.pack(pady=10)

        self.home_button = ctk.CTkButton(
            login_frame,
            text="Anasayfaya Dön",
            command=self.show_welcome_screen,
            fg_color="#666666",
            hover_color="#555555",
            width=250
        )
        self.home_button.pack(pady=10)

    # Kayıt Ekranı
    def show_register_screen(self):
        self.clear_window()
        self.geometry("400x600")
        
        # Ana container frame
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)  # Dikey ve yatay olarak ortala
        
        # Register frame
        register_frame = ctk.CTkFrame(container, fg_color="#ffffff", corner_radius=15)
        register_frame.pack(padx=20, pady=20)
        
        # İçerik
        self.label = ctk.CTkLabel(register_frame, text="Kayıt Ol", font=("Arial Bold", 24))
        self.label.pack(pady=20)

        self.username_entry = ctk.CTkEntry(register_frame, placeholder_text="Kullanıcı Adı", width=250)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(register_frame, placeholder_text="Şifre", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.register_button = ctk.CTkButton(
            register_frame,
            text="Kayıt Ol",
            command=self.register_user,
            fg_color="#28666E",
            hover_color="#1B474D",
            width=250
        )
        self.register_button.pack(pady=10)

        self.home_button = ctk.CTkButton(
            register_frame,
            text="Anasayfaya Dön",
            command=self.show_welcome_screen,
            fg_color="#666666",
            hover_color="#555555",
            width=250
        )
        self.home_button.pack(pady=10)

    # Kayıt işlemi
    def register_user(self):
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()

        if save_user(new_username, new_password):
            # Başarılı kayıt mesajı
            success_label = ctk.CTkLabel(self, text="Kayıt başarılı! Giriş yapabilirsiniz.", text_color="green")
            success_label.pack(pady=5)
            
            # 2 saniye bekleyip giriş ekranına yönlendir
            self.after(2000, lambda: [
                success_label.destroy(),
                self.show_login_screen()
            ])
        else:
            error_label = ctk.CTkLabel(self, text="Bu kullanıcı adı zaten mevcut!", text_color="red")
            error_label.pack(pady=5)
            self.after(3000, error_label.destroy)

    # Giriş kontrolü
    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in FAILED_ATTEMPTS and FAILED_ATTEMPTS[username]["lock_until"] > datetime.now():
            error_label = ctk.CTkLabel(self, text="Çok fazla hatalı giriş! Lütfen bekleyin.", text_color="red")
            error_label.pack(pady=5)
            self.after(3000, error_label.destroy)
            return

        if validate_user(username, password):
            FAILED_ATTEMPTS.pop(username, None)  # Başarılı girişte sıfırla
            self.show_main_menu()
        else:
            if username not in FAILED_ATTEMPTS:
                FAILED_ATTEMPTS[username] = {"attempts": 0, "lock_until": None}

            FAILED_ATTEMPTS[username]["attempts"] += 1
            if FAILED_ATTEMPTS[username]["attempts"] >= 3:
                FAILED_ATTEMPTS[username]["lock_until"] = datetime.now() + LOCK_DURATION
                error_label = ctk.CTkLabel(self, text="Çok fazla hatalı giriş! Lütfen bekleyin.", text_color="red")
                error_label.pack(pady=5)
            else:
                error_label = ctk.CTkLabel(self, text="Hatalı kullanıcı adı veya şifre!", text_color="red")
                error_label.pack(pady=5)
            
            self.after(3000, error_label.destroy)

    # Ana Menü
    def show_main_menu(self):
        self.clear_window()
        self.geometry("600x400")
        self.label = ctk.CTkLabel(self, text="İşlem yapmak istediğiniz bölümü seçin", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill="both", expand=True, padx=20, pady=20)

        for table, color in table_colors.items():
            button = ctk.CTkButton(self.buttons_frame, text=table,
                                   command=lambda t=table, c=color: self.open_table_window(t, c), fg_color=color,
                                   text_color="black", font=("Arial", 12, "bold"))
            button.pack(pady=10, padx=20, fill="x")

        # Dinamik MSSQL Sorgu Girişi Butonu
        query_button = ctk.CTkButton(self.buttons_frame, text="MSSQL Sorgusu Gir", command=self.open_query_window,
                                     fg_color="#4B7A8A", text_color="white", font=("Arial", 12, "bold"))
        query_button.pack(pady=10, padx=20, fill="x")

        # Çıkış Butonu
        logout_button = ctk.CTkButton(self.buttons_frame, text="Çıkış", command=self.show_login_screen,
                                      fg_color="#FF0000", text_color="white", font=("Arial", 12, "bold"))
        logout_button.pack(pady=10, padx=20, fill="x")

    # MSSQL Sorgu Penceresi
    def open_query_window(self):
        query_window = ctk.CTkToplevel(self)
        query_window.title("SQL Sorgu Penceresi")
        query_window.geometry("1200x800")
        query_window.configure(fg_color="#E8F3E8")
        
        # Pencereyi ana pencereye bağla
        query_window.transient(self)  # Ana pencereye bağlı pencere olarak ayarla
        query_window.grab_set()       # Pencereyi aktif ve odaklanmış tut
        
        # Pencereyi ekranın ortasında konumlandır
        window_width = 1200
        window_height = 800
        screen_width = query_window.winfo_screenwidth()
        screen_height = query_window.winfo_screenheight()
        
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        query_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Başlık
        title_frame = ctk.CTkFrame(query_window, fg_color="white", height=60)
        title_frame.pack(fill="x", padx=20, pady=(10, 20))
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="SQL Sorgu Penceresi",
            font=("Arial Bold", 24),
            text_color="#2B7539"
        )
        title_label.pack(expand=True)

        # Ana içerik container
        main_container = ctk.CTkFrame(query_window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Sol taraf - Sorgu girişi (Daha dar)
        left_frame = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10), pady=10, ipadx=10)
        left_frame.configure(width=400)  # Sabit genişlik

        query_label = ctk.CTkLabel(
            left_frame, 
            text="SQL Sorgunuzu Yazın:",
            font=("Arial Bold", 16),
            text_color="#2B7539"
        )
        query_label.pack(pady=(15, 5), padx=15)
        
        # Sorgu girişi için text widget (Daha küçük)
        query_text = ctk.CTkTextbox(
            left_frame, 
            height=200,  # Yükseklik azaltıldı
            width=380,   # Genişlik sabitlendi
            font=("Consolas", 14),
            fg_color="#FFFFFF",
            text_color="#000000",
            border_color="#2B7539",
            border_width=2,
            wrap="none"
        )
        query_text.pack(padx=15, pady=(5, 15))

        # Butonlar için frame
        button_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 15), padx=15)

        def clear_query():
            query_text.delete("1.0", "end")
            query_text.focus()

        execute_button = ctk.CTkButton(
            button_frame,
            text="Sorguyu Çalıştır",
            command=lambda: execute_query(),
            font=("Arial Bold", 14),
            fg_color="#2B7539",
            hover_color="#1E5228",
            width=150,
            height=35
        )
        execute_button.pack(side="left", padx=5)

        clear_button = ctk.CTkButton(
            button_frame,
            text="Temizle",
            command=clear_query,
            font=("Arial Bold", 14),
            fg_color="#666666",
            hover_color="#555555",
            width=150,
            height=35
        )
        clear_button.pack(side="left", padx=5)

        # Sağ taraf - Sonuçlar (Daha geniş)
        right_frame = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        result_label = ctk.CTkLabel(
            right_frame, 
            text="Sorgu Sonuçları",
            font=("Arial Bold", 16),
            text_color="#2B7539"
        )
        result_label.pack(pady=(15, 5))

        # Sonuçlar için tablo frame
        table_frame = ctk.CTkScrollableFrame(
            right_frame,
            fg_color="#F8F9FA",
            corner_radius=5
        )
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)

        def execute_query():
            # Önceki sonuçları temizle
            for widget in table_frame.winfo_children():
                widget.destroy()

            try:
                query = query_text.get("1.0", "end-1c").strip()
                if not query:
                    raise ValueError("Lütfen bir sorgu girin!")

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(query)

                try:
                    # Sütun başlıkları
                    columns = [column[0] for column in cursor.description]
                    
                    # Tablo başlıkları için frame
                    header_frame = ctk.CTkFrame(table_frame, fg_color="#E8F3E8")
                    header_frame.pack(fill="x", pady=(0, 2))

                    # Başlık etiketleri
                    for i, col in enumerate(columns):
                        header = ctk.CTkLabel(
                            header_frame,
                            text=str(col),
                            font=("Arial Bold", 12),
                            text_color="#2B7539",
                            width=120
                        )
                        header.grid(row=0, column=i, padx=5, pady=5, sticky="w")
                        header_frame.grid_columnconfigure(i, weight=1)

                    # Veriler için frame
                    data_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
                    data_frame.pack(fill="both", expand=True)

                    # Verileri göster
                    rows = cursor.fetchall()
                    for row_idx, row in enumerate(rows, start=0):
                        row_frame = ctk.CTkFrame(
                            data_frame, 
                            fg_color="#FFFFFF" if row_idx % 2 == 0 else "#F8F9FA"
                        )
                        row_frame.pack(fill="x", pady=1)
                        
                        for col_idx, value in enumerate(row):
                            cell = ctk.CTkLabel(
                                row_frame,
                                text=str(value),
                                font=("Arial", 12),
                                text_color="#333333",
                                width=120
                            )
                            cell.grid(row=0, column=col_idx, padx=5, pady=3, sticky="w")
                            row_frame.grid_columnconfigure(col_idx, weight=1)

                    # Sonuç sayısını göster
                    result_count = ctk.CTkLabel(
                        table_frame,
                        text=f"Toplam {len(rows)} sonuç bulundu",
                        font=("Arial", 12),
                        text_color="#666666"
                    )
                    result_count.pack(pady=(10, 0))

                except Exception as e:
                    # SELECT olmayan sorgular için
                    conn.commit()
                    success_label = ctk.CTkLabel(
                        table_frame,
                        text=f"Sorgu başarıyla çalıştırıldı.\nEtkilenen satır sayısı: {cursor.rowcount}",
                        font=("Arial Bold", 14),
                        text_color="#2B7539"
                    )
                    success_label.pack(pady=20)

                conn.close()

            except Exception as e:
                error_label = ctk.CTkLabel(
                    table_frame,
                    text=f"Hata: {str(e)}",
                    font=("Arial", 12),
                    text_color="#FF0000"
                )
                error_label.pack(pady=20)

        # Örnek sorgular bölümü
        example_frame = ctk.CTkFrame(left_frame, fg_color="#F8F9FA", corner_radius=5)
        example_frame.pack(fill="x", padx=15, pady=(0, 15))

        example_label = ctk.CTkLabel(
            example_frame,
            text="Örnek Sorgular:",
            font=("Arial Bold", 14),
            text_color="#2B7539"
        )
        example_label.pack(pady=(10, 5), padx=10)

        examples = [
            "SELECT * FROM Ciftlikler",
            "SELECT * FROM UrunBilgi",
            "SELECT * FROM Hasat",
            "SELECT * FROM Satislar",
            "SELECT * FROM Lojistik"
        ]

        for example in examples:
            example_btn = ctk.CTkButton(
                example_frame,
                text=example,
                command=lambda q=example: [query_text.delete("1.0", "end"), 
                                         query_text.insert("1.0", q)],
                font=("Consolas", 12),
                fg_color="transparent",
                text_color="#2B7539",
                hover_color="#E8F3E8",
                height=30
            )
            example_btn.pack(pady=2, padx=10, fill="x")

    # Tablo Penceresi
    def open_table_window(self, table_name, color):
        try:
            table_window = ctk.CTkToplevel(self)
            table_window.title(f"{table_name} Tablosu")
            table_window.geometry("1000x600")
            
            # Pencereyi ana pencereye bağla
            table_window.transient(self)
            
            label = ctk.CTkLabel(table_window, text=f"{table_name} Tablosu", font=("Arial", 24, "bold"))
            label.pack(pady=20)

            # Butonlar için frame
            button_frame = ctk.CTkFrame(table_window)
            button_frame.pack(pady=10)

            # CRUD butonları - command'leri güncellendi
            add_button = ctk.CTkButton(
                button_frame, 
                text="Ekle", 
                command=lambda: self.add_record_window(table_name, table_window)
            )
            add_button.pack(side="left", padx=5)

            update_button = ctk.CTkButton(
                button_frame, 
                text="Güncelle", 
                command=lambda: self.update_record_window(table_name, table_window)
            )
            update_button.pack(side="left", padx=5)

            delete_button = ctk.CTkButton(
                button_frame, 
                text="Sil", 
                command=lambda: self.delete_record_window(table_name, table_window)
            )
            delete_button.pack(side="left", padx=5)

            # Tablo frame
            table_frame = ctk.CTkFrame(table_window)
            table_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Sütun başlıkları
            columns = tables_columns[table_name]
            for i, column in enumerate(columns):
                label = ctk.CTkLabel(table_frame, text=column, font=("Arial", 12, "bold"))
                label.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")

            # Verileri göster
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            for i, row in enumerate(rows, start=1):
                for j, value in enumerate(row):
                    label = ctk.CTkLabel(table_frame, text=str(value))
                    label.grid(row=i, column=j, padx=10, pady=5, sticky="nsew")

            conn.close()

            # Grid yapılandırması
            for i in range(len(columns)):
                table_frame.grid_columnconfigure(i, weight=1)

        except Exception as e:
            print(f"Tablo açma hatası: {str(e)}")

    def add_record_window(self, table_name, parent_window):
        dialog = ctk.CTkToplevel(parent_window)
        dialog.title(f"{table_name} Kaydı Ekle")
        dialog.geometry("400x600")
        
        # Pencereyi ana pencereye bağla
        dialog.transient(parent_window)
        dialog.grab_set()
        
        # Başlık
        title_label = ctk.CTkLabel(
            dialog, 
            text=f"{table_name} Kaydı Ekle",
            font=("Arial Bold", 16)
        )
        title_label.pack(pady=20)
        
        # Entry'ler için frame
        entries_frame = ctk.CTkFrame(dialog)
        entries_frame.pack(pady=10, padx=20, fill="x")
        
        # Sütunlar için entry'ler
        entries = []
        columns = tables_columns[table_name]
        for column in columns[1:]:  # İlk sütunu (ID) atlıyoruz
            label = ctk.CTkLabel(entries_frame, text=column)
            label.pack(pady=5)
            entry = ctk.CTkEntry(entries_frame, width=200)
            entry.pack(pady=5)
            entries.append(entry)
        
        def save_record():
            try:
                # Değerleri al
                values = [entry.get() for entry in entries]
                if not all(values):
                    messagebox.showerror("Hata", "Tüm alanları doldurun!")
                    return
                
                # Veritabanı bağlantısı
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # INSERT sorgusu
                columns_str = ", ".join(tables_columns[table_name][1:])
                placeholders = ", ".join(["?" for _ in values])
                query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                
                # Sorguyu çalıştır
                cursor.execute(query, values)
                conn.commit()
                conn.close()
                
                # Başarı mesajı
                messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi!")
                
                # Entry'leri temizle
                for entry in entries:
                    entry.delete(0, 'end')
                    
                # Tabloyu yenile
                self.refresh_table(table_name, parent_window)
                
            except Exception as e:
                messagebox.showerror("Hata", f"Kayıt eklenirken hata oluştu: {str(e)}")

        # Kaydet butonu
        save_button = ctk.CTkButton(
            dialog,
            text="Kaydet",
            command=save_record,
            fg_color="#2B7539",
            hover_color="#1E5228"
        )
        save_button.pack(pady=20)

    def delete_record_window(self, table_name, parent_window):
        dialog = ctk.CTkToplevel(parent_window)
        dialog.title(f"{table_name} Kaydı Sil")
        dialog.geometry("400x300")
        
        # Pencereyi ana pencereye bağla
        dialog.transient(parent_window)
        dialog.grab_set()
        
        # Başlık
        title_label = ctk.CTkLabel(
            dialog, 
            text=f"{table_name} Kayd�� Sil",
            font=("Arial Bold", 16)
        )
        title_label.pack(pady=20)
        
        # ID giriş alanı
        id_column = tables_columns[table_name][0]
        label = ctk.CTkLabel(dialog, text=f"Silinecek {id_column}:")
        label.pack(pady=5)
        
        id_entry = ctk.CTkEntry(dialog, width=200)
        id_entry.pack(pady=10)
        
        def delete_record():
            try:
                id_value = id_entry.get()
                if not id_value:
                    messagebox.showerror("Hata", "ID değeri girilmeli!")
                    return
                
                # Onay iste
                if not messagebox.askyesno("Onay", "Bu kaydı silmek istediğinizden emin misiniz?"):
                    return
                
                # Veritabanı bağlantısı
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # DELETE sorgusu
                query = f"DELETE FROM {table_name} WHERE {id_column} = ?"
                cursor.execute(query, (id_value,))
                conn.commit()
                conn.close()
                
                # Başarı mesajı
                messagebox.showinfo("Başarılı", "Kayıt başarıyla silindi!")
                
                # Entry'i temizle
                id_entry.delete(0, 'end')
                
                # Tabloyu yenile
                self.refresh_table(table_name, parent_window)
                
            except Exception as e:
                messagebox.showerror("Hata", f"Kayıt silinirken hata oluştu: {str(e)}")

        # Sil butonu
        delete_button = ctk.CTkButton(
            dialog,
            text="Sil",
            command=delete_record,
            fg_color="red",
            hover_color="#8B0000"
        )
        delete_button.pack(pady=20)

    def refresh_table(self, table_name, parent_window):
        """Tabloyu yeniler"""
        try:
            # Mevcut tablo frame'ini bul ve içeriğini temizle
            table_frame = None
            for widget in parent_window.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget not in [parent_window.children.get('!ctkframe')]:
                    if len(widget.winfo_children()) > 0:  # Tablo frame'i içinde widget'lar varsa
                        table_frame = widget
                        for child in widget.winfo_children():
                            child.destroy()
                        break

            if table_frame:
                # Sütun başlıkları
                columns = tables_columns[table_name]
                for i, column in enumerate(columns):
                    label = ctk.CTkLabel(table_frame, text=column, font=("Arial", 12, "bold"))
                    label.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")

                # Verileri göster
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                for i, row in enumerate(rows, start=1):
                    for j, value in enumerate(row):
                        label = ctk.CTkLabel(table_frame, text=str(value))
                        label.grid(row=i, column=j, padx=10, pady=5, sticky="nsew")

                conn.close()

                # Grid yapılandırması
                for i in range(len(columns)):
                    table_frame.grid_columnconfigure(i, weight=1)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Tablo yenilenirken hata oluştu: {str(e)}")

    # Pencereyi temizle
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Pencere kapatma işlemi
    def on_closing(self):
        self.destroy()


# Uygulamayı başlat
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
