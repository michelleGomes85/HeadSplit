import tkinter as tk
from tkinter import ttk, messagebox

from header_protocols.BitOrientedHeader import BitOrientedHeader
from header_protocols.CharacterOrientedHeader import CharacterOrientedHeader
from header_protocols.ByteCountOrientedHeader import ByteCountOrientedHeader
from expections.InvalidDataError import InvalidDataError

class HeaderApplication(tk.Tk):
    
    def __init__(self):
        
        super().__init__()
        self.title("Manipulação de Cabeçalhos de Protocolo")
        self.geometry("400x400")
        self.resizable(False, False)
        self.center_window(400, 340)
        
        self.create_widgets()

    def center_window(self, width, heigh):
        
        window_width = width
        window_height = heigh
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    def create_widgets(self):
        
        self.format_label = ttk.Label(self, text="Escolha o formato de cabeçalho:")
        self.format_label.pack(pady=10)
        
        # Combobox com as opções disponiveis
        self.format_var = tk.StringVar()
        self.format_combobox = ttk.Combobox(self, textvariable=self.format_var, state="readonly")
        self.format_combobox['values'] = ("Orientado a Bit", "Orientado a Caractere", "Orientado a Contagem de Byte")
        self.format_combobox.current(0)
        self.format_combobox.pack(pady=5)
        
        # Detecta a mudança de seleção
        self.format_combobox.bind("<<ComboboxSelected>>", self.on_format_change)

        # Campo para escrever a mensagem
        self.data_label = ttk.Label(self, text="Corpo da Mensagem:")
        self.data_label.pack(pady=10)
        self.data_entry = ttk.Entry(self)
        self.data_entry.pack(pady=5)

        # Campo de entrada para o tamanho em bytes (inicialmente oculto)
        self.byte_size_label = ttk.Label(self, text="Tamanho em Bytes:")
        self.byte_size_entry = ttk.Entry(self)
        
        # Botões para montar e desmontar
        self.mount_button = ttk.Button(self, text="Montar Cabeçalho", command=self.mount_header)
        self.mount_button.pack(pady=5)
        self.unmount_button = ttk.Button(self, text="Desmontar Cabeçalho", command=self.unmount_header)
        self.unmount_button.pack(pady=5)

        # Campo de saída
        self.result_label = ttk.Label(self, text="Resultado:")
        self.result_label.pack(pady=10)
        self.result_text = tk.Text(self, height=5, wrap="word", state=tk.DISABLED)
        self.result_text.pack(pady=5)

    def on_format_change(self, event=None):
        
        if self.format_var.get() == "Orientado a Contagem de Byte":
            self.byte_size_label.pack(after=self.data_entry, pady=5)
            self.byte_size_entry.pack(after=self.byte_size_label, pady=5)
            self.center_window(400, 400)
        else:
            self.byte_size_label.pack_forget()
            self.byte_size_entry.pack_forget()
            self.center_window(400, 340)

    def mount_header(self):
        
        data = self.data_entry.get()
        format_type = self.format_var.get()
        
        try:
            if format_type == "Orientado a Bit":
                result = BitOrientedHeader.mount(data)
            elif format_type == "Orientado a Caractere":
                result = CharacterOrientedHeader.mount(data)
            elif format_type == "Orientado a Contagem de Byte":
                result = ByteCountOrientedHeader.mount(data, self.byte_size_entry.get())
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            self.result_text.config(state=tk.DISABLED)
            
        except InvalidDataError as e:
            messagebox.showerror("Erro", str(e))

    def unmount_header(self):
        
        header = self.result_text.get("1.0", tk.END).strip()  
        format_type = self.format_var.get()
        
        try:
            if format_type == "Orientado a Bit":
                result = BitOrientedHeader.unmount(header)
            elif format_type == "Orientado a Caractere":
                result = CharacterOrientedHeader.unmount(header)
            elif format_type == "Orientado a Contagem de Byte":
                result = ByteCountOrientedHeader.unmount(header)
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            self.result_text.config(state=tk.DISABLED)
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))