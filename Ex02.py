class Especie:
    def __init__(self, codigoRaridade, nomeComum, nomeCientifico,
                 continenteOrigem, qtdAmostras):
        self.codigoRaridade    = codigoRaridade      
        self.nomeComum         = nomeComum
        self.nomeCientifico    = nomeCientifico
        self.continenteOrigem  = continenteOrigem
        self.qtdAmostras       = qtdAmostras

    def __str__(self):
        return (f"[Raridade: {self.codigoRaridade}] {self.nomeComum} "
                f"({self.nomeCientifico}) | Continente: {self.continenteOrigem} "
                f"| Amostras: {self.qtdAmostras}")

class No:
    def __init__(self, especie):
        self.dado  = especie   
        self.esq   = None
        self.dir   = None
        self.altura = 1        

class AVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self._altura(no.esq), self._altura(no.dir))

    def _fator(self, no):
        if no is None:
            return 0
        return self._altura(no.esq) - self._altura(no.dir)

    def _rotacao_direita(self, y):
        x  = y.esq
        T2 = x.dir
        x.dir = y
        y.esq = T2
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        return x   

    def _rotacao_esquerda(self, x):
        y  = x.dir
        T2 = y.esq
        y.esq = x
        x.dir = T2
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y   

    def _balancear(self, no):
        self._atualizar_altura(no)
        fb = self._fator(no)
        if fb > 1 and self._fator(no.esq) >= 0:
            return self._rotacao_direita(no)
        if fb > 1 and self._fator(no.esq) < 0:
            no.esq = self._rotacao_esquerda(no.esq)
            return self._rotacao_direita(no)
        if fb < -1 and self._fator(no.dir) <= 0:
            return self._rotacao_esquerda(no)
        if fb < -1 and self._fator(no.dir) > 0:
            no.dir = self._rotacao_direita(no.dir)
            return self._rotacao_esquerda(no)
        return no   

    def inserir(self, especie):
        self.raiz = self._inserir(self.raiz, especie)

    def _inserir(self, no, especie):
        if no is None:
            return No(especie)
        if especie.codigoRaridade < no.dado.codigoRaridade:
            no.esq = self._inserir(no.esq, especie)
        elif especie.codigoRaridade > no.dado.codigoRaridade:
            no.dir = self._inserir(no.dir, especie)
        else:
            print("Codigo de raridade ja existe na arvore.")
            return no
        return self._balancear(no)   

    def atualizar_raridade(self, codigo_atual, novo_codigo):
        especie = self.buscar(codigo_atual)
        if especie is None:
            return False
        self.remover(codigo_atual)
        especie.codigoRaridade = novo_codigo
        self.inserir(especie)
        return True

    def resgatar_mais_rara(self):
        if self.raiz is None:
            return None
        mais_rara = self._maximo(self.raiz).dado
        self.raiz = self._remover(self.raiz, mais_rara.codigoRaridade)
        return mais_rara

    def _maximo(self, no):
        while no.dir is not None:
            no = no.dir
        return no

    def _minimo(self, no):
        while no.esq is not None:
            no = no.esq
        return no

    def buscar(self, codigo):
        return self._buscar(self.raiz, codigo)

    def _buscar(self, no, codigo):
        if no is None:
            return None
        if codigo == no.dado.codigoRaridade:
            return no.dado
        elif codigo < no.dado.codigoRaridade:
            return self._buscar(no.esq, codigo)
        else:
            return self._buscar(no.dir, codigo)

    def remover(self, codigo):
        self.raiz = self._remover(self.raiz, codigo)

    def _remover(self, no, codigo):
        if no is None:
            return None
        if codigo < no.dado.codigoRaridade:
            no.esq = self._remover(no.esq, codigo)
        elif codigo > no.dado.codigoRaridade:
            no.dir = self._remover(no.dir, codigo)
        else:
            if no.esq is None and no.dir is None:
                return None
            if no.esq is None:
                return no.dir
            if no.dir is None:
                return no.esq
            sucessor = self._minimo(no.dir)
            no.dado  = sucessor.dado
            no.dir   = self._remover(no.dir, sucessor.dado.codigoRaridade)
        return self._balancear(no)   

    def relatorio_emergencia(self):
        resultado = []
        self._em_ordem_invertida(self.raiz, resultado)
        return resultado

    def _em_ordem_invertida(self, no, resultado):
        if no is None:
            return
        self._em_ordem_invertida(no.dir, resultado)
        resultado.append(no.dado)
        self._em_ordem_invertida(no.esq, resultado)

    def em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no is None:
            return
        self._em_ordem(no.esq, resultado)
        resultado.append(no.dado)
        self._em_ordem(no.dir, resultado)

def menu():
    arvore = AVL()
    while True:
        print("\n" + "=" * 55)
        print("      ArkSeed 2203 - Estacao Orbital ArkSeed     ")
        print("=" * 55)
        print("a) Catalogar especie")
        print("b) Alerta de extincao (atualizar codigo de raridade)")
        print("c) Resgatar especie mais rara")
        print("d) Buscar por codigo de raridade")
        print("e) Relatorio de emergencia (mais rara -> mais comum)")
        print("0) Sair")
        print("-" * 55)
        opcao = input("Escolha: ").strip().lower()

        if opcao == 'a':
            try:
                codigo = int(input("Codigo de raridade (1-9999): "))
                if not (1 <= codigo <= 9999):
                    print("Codigo fora do intervalo permitido (1-9999).")
                    continue
                nomeComum        = input("Nome comum: ")
                nomeCientifico   = input("Nome cientifico: ")
                continenteOrigem = input("Continente de origem: ")
                qtdAmostras      = int(input("Quantidade de amostras: "))
                especie = Especie(codigo, nomeComum, nomeCientifico,
                                  continenteOrigem, qtdAmostras)
                arvore.inserir(especie)
                print(f"Especie catalogada com codigo {codigo}!")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == 'b':
            try:
                atual = int(input("Codigo de raridade atual: "))
                novo  = int(input("Novo codigo de raridade (1-9999): "))
                if not (1 <= novo <= 9999):
                    print("Codigo fora do intervalo permitido.")
                    continue
                if arvore.atualizar_raridade(atual, novo):
                    print(f"Codigo atualizado: {atual} -> {novo}. Arvore rebalanceada.")
                else:
                    print("Especie nao encontrada.")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == 'c':
            especie = arvore.resgatar_mais_rara()
            if especie:
                print(f"Especie mais rara resgatada e removida da arvore:")
                print(f"{especie}")
            else:
                print("Nenhuma especie cadastrada.")

        elif opcao == 'd':
            try:
                codigo = int(input("Codigo de raridade: "))
                especie = arvore.buscar(codigo)
                if especie:
                    print(f"Encontrada: {especie}")
                else:
                    print("Especie nao encontrada.")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == 'e':
            lista = arvore.relatorio_emergencia()
            if lista:
                print("\nRelatorio de emergencia (mais rara -> mais comum):")
                for i, e in enumerate(lista, 1):
                    print(f"{i}. {e}")
            else:
                print("Nenhuma especie cadastrada.")

        elif opcao == '0':
            print("Saindo... ")
            break
        else:
            print("Opcao invalida.")

if __name__ == '__main__':
    menu()
