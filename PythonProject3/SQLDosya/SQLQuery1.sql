USE TARIMTAKIP;

CREATE TABLE Ciftlikler (
    Ciftlik_No INT PRIMARY KEY IDENTITY(1,1),
    Ciftlik_Adi NVARCHAR(100) NOT NULL,
    Ciftlik_Sahibi NVARCHAR(100),
    Konum_Sehir NVARCHAR(100),
    Konum_Ulke NVARCHAR(100)
);

INSERT INTO Ciftlikler (Ciftlik_Adi, Ciftlik_Sahibi, Konum_Sehir, Konum_Ulke)
VALUES 
    ('Yeþil Vadi Çiftliði', 'Ahmet Kaya', 'Ankara', 'Türkiye'),
    ('Bahar Çiftliði', 'Mehmet Öz', 'Ýzmir', 'Türkiye'),
    ('Verimli Topraklar', 'Ayþe Yýlmaz', 'Adana', 'Türkiye'),
    ('Doða Çiftliði', 'Fatma Demir', 'Bursa', 'Türkiye'),
    ('Altýnova Çiftliði', 'Zeynep Koç', 'Manisa', 'Türkiye'),
    ('Güneþli Çiftlik', 'Ali Veli', 'Konya', 'Türkiye'),
    ('Huzur Bahçesi', 'Hüseyin Çelik', 'Trabzon', 'Türkiye');


ALTER TABLE Ciftlikler
ADD Urun_Adi NVARCHAR(100);

UPDATE Ciftlikler
SET Urun_Adi = CASE 
    WHEN Ciftlik_Adi = 'Yeþil Vadi Çiftliði' THEN 'Buðday'
    WHEN Ciftlik_Adi = 'Bahar Çiftliði' THEN 'Arpa'
    WHEN Ciftlik_Adi = 'Verimli Topraklar' THEN 'Mýsýr'
    WHEN Ciftlik_Adi = 'Doða Çiftliði' THEN 'Çilek'
    WHEN Ciftlik_Adi = 'Altýnova Çiftliði' THEN 'Elma'
    WHEN Ciftlik_Adi = 'Güneþli Çiftlik' THEN 'Patates'
    WHEN Ciftlik_Adi = 'Huzur Bahçesi' THEN 'Havuç'
    ELSE NULL
END;




CREATE TABLE Urunler (
    Urun_ID INT PRIMARY KEY IDENTITY(1,1),
    Urun_Adi NVARCHAR(100) NOT NULL,
    Urun_Turu NVARCHAR(50),
    Birim_Fiyat DECIMAL(10,2),
    Saklama_Kosullari NVARCHAR(255)
);


INSERT INTO Urunler (Urun_Adi, Urun_Turu, Birim_Fiyat, Saklama_Kosullari)
VALUES 
    ('Buðday', 'Tahýl', 4.50, 'Serin ve kuru ortamda saklanmalý'),
    ('Arpa', 'Tahýl', 3.75, 'Serin ve kuru ortamda saklanmalý'),
    ('Mýsýr', 'Tahýl', 5.00, 'Güneþ görmeyen bir yerde saklanmalý'),
    ('Çilek', 'Meyve', 15.00, 'Soðuk hava deposunda saklanmalý'),
    ('Elma', 'Meyve', 10.00, 'Serin bir yerde saklanmalý'),
    ('Patates', 'Sebze', 2.50, 'Karanlýk ve kuru bir ortamda saklanmalý'),
    ('Havuç', 'Sebze', 3.00, 'Nemli bir ortamda saklanmalý');


CREATE TABLE Hasat (
    Hasat_No INT PRIMARY KEY IDENTITY(1,1),
    Ciftlik_No INT NOT NULL,
	Ciftlik_Adi NVARCHAR(100) NOT NULL,
    Urun_ID INT NOT NULL,
	Urun_Adi NVARCHAR(100) NOT NULL,
    Hasat_Tarihi DATE,
    Hasat_Miktari DECIMAL(10,2),
    FOREIGN KEY (Ciftlik_No) REFERENCES Ciftlikler(Ciftlik_No) ON DELETE CASCADE,
    FOREIGN KEY (Urun_ID) REFERENCES Urunler(Urun_ID) ON DELETE CASCADE
);

