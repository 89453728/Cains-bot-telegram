CREATE TABLE fracasos (id INT AUTO_INCREMENT IDENTITY(0,1) PRIMARY KEY ,texto TEXT NOT NULL);
CREATE TABLE triunfos (id INT AUTO_INCREMENT IDENTITY(0,1) PRIMARY KEY ,texto TEXT NOT NULL);


INSERT INTO fracasos (id,texto) VALUES (0,"hola");
INSERT INTO fracasos (id,texto) VALUES (1,"bnjbnjwenc");
INSERT INTO fracasos (id,texto) VALUES (2,"wvewrvrvrve");
INSERT INTO fracasos (id,texto) VALUES (3,"wevvwrev");
INSERT INTO fracasos (id,texto) VALUES (4,"wewvwevwv");
INSERT INTO fracasos (id,texto) VALUES (5,"vewwevewvw");
INSERT INTO fracasos (id,texto) VALUES (6,"wevvwvwev");
INSERT INTO fracasos (id,texto) VALUES (7,"wfgehbtyn");
INSERT INTO fracasos (id,texto) VALUES (8,"nyWEbebtrhn");
INSERT INTO fracasos (id,texto) VALUES (9,"erbnjknerjklnbk");
INSERT INTO fracasos (id,texto) VALUES (10,"neowuiuinur");


SELECT texto FROM fracasos WHERE id = x;
SELECT texto FROM fracasos WHERE id != x;
SELECT texto FROM fracasos WHERE id > x;
SELECT texto FROM fracasos WHERE id < x;
SELECT texto FROM fracasos WHERE id >= x;
SELECT texto FROM fracasos WHERE id <= x;

SELECT texto FROM fracasos ORDER BY id ASC;
SELECT texto FROM fracasos ORDER BY id DESC;

INSERT INTO fracasos (id, texto) VALUES ((SELECT MAX(ID) FROM fracasos) + 1,"hgola");