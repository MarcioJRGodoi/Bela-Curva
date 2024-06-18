import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics import r2_score

class AplicacaoAjusteCurva(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Ajuste de Curva - Exponencial, Logarítmico, Polinômio 1º ou 2º Grau')

        # Variáveis para os inputs de X e Y
        self.label_x = tk.Label(self, text='Valores de X (separados por vírgula):')
        self.label_x.pack()
        self.entry_x = tk.Entry(self, width=50)
        self.entry_x.pack()

        self.label_y = tk.Label(self, text='Valores de Y (separados por vírgula):')
        self.label_y.pack()
        self.entry_y = tk.Entry(self, width=50)
        self.entry_y.pack()

        # Botão para executar o ajuste e mostrar o gráfico
        self.button_ajustar = tk.Button(self, text='Ajustar e Mostrar Gráfico', command=self.ajustar_e_mostrar, bg='blue', fg='white', font=('Arial', 12, 'bold'))
        self.button_ajustar.pack()

        # Frame para exibir o gráfico
        self.frame_grafico = tk.Frame(self, bg='white', bd=2, relief=tk.SUNKEN)
        self.frame_grafico.pack(padx=10, pady=10)

        # Entry para mostrar a função ajustada
        self.label_funcao = tk.Label(self, text='Função Ajustada:', font=('Arial', 12, 'bold'))
        self.label_funcao.pack()
        self.entry_funcao = tk.Entry(self, width=70, state='readonly')
        self.entry_funcao.pack()

    def ajustar_e_mostrar(self):
        # Obter valores de X e Y dos inputs
        try:
            x = list(map(float, self.entry_x.get().strip().split(',')))
            y = list(map(float, self.entry_y.get().strip().split(',')))

            if len(x) != len(y):
                messagebox.showerror('Erro', 'O número de valores em X e Y deve ser o mesmo.')
                return
        except ValueError:
            messagebox.showerror('Erro', 'Certifique-se de inserir valores numéricos separados por vírgula.')
            return

        # Identificar tipo de ajuste e obter coeficientes
        tipo_funcao, coeficientes = self.identificar_tipo_ajuste(x, y)

        # Verificar se a melhor lei encontrada é válida (exponencial, logarítmica, polinômio 1º ou 2º grau)
        if tipo_funcao not in ['exponencial', 'logaritmico', 'polinomio_1', 'polinomio_2']:
            messagebox.showerror('Erro', 'A melhor lei de ajuste encontrada não é válida.')
            return

        # Limpar frame anterior do gráfico
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Plotar gráfico com ajuste de curva
        self.plotar_grafico(x, y, tipo_funcao, coeficientes)

        # Atualizar Entry com a função ajustada
        if tipo_funcao == 'exponencial':
            a, b = coeficientes
            funcao_ajustada = f'y = {a:.2f} * exp({b:.2f} * x)'
        elif tipo_funcao == 'logaritmico':
            a, b = coeficientes
            funcao_ajustada = f'y = {a:.2f} * ln(x) + {b:.2f}'
        elif tipo_funcao == 'polinomio_1':
            a, b = coeficientes
            funcao_ajustada = f'y = {a:.2f} * x + {b:.2f}'
        elif tipo_funcao == 'polinomio_2':
            a, b, c = coeficientes
            funcao_ajustada = f'y = {a:.2f} * x^2 + {b:.2f} * x + {c:.2f}'

        self.entry_funcao.config(state='normal')
        self.entry_funcao.delete(0, tk.END)
        self.entry_funcao.insert(0, funcao_ajustada)
        self.entry_funcao.config(state='readonly')

    def identificar_tipo_ajuste(self, x, y):
        # Ajuste exponencial
        def ajuste_exponencial(x, y):
            log_y = np.log(y)
            b, a_log = np.polyfit(x, log_y, 1)
            a = np.exp(a_log)
            return a, b

        # Ajuste logarítmico
        def ajuste_logaritmico(x, y):
            log_x = np.log(x)
            a, b = np.polyfit(log_x, y, 1)
            return a, b

        # Ajuste polinômio de 1º grau
        def ajuste_polinomio_1(x, y):
            a, b = np.polyfit(x, y, 1)
            return a, b

        # Ajuste polinômio de 2º grau
        def ajuste_polinomio_2(x, y):
            a, b, c = np.polyfit(x, y, 2)
            return a, b, c

        # Verificar qual ajuste tem melhor coeficiente de determinação (R^2)
        # Ajuste exponencial
        a_exp, b_exp = ajuste_exponencial(x, y)
        y_exp_fit = a_exp * np.exp(b_exp * np.array(x))
        r2_exp = r2_score(y, y_exp_fit)

        # Ajuste logarítmico
        a_log, b_log = ajuste_logaritmico(x, y)
        y_log_fit = a_log * np.log(np.array(x)) + b_log
        r2_log = r2_score(y, y_log_fit)

        # Ajuste polinômio de 1º grau
        a_poly1, b_poly1 = ajuste_polinomio_1(x, y)
        y_poly1_fit = a_poly1 * np.array(x) + b_poly1
        r2_poly1 = r2_score(y, y_poly1_fit)

        # Ajuste polinômio de 2º grau
        a_poly2, b_poly2, c_poly2 = ajuste_polinomio_2(x, y)
        y_poly2_fit = a_poly2 * np.array(x)**2 + b_poly2 * np.array(x) + c_poly2
        r2_poly2 = r2_score(y, y_poly2_fit)

        # Determinar o tipo de ajuste com melhor R²
        r2_values = {
            'exponencial': r2_exp,
            'logaritmico': r2_log,
            'polinomio_1': r2_poly1,
            'polinomio_2': r2_poly2
        }

        melhor_ajuste = max(r2_values, key=r2_values.get)

        # Verificar se é uma das opções válidas
        if melhor_ajuste not in ['exponencial', 'logaritmico', 'polinomio_1', 'polinomio_2']:
            raise ValueError("Nenhum ajuste válido encontrado.")

        if melhor_ajuste == 'exponencial':
            return 'exponencial', ajuste_exponencial(x, y)
        elif melhor_ajuste == 'logaritmico':
            return 'logaritmico', ajuste_logaritmico(x, y)
        elif melhor_ajuste == 'polinomio_1':
            return 'polinomio_1', ajuste_polinomio_1(x, y)
        elif melhor_ajuste == 'polinomio_2':
            return 'polinomio_2', ajuste_polinomio_2(x, y)

    def plotar_grafico(self, x, y, tipo_funcao, coeficientes):
        # Configurar plot
        fig = plt.figure(figsize=(8, 6), facecolor='white')
        ax = fig.add_subplot(111)

        # Scatter plot dos dados
        ax.scatter(x, y, color='blue', label='Pontos (X, Y)')

        # Calcular a linha da função ajustada
        if tipo_funcao == 'exponencial':
            a, b = coeficientes
            x_fit = np.linspace(min(x), max(x), 500)
            y_fit = a * np.exp(b * x_fit)
            ax.plot(x_fit, y_fit, color='red', label=f'Ajuste Exponencial: y = {a:.2f} * exp({b:.2f} * x)', linewidth=2)
            x_infinito = np.linspace(min(x) - 1, max(x) + 1, 500)
            y_infinito = a * np.exp(b * x_infinito)
            ax.plot(x_infinito, y_infinito, '--', color='red', alpha=0.5, linewidth=1)

        elif tipo_funcao == 'logaritmico':
            a, b = coeficientes
            x_fit = np.linspace(min(x), max(x), 500)
            y_fit = a * np.log(x_fit) + b
            ax.plot(x_fit, y_fit, color='green', label=f'Ajuste Logarítmico: y = {a:.2f} * ln(x) + {b:.2f}', linewidth=2)
            x_infinito = np.linspace(min(x) - 1, max(x) + 1, 500)
            y_infinito = a * np.log(x_infinito) + b
            ax.plot(x_infinito, y_infinito, '--', color='green', alpha=0.5, linewidth=1)

        elif tipo_funcao == 'polinomio_1':
            a, b = coeficientes
            x_fit = np.linspace(min(x), max(x), 500)
            y_fit = a * x_fit + b
            ax.plot(x_fit, y_fit, color='purple', label=f'Ajuste Polinomial 1º Grau: y = {a:.2f} * x + {b:.2f}', linewidth=2)
            x_infinito = np.linspace(min(x) - 1, max(x) + 1, 500)
            y_infinito = a * x_infinito + b
            ax.plot(x_infinito, y_infinito, '--', color='purple', alpha=0.5, linewidth=1)

        elif tipo_funcao == 'polinomio_2':
            a, b, c = coeficientes
            x_fit = np.linspace(min(x), max(x), 500)
            y_fit = a * x_fit**2 + b * x_fit + c
            ax.plot(x_fit, y_fit, color='orange', label=f'Ajuste Polinomial 2º Grau: y = {a:.2f} * x^2 + {b:.2f} * x + {c:.2f}', linewidth=2)
            x_infinito = np.linspace(min(x) - 1, max(x) + 1, 500)
            y_infinito = a * x_infinito**2 + b * x_infinito + c
            ax.plot(x_infinito, y_infinito, '--', color='orange', alpha=0.5, linewidth=1)

        ax.set_title('Ajuste de Curva Exponencial, Logarítmico, Polinômio 1º ou 2º Grau', fontsize=14)
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Embed plot na GUI
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Iniciar a aplicação
if __name__ == "__main__":
    app = AplicacaoAjusteCurva()
    app.mainloop()


       
