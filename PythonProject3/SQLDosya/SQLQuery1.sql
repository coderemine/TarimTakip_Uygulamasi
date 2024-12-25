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
    ('Ye�il Vadi �iftli�i', 'Ahmet Kaya', 'Ankara', 'T�rkiye'),
    ('Bahar �iftli�i', 'Mehmet �z', '�zmir', 'T�rkiye'),
    ('Verimli Topraklar', 'Ay�e Y�lmaz', 'Adana', 'T�rkiye'),
    ('Do�a �iftli�i', 'Fatma Demir', 'Bursa', 'T�rkiye'),
    ('Alt�nova �iftli�i', 'Zeynep Ko�', 'Manisa', 'T�rkiye'),
    ('G�ne�li �iftlik', 'Ali Veli', 'Konya', 'T�rkiye'),
    ('Huzur Bah�esi', 'H�seyin �elik', 'Trabzon', 'T�rkiye');


ALTER TABLE Ciftlikler
ADD Urun_Adi NVARCHAR(100);

UPDATE Ciftlikler
SET Urun_Adi = CASE 
    WHEN Ciftlik_Adi = 'Ye�il Vadi �iftli�i' THEN 'Bu�day'
    WHEN Ciftlik_Adi = 'Bahar �iftli�i' THEN 'Arpa'
    WHEN Ciftlik_Adi = 'Verimli Topraklar' THEN 'M�s�r'
    WHEN Ciftlik_Adi = 'Do�a �iftli�i' THEN '�ilek'
    WHEN Ciftlik_Adi = 'Alt�nova �iftli�i' THEN 'Elma'
    WHEN Ciftlik_Adi = 'G�ne�li �iftlik' THEN 'Patates'
    WHEN Ciftlik_Adi = 'Huzur Bah�esi' THEN 'Havu�'
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
    ('Bu�day', 'Tah�l', 4.50, 'Serin ve kuru ortamda saklanmal�'),
    ('Arpa', 'Tah�l', 3.75, 'Serin ve kuru ortamda saklanmal�'),
    ('M�s�r', 'Tah�l', 5.00, 'G�ne� g�rmeyen bir yerde saklanmal�'),
    ('�ilek', 'Meyve', 15.00, 'So�uk hava deposunda saklanmal�'),
    ('Elma', 'Meyve', 10.00, 'Serin bir yerde saklanmal�'),
    ('Patates', 'Sebze', 2.50, 'Karanl�k ve kuru bir ortamda saklanmal�'),
    ('Havu�', 'Sebze', 3.00, 'Nemli bir ortamda saklanmal�');


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
    (1, 'Ye�il Vadi �iftli�i', 1, 'Bu�day', '2024-11-15', 1000.00),
    (2, 'Bahar �iftli�i', 2, 'Arpa', '2024-11-16', 800.00),
    (3, 'Verimli Topraklar', 3, 'M�s�r', '2024-11-17', 1200.00),
    (4, 'Do�a �iftli�i', 4, '�ilek', '2024-11-18', 500.00),
    (5, 'Alt�nova �iftli�i', 5, 'Elma', '2024-11-19', 900.00),
    (6, 'G�ne�li �iftlik', 6, 'Patates', '2024-11-20', 1500.00),
    (7, 'Huzur Bah�esi', 7, 'Havu�', '2024-11-21', 700.00);



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
    (1, 'Ali Veli', '05001234567', '2024-11-22', 200.00, 900.00),   -- Bu�day sat���
    (2, 'Ay�e Y�lmaz', '05007654321', '2024-11-23', 300.00, 1125.00), -- Arpa sat���
    (3, 'Mehmet �zt�rk', '05009876543', '2024-11-24', 150.00, 750.00), -- M�s�r sat���
    (4, 'Zeynep Kaya', '05004567891', '2024-11-25', 50.00, 750.00),  -- �ilek sat���
    (5, 'H�seyin �elik', '05007891234', '2024-11-26', 100.00, 1000.00), -- Elma sat���
    (6, 'Fatma Demir', '05003456789', '2024-11-27', 500.00, 1250.00), -- Patates sat���
    (7, 'Ahmet Kaya', '05001230987', '2024-11-28', 100.00, 300.00);   -- Havu� sat���



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
    (1, 'KARGO001', '2024-11-23', 'Teslim Edildi', 'Yurti�i Kargo'),  -- Sat�� 1 i�in
    (2, 'KARGO002', '2024-11-24', 'Yolda', 'Aras Kargo'),             -- Sat�� 2 i�in
    (3, 'KARGO003', '2024-11-25', 'Teslim Edildi', 'MNG Kargo'),      -- Sat�� 3 i�in
    (4, 'KARGO004', '2024-11-26', 'Teslim Edildi', 'PTT Kargo'),      -- Sat�� 4 i�in
    (5, 'KARGO005', '2024-11-27', 'Yolda', 'S�rat Kargo'),            -- Sat�� 5 i�in
    (6, 'KARGO006', '2024-11-28', 'Teslim Edildi', 'Yurti�i Kargo'),  -- Sat�� 6 i�in
    (7, 'KARGO007', '2024-11-29', 'Teslim Edildi', 'Aras Kargo');     -- Sat�� 7 i�in


SELECT *FROM Ciftlikler
SELECT * FROM Urunler
SELECT *FROM Hasat
SELECT *FROM Satislar
SELECT *FROM Lojistik
