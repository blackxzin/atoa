import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
import threading
import os

class ConversorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor Vídeo para MP3")
        self.root.geometry("400x250")
        self.root.configure(padx=20, pady=20)

        # UI Elements
        self.label = tk.Label(root, text="Extrator de Áudio de Alta Performance", font=("Arial", 12, "bold"))
        self.label.pack(pady=10)

        self.btn_selecionar = tk.Button(root, text="Selecionar Vídeo e Converter", 
                                        command=self.iniciar_thread, 
                                        bg="#3498db", fg="white", font=("Arial", 10),
                                        height=2, width=30)
        self.btn_selecionar.pack(pady=20)

        # Barra de Progresso 
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        self.status = tk.Label(root, text="Aguardando arquivo...", fg="gray")
        self.status.pack()

    def iniciar_thread(self):
        arquivo_video = filedialog.askopenfilename(
            filetypes=[("Vídeos", "*.mp4 *.avi *.mkv *.mov *.wmv")]
        )
        
        if arquivo_video:
            arquivo_audio = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[("MP3", "*.mp3")],
                initialfile=os.path.splitext(os.path.basename(arquivo_video))[0] + ".mp3"
            )
            
            if arquivo_audio:
                self.btn_selecionar.config(state=tk.DISABLED)
                # Inicia a conversão em segundo plano
                threading.Thread(target=self.converter, args=(arquivo_video, arquivo_audio), daemon=True).start()

    def atualizar_barra(self, t):
        """Função chamada pelo MoviePy para atualizar o progresso."""
        # O MoviePy passa o tempo atual do vídeo processado
        porcentagem = (t / self.duracao_total) * 100
        self.progress['value'] = porcentagem
        self.status.config(text=f"Processando: {int(porcentagem)}%", fg="blue")
        self.root.update_idletasks()

    def converter(self, caminho_video, caminho_audio):
        try:
            with VideoFileClip(caminho_video) as video:
                self.duracao_total = video.duration
                self.progress['value'] = 0
                
                # O parâmetro 'logger' nos permite criar o callback para a barra
                # Usamos um logger customizado simples
                video.audio.write_audiofile(
                    caminho_audio, 
                    logger=ProgressoLogger(self.atualizar_barra)
                )

            self.finalizar("Conversão concluída com sucesso!")
        except Exception as e:
            self.finalizar(f"Erro: {str(e)}", erro=True)

    def finalizar(self, mensagem, erro=False):
        self.btn_selecionar.config(state=tk.NORMAL)
        self.progress['value'] = 100 if not erro else 0
        cor = "red" if erro else "green"
        self.status.config(text=mensagem, fg=cor)
        
        if erro:
            messagebox.showerror("Erro", mensagem)
        else:
            messagebox.showinfo("Sucesso", "O áudio foi extraído perfeitamente!")

# Classe auxiliar para "ouvir" o MoviePy
class ProgressoLogger:
    def __init__(self, callback):
        self.callback = callback
    def log_start(self, **kwargs): pass
    def log_stop(self, **kwargs): pass
    def callback_write(self, **kwargs): pass
    def __call__(self, **kwargs): pass
    
    def message(self, msg): pass
    
    def bars_callback(self, bar, attr, value, total):
        # Esta é a função que o MoviePy chama durante a escrita do arquivo
        if bar == 't': # 't' representa o tempo/progresso
            self.callback(value)

if __name__ == "__main__":
    app_root = tk.Tk()
    ConversorPro(app_root)
    app_root.mainloop()
