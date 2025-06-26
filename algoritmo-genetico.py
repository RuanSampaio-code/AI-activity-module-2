import random

# Atributos e mapeamentos
CORES = ["Amarela", "Azul", "Branca", "Verde", "Vermelha"]
NACIONALIDADES = ["Norueguês", "Dinamarquês", "Inglês", "Alemão", "Sueco"]
BEBIDAS = ["Água", "Chá", "Leite", "Cerveja", "Café"]
CIGARROS = ["Blends", "Dunhill", "BlueMaster", "Pall Mall", "Prince"]
ANIMAIS = ["Gatos", "Cavalos", "Cachorros", "Pássaros", "Peixes"]

TAMANHO_CASA = 15
CASAS_TOTAL = 5
TAMANHO_CROMOSSOMO = TAMANHO_CASA * CASAS_TOTAL

def binario_para_inteiro(bits): return int(bits, 2)

def inteiro_para_binario(valor, tamanho=3): return format(valor, f'0{tamanho}b')

def decodificar_casa(bits_15):
    """Decodifica uma casa (15 bits) para atributos legíveis"""
    cor = CORES[binario_para_inteiro(bits_15[0:3]) % 5]
    nacionalidade = NACIONALIDADES[binario_para_inteiro(bits_15[3:6]) % 5]
    bebida = BEBIDAS[binario_para_inteiro(bits_15[6:9]) % 5]
    cigarro = CIGARROS[binario_para_inteiro(bits_15[9:12]) % 5]
    animal = ANIMAIS[binario_para_inteiro(bits_15[12:15]) % 5]
    return {
        "cor": cor,
        "nacionalidade": nacionalidade,
        "bebida": bebida,
        "cigarro": cigarro,
        "animal": animal
    }


def decodificar_cromossomo(bits_75):
    """Decodifica um cromossomo de 75 bits para todas as casas"""
    casas = []
    for i in range(CASAS_TOTAL):
        inicio = i * TAMANHO_CASA
        casas.append(decodificar_casa(bits_75[inicio:inicio + TAMANHO_CASA]))
    return casas
def fitness(bits_75):
    """Calcula quantas regras são atendidas (usando pesos diferentes para algumas regras)"""
    casas = decodificar_cromossomo(bits_75)
    score = 0
    get_casa = lambda i: casas[i]

    # 1. O Norueguês vive na primeira casa
    if get_casa(0)['nacionalidade'] == 'Norueguês': score += 4

    # 2. O Inglês vive na casa Vermelha
    if any(c['nacionalidade'] == 'Inglês' and c['cor'] == 'Vermelha' for c in casas): score += 1

    # 3. O Sueco tem Cachorros como animais de estimação
    if any(c['nacionalidade'] == 'Sueco' and c['animal'] == 'Cachorros' for c in casas): score += 1

    # 4. O Dinamarquês bebe Chá
    if any(c['nacionalidade'] == 'Dinamarquês' and c['bebida'] == 'Chá' for c in casas): score += 1

    # 5. A casa Verde fica à esquerda da casa Branca
    cores = [c['cor'] for c in casas]
    if 'Verde' in cores and 'Branca' in cores:
        if cores.index('Verde') == cores.index('Branca') - 1:
            score += 4

    # 6. O homem que vive na casa Verde bebe Café
    if any(c['cor'] == 'Verde' and c['bebida'] == 'Café' for c in casas): score += 1

    # 7. O homem que fuma Pall Mall cria Pássaros
    if any(c['cigarro'] == 'Pall Mall' and c['animal'] == 'Pássaros' for c in casas): score += 1

    # 8. O homem que vive na casa Amarela fuma Dunhill
    if any(c['cor'] == 'Amarela' and c['cigarro'] == 'Dunhill' for c in casas): score += 1

    # 9. O homem que vive na casa do meio bebe Leite
    if get_casa(2)['bebida'] == 'Leite': score += 4

    # 10. O homem que fuma Blends vive ao lado do que tem Gatos
    for i, c in enumerate(casas):
        if c['cigarro'] == 'Blends':
            if ((i > 0 and casas[i-1]['animal'] == 'Gatos') or (i < 4 and casas[i+1]['animal'] == 'Gatos')):
                score += 4
                break

    # 11. O homem que cria Cavalos vive ao lado do que fuma Dunhill
    for i, c in enumerate(casas):
        if c['animal'] == 'Cavalos':
            if ((i > 0 and casas[i-1]['cigarro'] == 'Dunhill') or (i < 4 and casas[i+1]['cigarro'] == 'Dunhill')):
                score += 1
                break

    # 12. O homem que fuma BlueMaster bebe Cerveja
    if any(c['cigarro'] == 'BlueMaster' and c['bebida'] == 'Cerveja' for c in casas): score += 1

    # 13. O Alemão fuma Prince
    if any(c['nacionalidade'] == 'Alemão' and c['cigarro'] == 'Prince' for c in casas): score += 1

    # 14. O Norueguês vive ao lado da casa Azul
    for i, c in enumerate(casas):
        if c['nacionalidade'] == 'Norueguês':
            if ((i > 0 and casas[i-1]['cor'] == 'Azul') or (i < 4 and casas[i+1]['cor'] == 'Azul')):
                score += 4
                break

    # 15. O homem que fuma Blends é vizinho do que bebe Água
    for i, c in enumerate(casas):
        if c['cigarro'] == 'Blends':
            if ((i > 0 and casas[i-1]['bebida'] == 'Água') or (i < 4 and casas[i+1]['bebida'] == 'Água')):
                score += 1
                break

    return score


