class CriarLista:
    def __init__(self):
        self.lista_vertice = {}

    def inserir_vertice(self, vertices:list):
        for v in vertices:
            if v not in self.lista_vertice:
                self.lista_vertice[v] = []
       
        return self.lista_vertice

    def remover_vertice(self, vertices):
        for vertice in vertices:
            if vertice in self.lista_vertice:
                del self.lista_vertice[vertice]
                for v in self.lista_vertice:
                    if vertice in self.lista_vertice[v]:
                        self.lista_vertice[v].remove(vertice)

        return self.lista_vertice

    def inserir_aresta(self, origem, destino, direcionado=False):
        if origem in self.lista_vertice and destino in self.lista_vertice:
            if destino not in self.lista_vertice[origem]:
                self.lista_vertice[origem].append(destino)
            if not direcionado and origem not in self.lista_vertice[destino]:
                self.lista_vertice[destino].append(origem)

        else:
            print('Erro: Vértices inválidos.')

    def remover_aresta(self, arestas, direcionado=False):
        origem, destino = arestas

        if origem in self.lista_vertice and destino in self.lista_vertice[origem]:
            self.lista_vertice[origem].remove(destino)

        if not direcionado:
            if destino in self.lista_vertice and origem in self.lista_vertice[destino]:
                self.lista_vertice[destino].remove(origem)

        return self.lista_vertice

    def calc_grau(self, direcionado=False):
        # não direcionado
        if not direcionado:
            print(f"Grau de cada vértice:")
            for v in self.lista_vertice:
                print(f"d({v}): {len(self.lista_vertice[v])}")

        if direcionado:
            print(f"\nGrau de entrada e saída de cada vértice:")
            print("  | din | dout |")
            for v in self.lista_vertice:
                grau_entrada = 0
                grau_saida = len(self.lista_vertice[v])
                for u in self.lista_vertice:
                    if v in self.lista_vertice[u]:
                        grau_entrada += 1
                print(f"{v} |  {grau_entrada}  |   {grau_saida}  |")
        
        return self.lista_vertice 

    def verificar_adj(self, origem, destino):
        if origem in self.lista_vertice and destino in self.lista_vertice:
            if destino in self.lista_vertice[origem]:
                print(f"\nOs vértices {origem} e {destino} são adjacentes.")
            else:
                print(f"\nOs vértices {origem} e {destino} não são adjacentes.")
        else:
            print('Erro. Vértices inválidas.')

    def listar_vizinhos(self, vertice):
        if vertice in self.lista_vertice:
            vizinhos = self.lista_vertice[vertice]
            if vizinhos:
                print(f"\nVizinhos do vértice {vertice}: {', '.join(vizinhos)}")
            else:
                print(f"\nO vértice {vertice} não possui vizinhos.")
        else:
            print(f"\nO vértice {vertice} não existe no grafo.")

    def verificar_percurso(self, caminho, direcionado=False):
        if not caminho or len(caminho) < 2:
            print("Percurso inválido: deve conter ao menos dois vértices.")
            return False
        
        for v in caminho:
            if v not in self.lista_vertice:
                print(f"Percurso inválido: o vértice {v} não existe no grafo.")
                return False
            
        for i in range(len(caminho) - 1):
            origem = caminho[i]
            destino = caminho[i + 1]

            if destino not in self.lista_vertice[origem]:
                if not direcionado and origem in self.lista_vertice[destino]:
                    continue
                print(f"Percurso inválido: não há aresta entre {origem} e {destino}.")
                return False
            
        print(f"\nPercurso válido: {' → '.join(caminho)}")

        return True

    def mostrar_lista(self):
        for chave, valor in self.lista_vertice.items():
            if valor:
                for v in valor:
                    print(f"| {chave} | {v} |")


            else:
                print(f"| {chave} |   |")


        print('---------')

    def limpar_grafo(self):
        self.lista_vertice.clear()
        return self.lista_vertice



class BuscaProfundidade(CriarLista):
    def __init__(self):
        super().__init__()
        self.visitados = []
        self.pilha = []
        self.ciclos_encontrados = []

    def _print_estado(self, passo):
        pilha_formatada = [item['vertice'] for item in self.pilha]
        print(f"\n{passo}°")
        print(f"Visitados: {self.visitados}")
        print(f"Pilha: {pilha_formatada}")

    def dfs(self, inicio):
        if inicio not in self.lista_vertice:
            print(f"Erro: o vértice '{inicio}' não existe no grafo.")
            return []
        
        self.visitados = []
        self.pilha = []
        self.ciclos_encontrados = []
        passo = 1

        self._print_estado(passo)
        passo += 1

        self.pilha.append({'vertice': inicio, 'pai': None})
        self._print_estado(passo)
        passo += 1

        while len(self.pilha) > 0:
            item_atual = self.pilha.pop()
            vertice_atual = item_atual['vertice']
            pai = item_atual['pai']

            if vertice_atual not in self.visitados:
                self.visitados.append(vertice_atual)

            vizinhos = self.lista_vertice[vertice_atual]

            for vizinho in reversed(vizinhos):
                vizinho_pilha = False
                for i in self.pilha:
                    if i['vertice'] == vizinho:
                        vizinho_pilha = True
                        break

                vizinho_visitado = vizinho in self.visitados
                
                if not vizinho_visitado and not vizinho_pilha:
                    self.pilha.append({'vertice': vizinho, 'pai': vertice_atual})

                else:
                    if vizinho != pai:
                        descricao_ciclo = f"{vertice_atual} -> {vizinho}"
                        if descricao_ciclo not in self.ciclos_encontrados:
                            self.ciclos_encontrados.append(descricao_ciclo)
            self._print_estado(passo)
            passo += 1

        if self.ciclos_encontrados:
            print(f"\nForam detectados {len(self.ciclos_encontrados)} ciclo(s) no grafo:")
            for c in self.ciclos_encontrados:
                print(f"{c}")   
        else:
            print("\nNenhum ciclo encontrado.")

        return self.visitados

grafo = CriarLista()

grafo.inserir_vertice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
grafo.inserir_aresta('A', 'B')
grafo.inserir_aresta('A', 'D')
grafo.inserir_aresta('B', 'C')
grafo.inserir_aresta('D', 'E')
grafo.inserir_aresta('D', 'F')
grafo.inserir_aresta('D', 'H')
grafo.inserir_aresta('H', 'I')
grafo.inserir_aresta('F', 'G')
grafo.inserir_aresta('E', 'G')
grafo.inserir_aresta('E', 'A')
grafo.inserir_aresta('G', 'I')
grafo.inserir_aresta('B', 'A')

buscar = BuscaProfundidade()

buscar.lista_vertice = grafo.lista_vertice

buscar.dfs('A')
