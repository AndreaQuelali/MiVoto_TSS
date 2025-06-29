"""
Utilidades para configuración de estilos de la interfaz gráfica
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from config.settings import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, BG_COLOR, TEXT_COLOR


def configurar_estilos():
    """
    Configura los estilos visuales de la aplicación.
    
    Returns:
        ttk.Style: Objeto de estilos configurado
    """
    style = ttk.Style()
    style.theme_use('clam')
    
    # Estilos básicos
    style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=('Arial', 10))
    style.configure('TFrame', background=BG_COLOR)
    style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
    
    # Estilos de encabezados
    style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground=PRIMARY_COLOR)
    style.configure('Subheader.TLabel', font=('Arial', 12, 'bold'), foreground=SECONDARY_COLOR)
    
    # Estilos de botones
    style.configure('TButton', font=('Arial', 10, 'bold'), background=PRIMARY_COLOR, 
                   foreground='white', padding=8)
    style.map('TButton', background=[('active', SECONDARY_COLOR)])
    
    # Estilos de notebook (pestañas)
    style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
    style.configure('TNotebook.Tab', background=SECONDARY_COLOR, foreground='white', padding=[10, 5])
    style.map('TNotebook.Tab',
              background=[('selected', PRIMARY_COLOR)],
              foreground=[('selected', 'white')])
    
    # Estilos de frames con etiqueta
    style.configure('TLabelframe', background=BG_COLOR, foreground=PRIMARY_COLOR)
    style.configure('TLabelframe.Label', font=('Arial', 12, 'bold'), foreground=PRIMARY_COLOR)
    
    # Estilos de Treeview
    style.configure('Treeview',
                   background="#ffffff",
                   foreground="#333333",
                   fieldbackground="#ffffff",
                   font=('Arial', 9))
    style.map('Treeview',
              background=[('selected', PRIMARY_COLOR)])
    style.configure('Treeview.Heading',
                   font=('Arial', 10, 'bold'),
                   background=SECONDARY_COLOR,
                   foreground='white')
    
    return style


def crear_scrollable_frame(parent):
    """
    Crea un frame con scrollbar vertical.
    
    Args:
        parent: Widget padre
        
    Returns:
        tuple: (canvas, scrollbar, scrollable_frame)
    """
    # Frame principal con scrollbar
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill='both', expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return canvas, scrollbar, scrollable_frame


def aplicar_estilo_grafico(fig, ax):
    """
    Aplica estilos consistentes a los gráficos de matplotlib.
    
    Args:
        fig: Figura de matplotlib
        ax: Ejes de matplotlib
    """
    # Configurar colores de fondo
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    # Configurar colores de texto
    ax.tick_params(colors='#333333')
    ax.xaxis.label.set_color('#333333')
    ax.yaxis.label.set_color('#333333')
    ax.title.set_color('#333333')
    
    # Configurar grid
    ax.grid(True, linestyle='--', alpha=0.7, color='#cccccc')
    
    # Configurar bordes
    for spine in ax.spines.values():
        spine.set_color('#cccccc')
    
    # Ajustar layout
    fig.tight_layout()