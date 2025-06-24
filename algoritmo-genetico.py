""" import random

# Valores possíveis para cada característica
CORES = ['Vermelha', 'Verde', 'Branca', 'Amarela', 'Azul']
NACIONALIDADES = ['Inglês', 'Sueco', 'Dinamarquês', 'Norueguês', 'Alemão']
BEBIDAS = ['Chá', 'Café', 'Leite', 'Cerveja', 'Água']
CIGARROS = ['Pall Mall', 'Dunhill', 'Blends', 'BlueMaster', 'Prince']
ANIMAIS = ['Cachorros', 'Pássaros', 'Gatos', 'Cavalos', 'Peixe']

POP_SIZE = 200
MAX_GEN = 10000

# Gera um indivíduo válido (sem repetição por coluna)
def gerar_individuo():
    cores = random.sample(CORES, 5)
    nacs = random.sample(NACIONALIDADES, 5)
    bebs = random.sample(BEBIDAS, 5)
    cigs = random.sample(CIGARROS, 5)
    anis = random.sample(ANIMAIS, 5)

    individuo = []
    for i in range(5):
        casa = (cores[i], nacs[i], bebs[i], cigs[i], anis[i])
        individuo.append(casa)
    return individuo

# Avalia um indivíduo com base nas 15 regras
def fitness(ind):
    score = 0
    casas = ind

    for i, casa in enumerate(casas):
        cor, nac, beb, cig, ani = casa

        if nac == 'Norueguês' and i == 0:
            score += 1
        if nac == 'Inglês' and cor == 'Vermelha':
            score += 1
        if nac == 'Sueco' and ani == 'Cachorros':
            score += 1
        if nac == 'Dinamarquês' and beb == 'Chá':
            score += 1
        if cor == 'Verde' and i < 4 and casas[i+1][0] == 'Branca':
            score += 1
        if cor == 'Verde' and beb == 'Café':
            score += 1
        if cig == 'Pall Mall' and ani == 'Pássaros':
            score += 1
        if cor == 'Amarela' and cig == 'Dunhill':
            score += 1
        if i == 2 and beb == 'Leite':
            score += 1
        if cig == 'Blends' and vizinho(i, casas, lambda x: x[4] == 'Gatos'):
            score += 1
        if ani == 'Cavalos' and vizinho(i, casas, lambda x: x[3] == 'Dunhill'):
            score += 1
        if cig == 'BlueMaster' and beb == 'Cerveja':
            score += 1
        if nac == 'Alemão' and cig == 'Prince':
            score += 1
        if nac == 'Norueguês' and vizinho(i, casas, lambda x: x[0] == 'Azul'):
            score += 1
        if cig == 'Blends' and vizinho(i, casas, lambda x: x[2] == 'Água'):
            score += 1

    return score

def vizinho(i, casas, cond):
    if i > 0 and cond(casas[i-1]):
        return True
    if i < 4 and cond(casas[i+1]):
        return True
    return False

# Seleção por roleta
def selecao_roleta(pop, scores):
    total = sum(scores)
    pick = random.uniform(0, total)
    current = 0
    for i, ind in enumerate(pop):
        current += scores[i]
        if current > pick:
            return ind
    return pop[-1]

# Crossover por casa
def crossover(p1, p2):
    ponto = random.randint(1, 4)
    filho = p1[:ponto] + p2[ponto:]
    return filho

# Mutação simples
def mutacao(ind):
    i1, i2 = random.sample(range(5), 2)
    attr = random.randint(0, 4)

    casa1 = list(ind[i1])
    casa2 = list(ind[i2])

    casa1[attr], casa2[attr] = casa2[attr], casa1[attr]
    ind[i1], ind[i2] = casa1, casa2
    return ind

# Loop principal
def algoritmo_genetico():
    pop = [gerar_individuo() for _ in range(POP_SIZE)]
    for gen in range(MAX_GEN):
        scores = [fitness(ind) for ind in pop]
        if 15 in scores:
            index = scores.index(15)
            print(f"\n\u2714 Solução encontrada na geração {gen}:")
            mostrar_individuo(pop[index])
            return pop[index]

        nova_pop = []
        for _ in range(int(POP_SIZE * 0.2)):
            nova_pop.append(selecao_roleta(pop, scores))
        while len(nova_pop) < POP_SIZE:
            pai1 = selecao_roleta(pop, scores)
            pai2 = selecao_roleta(pop, scores)
            filho = crossover(pai1, pai2)
            if random.random() < 0.1:
                filho = mutacao(filho)
            nova_pop.append(filho)
        pop = nova_pop
    print("\n\u274C Nenhuma solução encontrada.")

def mostrar_individuo(ind):
    print("\nCasa\tCor\t\tNacionalidade\tBebida\t\tCigarro\t\tAnimal")
    for i, casa in enumerate(ind):
        print(f"{i+1}\t" + "\t".join(f"{c}".ljust(10) for c in casa))

if __name__ == "__main__":
    algoritmo_genetico()
 """

