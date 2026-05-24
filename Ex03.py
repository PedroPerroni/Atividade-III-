import random

class Ativo:
    def __init__(self, ticker, nomeEmpresa, setor, cotacaoAtual, qtdCotas, tipoAtivo):
        self.codigoAtivo  = random.randint(1000, 9999)
        self.ticker       = ticker
        self.nomeEmpresa  = nomeEmpresa
        self.setor        = setor
        self.cotacaoAtual = cotacaoAtual
        self.qtdCotas     = qtdCotas
        self.tipoAtivo    = tipoAtivo

    def __str__(self):
        total = self.cotacaoAtual * self.qtdCotas
        return (f"[Codigo: {self.codigoAtivo}] {self.ticker} - {self.nomeEmpresa} "
                f"| Setor: {self.setor} | Tipo: {self.tipoAtivo} "
                f"| Cotacao: R$ {self.cotacaoAtual:.2f} | Cotas: {self.qtdCotas} "
                f"| Total em custodia: R$ {total:.2f}")


class No:
    def __init__(self, ativo):
        self.dado = ativo
        self.esq  = None
        self.dir  = None


class BST:
    def __init__(self):
        self.raiz = None

    def inserir(self, ativo):
        self.raiz = self._inserir(self.raiz, ativo)

    def _inserir(self, no, ativo):
        if no is None:
            return No(ativo)
        if ativo.codigoAtivo < no.dado.codigoAtivo:
            no.esq = self._inserir(no.esq, ativo)
        elif ativo.codigoAtivo > no.dado.codigoAtivo:
            no.dir = self._inserir(no.dir, ativo)
        return no

    def buscar(self, codigo):
        return self._buscar(self.raiz, codigo)

    def _buscar(self, no, codigo):
        if no is None:
            return None
        if codigo == no.dado.codigoAtivo:
            return no.dado
        elif codigo < no.dado.codigoAtivo:
            return self._buscar(no.esq, codigo)
        else:
            return self._buscar(no.dir, codigo)

    def atualizar_cotacao(self, codigo, nova_cotacao):
        ativo = self.buscar(codigo)
        if ativo is None:
            return False
        ativo.cotacaoAtual = nova_cotacao
        return True

    def remover(self, codigo):
        self.raiz = self._remover(self.raiz, codigo)

    def _remover(self, no, codigo):
        if no is None:
            return None
        if codigo < no.dado.codigoAtivo:
            no.esq = self._remover(no.esq, codigo)
        elif codigo > no.dado.codigoAtivo:
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
            no.dir   = self._remover(no.dir, sucessor.dado.codigoAtivo)
        return no

    def _minimo(self, no):
        while no.esq is not None:
            no = no.esq
        return no

    def _buscar_no(self, no, codigo):
        if no is None:
            return None
        if codigo == no.dado.codigoAtivo:
            return no
        elif codigo < no.dado.codigoAtivo:
            return self._buscar_no(no.esq, codigo)
        else:
            return self._buscar_no(no.dir, codigo)

    def valor_patrimonial(self, no):
        if no is None:
            return 0.0
        return (no.dado.cotacaoAtual * no.dado.qtdCotas
                + self.valor_patrimonial(no.esq)
                + self.valor_patrimonial(no.dir))

    def contar_ativos(self, no):
        if no is None:
            return 0
        return 1 + self.contar_ativos(no.esq) + self.contar_ativos(no.dir)

    def relatorio_subarvore(self, codigo):
        no = self._buscar_no(self.raiz, codigo)
        if no is None:
            return None

        valor_proprio      = no.dado.cotacaoAtual * no.dado.qtdCotas
        valor_subarvore    = self.valor_patrimonial(no)
        ativos_subarvore   = self.contar_ativos(no)
        valor_total        = self.valor_patrimonial(self.raiz)

        if valor_total == 0:
            participacao = 0.0
        else:
            participacao = (valor_subarvore / valor_total) * 100

        return {
            "ativo"           : no.dado,
            "valor_proprio"   : valor_proprio,
            "valor_subarvore" : valor_subarvore,
            "ativos_subarvore": ativos_subarvore,
            "participacao"    : participacao
        }


def menu():
    carteira = BST()

    while True:
        print("\n" + "=" * 55)
        print("       CapitalTree - Gestora de Fundos            ")
        print("=" * 55)
        print("a) Cadastrar ativo")
        print("b) Buscar ativo por codigo")
        print("c) Atualizar cotacao")
        print("d) Retirar ativo da carteira")
        print("e) Valor patrimonial da SubArvore")
        print("0) Sair")
        print("-" * 55)
        opcao = input("Escolha: ").strip().lower()

        if opcao == 'a':
            try:
                ticker       = input("Ticker (ex: PETR4): ")
                nomeEmpresa  = input("Nome da empresa: ")
                setor        = input("Setor: ")
                cotacao      = float(input("Cotacao atual (R$): "))
                qtdCotas     = int(input("Quantidade de cotas: "))
                tipoAtivo    = input("Tipo (ACAO / FII / TITULO): ").upper()
                ativo = Ativo(ticker, nomeEmpresa, setor, cotacao, qtdCotas, tipoAtivo)
                carteira.inserir(ativo)
                print(f"Ativo cadastrado com codigo {ativo.codigoAtivo}!")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == 'b':
            try:
                codigo = int(input("Codigo do ativo: "))
                ativo  = carteira.buscar(codigo)
                if ativo:
                    print(f"Encontrado: {ativo}")
                else:
                    print("Ativo nao encontrado.")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == 'c':
            try:
                codigo      = int(input("Codigo do ativo: "))
                nova_cotacao = float(input("Nova cotacao (R$): "))
                if carteira.atualizar_cotacao(codigo, nova_cotacao):
                    print(f"Cotacao atualizada para R$ {nova_cotacao:.2f}")
                else:
                    print("Ativo nao encontrado.")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == 'd':
            try:
                codigo = int(input("Codigo do ativo a remover: "))
                if carteira.buscar(codigo):
                    carteira.remover(codigo)
                    print(f"Ativo {codigo} removido da carteira.")
                else:
                    print("Ativo nao encontrado.")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == 'e':
            try:
                codigo    = int(input("Codigo do ativo: "))
                resultado = carteira.relatorio_subarvore(codigo)
                if resultado:
                    a = resultado["ativo"]
                    print(f"\nAtivo consultado:    {a.ticker} (codigo: {a.codigoAtivo})")
                    print(f"Valor proprio:       R$ {resultado['valor_proprio']:.2f} "
                          f"(cotacao: R$ {a.cotacaoAtual:.2f} x {a.qtdCotas} cotas)")
                    print(f"Ativos na SubArvore: {resultado['ativos_subarvore']}")
                    print(f"Valor patrimonial da SubArvore: R$ {resultado['valor_subarvore']:.2f}")
                    print(f"Participacao no patrimonio total: {resultado['participacao']:.1f}%")
                else:
                    print("Ativo nao encontrado.")
            except ValueError:
                print("Entrada invalida.")

        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opcao invalida.")


if __name__ == '__main__':
    menu()
