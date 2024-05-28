import tkinter as tk
from tkinter import messagebox
import requests

class ConcessionariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Concessionária")
        self.create_choice_widgets()

    def create_choice_widgets(self):
        self.clear_widgets()
        self.choice_label = tk.Label(self.root, text="Escolha seu perfil:")
        self.choice_label.pack()

        self.comprador_button = tk.Button(self.root, text="Comprador", command=self.create_comprador_widgets)
        self.comprador_button.pack()

        self.vendedor_button = tk.Button(self.root, text="Vendedor", command=self.create_vendedor_widgets)
        self.vendedor_button.pack()

    def create_comprador_widgets(self):
        self.clear_widgets()
        self.carros_listbox = tk.Listbox(self.root)
        self.carros_listbox.pack()

        self.cliente_nome_entry = tk.Entry(self.root)
        self.cliente_nome_entry.pack()
        self.cliente_nome_entry.insert(0, "Nome do Cliente")

        self.registrar_venda_button = tk.Button(self.root, text="Registrar Venda", command=self.registrar_venda)
        self.registrar_venda_button.pack()

        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.create_choice_widgets)
        self.voltar_button.pack()

        self.listar_carros()

    def create_vendedor_widgets(self):
        self.clear_widgets()
        tk.Label(self.root, text="Marca:").pack()
        self.marca_entry = tk.Entry(self.root)
        self.marca_entry.pack()

        tk.Label(self.root, text="Modelo:").pack()
        self.modelo_entry = tk.Entry(self.root)
        self.modelo_entry.pack()

        tk.Label(self.root, text="Ano:").pack()
        self.ano_entry = tk.Entry(self.root)
        self.ano_entry.pack()

        tk.Label(self.root, text="Preço:").pack()
        self.preco_entry = tk.Entry(self.root)
        self.preco_entry.pack()

        tk.Label(self.root, text="Cor:").pack()
        self.cor_entry = tk.Entry(self.root)
        self.cor_entry.pack()

        self.cadastrar_carro_button = tk.Button(self.root, text="Cadastrar Carro", command=self.cadastrar_carro)
        self.cadastrar_carro_button.pack()

        self.voltar_button = tk.Button(self.root, text="Voltar", command=self.create_choice_widgets)
        self.voltar_button.pack()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def listar_carros(self):
        response = requests.get("http://localhost:8000/carros/")
        if response.status_code == 200:
            carros = response.json()
            for carro in carros:
                self.carros_listbox.insert(tk.END, f"{carro['id']} - {carro['marca']} {carro['modelo']} ({carro['ano']}) - {carro['cor']} - R${carro['preco']}")
        else:
            messagebox.showerror("Erro", "Não foi possível listar os carros")

    def registrar_venda(self):
        selected_car = self.carros_listbox.get(tk.ACTIVE)
        if not selected_car:
            messagebox.showwarning("Atenção", "Selecione um carro")
            return

        carro_id = selected_car.split(' - ')[0]
        cliente_nome = self.cliente_nome_entry.get()
        if not cliente_nome or cliente_nome == "Nome do Cliente":
            messagebox.showwarning("Atenção", "Insira o nome do cliente")
            return

        data = {'carro_id': carro_id, 'cliente_nome': cliente_nome}
        response = requests.post("http://localhost:8000/registrar_venda/", data=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso")
        else:
            messagebox.showerror("Erro", "Não foi possível registrar a venda")

    def cadastrar_carro(self):
        marca = self.marca_entry.get()
        modelo = self.modelo_entry.get()
        ano = self.ano_entry.get()
        preco = self.preco_entry.get()
        cor = self.cor_entry.get()

        if not marca or not modelo or not ano or not preco or not cor:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        data = {'marca': marca, 'modelo': modelo, 'ano': ano, 'preco': preco, 'cor': cor}
        response = requests.post("http://localhost:8000/cadastrar_carro/", data=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Carro cadastrado com sucesso")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o carro")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConcessionariaApp(root)
    root.mainloop()