import random
import copy
import matplotlib.pyplot as plt
from collections import defaultdict

# Configurações Gerais
tamanho_populacao = 200
taxa_sobrevivencia = 0.35
taxa_cruzamento = 0.65
taxa_mutacao = 0.05
taxa_migracao = 0.05

parametros = {
    "cor": ["amarela", "azul", "branca", "verde", "vermelha"],
    "nacionalidade": ["alemao", "dinamarques", "noruegues", "ingles", "sueco"],
    "bebida": ["agua", "cha", "cafe", "leite", "cerveja"],
    "cigarro": ["dunhill", "blends", "pall mall", "prince", "blue master"],
    "animal": ["gatos", "passaros", "cavalos", "peixes", "cachorros"]
}


# Cria uma solução válida escolhendo aleatoriamente
# uma cor, nacionalidade, bebida, cigarro e animal.
def create():
    parametros_copy = copy.deepcopy(parametros)
    solucao = []

    for i in range(5):
        casa = {}
        for parametro in parametros_copy:
            atributo = random.choice(parametros_copy[parametro])
            parametros_copy[parametro].remove(atributo)
            casa[parametro] = atributo
        solucao.append(casa)
    return solucao


# Avalia a solução com base nos critérios estabelecidos.
def fitness(solucao):
    pontuacao = 0
    for i in range(len(solucao)):
        casa = solucao[i]

        # O Norueguês vive na primeira casa
        if (casa["nacionalidade"] == "noruegues" and i == 0):
            pontuacao += 4

        # O Inglês vive na casa Vermelha.
        if (casa["cor"] == "vermelha" and casa["nacionalidade"] == "ingles"):
            pontuacao += 1

        # O Sueco tem Cachorros como animais de estimação.
        if (casa["nacionalidade"] == "sueco" and casa["animal"] == "cachorros"):
            pontuacao += 1

        # O Dinamarquês bebe Chá.
        if (casa["nacionalidade"] == "dinamarques" and casa["bebida"] == "cha"):
            pontuacao += 1

        # A casa Verde fica do lado esquerdo da casa Branca.
        if (i + 1 < len(solucao) and solucao[i]["cor"] == "verde"
                and solucao[i + 1]["cor"] == "branca"):
            pontuacao += 4

        # O homem que vive na casa Verde bebe Café.
        if (casa["cor"] == "verde" and casa["bebida"] == "cafe"):
            pontuacao += 1

        # O homem que fuma cigarro cria pássaros
        if (casa["cigarro"] == "pall mall" and casa["animal"] == "passaros"):
            pontuacao += 1

        # O homem que mora na casa amarela fuma dunhill
        if (casa["cor"] == "amarela" and casa["cigarro"] == "dunhill"):
            pontuacao += 1

        # O homem que vive na casa do meio bebe Leite
        if (i == 2 and casa["bebida"] == "leite"):
            pontuacao += 4

        # O homem que fuma Blends vive ao lado do que tem Gatos
        if (casa["cigarro"] == "blends"):
            if ((i - 1 >= 0 and solucao[i - 1]["animal"] == "gatos")
                    or (i + 1 < len(solucao) and solucao[i + 1]["animal"] == "gatos")):
                pontuacao += 4

        # O homem que cria Cavalos vive ao lado do que fuma Dunhill
        if (casa["animal"] == "cavalos"):
            if ((i - 1 >= 0 and solucao[i - 1]["cigarro"] == "dunhill") or
                    (i + 1 < len(solucao) and solucao[i + 1]["cigarro"] == "dunhill")):
                pontuacao += 4

        # O homem que fuma BlueMaster bebe Cerveja
        if (casa["cigarro"] == "blue master" and casa["bebida"] == "cerveja"):
            pontuacao += 1

        # O Alemão fuma Prince
        if (casa["nacionalidade"] == "alemao" and casa["cigarro"] == "prince"):
            pontuacao += 1

        # O Norueguês vive ao lado da casa Azul
        if (casa["nacionalidade"] == "noruegues"):
            if ((i - 1 >= 0 and solucao[i - 1]["cor"] == "azul")
                    or (i + 1 < len(solucao) and solucao[i + 1]["cor"] == "azul")):
                pontuacao += 4

        # O homem que fuma Blends é vizinho do que bebe Água
        if (casa["cigarro"] == "blends"):
            if ((i - 1 >= 0 and solucao[i - 1]["bebida"] == "agua")
                    or (i + 1 < len(solucao) and solucao[i + 1]["bebida"] == "agua")):
                pontuacao += 4
    return pontuacao


# Realiza o cruzamento de duas soluções gerando dois filhos
def crossover(solucao1, solucao2):
    filho1 = []
    filho2 = []

    for i in range(5):
        filho1.append({"cor": solucao1[i]["cor"],
                       "nacionalidade": solucao1[i]["nacionalidade"],
                       "bebida": solucao2[i]["bebida"],
                       "cigarro": solucao2[i]["cigarro"],
                       "animal": solucao2[i]["animal"],
                       })
        filho2.append({"cor": solucao2[i]["cor"],
                       "nacionalidade": solucao2[i]["nacionalidade"],
                       "bebida": solucao1[i]["bebida"],
                       "cigarro": solucao1[i]["cigarro"],
                       "animal": solucao1[i]["animal"],
                       })

    return filho1, filho2


