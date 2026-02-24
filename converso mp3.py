from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog, messagebox

def converter():
    try:
        arquivo = filedialog.askopenfilename(
            title="Escolha o vídeo",
            filetypes=[("Vídeos", "*.mp4 *.avi *.mkv *.mov")]
        )

        if arquivo:
            video = VideoFileClip(arquivo)

            salvar = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[("MP3", "*.mp3")]
            )

            video.audio.write_audiofile(salvar)

            messagebox.showinfo("Sucesso", "Convertido para MP3!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


janela = tk.Tk()
janela.title("Conversor Video → MP3")
janela.geometry("300x150")

botao = tk.Button(janela,
text="Selecionar Vídeo",
command=converter,
height=2,
width=20)

botao.pack(pady=40)

janela.mainloop()