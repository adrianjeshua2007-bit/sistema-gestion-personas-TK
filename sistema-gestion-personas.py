import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import hashlib
import os


# ✅ NUEVO: Configuración de rutas para Docker
# En la función setup_database(), agrega esta alternativa:
def setup_database():
    # ✅ USAR /tmp QUE SIEMPRE TIENE PERMISOS DE ESCRITURA EN DOCKER
    db_path = '/tmp/person_management.db'
    print(f"✅ Usando base de datos en: {db_path}")
    
    # Verificar que podemos escribir en /tmp
    try:
        test_file = '/tmp/test_write.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✅ Permisos de escritura en /tmp: OK")
        
    except Exception as e:
        print(f"❌ Error de permisos en /tmp: {e}")
        # Último recurso: base de datos en memoria
        db_path = ':memory:'
        print("⚠️  Usando base de datos en memoria (datos temporales)")
    
    return db_path # ✅ NUEVO: Función para verificar y crear la base de datos
def initialize_database(db_path):
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        # Crear tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS persons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_completo TEXT,
                        cedula TEXT UNIQUE,
                        altura_cm INTEGER,
                        peso_kg REAL,
                        edad INTEGER,
                        direccion TEXT,
                        nacionalidad TEXT)''')
        
        conn.commit()
        conn.close()
        print(f"✅ Base de datos inicializada en: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Personas - Login")
        self.root.geometry("400x300")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Centrar la ventana
        self.root.eval('tk::PlaceWindow . center')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores
        self.bg_color = '#2c3e50'
        self.fg_color = '#ecf0f1'
        self.accent_color = '#3498db'
        
        # Configurar fuentes
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = tkfont.Font(family="Helvetica", size=10)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Título
        title_label = tk.Label(main_frame, text="Inicio de Sesión", 
                              font=self.title_font, bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=(0, 30))
        
        # Campos de usuario y contraseña
        fields = [
            ("Usuario", "usuario"),
            ("Contraseña", "contraseña")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            frame = tk.Frame(main_frame, bg=self.bg_color)
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=label + ":", width=15, anchor=tk.W, 
                    bg=self.bg_color, fg=self.fg_color, 
                    font=self.normal_font).pack(side=tk.LEFT)
            
            if field == "contraseña":
                entry = tk.Entry(frame, width=20, font=self.normal_font,
                                bg='#34495e', fg=self.fg_color, 
                                insertbackground='white', show="*")
            else:
                entry = tk.Entry(frame, width=20, font=self.normal_font,
                                bg='#34495e', fg=self.fg_color, 
                                insertbackground='white')
                
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[field] = entry
        
        # Botón de login
        login_btn = tk.Button(main_frame, text="Iniciar Sesión", command=self.authenticate,
                             bg=self.accent_color, fg='white', font=self.normal_font,
                             relief=tk.FLAT, padx=15, pady=8, width=15)
        login_btn.pack(pady=20)
        
        # Bind Enter key to authenticate
        self.root.bind('<Return>', lambda event: self.authenticate())
        
    def authenticate(self):
        usuario = self.entries['usuario'].get()
        contraseña = self.entries['contraseña'].get()
        
        # Hash de la contraseña para comparar
        hashed_password = hashlib.sha256("07062007".encode()).hexdigest()
        input_hashed_password = hashlib.sha256(contraseña.encode()).hexdigest()
        
        if usuario == "adrianjeshua" and input_hashed_password == hashed_password:
            self.root.destroy()
            root = tk.Tk()
            app = PersonManagement(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

class PersonManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Personas")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores
        self.bg_color = '#2c3e50'
        self.fg_color = '#ecf0f1'
        self.accent_color = '#3498db'
        self.success_color = '#2ecc71'
        self.warning_color = '#f39c12'
        self.danger_color = '#e74c3c'
        self.header_color = '#34495e'
        
        # Configurar fuentes
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.header_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.normal_font = tkfont.Font(family="Helvetica", size=10)
        
        # ✅ NUEVO: Configuración mejorada de base de datos
        self.db_path = setup_database()
        
        # ✅ NUEVO: Inicializar base de datos antes de conectar
        if not initialize_database(self.db_path):
            messagebox.showerror("Error", "No se pudo inicializar la base de datos")
            self.root.destroy()
            return
        
        # Conectar a la base de datos
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.c = self.conn.cursor()
            print(f"✅ Conexión exitosa a: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            self.root.destroy()
            return
        
        # Crear tabla si no existe (por si acaso)
        self.create_table()
        
        # Interfaz gráfica
        self.create_widgets()
        
        # Cargar datos
        self.view_records()
        
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS persons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_completo TEXT,
                        cedula TEXT UNIQUE,
                        altura_cm INTEGER,
                        peso_kg REAL,
                        edad INTEGER,
                        direccion TEXT,
                        nacionalidad TEXT)''')
        self.conn.commit()
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Título
        title_label = tk.Label(main_frame, text="Sistema de Gestión de Personas", 
                              font=self.title_font, bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=(0, 20))
        
        # Frame de búsqueda
        search_frame = tk.Frame(main_frame, bg=self.bg_color)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(search_frame, text="Buscar:", bg=self.bg_color, fg=self.fg_color, 
                font=self.normal_font).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_entry = tk.Entry(search_frame, width=30, font=self.normal_font, 
                                    bg='#34495e', fg=self.fg_color, insertbackground='white')
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.search_records)
        
        search_options = ["Nombre", "Cédula", "Dirección", "Nacionalidad"]
        self.search_combo = ttk.Combobox(search_frame, values=search_options, 
                                        state="readonly", width=15, font=self.normal_font)
        self.search_combo.set("Nombre")
        self.search_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        add_btn = tk.Button(button_frame, text="Agregar Persona", command=self.add_record, 
                           bg=self.success_color, fg='white', font=self.header_font,
                           relief=tk.FLAT, padx=15, pady=5)
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        edit_btn = tk.Button(button_frame, text="Editar Persona", command=self.edit_record, 
                            bg=self.accent_color, fg='white', font=self.header_font,
                            relief=tk.FLAT, padx=15, pady=5)
        edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_btn = tk.Button(button_frame, text="Eliminar Persona", command=self.delete_record, 
                              bg=self.danger_color, fg='white', font=self.header_font,
                              relief=tk.FLAT, padx=15, pady=5)
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = tk.Button(button_frame, text="Actualizar", command=self.view_records, 
                               bg=self.warning_color, fg='white', font=self.header_font,
                               relief=tk.FLAT, padx=15, pady=5)
        refresh_btn.pack(side=tk.LEFT)
        
        # Treeview para mostrar los datos
        tree_frame = tk.Frame(main_frame, bg=self.bg_color)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Crear el treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Nombre Completo", "Cédula", "Altura (cm)", "Peso (kg)", "Edad", "Dirección", "Nacionalidad"
        ), yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, show='headings')
        
        # Configurar estilo del treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#34495e",
                        foreground=self.fg_color,
                        rowheight=25,
                        fieldbackground="#34495e",
                        font=self.normal_font)
        style.configure("Treeview.Heading", 
                        background=self.header_color,
                        foreground=self.fg_color,
                        font=self.header_font,
                        relief=tk.FLAT)
        style.map('Treeview', background=[('selected', self.accent_color)])
        
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)
        
        # Definir columnas
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nombre Completo", width=200, anchor=tk.W)
        self.tree.column("Cédula", width=120, anchor=tk.W)
        self.tree.column("Altura (cm)", width=80, anchor=tk.CENTER)
        self.tree.column("Peso (kg)", width=80, anchor=tk.CENTER)
        self.tree.column("Edad", width=60, anchor=tk.CENTER)
        self.tree.column("Dirección", width=150, anchor=tk.W)
        self.tree.column("Nacionalidad", width=120, anchor=tk.W)
        
        # Encabezados
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre Completo", text="Nombre Completo")
        self.tree.heading("Cédula", text="Cédula")
        self.tree.heading("Altura (cm)", text="Altura (cm)")
        self.tree.heading("Peso (kg)", text="Peso (kg)")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Nacionalidad", text="Nacionalidad")
        
        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Estadísticas
        stats_frame = tk.Frame(main_frame, bg=self.bg_color)
        stats_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.stats_label = tk.Label(stats_frame, text="Total de personas: 0", 
                                   bg=self.bg_color, fg=self.fg_color, font=self.normal_font)
        self.stats_label.pack(side=tk.LEFT)
    
    def add_record(self):
        AddWindow(self)
    
    def edit_record(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una persona para editar.")
            return
        
        item = self.tree.item(selected)
        record_id = item['values'][0]
        EditWindow(self, record_id)
    
    def on_double_click(self, event):
        self.edit_record()
    
    def delete_record(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione una persona para eliminar.")
            return
        
        item = self.tree.item(selected)
        record_id = item['values'][0]
        nombre = item['values'][1]
        cedula = item['values'][2]
        
        confirm = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar a '{nombre} - {cedula}'?"
        )
        
        if confirm:
            self.c.execute("DELETE FROM persons WHERE id=?", (record_id,))
            self.conn.commit()
            self.view_records()
            messagebox.showinfo("Éxito", "Persona eliminada correctamente.")
    
    def search_records(self, event=None):
        search_term = self.search_entry.get()
        search_by = self.search_combo.get()
        
        if search_by == "Nombre":
            self.c.execute("SELECT * FROM persons WHERE nombre_completo LIKE ?", ('%' + search_term + '%',))
        elif search_by == "Cédula":
            self.c.execute("SELECT * FROM persons WHERE cedula LIKE ?", ('%' + search_term + '%',))
        elif search_by == "Dirección":
            self.c.execute("SELECT * FROM persons WHERE direccion LIKE ?", ('%' + search_term + '%',))
        elif search_by == "Nacionalidad":
            self.c.execute("SELECT * FROM persons WHERE nacionalidad LIKE ?", ('%' + search_term + '%',))
        
        records = self.c.fetchall()
        self.update_treeview(records)
    
    def view_records(self):
        self.c.execute("SELECT * FROM persons")
        records = self.c.fetchall()
        self.update_treeview(records)
        
        # Actualizar estadísticas
        self.stats_label.config(text=f"Total de personas: {len(records)}")
    
    def update_treeview(self, records):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar nuevos registros
        for record in records:
            self.tree.insert("", tk.END, values=record)
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

class AddWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Agregar Nueva Persona")
        self.window.geometry("500x600")
        self.window.configure(bg=parent.bg_color)
        self.window.grab_set()  # Modal window
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg=self.parent.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Agregar Nueva Persona", 
                              font=self.parent.title_font, bg=self.parent.bg_color, 
                              fg=self.parent.fg_color)
        title_label.pack(pady=(0, 20))
        
        # Campos del formulario
        fields = [
            ("Nombre Completo", "nombre_completo"),
            ("Cédula de Identidad", "cedula"),
            ("Altura (cm)", "altura_cm"),
            ("Peso (kg)", "peso_kg"),
            ("Edad", "edad"),
            ("Dirección", "direccion"),
            ("Nacionalidad", "nacionalidad")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            frame = tk.Frame(main_frame, bg=self.parent.bg_color)
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(frame, text=label + ":", width=20, anchor=tk.W, 
                    bg=self.parent.bg_color, fg=self.parent.fg_color, 
                    font=self.parent.normal_font).pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, width=30, font=self.parent.normal_font,
                            bg='#34495e', fg=self.parent.fg_color, 
                            insertbackground='white')
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[field] = entry
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=self.parent.bg_color)
        button_frame.pack(fill=tk.X, pady=20)
        
        save_btn = tk.Button(button_frame, text="Guardar", command=self.save_record,
                 bg=self.parent.success_color, fg='white', font=self.parent.header_font,
                 relief=tk.FLAT, padx=15, pady=5)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="Cancelar", command=self.window.destroy,
                 bg=self.parent.danger_color, fg='white', font=self.parent.header_font,
                 relief=tk.FLAT, padx=15, pady=5)
        cancel_btn.pack(side=tk.LEFT)
    
    def save_record(self):
        # Validar campos obligatorios
        if not self.entries['nombre_completo'].get() or not self.entries['cedula'].get():
            messagebox.showerror("Error", "Los campos 'Nombre Completo' y 'Cédula' son obligatorios.")
            return
        
        try:
            # Obtener valores con manejo de campos vacíos
            altura = self.entries['altura_cm'].get()
            peso = self.entries['peso_kg'].get()
            edad = self.entries['edad'].get()
            
            # Insertar en la base de datos
            self.parent.c.execute('''INSERT INTO persons 
                                (nombre_completo, cedula, altura_cm, peso_kg, edad, direccion, nacionalidad)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                (
                                    self.entries['nombre_completo'].get(),
                                    self.entries['cedula'].get(),
                                    int(altura) if altura else 0,
                                    float(peso) if peso else 0.0,
                                    int(edad) if edad else 0,
                                    self.entries['direccion'].get(),
                                    self.entries['nacionalidad'].get()
                                ))
            self.parent.conn.commit()
            self.parent.view_records()
            self.window.destroy()
            messagebox.showinfo("Éxito", "Persona agregada correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "La cédula ya existe en la base de datos.")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos para altura, peso y edad.")

class EditWindow(AddWindow):
    def __init__(self, parent, record_id):
        self.record_id = record_id
        super().__init__(parent)
        self.window.title("Editar Persona")
        self.load_record_data()
    
    def load_record_data(self):
        self.parent.c.execute("SELECT * FROM persons WHERE id=?", (self.record_id,))
        record = self.parent.c.fetchone()
        
        if record:
            fields = ["nombre_completo", "cedula", "altura_cm", "peso_kg", "edad", "direccion", "nacionalidad"]
            
            for i, field in enumerate(fields, start=1):
                self.entries[field].delete(0, tk.END)
                if record[i] is not None:
                    self.entries[field].insert(0, str(record[i]))
    
    def save_record(self):
        # Validar campos obligatorios
        if not self.entries['nombre_completo'].get() or not self.entries['cedula'].get():
            messagebox.showerror("Error", "Los campos 'Nombre Completo' y 'Cédula' son obligatorios.")
            return
        
        try:
            # Obtener valores con manejo de campos vacíos
            altura = self.entries['altura_cm'].get()
            peso = self.entries['peso_kg'].get()
            edad = self.entries['edad'].get()
            
            # Actualizar en la base de datos
            self.parent.c.execute('''UPDATE persons SET 
                                nombre_completo=?, cedula=?, altura_cm=?, peso_kg=?, edad=?, direccion=?, nacionalidad=?
                                WHERE id=?''',
                                (
                                    self.entries['nombre_completo'].get(),
                                    self.entries['cedula'].get(),
                                    int(altura) if altura else 0,
                                    float(peso) if peso else 0.0,
                                    int(edad) if edad else 0,
                                    self.entries['direccion'].get(),
                                    self.entries['nacionalidad'].get(),
                                    self.record_id
                                ))
            self.parent.conn.commit()
            self.parent.view_records()
            self.window.destroy()
            messagebox.showinfo("Éxito", "Persona actualizada correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "La cédula ya existe en la base de datos.")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos para altura, peso y edad.")

if __name__ == "__main__":
    # Configuración para Docker - asegurar que Tkinter funcione
    try:
        root = tk.Tk()
        # Testear que Tkinter funciona antes de proceder
        root.withdraw()  # Ocultar ventana temporalmente
        login = LoginWindow(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        print("Asegúrate de que XLaunch esté ejecutándose en Windows")
        input("Presiona Enter para salir...")