# Realiza mutação em uma solução
def mutation(solucao):
    pos_casa1 = random.randint(0,4)
    pos_casa2 = random.randint(0,4)
    while (pos_casa1 == pos_casa2):
        pos_casa2 = random.randint(0, 4)

    pos_atributo = random.randint(0,4)

    atributos = ["cor","nacionalidade","bebida","cigarro","animal"]
    mutante = solucao

    aux_atributo = ""
    aux_atributo = mutante[pos_casa1][atributos[pos_atributo]]
    mutante[pos_casa1][atributos[pos_atributo]] = mutante[pos_casa2][atributos[pos_atributo]]
    mutante[pos_casa2][atributos[pos_atributo]] = aux_atributo
    return mutante


def insere_imigrante():
    return create()


def roleta(tabela):
    tipos_de_pontos = []
    for i in tabela:
        tipos_de_pontos.append(i)

    result1 = random.choices(tipos_de_pontos, weights=tipos_de_pontos, k=1)[0]
    result2 = random.choices(tipos_de_pontos, weights=tipos_de_pontos, k=1)[0]
    return  random.choice(tabela[result1]), random.choice(tabela[result2])


def imprime_solucao(resposta):
    i = 1
    for casa in resposta:
        print(f"==Casa {i}==")
        i += 1
        for chave, valor in casa.items():
            print(f"{chave}: {valor}")
        print()  # Adiciona uma linha em branco entre os dicionários para melhor legibilidade

populacao = []
geracao = []
quantidade_geracoes = 0
maior_pontuacao = 0
resposta = []

x_media = []
y_media = []
x_maior = []
y_maior = []

# Criando população inicial
for i in range(tamanho_populacao):
    populacao.append(create())

while (maior_pontuacao != 36):
    # log da geração atual
    log = "Geração {n_geracao}... maior pontuação: {pontuacao}..."
    print(log.format(n_geracao=quantidade_geracoes, solucao=resposta, pontuacao=maior_pontuacao))

    # Avaliando cada solução com a função fitness

        #ranking se dá dessa forma: ranking[id_da_solucao] = pontuacao
    ranking = {}
        #tabela de pontos se dá dessa forma: tabela_de_pontos [pontuacao] = solucao
    tabela_por_pontos = defaultdict(list)
    media_pontos = 0
    for i in range(tamanho_populacao):
        solucao = populacao[i]
        pontuacao = fitness(solucao)
        tabela_por_pontos[pontuacao].append(solucao)
        ranking[i] = pontuacao
        media_pontos += pontuacao
    media_pontos = media_pontos / tamanho_populacao

    # Ordenando a tabela ranking para que os primeiros sejam os mais aptos
    ranking = dict(
        sorted(ranking.items(), key=lambda item: item[1], reverse=True))

    #contem todas as pontuações em ordem decrescente
    classificacao = list(ranking.values())

    maior_pontuacao = classificacao[0]
    resposta = tabela_por_pontos[maior_pontuacao]

    # chaves_ranking recebe a lista de todas as chaves ordenadas decrescentemente, de acordo com a pontuação.
    # a chave funciona como id de uma solucao
    chaves_ranking = list(ranking.keys())

    # Sobrevivendo as melhores soluções
    for i in range(round(taxa_sobrevivencia * tamanho_populacao)):
        geracao.append(populacao[chaves_ranking[i]])

    # Cruzamento utilizando roleta
    for i in range(round(taxa_sobrevivencia * tamanho_populacao),
                   tamanho_populacao,2):
        if (i + 1 < tamanho_populacao):
            pai1, pai2 = roleta(tabela_por_pontos)
            filho1, filho2 = crossover(pai1, pai2)
            geracao.append(filho1)
            geracao.append(filho2)

    # Realizando mutação
    for i in range(round(taxa_mutacao * tamanho_populacao), tamanho_populacao):
        if random.random() <= taxa_mutacao:
            geracao[i] = mutation(geracao[i])

    #Adicionando imigrante
    for i in range(round(taxa_migracao * tamanho_populacao),
                   tamanho_populacao):
        if random.random() <= taxa_migracao:
            geracao[i] = insere_imigrante()

    populacao = geracao
    geracao = []
    ranking = {}
    quantidade_geracoes += 1
    tabela_por_pontos.clear()
    x_media.append(quantidade_geracoes)
    y_media.append(media_pontos)
    x_maior.append(quantidade_geracoes)
    y_maior.append(maior_pontuacao)

log = "Geração {n_geracao}... Solução: "
print(log.format(n_geracao=quantidade_geracoes))
imprime_solucao(resposta[0])

plt.plot(x_media, y_media, color='blue')
plt.plot(x_maior, y_maior, color='green')
plt.show()