INSERT INTO Hasat (Ciftlik_No, Ciftlik_Adi, Urun_ID, Urun_Adi, Hasat_Tarihi, Hasat_Miktari)
VALUES 
    (1, 'Yeþil Vadi Çiftliði', 1, 'Buðday', '2024-11-15', 1000.00),
    (2, 'Bahar Çiftliði', 2, 'Arpa', '2024-11-16', 800.00),
    (3, 'Verimli Topraklar', 3, 'Mýsýr', '2024-11-17', 1200.00),
    (4, 'Doða Çiftliði', 4, 'Çilek', '2024-11-18', 500.00),
    (5, 'Altýnova Çiftliði', 5, 'Elma', '2024-11-19', 900.00),
    (6, 'Güneþli Çiftlik', 6, 'Patates', '2024-11-20', 1500.00),
    (7, 'Huzur Bahçesi', 7, 'Havuç', '2024-11-21', 700.00);



CREATE TABLE Satislar (
    Satis_No INT PRIMARY KEY IDENTITY(1,1),
    Urun_ID INT NOT NULL,
    Musteri_AdiSoyad NVARCHAR(100),
    Musteri_TelNo NVARCHAR(15),
    Satis_Tarihi DATE NOT NULL,
    Satis_Miktari DECIMAL(10,2),
    Toplam_Tutar DECIMAL(10,2),
    FOREIGN KEY (Urun_ID) REFERENCES Urunler(Urun_ID) ON DELETE CASCADE
);


INSERT INTO Satislar (Urun_ID, Musteri_AdiSoyad, Musteri_TelNo, Satis_Tarihi, Satis_Miktari, Toplam_Tutar)
VALUES 
    (1, 'Ali Veli', '05001234567', '2024-11-22', 200.00, 900.00),   -- Buðday satýþý
    (2, 'Ayþe Yýlmaz', '05007654321', '2024-11-23', 300.00, 1125.00), -- Arpa satýþý
    (3, 'Mehmet Öztürk', '05009876543', '2024-11-24', 150.00, 750.00), -- Mýsýr satýþý
    (4, 'Zeynep Kaya', '05004567891', '2024-11-25', 50.00, 750.00),  -- Çilek satýþý
    (5, 'Hüseyin Çelik', '05007891234', '2024-11-26', 100.00, 1000.00), -- Elma satýþý
    (6, 'Fatma Demir', '05003456789', '2024-11-27', 500.00, 1250.00), -- Patates satýþý
    (7, 'Ahmet Kaya', '05001230987', '2024-11-28', 100.00, 300.00);   -- Havuç satýþý



CREATE TABLE Lojistik (
    Lojistik_ID INT PRIMARY KEY IDENTITY(1,1),
    Satis_No INT NOT NULL,
    Kargo_No NVARCHAR(50),
    Teslimat_Tarihi DATE,
    Teslimat_Durumu NVARCHAR(50),
    Tasima_Sirketi NVARCHAR(100),
    FOREIGN KEY (Satis_No) REFERENCES Satislar(Satis_No) ON DELETE CASCADE
);

INSERT INTO Lojistik (Satis_No, Kargo_No, Teslimat_Tarihi, Teslimat_Durumu, Tasima_Sirketi)
VALUES 
    (1, 'KARGO001', '2024-11-23', 'Teslim Edildi', 'Yurtiçi Kargo'),  -- Satýþ 1 için
    (2, 'KARGO002', '2024-11-24', 'Yolda', 'Aras Kargo'),             -- Satýþ 2 için
    (3, 'KARGO003', '2024-11-25', 'Teslim Edildi', 'MNG Kargo'),      -- Satýþ 3 için
    (4, 'KARGO004', '2024-11-26', 'Teslim Edildi', 'PTT Kargo'),      -- Satýþ 4 için
    (5, 'KARGO005', '2024-11-27', 'Yolda', 'Sürat Kargo'),            -- Satýþ 5 için
    (6, 'KARGO006', '2024-11-28', 'Teslim Edildi', 'Yurtiçi Kargo'),  -- Satýþ 6 için
    (7, 'KARGO007', '2024-11-29', 'Teslim Edildi', 'Aras Kargo');     -- Satýþ 7 için


SELECT *FROM Ciftlikler
SELECT * FROM Urunler
SELECT *FROM Hasat
SELECT *FROM Satislar
SELECT *FROM Lojistik
