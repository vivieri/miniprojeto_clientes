import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Criar banco
conexao = sqlite3.connect("clientes.db")
cursor = conexao.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefone TEXT
)
""")
conexao.commit()

def adicionar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    if nome and email:
        try:
            cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", (nome, email, telefone))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Cliente adicionado!")
            listar_clientes()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Esse e-mail já existe!")
    else:
        messagebox.showwarning("Aviso", "Nome e E-mail são obrigatórios!")

def listar_clientes():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM clientes")
    for cliente in cursor.fetchall():
        tree.insert("", "end", values=cliente)

def deletar_cliente():
    selecionado = tree.selection()
    if selecionado:
        id_cliente = tree.item(selecionado)["values"][0]
        cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
        conexao.commit()
        listar_clientes()
        messagebox.showinfo("Sucesso", "Cliente deletado!")

janela = tk.Tk()
janela.title("Cadastro de Clientes")

tk.Label(janela, text="Nome").grid(row=0, column=0)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1)

tk.Label(janela, text="Email").grid(row=1, column=0)
entry_email = tk.Entry(janela)
entry_email.grid(row=1, column=1)

tk.Label(janela, text="Telefone").grid(row=2, column=0)
entry_telefone = tk.Entry(janela)
entry_telefone.grid(row=2, column=1)

tk.Button(janela, text="Adicionar", command=adicionar_cliente).grid(row=3, column=0, pady=5)
tk.Button(janela, text="Deletar", command=deletar_cliente).grid(row=3, column=1, pady=5)

colunas = ("ID", "Nome", "Email", "Telefone")
tree = ttk.Treeview(janela, columns=colunas, show="headings")
for col in colunas:
    tree.heading(col, text=col)
tree.grid(row=4, column=0, columnspan=2)

listar_clientes()

janela.mainloop()