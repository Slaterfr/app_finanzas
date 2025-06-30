import tkinter as tk
from funciones import Ingreso, Gasto, guardar_datos_pickle, cargar_datos_pickle

def crear_interfaz(root):
    root.title("Calculo de balance mensual")
    root.geometry("700x700")

    datos = cargar_datos_pickle()
    ingresos = Ingreso()
    gastos = Gasto()
    ingresos.datos = datos.get("ingresos", {})
    gastos.datos = datos.get("gastos", {})

    frame_entrada = tk.Frame(root)
    frame_resultados = tk.Frame(root)

    def mostrar_frame(frame):
        frame_entrada.pack_forget()
        frame_resultados.pack_forget()
        frame.pack(fill="both", expand=True)

    frame_entrada.pack(padx=10, pady=10, fill="both", expand=True)
    tk.Label(frame_entrada, text="Nombre del ingreso:").grid(row=0, column=0, pady=5)
    categoria_ingreso = tk.Entry(frame_entrada)
    categoria_ingreso.grid(row=0, column=1, pady=5)

    tk.Label(frame_entrada, text="Monto del ingreso(₡):").grid(row=1, column=0, pady=5)
    monto_ingreso = tk.Entry(frame_entrada)
    monto_ingreso.grid(row=1, column=1, pady=5)

    tk.Label(frame_entrada, text="Nombre del gasto:").grid(row=2, column=0, pady=5)
    categoria_gasto = tk.Entry(frame_entrada)
    categoria_gasto.grid(row=2, column=1, pady=5)

    tk.Label(frame_entrada, text="Monto del gasto(₡):").grid(row=3, column=0, pady=5)
    monto_gasto = tk.Entry(frame_entrada)
    monto_gasto.grid(row=3, column=1, pady=5)

    def actualizar_datos_label():
        datos_label.config(text=f"Ingresos: {ingresos.datos}\nGastos: {gastos.datos}")

    def actualizar_lista_transacciones():
        lista_transacciones.delete(0, tk.END)
        lista_transacciones.insert(tk.END, "Ingresos:")
        for categoria, monto in ingresos.datos.items():
            lista_transacciones.insert(tk.END, f" [I] {categoria}: ₡{monto}")
        lista_transacciones.insert(tk.END, "Gastos:")
        for categoria, monto in gastos.datos.items():
            lista_transacciones.insert(tk.END, f" [G] {categoria}: ₡{monto}")

    def agregar_ingreso():
        try:
            categoria = categoria_ingreso.get()
            monto = float(monto_ingreso.get())
            if categoria and monto >= 0:
                ingresos.ingresar_datos(categoria, monto)
                guardar_datos_pickle(ingresos, gastos)
                monto_ingreso.delete(0, tk.END)
                categoria_ingreso.delete(0, tk.END)
                resultado_label.config(text="Ingreso agregado correctamente.")
                actualizar_datos_label()
                actualizar_lista_transacciones()
        except ValueError:
            resultado_label.config(text="Error: Ingresa datos válidos")

    def agregar_gasto():
        try:
            categoria = categoria_gasto.get()
            monto = float(monto_gasto.get())
            if categoria and monto >= 0:
                gastos.ingresar_datos(categoria, monto)
                guardar_datos_pickle(ingresos, gastos)
                monto_gasto.delete(0, tk.END)
                categoria_gasto.delete(0, tk.END)
                resultado_label.config(text="Gasto agregado correctamente.")
                actualizar_datos_label()
                actualizar_lista_transacciones()
        except ValueError:
            resultado_label.config(text="Error: Ingresa datos válidos.")

    def modificar_ingreso():
        try:
            categoria = categoria_ingreso.get()
            monto = float(monto_ingreso.get())
            if categoria and monto >= 0:
                ingresos.modificar_datos(categoria, monto)
                guardar_datos_pickle(ingresos, gastos)
                resultado_label.config(text="Ingreso modificado correctamente.")
                actualizar_datos_label()
                actualizar_lista_transacciones()
        except ValueError:
            resultado_label.config(text="Error: Ingresa datos válidos.")

    def modificar_gasto():
        try:
            categoria = categoria_gasto.get()
            monto = float(monto_gasto.get())
            if categoria and monto >= 0:
                gastos.modificar_datos(categoria, monto)
                guardar_datos_pickle(ingresos, gastos)
                resultado_label.config(text="Gasto modificado correctamente.")
                actualizar_datos_label()
                actualizar_lista_transacciones()
        except ValueError:
            resultado_label.config(text="Error: Ingresa datos válidos.")

    def mostrar_balance():
        total_ingresos = sum(ingresos.datos.values())
        total_gastos = sum(gastos.datos.values())
        balance = total_ingresos - total_gastos
        if balance > 20000:
            resultado_label.config(text=f"Ingresos: ₡{total_ingresos}, Gastos: ₡{total_gastos}, ahorro mensual: ₡{balance:.2f}")
        elif 0 < balance < 20000:
            resultado_label.config(text=f"Ingresos: ₡{total_ingresos}, Gastos: ₡{total_gastos}, ahorro mensual: ₡{balance:.2f}. Se recomienda reducir los gastos levemente.")
        elif balance < 0:
            resultado_label.config(text=f"Ingresos: ₡{total_ingresos}, Gastos: ₡{total_gastos}, resultado: ₡{balance:.2f}, estado de balance negativo.")
        elif balance == 0:
            resultado_label.config(text=f"Ingresos: ₡{total_ingresos}, Gastos: ₡{total_gastos}, ahorro mensual ₡{balance:.2f}. Ahorro mensual nulo.")

    def eliminar_seleccionado():
        seleccion = lista_transacciones.get(tk.ACTIVE)
        if seleccion.startswith(" [I] "):
            categoria = seleccion[5:].split(":")[0]
            if categoria in ingresos.datos:
                del ingresos.datos[categoria]
        elif seleccion.startswith(" [G] "):
            categoria = seleccion[5:].split(":")[0]
            if categoria in gastos.datos:
                del gastos.datos[categoria]
        else:
            resultado_label.config(text="Selecciona una categoría válida.")
            return
        guardar_datos_pickle(ingresos, gastos)
        resultado_label.config(text=f"'{categoria}' eliminado correctamente.")
        actualizar_datos_label()
        actualizar_lista_transacciones()

    tk.Label(frame_resultados, text="Resultados del balance mensual").pack(pady=10)
    resultado_label = tk.Label(frame_resultados, text="")
    resultado_label.pack(pady=5)

    datos_label = tk.Label(frame_resultados)
    datos_label.pack(pady=5)

    lista_transacciones = tk.Listbox(frame_resultados, width=60, height=10)
    lista_transacciones.pack(pady=10)

    actualizar_datos_label()
    actualizar_lista_transacciones()

    tk.Button(frame_entrada, text="Agregar Ingreso", command=agregar_ingreso).grid(row=4, column=0, pady=5)
    tk.Button(frame_entrada, text="Agregar Gasto", command=agregar_gasto).grid(row=4, column=1, pady=5)
    tk.Button(frame_entrada, text="Modificar Ingreso", command=modificar_ingreso).grid(row=5, column=0, pady=5)
    tk.Button(frame_entrada, text="Modificar Gasto", command=modificar_gasto).grid(row=5, column=1, pady=5)
    tk.Button(frame_entrada, text="Ventana de Resultados", command=lambda: mostrar_frame(frame_resultados)).grid(row=4, column=2, pady=5)

    tk.Button(frame_resultados, text="Calcular Balance", command=mostrar_balance).pack(pady=5)
    tk.Button(frame_resultados, text="Eliminar Seleccionado", command=eliminar_seleccionado).pack(pady=5)
    tk.Button(frame_resultados, text="Regresar a la ventana principal", command=lambda: mostrar_frame(frame_entrada)).pack(pady=5)

    def cerrar_ventana():
        print("Cerrando la ventana...")
        root.destroy()

    tk.Button(frame_resultados, text="Cerrar", command=cerrar_ventana).pack(pady=20)



    





















