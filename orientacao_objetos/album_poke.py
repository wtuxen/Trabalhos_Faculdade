import csv
import os
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

class AlbumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Álbum de Figurinhas Pokémon")

        # Carregar dados
        self.usuarios, self.figurinhas, self.trocas = self.carregar_dados()

        # Atributo para armazenar o nome do usuário atual
        self.nome_usuario_atual = None

        # Interface
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack()

        self.label_username = tk.Label(self.frame_login, text="Nome de Usuário:")
        self.label_password = tk.Label(self.frame_login, text="Senha:")

        self.entry_username = tk.Entry(self.frame_login)
        self.entry_password = tk.Entry(self.frame_login, show="*")

        self.btn_login = tk.Button(self.frame_login, text="Login", command=self.login)
        self.btn_novo_album = tk.Button(self.frame_login, text="Novo Álbum", command=self.novo_album)

        # Posicionamento dos elementos
        self.label_username.grid(row=0, column=0, padx=5, pady=5)
        self.label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)
        self.btn_novo_album.grid(row=3, column=0, columnspan=2, pady=10)

    def carregar_dados(self):
        usuarios = []
        figurinhas = []
        trocas = []

        if os.path.exists("usuarios.csv"):
            with open("usuarios.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    usuarios.append(row)

        if os.path.exists("figurinhas.csv"):
            with open("figurinhas.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    figurinhas.append(row)

        if os.path.exists("trocas.csv"):
            with open("trocas.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    trocas.append(row)

        return usuarios, figurinhas, trocas

    def salvar_dados(self):
        with open("usuarios.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.usuarios)

        with open("figurinhas.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.figurinhas)

        with open("trocas.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.trocas)

    def novo_album(self):
        nome_usuario = simpledialog.askstring("Novo Álbum", "Digite seu nome de usuário:")
        senha = simpledialog.askstring("Novo Álbum", "Digite sua senha:")

        for usuario in self.usuarios:
            if usuario[0] == nome_usuario:
                messagebox.showinfo("Erro", "Usuário já existe. Tente novamente.")
                return

        self.usuarios.append([nome_usuario, senha, ""])
        messagebox.showinfo("Sucesso", f"Álbum criado com sucesso para o usuário {nome_usuario}!")

    def login(self):
        nome_usuario = self.entry_username.get()
        senha = self.entry_password.get()

        for usuario in self.usuarios:
            if usuario[0] == nome_usuario and usuario[1] == senha:
                # Definir o nome do usuário atual
                self.nome_usuario_atual = nome_usuario
                self.mostrar_album()
                return

        messagebox.showinfo("Erro", "Nome de usuário ou senha incorretos. Tente novamente.")

    def mostrar_album(self):
        self.frame_login.destroy()

        self.frame_album = tk.Frame(self.root)
        self.frame_album.pack()

        self.label_bem_vindo = tk.Label(self.frame_album, text=f"Bem-vindo ao álbum de {self.nome_usuario_atual}!")
        self.label_figurinhas = tk.Label(self.frame_album, text="Figurinhas no álbum:")

        album = self.usuarios[self.encontrar_indice_usuario(self.nome_usuario_atual)][2].split(",")
        self.label_figurinhas_detalhe = tk.Label(self.frame_album, text=", ".join(album))

        self.btn_abrir_pacote = tk.Button(self.frame_album, text="Abrir Pacote", command=self.abrir_pacote)
        self.btn_trocar_figurinhas = tk.Button(self.frame_album, text="Trocar Figurinhas", command=self.trocar_figurinhas)

        # Posicionamento dos elementos
        self.label_bem_vindo.grid(row=0, column=0, columnspan=2, pady=10)
        self.label_figurinhas.grid(row=1, column=0, pady=5)
        self.label_figurinhas_detalhe.grid(row=1, column=1, pady=5)
        self.btn_abrir_pacote.grid(row=2, column=0, pady=10)
        self.btn_trocar_figurinhas.grid(row=2, column=1, pady=10)

    def encontrar_indice_usuario(self, nome_usuario):
        for i, usuario in enumerate(self.usuarios):
            if usuario[0] == nome_usuario:
                return i

    def abrir_pacote(self):
        # Certifique-se de que o usuário tenha feito login
        if not self.nome_usuario_atual:
            messagebox.showinfo("Erro", "Faça login antes de abrir um pacote.")
            return

        # Código para abrir um pacote de figurinhas a partir do arquivo "pokemon.csv"
        # Você pode ajustar isso conforme sua necessidade
        pacote = self.abrir_pacote_pokemon()

        usuario_index = self.encontrar_indice_usuario(self.nome_usuario_atual)
        album = self.usuarios[usuario_index][2].split(",")

        for figurinha in pacote:
            if figurinha not in album:
                album.append(figurinha)

        self.usuarios[usuario_index][2] = ",".join(album)
        self.mostrar_album()

    def abrir_pacote_pokemon(self):
        # Código para abrir um pacote de figurinhas a partir do arquivo "pokemon.csv"
        # Você pode ajustar isso conforme sua necessidade
        pokemon = []
        path = r'F:trabalhos_faculdade\\orientacao_objetos\\album pokemon\\pokemon.csv'
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                pokemon.append(row[0])

        # Sortear 5 pokémons diferentes
        pacote = random.sample(pokemon, 5)
        return pacote

    def trocar_figurinhas(self):
        nome_usuario_destino = simpledialog.askstring("Troca de Figurinhas", "Digite o nome de usuário com quem deseja trocar:")

        if nome_usuario_destino not in [usuario[0] for usuario in self.usuarios]:
            messagebox.showinfo("Erro", "Nome de usuário inválido. Tente novamente.")
            return

        if nome_usuario_destino == self.nome_usuario_atual:
            messagebox.showinfo("Erro", "Não é possível trocar figurinhas com o mesmo usuário.")
            return

        # Verificar se ambos os usuários têm figurinhas para trocar
        indice_destino = self.encontrar_indice_usuario(nome_usuario_destino)

        if not self.usuarios[indice_destino][2]:
            messagebox.showinfo("Erro", f"{nome_usuario_destino} não tem figurinhas para trocar.")
            return

        # Escolher uma figurinha aleatória do usuário atual
        figurinha_origem = random.choice(self.usuarios[self.encontrar_indice_usuario(self.nome_usuario_atual)][2].split(","))
        # Escolher uma figurinha aleatória do usuário destino
        figurinha_destino = random.choice(self.usuarios[indice_destino][2].split(","))

        # Trocar as figurinhas
        self.usuarios[self.encontrar_indice_usuario(self.nome_usuario_atual)][2] = \
            self.usuarios[self.encontrar_indice_usuario(self.nome_usuario_atual)][2].replace(figurinha_origem, figurinha_destino)

        self.usuarios[indice_destino][2] = self.usuarios[indice_destino][2].replace(figurinha_destino, figurinha_origem)

        messagebox.showinfo("Sucesso", f"Troca realizada!\n{self.nome_usuario_atual} trocou {figurinha_origem} com {nome_usuario_destino} ({figurinha_destino})")

        # Atualizar a interface
        self.mostrar_album()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlbumApp(root)
    root.mainloop()
