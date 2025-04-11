import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

# Obtener mes y año actual para el nombre del archivo
mes_actual = datetime.now().strftime("%B").lower()  # por ejemplo "abril"
anio_actual = datetime.now().year
ARCHIVO_TAREAS = f"{mes_actual}_{anio_actual}.json"

# Colores personalizados
bg_color = "#e3f2fd"
text_color = "#0d47a1"
accent_color = "#64b5f6"
exit_color = "#ef5350"

# Funciones para cargar y guardar tareas
def cargar_tareas():
    if os.path.exists(ARCHIVO_TAREAS):
        with open(ARCHIVO_TAREAS, "r") as f:
            return json.load(f)
    return []

def guardar_tareas(tareas):
    with open(ARCHIVO_TAREAS, "w") as f:
        json.dump(tareas, f, indent=4)

# Agregar una nueva tarea
def agregar_tarea():
    tarea_texto = simpledialog.askstring("Nueva tarea", "Escribe la tarea:")
    if tarea_texto:
        tareas.append({"descripcion": tarea_texto, "estado": "En proceso"})
        guardar_tareas(tareas)
        actualizar_lista()

# Actualizar lista de tareas en pantalla
def actualizar_lista():
    lista_tareas.delete(0, tk.END)
    for idx, t in enumerate(tareas):
        lista_tareas.insert(tk.END, f"{idx+1}. {t['descripcion']} [{t['estado']}]")

# Eliminar una tarea seleccionada
def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        index = seleccion[0]
        confirmacion = messagebox.askyesno("Eliminar", "¿Estás seguro de eliminar esta tarea?")
        if confirmacion:
            tareas.pop(index)
            guardar_tareas(tareas)
            actualizar_lista()

# Editar una tarea seleccionada
def editar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        index = seleccion[0]
        nueva_descripcion = simpledialog.askstring("Editar tarea", "Modifica la tarea:", initialvalue=tareas[index]["descripcion"])
        if nueva_descripcion:
            tareas[index]["descripcion"] = nueva_descripcion
            guardar_tareas(tareas)
            actualizar_lista()

# Cambiar estado de una tarea
def cambiar_estado():
    seleccion = lista_tareas.curselection()
    if seleccion:
        index = seleccion[0]
        estado_actual = tareas[index]["estado"]
        tareas[index]["estado"] = "Solucionado" if estado_actual == "En proceso" else "En proceso"
        guardar_tareas(tareas)
        actualizar_lista()

# Salir
def salir():
    ventana.destroy()

# ------------------ Interfaz gráfica ------------------
ventana = tk.Tk()
ventana.title("Departamento TI💼")
ventana.geometry("700x400")
ventana.configure(bg=bg_color)

# Mensaje motivador
motivador = tk.Label(ventana, text="💡 La disciplina te hará libre 💡",
                     font=("Arial", 14, "bold"), bg=bg_color, fg=text_color)
motivador.pack(pady=10)

# Título con el mes actual
titulo_rutina = tk.Label(ventana, text=f"📅 Tareas Realizadas en el Mes: {mes_actual.capitalize()} {anio_actual}",
                         font=("Arial", 12, "bold"), bg=bg_color, fg=text_color)
titulo_rutina.pack()

# Lista de tareas
lista_tareas = tk.Listbox(ventana, width=70, height=12, font=("Arial", 10),
                          bg="white", fg="black", borderwidth=2, relief="groove")
lista_tareas.pack(pady=10)

# Botones
frame_botones = tk.Frame(ventana, bg=bg_color)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="+ Añadir", command=agregar_tarea,
          bg=accent_color, fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5)

tk.Button(frame_botones, text="✏️ Editar", command=editar_tarea,
          bg="#ffd54f", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5)

tk.Button(frame_botones, text="❌ Eliminar", command=eliminar_tarea,
          bg=exit_color, fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=2, padx=5)

tk.Button(frame_botones, text="🔁 Estado", command=cambiar_estado,
          bg="#81c784", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=3, padx=5)

# Botón de salida
tk.Button(ventana, text="Salir", command=salir,
          bg=exit_color, fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=5)

# Cargar y mostrar tareas del mes actual
tareas = cargar_tareas()
actualizar_lista()

ventana.mainloop()