def gerar_individuo_aleatorio():
    """Gera uma solução de 75 bits com atributos aleatórios"""
    individuo = []
    for _ in range(CASAS_TOTAL):
        individuo.extend(inteiro_para_binario(random.randrange(5)))  # Cor
        individuo.extend(inteiro_para_binario(random.randrange(5)))  # Nacionalidade
        individuo.extend(inteiro_para_binario(random.randrange(5)))  # Bebida
        individuo.extend(inteiro_para_binario(random.randrange(5)))  # Cigarro
        individuo.extend(inteiro_para_binario(random.randrange(5)))  # Animal
    return ''.join(individuo)

def crossover(a, b):
    """Crossover de um ponto"""
    ponto = random.randint(1, TAMANHO_CROMOSSOMO - 1)
    return a[:ponto] + b[ponto:], b[:ponto] + a[ponto:]

def mutacao(individuo, taxa=0.01):
    """Inverte bits com uma certa taxa"""
    return ''.join(random.choice(['0','1']) if random.random() < taxa else bit for bit in individuo)

def selecao(populacao, scores):
    """Roleta para seleção"""
    total = sum(scores)
    pick = random.uniform(0, total)
    atual = 0
    for individuo, score in zip(populacao, scores):
        atual += score
        if atual >= pick:
            return individuo
def selecao_torneio(populacao, scores, k=3):
    """Seleciona o melhor de k indivíduos aleatórios (Torneio)"""
    escolhidos = random.sample(list(zip(populacao, scores)), k)
    vencedor = max(escolhidos, key=lambda x: x[1])
    return vencedor[0]

def executar_ag(tam_pop=300, taxa_mut=0.01, max_geracoes=10000, elitismo=1):
    """Execução do AG com Elitismo e Seleção por Torneio para melhorar eficiência"""
    populacao = [gerar_individuo_aleatorio() for _ in range(tam_pop)]
    melhor_individuo = None
    melhor_score = -1

    for geracao in range(1, max_geracoes + 1):
        scores = [fitness(ind) for ind in populacao]
        score_max = max(scores)

        # Armazena o melhor atual
        if score_max > melhor_score:
            melhor_score = score_max
            melhor_individuo = populacao[scores.index(score_max)]

        # Relatório
        print(f"Geração {geracao:>5} | Maior Pontuação: {score_max}")

        # Critério de sucesso
        if 30 in scores:
            indice = scores.index(30)
            vencedor = populacao[indice]
            print(f"\n🏁 Solução encontrada na geração {geracao}! \n")
            casas_solucao = decodificar_cromossomo(vencedor)
            for i, casa in enumerate(casas_solucao, 1):
                print(f"Casa {i}: {casa}")
            return vencedor

        # Elitismo: preserva os melhores indivíduos
        nova_pop = []
        elite = sorted(populacao, key=lambda ind: fitness(ind), reverse=True)[:elitismo]
        nova_pop.extend(elite)

        # Preenche o restante com seleção por torneio
        while len(nova_pop) < tam_pop:
            p1 = selecao_torneio(populacao, scores)
            p2 = selecao_torneio(populacao, scores)
            filho1, filho2 = crossover(p1, p2)
            nova_pop.extend([
                mutacao(filho1, taxa_mut),
                mutacao(filho2, taxa_mut)
            ])

        populacao = nova_pop[:tam_pop]

    # Resultado Final
    print("\n❌ Não encontrou solução perfeita no número máximo de gerações.")
    print(f"💡 Melhor solução encontrada (Pontuação: {melhor_score}):\n")
    casas_solucao = decodificar_cromossomo(melhor_individuo)
    for i, casa in enumerate(casas_solucao, 1):
        print(f"Casa {i}: {casa}")

    return None




if __name__ == '__main__':
  executar_ag()