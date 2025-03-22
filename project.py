import os
folder ="files"
def ler_config(S):
    """
    Lê o ficheiro de configuração "config_S.txt" e devolve um dicionário com os parâmetros.

    Args:
        S (str): Código da simulação (por exemplo, "T11").

    Returns:
        dict: Dicionário contendo as constantes e os valores lidos do ficheiro.
    """
    ficheiro = os.path.join(folder, f"config_{S}.txt")
    parametros = {}

    try:
        with open(ficheiro, "r") as f:
            linhas = f.readlines()

        # Processar linha a linha
        for linha in linhas:
            # Ignorar linhas vazias ou comentários
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue

            # Separar chave e valor
            chave, valor = linha.split("=", 1)
            chave = chave.strip()
            valor = valor.strip()

            # Verifica dacă expresia conține chei (și păstreaz-o neevaluată)
            if any(key in valor for key in parametros):
                parametros[chave] = valor  # Păstrează expresia ca text
            else:
                try:
                    parametros[chave] = eval(valor, {}, parametros)
                except Exception:
                    parametros[chave] = valor  # Salvează ca string dacă nu poate fi evaluat

    except Exception as e:
        print(f"Erro ao processar o ficheiro {ficheiro}: {e}")

    return parametros







#T12
def nova_pessoa(idade=0):
    global CC

    genero = "M" if CC % 2 == 0 else "F"

    # Determinarea salariului și pensiei în funcție de vârstă
    if idade < 23:
        salario = 0
        pensao = 0
    elif idade in range(23, IDADE_REFORMA + 1):
        salario = SALARIO_BASE
        pensao = 0
    else:  # idade > IDADE_REFORMA
        salario = 0
        pensao = PENSAO_BASE

    pessoa = {
        "cc": CC,
        "nome": f"Pessoa_{CC}",
        "genero": genero,
        "idade": idade,
        "salario": salario,
        "pensao": pensao,
    }

    CC += 1
    return pessoa


#T13
def ler_populacao_inicial(S):
    new_population=[]


    file = os.path.join(folder, f"população_inicial_{S}.txt")
    with open(file,'r') as population:

        for line in population:
            dados=line.strip().split(',')

            idade=int(dados[3])
            #genero=dados[2].strip()


            new_p=nova_pessoa(idade)
            new_population.append(new_p)



    return new_population




#exclude
def exclude_entities(entities, p, year):
    """
    Exclude a percentage p of entities deterministically based on the year.

    Parameters:
        entities (list of dict): List of entities.
        p (float): The percentage of entities to exclude (0 <= p <= 1).
        year (int): The year used for deterministic variation.

    Returns:
        list of dict: List of entities that are not excluded.
    """
    num_to_exclude = int(len(entities) * p)

    # Calculate a score for each entity based on its index and the year
    entities_sorted = sorted(
        enumerate(entities),
        key=lambda e: (e[0] + year) % 100  # e[0] is the index
    )

    # Exclude the first num_to_exclude entities based on the sorted order
    included_entities = [entity for i, entity in entities_sorted[num_to_exclude:]]
    return included_entities







#T21
def simula_ano(populacao, ano_corrente):
    """
    Simula a passagem de um ano em termos demográficos.

    Args:
        populacao (list): Lista de pessoas (dicionários com atributo 'idade').
        ano_corrente (int): Ano atual da simulação.

    Returns:
        list: Nova população após a simulação do ano.
    """
    # 1. Salvar o tamanho da população original (antes da mortalidade)
    tamanho_original = len(populacao)


        # Incrementăm vârsta
    for pessoa in populacao:
        pessoa['idade'] += 1

        # Recalculăm salariile și pensiile conform regulilor
        if pessoa['idade'] >= IDADE_REFORMA:
            pessoa['salario'] = 0
            pessoa['pensao'] = PENSAO_BASE
        elif pessoa['idade'] in range(23, IDADE_REFORMA+1):
            pessoa['salario'] = SALARIO_BASE
            pessoa['pensao'] = 0
        else:
            pessoa['salario'] = 0
            pessoa['pensao'] = 0

        # Restul logicii (mortalitate, nașteri etc.)
    populacao = [p for p in populacao if p['idade'] <= 100]

    nova_populacao = []
    for faixa_etaria, (range_idade, taxa_mortalitate) in MORTALIDADE.items():
        grupo_atual = [p for p in populacao if p['idade'] in range_idade]
        sobreviventes = exclude_entities(grupo_atual, taxa_mortalitate, ano_corrente)
        nova_populacao.extend(sobreviventes)

    populacao = nova_populacao

    num_bebes = max(1, (tamanho_original) // NATALIDADE)
    novos_bebes = [nova_pessoa(idade=0) for _ in range(num_bebes)]
    populacao.extend(novos_bebes)

    return populacao









#T22
def cobra_seg_social(ano, total, population):

    contribution = sum(
        person['salario'] * DESCONTOS for person in population if 23 <= person['idade'] <= IDADE_REFORMA
        )
    pensao = sum(
        person['pensao'] for person in population if person['idade'] > IDADE_REFORMA
        )
    total += contribution - pensao
    return float(total)


#T3

### Programação 1 Grupo 236
### Vlad Digori - 64120
### Gilson Sanca- 58783

config=ler_config('11')

DESCONTOS=config['DESCONTOS']
CC=config['CC']

IDADE_REFORMA=config['IDADE_REFORMA']
SALARIO_BASE=config['SALARIO_BASE']
PENSAO_BASE=config['PENSAO_BASE']
ano_start=config['ANO_INICIAL']
fundo_p=config['FUNDO_PENSOES_INICIAL']
epocas=config['EPOCAS']
populacao = ler_populacao_inicial(11)
MORTALIDADE=config['MORTALIDADE']
NATALIDADE=config['NATALIDADE']

print(f'A simulação começou no ano {ano_start}, com população total de {len(populacao)}, e o fundo de pensões a valer {fundo_p}.')

for i in range(epocas+1):
    ano_actual=ano_start+i
    populacao=simula_ano(populacao,ano_actual)
    fundo_p=cobra_seg_social(ano_actual,fundo_p,populacao)
    if fundo_p<0:
        print(f"No ano {ano_actual}, a população foi {len(populacao)} e o fundo de pensões foi negativo, com valor {fundo_p}.")

        #10000000 no config
print(f'A simulação terminou no ano {ano_actual}, com população total de {len(populacao)} pessoas e o fundo de pensões vale {fundo_p}.')


ficheiro_final =os.path.join(folder, f'populaçao_final_{11}.txt')
with open(ficheiro_final, 'w') as f:
    for pessoa in populacao:
        linha = f"{pessoa['cc']}, {pessoa['nome']}, {pessoa['genero']}, {pessoa['idade']}, {pessoa['salario']}, {pessoa['pensao']}\n"
        f.write(linha)

