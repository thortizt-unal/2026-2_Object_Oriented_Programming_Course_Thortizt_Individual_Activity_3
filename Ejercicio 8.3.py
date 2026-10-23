import math
import os
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------
#  JERARQUIA DE CLASES: FiguraGeometrica (padre) y sus hijas
# ---------------------------------------------------------------
class FiguraGeometrica:

    def calcular_volumen(self) -> float:
        # Cada figura hija reescribe este metodo con su propia formula
        raise NotImplementedError("La figura hija debe definir el volumen")

    def calcular_superficie(self) -> float:
        # Cada figura hija reescribe este metodo con su propia formula
        raise NotImplementedError("La figura hija debe definir la superficie")


class Cilindro(FiguraGeometrica):
    NOMBRE = "Cilindro"
    IMAGEN = "cilindro.png"
    DATOS = ["Radio (cm):", "Altura (cm):"]  # Datos que pide la figura

    def __init__(self, radio: float, altura: float):
        self._radio = radio
        self._altura = altura

    def calcular_volumen(self) -> float:
        return math.pi * self._radio ** 2 * self._altura

    def calcular_superficie(self) -> float:
        return 2 * math.pi * self._radio * (self._radio + self._altura)


class Esfera(FiguraGeometrica):
    NOMBRE = "Esfera"
    IMAGEN = "esfera.png"
    DATOS = ["Radio (cm):"]

    def __init__(self, radio: float):
        self._radio = radio

    def calcular_volumen(self) -> float:
        return (4 / 3) * math.pi * self._radio ** 3

    def calcular_superficie(self) -> float:
        return 4 * math.pi * self._radio ** 2


class Piramide(FiguraGeometrica):
    # Se asume una piramide de base cuadrada: "base" es el lado del cuadrado
    NOMBRE = "Piramide"
    IMAGEN = "piramide.png"
    DATOS = ["Base (cm):", "Altura (cm):", "Apotema (cm):"]

    def __init__(self, base: float, altura: float, apotema: float):
        self._base = base
        self._altura = altura
        self._apotema = apotema

    def calcular_volumen(self) -> float:
        return (self._base ** 2 * self._altura) / 3

    # Superficie = area de la base + 4 triangulos laterales
    def calcular_superficie(self) -> float:
        return self._base ** 2 + 2 * self._base * self._apotema


class Cubo(FiguraGeometrica):
    NOMBRE = "Cubo"
    IMAGEN = "cubo.png"
    DATOS = ["Lado (cm):"]

    def __init__(self, lado: float):
        self._lado = lado

    def calcular_volumen(self) -> float:
        return self._lado ** 3

    def calcular_superficie(self) -> float:
        return 6 * self._lado ** 2


class Prisma(FiguraGeometrica):
    # Se asume un prisma rectangular (con largo, ancho y altura)
    NOMBRE = "Prisma"
    IMAGEN = "prisma.png"
    DATOS = ["Largo (cm):", "Ancho (cm):", "Altura (cm):"]

    def __init__(self, largo: float, ancho: float, altura: float):
        self._largo = largo
        self._ancho = ancho
        self._altura = altura

    def calcular_volumen(self) -> float:
        return self._largo * self._ancho * self._altura

    def calcular_superficie(self) -> float:
        return 2 * (self._largo * self._ancho
                    + self._largo * self._altura
                    + self._ancho * self._altura)


