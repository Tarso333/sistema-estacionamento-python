import mysql.connector
from datetime import datetime

TOTAL_VAGAS = 10
VAGAS_PRIORITARIAS = ["P1", "P2"]

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="estacionamento"
)

cursor = conexao.cursor()


def cadastrar_veiculo():
    placa = input("Placa: ")
    modelo = input("Modelo: ")
    tipo = input("Tipo (comum/prioritario): ")

    sql = "INSERT INTO Veiculo (placa, modelo, tipo) VALUES (%s,%s,%s)"
    cursor.execute(sql, (placa, modelo, tipo))
    conexao.commit()

    print("✅ Veículo cadastrado!")


def vagas_disponiveis():
    cursor.execute("""
    SELECT COUNT(*) 
    FROM Estacionamento
    WHERE hora_saida IS NULL
    """)

    ocupadas = cursor.fetchone()[0]
    disponiveis = TOTAL_VAGAS - ocupadas

    print(f"🚗 Vagas disponíveis: {disponiveis}")


def registrar_entrada():
    placa = input("Placa do veículo: ")
    vaga = input("Número da vaga: ")

    cursor.execute("""
    SELECT COUNT(*)
    FROM Estacionamento
    WHERE hora_saida IS NULL
    """)
    ocupadas = cursor.fetchone()[0]

    if ocupadas >= TOTAL_VAGAS:
        print("❌ Estacionamento lotado!")
        return

    # Pega o veículo pelo placa
    cursor.execute("SELECT id, tipo FROM Veiculo WHERE placa = %s", (placa,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("❌ Veículo não cadastrado!")
        return

    veiculo_id, tipo = resultado

    # Bloqueio reforçado para vagas prioritárias
    if vaga in VAGAS_PRIORITARIAS:
        if tipo != "prioritario":
            print(f"❌ Vaga {vaga} é prioritária! Veículo comum não pode estacionar aqui.")
            return
    else:
        if tipo == "prioritario":
            # Opcional: permitir que prioritário use vaga comum
            print(f"⚠️ Veículo prioritário usando vaga comum.")

    # Registra a entrada
    sql = """
    INSERT INTO Estacionamento (veiculo_id, vaga, hora_entrada)
    VALUES (%s,%s,NOW())
    """
    cursor.execute(sql, (veiculo_id, vaga))
    conexao.commit()

    print("✅ Entrada registrada!")


def registrar_saida():
    placa = input("Placa do veículo: ")

    cursor.execute("""
    SELECT E.id, E.hora_entrada
    FROM Estacionamento E
    JOIN Veiculo V ON V.id = E.veiculo_id
    WHERE V.placa = %s AND E.hora_saida IS NULL
    """, (placa,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("❌ Veículo não está estacionado!")
        return

    registro_id, hora_entrada = resultado

    agora = datetime.now()
    tempo = agora - hora_entrada

    if tempo.total_seconds() > 14400:
        print("⚠️ Veículo ficou mais de 4 horas!")

    cursor.execute("""
    UPDATE Estacionamento
    SET hora_saida = NOW()
    WHERE id = %s
    """, (registro_id,))

    conexao.commit()

    print("✅ Saída registrada!")


def listar_estacionados():

    cursor.execute("""
    SELECT V.placa, V.modelo, E.vaga, E.hora_entrada
    FROM Estacionamento E
    JOIN Veiculo V ON V.id = E.veiculo_id
    WHERE E.hora_saida IS NULL
    """)

    resultados = cursor.fetchall()

    print("\n🚗 Veículos estacionados:\n")

    for placa, modelo, vaga, entrada in resultados:
        print(f"{placa} | {modelo} | Vaga {vaga} | Entrada: {entrada}")


def total_veiculos_dia():

    cursor.execute("""
    SELECT COUNT(*)
    FROM Estacionamento
    WHERE DATE(hora_entrada) = CURDATE()
    """)

    total = cursor.fetchone()[0]

    print(f"📊 Total de veículos hoje: {total}")


while True:

    print("\n====== SISTEMA ESTACIONAMENTO ======")
    print("1 - Cadastrar veículo")
    print("2 - Registrar entrada")
    print("3 - Registrar saída")
    print("4 - Vagas disponíveis")
    print("5 - Listar estacionados")
    print("6 - Total veículos do dia")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_veiculo()

    elif opcao == "2":
        registrar_entrada()

    elif opcao == "3":
        registrar_saida()

    elif opcao == "4":
        vagas_disponiveis()

    elif opcao == "5":
        listar_estacionados()

    elif opcao == "6":
        total_veiculos_dia()

    elif opcao == "0":
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida!")