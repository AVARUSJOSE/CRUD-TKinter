"""importamos tkinter"""

from tkinter import *
from tkinter import ttk
import sqlite3


class Articulo:
    """clase que representara toda mi app  de escritorio"""

    db_nombre = "uso_tienda.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title("Inventario uso_tienda")

        # container LableFrame
        frame = LabelFrame(self.wind, text="Registra un nuevo articulo")
        frame.grid(row=0, column=0, columnspan=4, pady=20)

        # entrada numero de material
        Label(frame, text="Material: ").grid(row=1, column=0)
        self.material = Entry(frame)
        self.material.focus()
        self.material.grid(row=1, column=1)

        # entrada nombre de articulo

        Label(frame, text="Descripcion: ").grid(row=2, column=0)
        self.descripion = Entry(frame)
        self.descripion.grid(row=2, column=1)

        # entrada referencia articulo

        Label(frame, text="Referencia: ").grid(row=3, column=0)
        self.referencia = Entry(frame)
        self.referencia.grid(row=3, column=1)

        # entrada cantidad de articulo

        Label(frame, text="Cantidad: ").grid(row=4, column=0)
        self.cantidad = Entry(frame)
        self.cantidad.grid(row=4, column=1)

        # boton para agregar articulo

        ttk.Button(frame, text="Guardar Articulo", command=self.agregar_articulos).grid(
            row=5, columnspan=2, sticky=W + E)

        # mensaje despues del boton

        self.message = Label(frame, text="", fg="red")
        self.message.grid(row=6, column=0, columnspan=2, sticky=W + E)

        # tabla

        self.tree = ttk.Treeview(columns=('#1', '#2', '#3'))
        self.tree.grid(row=6, column=0, columnspan=2)
        self.tree.heading("#0", text="Material", anchor=CENTER)
        self.tree.heading("#1", text="Descripcion", anchor=CENTER)
        self.tree.heading("#2", text="Referencia", anchor=CENTER)
        self.tree.heading("#3", text="Cantidad", anchor=CENTER)

        # botones de actualizar y eliminar arcticulo

        ttk.Button(text="Borrar", command=self.eliminar_articulo).grid(
            row=7, column=0, sticky=W + E,)
        ttk.Button(text="Editar", command=self.actualizar_articulo).grid(
            row=7, column=1, sticky=W + E)
        ttk.Button(text="Hacer Nota").grid(row=8, column=0, sticky=W+E)
        ttk.Button(text="Salir").grid(row=8, column=1, sticky=W+E)

        # llenando filas de la tabla
        self.tomar_articulos()

    def consulta_db(self, query, parametros=()):
        """funcion para consutar a la base de datos"""
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
        return resultado

    def tomar_articulos(self):
        """funcion para ejecutar la consulta"""
        # limpiamos la tabla creada
        records = self.tree.get_children()
        for elemento in records:
            self.tree.delete(elemento)
        # consultamos datos
        query = "SELECT * FROM Inventario ORDER BY Descripcion DESC"
        resultados = self.consulta_db(query)
        # rellenando datos
        for row in resultados:
            self.tree.insert('', 0, text=row[0], values=(
                row[1], row[2], row[3], ...))

    # funcion para validar si la longitud de la entrada en diferente de 0
    def validacion(self):
        """validacion"""
        return len(self.material.get()) != 0 and len(self.descripion.get()) != 0 and len(self.referencia.get()) != 0 and len(self.cantidad.get()) != 0

    # funcion para agregar articulos
    def agregar_articulos(self):
        """funcion para agregar articulo nuevo"""
        if self.validacion() is True:
            query = "INSERT INTO Inventario VALUES (?, ?, ?, ?)"
            parametros = (self.material.get(), self.descripion.get(),
                          self.referencia.get(), self.cantidad.get())
            self.consulta_db(query, parametros)
            self.message["text"] = f"""El articulo {
                self.descripion.get()} ha sido guardado satisfactoriamente"""
            self.material.delete(0, END)
            self.descripion.delete(0, END)
            self.referencia.delete(0, END)
            self.cantidad.delete(0, END)
        else:
            self.message["text"] = "Se necesita rellenar todos los campos"

        self.tomar_articulos()

    # funcion para eliminar articulo

    def eliminar_articulo(self):
        """funcion que elimina articulo seleccionado"""
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona un registro"
            return
        self.message["text"] = ""
        descripcion1 = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM Inventario WHERE Material = ?"
        self.consulta_db(query, (descripcion1, ))
        self.message["text"] = f"""El articulo {
            descripcion1} ha sido eliminado satisfactoriamente"""
        self.tomar_articulos()

    def actualizar_articulo(self):
        """funcion para actualizar losa articulos"""
        self.message["text"] = ""  # {Barra Grande} HR4C 74 Ellipsis
        try:
            self.tree.item(self.tree.selection())["text"]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona un registro"
            return
        material = self.tree.item(self.tree.selection())["text"]  # material
        descripcion = self.tree.item(self.tree.selection())[
            "values"][0]  # descripcion
        referencia = self.tree.item(self.tree.selection())[
            "values"][1]  # referencia
        cantidad = self.tree.item(self.tree.selection())[
            "values"][2]  # cantidad
        self.ventana_editar = Toplevel()
        self.ventana_editar.title = "Editar articulo"

        # datos material viejos row 0
        Label(self.ventana_editar, text="Material a editar: ").grid(
            row=0, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=material), state="readonly").grid(row=0, column=2)
        # datos material nuevos row 1
        Label(self.ventana_editar, text="Material nuevo: ").grid(row=1, column=1)
        nuevo_material = Entry(self.ventana_editar)
        nuevo_material.grid(row=1, column=2)

        # datos descripcion viejos row 2
        Label(self.ventana_editar, text="Descripcion a editar: ").grid(
            row=2, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=descripcion), state="readonly").grid(row=2, column=2)
        # datos descripcion nuevos row 3
        Label(self.ventana_editar, text="Descripción nueva: ").grid(
            row=3, column=1)
        nueva_descripcion = Entry(self.ventana_editar)
        nueva_descripcion.grid(row=3, column=2)

        # datos referencia vieja row 4
        Label(self.ventana_editar, text="Referencia a editar: ").grid(
            row=4, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=referencia), state="readonly").grid(row=4, column=2)
        # datos descripcion nuevos row 5
        Label(self.ventana_editar, text="Referencia nueva: ").grid(
            row=5, column=1)
        nueva_referencia = Entry(self.ventana_editar)
        nueva_referencia.grid(row=5, column=2)

        # datos referencia vieja row 6
        Label(self.ventana_editar, text="Cantidad a editar: ").grid(
            row=6, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(
            self.ventana_editar, value=cantidad), state="readonly").grid(row=6, column=2)
        # datos descripcion nuevos row 7
        Label(self.ventana_editar, text="Cantidad nueva: ").grid(row=7, column=1)
        nueva_cantidad = Entry(self.ventana_editar)
        nueva_cantidad.grid(row=7, column=2)

        # boton para actualizar

        Button(self.ventana_editar, text="Actualizar", command=lambda: self.actualizar_datos(material, nuevo_material.get(), descripcion, nueva_descripcion.get(
        ), referencia, nueva_referencia.get(), cantidad, nueva_cantidad.get())).grid(row=8, column=2, sticky=W)

    def actualizar_datos(self, material, nuevo_material, descripcion, nueva_descripcion, referencia, nueva_referencia, cantidad, nueva_cantidad):
        """funcion para actualizar datos"""
        query = "UPDATE Inventario SET Material = ?, descripcion = ?, Referencia = ?, Cantidad = ? WHERE Material = ? AND descripcion = ? AND Referencia = ? AND Cantidad = ?"
        parametros = (nuevo_material, nueva_descripcion, nueva_referencia,
                    nueva_cantidad, material, descripcion, referencia, cantidad)
        self.consulta_db(query, parametros)
        self.ventana_editar.destroy()
        self.message["text"] = f"El articulo {descripcion} ha sido actualizado"
        self.tomar_articulos()


if __name__ == "__main__":
    window = Tk()
    app = Articulo(window)
    window.mainloop()
