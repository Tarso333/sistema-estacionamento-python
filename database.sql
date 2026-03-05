CREATE DATABASE estacionamento;

USE estacionamento;

CREATE TABLE Veiculo (
id INT AUTO_INCREMENT PRIMARY KEY,
placa VARCHAR(10) UNIQUE NOT NULL,
modelo VARCHAR(50) NOT NULL,
tipo ENUM ('comum', 'prioritario') NOT NULL
);

CREATE TABLE Estacionamento (
id INT AUTO_INCREMENT PRIMARY KEY,
veiculo_id INT NOT NULL,
vaga VARCHAR(10) NOT NULL,
hora_entrada DATETIME NOT NULL,
hora_saida DATETIME,
FOREIGN KEY (veiculo_id) REFERENCES Veiculo(id)
);