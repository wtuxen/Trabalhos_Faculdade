class Pais():
    def __init__(self, codigo_iso, nome, dimensao_km2):
        self.codigo_iso = codigo_iso
        self.nome = nome
        self.populacao = 0
        self.dimensao_km2 = dimensao_km2
        self.fronteiras = []

    def get_codigo_iso(self):
        return self.codigo_iso

    def set_codigo_iso(self, codigo_iso):
        self.codigo_iso = codigo_iso

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_populacao(self):
        return self.populacao

    def set_populacao(self, populacao):
        self.populacao = populacao

    def get_dimensao_km2(self):
        return self.dimensao_km2

    def set_dimensao_km2(self, dimensao_km2):
        self.dimensao_km2 = dimensao_km2

    def e_igual(self, outro_pais):
        return self.codigo_iso == outro_pais.get_codigo_iso()
    
    def e_limite_com(self, outro_pais):
        return outro_pais in self.fronteiras
    
    def densidade_populacional(self):
        if self.populacao == 0:
            return 0
        return self.populacao / self.dimensao_km2
    
    def vizinhos_comuns(self, outro_pais):
        return [pais for pais in self.fronteiras if pais.e_limite_com(outro_pais)]


class Continente():
    def __init__(self, nome):
        self.nome = nome
        self.paises = []

    def adicionar_pais(self, pais):
        self.paises.append(pais)

    def dimensao_total(self):
        return sum(pais.get_dimensao_km2() for pais in self.paises)
    
    def populacao_total(self):
        return sum(pais.get_populacao() for pais in self.paises)
    
    def densidade_populacional(self):
        dimensao = self.dimensao_total()
        populacao = self.populacao_total()
        if dimensao == 0:
            return 0
        return populacao / dimensao

    def pais_maior_populacao(self):
        if not self.paises:
            return None
        return max(self.paises, key=lambda pais: pais.populacao)
    
    def pais_menor_populacao(self):
        if not self.paises:
            return None
        return min(self.paises, key=lambda pais: pais.populacao)
    
    def pais_maior_dimensao(self):
        if not self.paises:
            return None
        return max(self.paises, key=lambda pais: pais.dimensao_km2)
    
    def pais_menor_dimensao(self):
        if not self.paises:
            return None
        return min(self.paises, key=lambda pais: pais.dimensao_km2)

    def razao_territorial(self):
        maior_dimensao = self.pais_maior_dimensao().get_dimensao_km2()
        menor_dimensao = self.pais_menor_dimensao().get_dimensao_km2()
        if menor_dimensao == 0:
            return 0
        return maior_dimensao / menor_dimensao


america_do_sul = Continente("América do Sul")
brasil = Pais("BRA", "Brasil", 8515767)
argentina = Pais("ARG", "Argentina", 2780400)
uruguai = Pais("URY", "Uruguai", 176215)
paraguai = Pais("PRY", "Paraguai", 406752)
bolivia = Pais("BOL", "Bolívia", 1098581)

brasil.set_populacao(211000000)
argentina.set_populacao(45000000)
uruguai.set_populacao(3500000)
paraguai.set_populacao(7000000)
bolivia.set_populacao(11000000)

brasil.fronteiras = [argentina, uruguai, paraguai, bolivia]
argentina.fronteiras = [brasil, uruguai, paraguai, bolivia]
uruguai.fronteiras = [brasil, argentina]
paraguai.fronteiras = [brasil, argentina, bolivia]
bolivia.fronteiras = [brasil, argentina, paraguai]

america_do_sul.adicionar_pais(brasil)
america_do_sul.adicionar_pais(argentina)
america_do_sul.adicionar_pais(uruguai)

print("Densidade populacional do Brasil:", brasil.densidade_populacional())
print("Argentina e Brasil são limítrofes:", argentina.e_limite_com(brasil))
print("Vizinhos comuns entre Brasil e Argentina:", [pais.get_nome() for pais in brasil.vizinhos_comuns(argentina)])

print("Dimensão total da América do Sul:", america_do_sul.dimensao_total(), "km2")
print("População total da América do Sul:", america_do_sul.populacao_total())
print("Densidade populacional da América do Sul:", america_do_sul.densidade_populacional())
print("País com maior população na América do Sul:", america_do_sul.pais_maior_populacao().get_nome())
print("País com menor população na América do Sul:", america_do_sul.pais_menor_populacao().get_nome())
print("País de maior dimensão territorial na América do Sul:", america_do_sul.pais_maior_dimensao().get_nome())
print("País de menor dimensão territorial na América do Sul:", america_do_sul.pais_menor_dimensao().get_nome())
print("Razão territorial na América do Sul:", america_do_sul.razao_territorial())