# ---------------------------------------------------------------
#  INTERFAZ GRAFICA
# ---------------------------------------------------------------
class VentanaPrincipal(tk.Tk):

    # Lista con las figuras disponibles
    FIGURAS = [Cilindro, Esfera, Piramide, Cubo, Prisma]

    # Tamano maximo de la imagen en pixeles (cambia estos numeros si la quieres mas grande o mas chica)
    ANCHO_MAXIMO = 150
    ALTO_MAXIMO = 150

    def __init__(self):
        super().__init__()
        self.title("Figuras geometricas")
        self.geometry("340x450")
        self.resizable(False, False)
        self.foto = None                     # Guarda la imagen (si no, tkinter la borra)
        self.crear_componentes()
        self.cambiar_figura()                # Muestra la primera figura al abrir

    def crear_componentes(self):
        # Lista desplegable para elegir la figura
        tk.Label(self, text="Figura:").place(x=20, y=20)
        nombres = [figura.NOMBRE for figura in self.FIGURAS]
        self.lista = ttk.Combobox(self, values=nombres, state="readonly")
        self.lista.current(0)
        self.lista.place(x=100, y=20, width=200)
        # LISTENER: cuando el usuario elige otra figura se llama a cambiar_figura
        self.lista.bind("<<ComboboxSelected>>", self.cambiar_figura)

        # 3 filas de etiqueta + campo (se usan solo las que pida la figura)
        self.etiquetas = []
        self.campos = []
        for i in range(3):
            etiqueta = tk.Label(self, text="")
            etiqueta.place(x=20, y=60 + i * 30)
            campo = tk.Entry(self)
            campo.place(x=130, y=60 + i * 30, width=170)
            self.etiquetas.append(etiqueta)
            self.campos.append(campo)

        # LISTENERS de los botones: command indica que metodo se ejecuta al hacer clic
        tk.Button(self, text="Calcular", command=self.clic_calcular).place(
            x=20, y=165, width=130, height=28)
        tk.Button(self, text="Limpiar", command=self.clic_limpiar).place(
            x=170, y=165, width=130, height=28)

        # Resultados
        self.etiqueta_volumen = tk.Label(self, text="Volumen = ")
        self.etiqueta_volumen.place(x=20, y=210)
        self.etiqueta_superficie = tk.Label(self, text="Superficie = ")
        self.etiqueta_superficie.place(x=20, y=240)

        # Aqui se muestra la imagen de la figura (ocupa el tamano maximo)
        self.etiqueta_imagen = tk.Label(self, text="")
        self.etiqueta_imagen.place(x=20, y=280, width=300, height=self.ALTO_MAXIMO)

    # Se ejecuta al abrir la ventana y cada vez que se cambia la figura
    def cambiar_figura(self, evento=None):
        figura = self.FIGURAS[self.lista.current()]

        # Muestra solo las filas que necesita la figura elegida
        for i in range(3):
            if i < len(figura.DATOS):
                self.etiquetas[i].config(text=figura.DATOS[i])
                self.etiquetas[i].place(x=20, y=60 + i * 30)
                self.campos[i].place(x=130, y=60 + i * 30, width=170)
            else:
                self.etiquetas[i].place_forget()     # Oculta lo que sobra
                self.campos[i].place_forget()

        self.clic_limpiar()
        self.mostrar_imagen(figura.IMAGEN)

    # Carga y muestra la imagen. La busca en la carpeta "Imagenes",
    # que esta al lado de este archivo
    def mostrar_imagen(self, nombre_imagen: str):
        carpeta = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(carpeta, "Imagenes", nombre_imagen)
        try:
            foto = tk.PhotoImage(file=ruta)

            # Si la imagen es mas grande que el maximo, se reduce.
            # subsample(n) toma 1 de cada n pixeles, asi que n debe ser entero
            factor = max(math.ceil(foto.width() / self.ANCHO_MAXIMO),
                         math.ceil(foto.height() / self.ALTO_MAXIMO))
            if factor > 1:
                foto = foto.subsample(factor)

            self.foto = foto
            self.etiqueta_imagen.config(image=self.foto, text="")
        except tk.TclError:
            # Si todavia no esta la imagen, avisa pero el programa sigue funcionando
            self.foto = None
            self.etiqueta_imagen.config(image="", text="(Falta la imagen " + nombre_imagen + ")")

    # Convierte el texto de un campo a numero. Es static porque no usa self
    @staticmethod
    def convertir_a_numero(texto: str) -> float:
        numero = float(texto.replace(",", "."))      # Acepta coma o punto decimal
        if numero <= 0 or not math.isfinite(numero):
            raise ValueError("El numero debe ser mayor que cero")
        return numero

    def clic_calcular(self):
        figura = self.FIGURAS[self.lista.current()]

        # Lee y valida cada dato
        valores = []
        for i in range(len(figura.DATOS)):
            try:
                valores.append(self.convertir_a_numero(self.campos[i].get()))
            except ValueError:
                messagebox.showerror(
                    "Error", "El dato '" + figura.DATOS[i] + "' debe ser un numero mayor que cero.")
                return

        # Crea la figura con los datos (el * reparte la lista en los parametros)
        objeto = figura(*valores)

        self.etiqueta_volumen.config(text=f"Volumen = {objeto.calcular_volumen():.2f} cm³")
        self.etiqueta_superficie.config(text=f"Superficie = {objeto.calcular_superficie():.2f} cm²")

    def clic_limpiar(self):
        for campo in self.campos:
            campo.delete(0, tk.END)
        self.etiqueta_volumen.config(text="Volumen = ")
        self.etiqueta_superficie.config(text="Superficie = ")


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()