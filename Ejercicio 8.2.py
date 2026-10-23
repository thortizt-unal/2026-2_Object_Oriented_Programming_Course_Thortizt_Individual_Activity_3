import math
import tkinter as tk
from tkinter import messagebox


class Notas:
  """Clase que define un array de notas numéricas y sus operaciones."""

  def __init__(self):
    # Crea una lista de 5 notas inicializadas en 0
    self.listaNotas = [0.0, 0.0, 0.0, 0.0, 0.0]

  def calcularPromedio(self):
    suma = 0
    for i in range(len(self.listaNotas)):
      suma = suma + self.listaNotas[i]
    return suma / len(self.listaNotas)

  def calcularDesviacion(self):
    prom = self.calcularPromedio()
    suma = 0
    for i in range(len(self.listaNotas)):
      suma = suma + ((self.listaNotas[i] - prom) ** 2)
    return math.sqrt(suma / len(self.listaNotas))

  def calcularMenor(self):
    menor = self.listaNotas[0]
    for i in range(len(self.listaNotas)):
      if self.listaNotas[i] < menor:
        menor = self.listaNotas[i]
    return menor

  def calcularMayor(self):
    mayor = self.listaNotas[0]
    for i in range(len(self.listaNotas)):
      if self.listaNotas[i] > mayor:
        mayor = self.listaNotas[i]
    return mayor


class VentanaPrincipal(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("Notas")
    self.geometry("280x380")
    self.resizable(False, False)
    self.inicio()

  def inicio(self):
    # Etiquetas y campos de texto para cada nota
    self.nota1 = tk.Label(self, text="Nota 1:")
    self.nota1.place(x=20, y=20, width=80, height=23)
    self.campoNota1 = tk.Entry(self)
    self.campoNota1.place(x=105, y=20, width=135, height=23)

    self.nota2 = tk.Label(self, text="Nota 2:")
    self.nota2.place(x=20, y=50, width=80, height=23)
    self.campoNota2 = tk.Entry(self)
    self.campoNota2.place(x=105, y=50, width=135, height=23)

    self.nota3 = tk.Label(self, text="Nota 3:")
    self.nota3.place(x=20, y=80, width=80, height=23)
    self.campoNota3 = tk.Entry(self)
    self.campoNota3.place(x=105, y=80, width=135, height=23)

    self.nota4 = tk.Label(self, text="Nota 4:")
    self.nota4.place(x=20, y=110, width=80, height=23)
    self.campoNota4 = tk.Entry(self)
    self.campoNota4.place(x=105, y=110, width=135, height=23)

    self.nota5 = tk.Label(self, text="Nota 5:")
    self.nota5.place(x=20, y=140, width=80, height=23)
    self.campoNota5 = tk.Entry(self)
    self.campoNota5.place(x=105, y=140, width=135, height=23)

    # Botones Calcular y Limpiar
    self.calcular = tk.Button(self, text="Calcular", command=self.clicCalcular)
    self.calcular.place(x=20, y=170, width=90, height=25)

    self.limpiar = tk.Button(self, text="Limpiar", command=self.clicLimpiar)
    self.limpiar.place(x=120, y=170, width=80, height=25)

    # Etiquetas de resultados inferiores
    self.promedio = tk.Label(self, text="Promedio = ")
    self.promedio.place(x=20, y=210, width=230, height=23)

    self.desviación = tk.Label(self, text="Desviación = ")
    self.desviación.place(x=20, y=240, width=230, height=23)

    self.mayor = tk.Label(self, text="Nota mayor = ")
    self.mayor.place(x=20, y=270, width=230, height=23)

    self.menor = tk.Label(self, text="Nota menor = ")
    self.menor.place(x=20, y=300, width=230, height=23)

  def clicCalcular(self):
    campos = [
        self.campoNota1,
        self.campoNota2,
        self.campoNota3,
        self.campoNota4,
        self.campoNota5,
    ]
    valores = []

    # Validaciones obligatorias (campos vacíos y datos no numéricos)
    for i in range(len(campos)):
      texto = campos[i].get().strip()

      if texto == "":
        messagebox.showerror(
            "Error", f"La Nota {i+1} no ha sido ingresada. Es obligatorio."
        )
        return

      try:
        numero = float(texto)
        valores.append(numero)
      except ValueError:
        messagebox.showerror(
            "Error",
            f"El valor de la Nota {i+1} ('{texto}') no es un número válido.",
        )
        return

    # Creamos el objeto de la clase Notas
    misNotas = Notas()
    misNotas.listaNotas[0] = valores[0]
    misNotas.listaNotas[1] = valores[1]
    misNotas.listaNotas[2] = valores[2]
    misNotas.listaNotas[3] = valores[3]
    misNotas.listaNotas[4] = valores[4]

    # Realizamos los cálculos y mostramos en las etiquetas (SIN tilde en calcularDesviacion)
    prom = misNotas.calcularPromedio()
    desv = misNotas.calcularDesviacion()
    may = misNotas.calcularMayor()
    men = misNotas.calcularMenor()

    self.promedio.config(text=f"Promedio = {prom:.2f}")
    self.desviación.config(text=f"Desviación = {desv:.2f}")
    self.mayor.config(text=f"Nota mayor = {may}")
    self.menor.config(text=f"Nota menor = {men}")

  def clicLimpiar(self):
    self.campoNota1.delete(0, tk.END)
    self.campoNota2.delete(0, tk.END)
    self.campoNota3.delete(0, tk.END)
    self.campoNota4.delete(0, tk.END)
    self.campoNota5.delete(0, tk.END)

    self.promedio.config(text="Promedio = ")
    self.desviación.config(text="Desviación Estandar = ")
    self.mayor.config(text="Nota mayor = ")
    self.menor.config(text="Nota menor = ")


if __name__ == "__main__":
  app = VentanaPrincipal()
  app.mainloop()