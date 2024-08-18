from tkinter import *
from tkinter import messagebox


def gera_qr_code():
    messagebox.showinfo(title="QR Code Gerado", message="QR Code gerado com sucesso!")


window = Tk()
window.title("Gerador de Código QR")
window.config(padx=10, pady=100)

# Labels
website_label = Label(text="URL:")
website_label.grid(row=2, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=2, column=1, columnspan=2)
website_entry.focus()
add_button = Button(text="Gerar QR Code", width=36, command=gera_qr_code)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()