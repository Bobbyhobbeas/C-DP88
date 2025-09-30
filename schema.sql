CREATE DATABASE IF NOT EXISTS attractiepark;
USE attractiepark;

CREATE TABLE IF NOT EXISTS Personeelslid (
  id INT AUTO_INCREMENT PRIMARY KEY,
  naam VARCHAR(45) NOT NULL,
  werktijd INT NOT NULL,
  beroepstype VARCHAR(45) NOT NULL,
  bevoegdheid VARCHAR(45) NOT NULL,
  specialist_in_attracties VARCHAR(255) NOT NULL,
  pauze_opsplitsen TINYINT(1) NOT NULL,
  leeftijd INT NOT NULL,
  verlaagde_fysieke_belasting INT NULL
);

CREATE TABLE IF NOT EXISTS Onderhoudstaak (
  id INT AUTO_INCREMENT PRIMARY KEY,
  omschrijving VARCHAR(255) NOT NULL,
  duur INT NOT NULL,
  prioriteit VARCHAR(10) NOT NULL,
  beroepstype VARCHAR(50) NOT NULL,
  bevoegdheid VARCHAR(10) NOT NULL,
  fysieke_belasting INT NULL,
  attractie VARCHAR(255) NULL,
  is_buitenwerk TINYINT(1) NOT NULL,
  afgerond TINYINT(1) NOT NULL DEFAULT 0,
  x_coord FLOAT NULL,
  y_coord FLOAT NULL
);

INSERT INTO Personeelslid
(naam, werktijd, beroepstype, bevoegdheid, specialist_in_attracties, pauze_opsplitsen, leeftijd, verlaagde_fysieke_belasting)
VALUES ('Piet de Jong', 240, 'Mechanisch Monteur', 'Senior', 'Mega Spin,River Rapids,Twister', 0, 45, 30);

INSERT INTO Onderhoudstaak
(omschrijving, duur, prioriteit, beroepstype, bevoegdheid, fysieke_belasting, attractie, is_buitenwerk)
VALUES
('Mechanisch onderhoud aan scharnieren', 45, 'Hoog', 'Mechanisch Monteur', 'Senior', 10, 'Twister', 1),
('Kettingspanning inspecteren', 30, 'Laag', 'Mechanisch Monteur', 'Senior', 15, 'Mega Spin', 0);
