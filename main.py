# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para ajuste linear
def linear_function(x, a, b):
    return a * x + b

def ajustar_e_plotar():
    try:
        # Obter os dados das entradas
        x_data = [float(entry.get()) for entry in entry_x_list]
        y_data = [float(entry.get()) for entry in entry_y_list]
        
        # Converter para arrays numpy
        x_data = np.array(x_data)
        y_data = np.array(y_data)
        
        # Ajuste da curva
        params, _ = curve_fit(linear_function, x_data, y_data)
        a, b = params
        
        # Mostrar os parâmetros ajustados
        result_text.set(f"Função ajustada: y = {a:.2f}x + {b:.2f}")
        
        # Plotar os dados e a função ajustada
        fig, ax = plt.subplots()
        ax.scatter(x_data, y_data, color='red', label='Dados')
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = linear_function(x_fit, *params)
        ax.plot(x_fit, y_fit, color='blue', label=f'Fit: $y = {a:.2f}x + {b:.2f}$')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.set_title('Ajuste de Curva Linear')
        
        # Limpar o canvas anterior
        for widget in plot_frame.winfo_children():
            widget.destroy()
        
        # Mostrar o gráfico na interface
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def add_entry():
    row = len(entry_x_list)
    
    label_par = tk.Label(input_frame, text=f"Par {row+1}:")
    label_par.grid(row=row, column=0, padx=5, pady=5, sticky='e')
    labels_list.append(label_par)
    
    entry_x = tk.Entry(input_frame, width=10)
    entry_x.grid(row=row, column=1, padx=5, pady=5)
    entry_x_list.append(entry_x)
    
    label_x = tk.Label(input_frame, text="x:")
    label_x.grid(row=row, column=2, padx=5, pady=5, sticky='e')
    labels_list.append(label_x)
    
    entry_y = tk.Entry(input_frame, width=10)
    entry_y.grid(row=row, column=3, padx=5, pady=5)
    entry_y_list.append(entry_y)
    
    label_y = tk.Label(input_frame, text="y:")
    label_y.grid(row=row, column=4, padx=5, pady=5, sticky='e')
    labels_list.append(label_y)

def remove_entry():
    if entry_x_list and entry_y_list:
        entry_x = entry_x_list.pop()
        entry_y = entry_y_list.pop()
        entry_x.destroy()
        entry_y.destroy()
        
        for _ in range(3):  # Remover três labels associados ao último par
            label = labels_list.pop()
            label.destroy()

# Criação da interface gráfica
root = tk.Tk()
root.title("Ajuste de Curva Linear")

# Configuração do layout
root.geometry("600x600")
root.resizable(False, False)

# Frame para as entradas de dados
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# Lista para armazenar as entradas e labels
entry_x_list = []
entry_y_list = []
labels_list = []

# Adicionar um par de entradas inicialmente
add_entry()

# Botões para adicionar/remover entradas
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Adicionar Par", command=add_entry, width=15).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Remover Par", command=remove_entry, width=15).pack(side=tk.LEFT, padx=5)

# Botão de ajuste e plotagem
tk.Button(root, text="Ajustar e Plotar", command=ajustar_e_plotar, width=20).pack(pady=10)

# Label para mostrar os resultados
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, font=('Arial', 12), fg='blue').pack(pady=10)

# Frame para o gráfico
plot_frame = tk.Frame(root)
plot_frame.pack(pady=20)

root.mainloop()
