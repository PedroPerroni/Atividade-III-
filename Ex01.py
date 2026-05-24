import random

class Musica:
    def __init__(self, titulo, artista, genero, duracao):
        self.id = random.randint(1000, 9999)  
        self.titulo = titulo
        self.artista = artista
        self.genero = genero
        self.duracao = duracao                 
        self.reproducoes = 0                   

    def __str__(self):
        return (f"[ID:{self.id}] {self.titulo} - {self.artista} "
                f"| Gênero: {self.genero} | Duração: {self.duracao}s "
                f"| Reproduções: {self.reproducoes}")

class No:
    def __init__(self, musica):
        self.dado = musica     
        self.esq = None
        self.dir = None

class ABB:
    def __init__(self):
        self.raiz = None

    def inserir(self, musica):
        self.raiz = self._inserir(self.raiz, musica)

    def _inserir(self, no, musica):
        if no is None:
            return No(musica)
        if musica.id < no.dado.id:
            no.esq = self._inserir(no.esq, musica)
        elif musica.id > no.dado.id:
            no.dir = self._inserir(no.dir, musica)
        return no

    def buscar(self, id):
        return self._buscar(self.raiz, id)

    def _buscar(self, no, id):
        if no is None:
            return None
        if id == no.dado.id:
            return no.dado
        elif id < no.dado.id:
            return self._buscar(no.esq, id)
        else:
            return self._buscar(no.dir, id)

    def ouvir(self, id):
        musica = self.buscar(id)
        if musica:
            musica.reproducoes += 1
            return musica
        return None

    def remover(self, id):
        self.raiz = self._remover(self.raiz, id)

    def _remover(self, no, id):
        if no is None:
            return None

        if id < no.dado.id:
            no.esq = self._remover(no.esq, id)
        elif id > no.dado.id:
            no.dir = self._remover(no.dir, id)
        else:
            if no.esq is None and no.dir is None:
                return None
            if no.esq is None:
                return no.dir
            if no.dir is None:
                return no.esq
            sucessor = self._minimo(no.dir)
            no.dado = sucessor.dado
            no.dir = self._remover(no.dir, sucessor.dado.id)

        return no

    def _minimo(self, no):
        while no.esq is not None:
            no = no.esq
        return no

    def top5(self):
        todas = []
        self._em_ordem(self.raiz, todas)
        todas.sort(key=lambda m: m.reproducoes, reverse=True)
        return todas[:5]

    def por_genero(self, genero):
        resultado = []
        self._em_ordem_genero(self.raiz, genero.lower(), resultado)
        return resultado

    def _em_ordem_genero(self, no, genero, resultado):
        if no is None:
            return
        self._em_ordem_genero(no.esq, genero, resultado)
        if no.dado.genero.lower() == genero:
            resultado.append(no.dado)
        self._em_ordem_genero(no.dir, genero, resultado)

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
    arvore = ABB()

    while True:
        print("\n" + "=" * 50)
        print("      NovaSom 2157 - Nave Helios-9   ")
        print("=" * 50)
        print("a) Cadastrar música")
        print("b) Buscar por ID")
        print("c) Ouvir música")
        print("d) Remover música")
        print("e) Relatório Top-5")
        print("f) Relatório por gênero")
        print("0) Sair")
        print("-" * 50)
        opcao = input("Escolha: ").strip().lower()

        if opcao == 'a':
            titulo  = input("Título: ")
            artista = input("Artista: ")
            genero  = input("Gênero: ")
            duracao = int(input("Duração (segundos): "))
            musica = Musica(titulo, artista, genero, duracao)
            arvore.inserir(musica)
            print(f"Musica cadastrada com ID {musica.id}!")

        elif opcao == 'b':
            id = int(input("Digite o ID: "))
            musica = arvore.buscar(id)
            if musica:
                print(f"Encontrada: {musica}")
            else:
                print("Musica não encontrada.")

        elif opcao == 'c':
            id = int(input("Digite o ID da música para ouvir: "))
            musica = arvore.ouvir(id)
            if musica:
                print(f"Reproduzindo: {musica.titulo} - reproduções: {musica.reproducoes}")
            else:
                print("Musica não encontrada.")

        elif opcao == 'd':
            id = int(input("Digite o ID a remover: "))
            if arvore.buscar(id):
                arvore.remover(id)
                print(f"Musica {id} removida.")
            else:
                print("Musica não encontrada.")

        elif opcao == 'e':
            top = arvore.top5()
            if top:
                print("\nTop-5 mais ouvidas:")
                for i, m in enumerate(top, 1):
                    print(f"{i}. {m}")
            else:
                print("Nenhuma música cadastrada.")

        elif opcao == 'f':
            genero = input("Digite o gênero: ")
            lista = arvore.por_genero(genero)
            if lista:
                print(f"\nMúsicas do gênero '{genero}':")
                for m in lista:
                    print(f"{m}")
            else:
                print(f"Nenhuma música do gênero '{genero}' encontrada.")

        elif opcao == '0':
            print("Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    menu()
