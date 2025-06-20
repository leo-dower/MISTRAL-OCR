import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import requests
import json
import socket
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import threading

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mistral OCR - Interface Simples")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Configurar pasta padrão
        self.pasta_padrao = r"ENDEREÇO_DA_PASTA_PADRÃO"
        self.pasta_destino = r"ENDEREÇO_DA_PASTA_DESTINO"

        # Criar interface
        self.criar_interface()

    def criar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        titulo = tk.Label(main_frame, text="Mistral OCR - Processador de PDFs", 
                         font=("Arial", 14, "bold"), fg="darkblue")
        titulo.grid(row=0, column=0, columnspan=3, pady=10)

        # API Key
        tk.Label(main_frame, text="API Key:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="e", padx=10, pady=8)
        self.api_key_entry = tk.Entry(main_frame, width=60, show="*", font=("Arial", 10))
        self.api_key_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=8, sticky="ew")

        # Arquivo PDF
        tk.Label(main_frame, text="Arquivo PDF:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="e", padx=10, pady=8)
        self.file_path_entry = tk.Entry(main_frame, width=50, font=("Arial", 10))
        self.file_path_entry.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        
        self.browse_button = tk.Button(main_frame, text="Selecionar Arquivo", 
                                      command=self.selecionar_arquivo,
                                      bg="lightblue", font=("Arial", 9))
        self.browse_button.grid(row=2, column=2, padx=5, pady=8)

        # Pasta de destino (apenas informativa)
        tk.Label(main_frame, text="Destino:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="e", padx=10, pady=8)
        destino_label = tk.Label(main_frame, text=self.pasta_destino, 
                                font=("Arial", 9), fg="darkgreen", 
                                relief="sunken", anchor="w")
        destino_label.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=8)

        # Botão processar
        self.processar_button = tk.Button(main_frame, text="PROCESSAR OCR", 
                                         command=self.processar_ocr_thread,
                                         bg="green", fg="white", 
                                         font=("Arial", 12, "bold"),
                                         height=2)
        self.processar_button.grid(row=4, column=0, columnspan=3, pady=15)

        # Status
        self.status_label = tk.Label(main_frame, text="Pronto para processar...", 
                                    fg="blue", font=("Arial", 10))
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)

        # Separador
        separator = tk.Frame(main_frame, height=2, bg="gray")
        separator.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)

        # Label para a caixa de logs
        log_label = tk.Label(main_frame, text="Log de Execução:", 
                            font=("Arial", 11, "bold"), fg="darkred")
        log_label.grid(row=7, column=0, columnspan=3, sticky="w", pady=(5,0))

        # Caixa de texto para logs
        self.log_text = scrolledtext.ScrolledText(main_frame, 
                                                 width=90, height=15,
                                                 font=("Consolas", 9),
                                                 bg="black", fg="lightgreen",
                                                 wrap=tk.WORD)
        self.log_text.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=5)

        # Botões para a caixa de logs
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=5)

        self.clear_button = tk.Button(button_frame, text="Limpar Log", 
                                     command=self.limpar_log,
                                     bg="orange", font=("Arial", 9))
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = tk.Button(button_frame, text="Copiar Log", 
                                    command=self.copiar_log,
                                    bg="lightblue", font=("Arial", 9))
        self.copy_button.pack(side=tk.LEFT, padx=5)

        # Configurar redimensionamento
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(8, weight=1)

        # Log inicial
        self.adicionar_log("=== MISTRAL OCR INICIADO ===")
        self.adicionar_log(f"Pasta padrão: {self.pasta_padrao}")
        self.adicionar_log(f"Pasta destino: {self.pasta_destino}")
        self.adicionar_log("Aguardando seleção de arquivo e API Key...")

    def adicionar_log(self, mensagem):
        """Adicionar mensagem ao log com timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {mensagem}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)  # Scroll automático para o final
        self.root.update_idletasks()

    def limpar_log(self):
        """Limpar a caixa de logs"""
        self.log_text.delete(1.0, tk.END)
        self.adicionar_log("Log limpo pelo usuário")

    def copiar_log(self):
        """Copiar todo o conteúdo do log para a área de transferência"""
        try:
            log_content = self.log_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(log_content)
            self.adicionar_log("✓ Log copiado para a área de transferência")
        except Exception as e:
            self.adicionar_log(f"✗ Erro ao copiar log: {str(e)}")

    def selecionar_arquivo(self):
        """Selecionar arquivo PDF da pasta padrão"""
        self.adicionar_log("Abrindo seletor de arquivos...")
        file_path = filedialog.askopenfilename(
            initialdir=self.pasta_padrao,
            title="Selecione o arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            self.adicionar_log(f"✓ Arquivo selecionado: {file_path}")
            self.adicionar_log(f"  Tamanho: {os.path.getsize(file_path)} bytes")
            self.atualizar_status(f"Arquivo selecionado: {os.path.basename(file_path)}")
        else:
            self.adicionar_log("Seleção de arquivo cancelada")

    def criar_sessao_robusta(self):
        """Criar sessão HTTP com configurações robustas"""
        self.adicionar_log("Criando sessão HTTP robusta...")
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.timeout = 30
        self.adicionar_log("✓ Sessão HTTP configurada")
        return session

    def upload_arquivo(self, caminho_arquivo, api_key):
        """Fazer upload do arquivo para a API"""
        try:
            self.adicionar_log("=== INICIANDO UPLOAD ===")
            self.adicionar_log(f"Arquivo: {caminho_arquivo}")
            
            # Verificar DNS
            self.adicionar_log("Resolvendo DNS para api.mistral.ai...")
            ip = socket.gethostbyname('api.mistral.ai')
            self.adicionar_log(f"✓ DNS resolvido: api.mistral.ai -> {ip}")
        except socket.gaierror as e:
            self.adicionar_log(f"✗ ERRO DNS: {str(e)}")
            return None

        session = self.criar_sessao_robusta()
        url = "https://api.mistral.ai/v1/files"
        headers = {"Authorization": f"Bearer {api_key}"}

        self.adicionar_log(f"URL de upload: {url}")
        self.adicionar_log("Preparando dados para upload...")

        try:
            with open(caminho_arquivo, "rb") as f:
                files = {"file": f}
                data = {"purpose": "ocr"}
                
                self.adicionar_log("Enviando arquivo...")
                response = session.post(url, headers=headers, files=files, data=data, timeout=60)

            self.adicionar_log(f"Status da resposta: {response.status_code}")
            self.adicionar_log(f"Headers da resposta: {dict(response.headers)}")
            self.adicionar_log(f"Conteúdo da resposta: {response.text}")

            if response.status_code == 200:
                self.adicionar_log("✓ Upload concluído com sucesso!")
                return response.json()
            else:
                self.adicionar_log(f"✗ ERRO NO UPLOAD: Status {response.status_code}")
                self.adicionar_log(f"Detalhes do erro: {response.text}")
                return None

        except requests.exceptions.ConnectionError as e:
            self.adicionar_log(f"✗ ERRO DE CONEXÃO: {str(e)}")
            return None
        except requests.exceptions.Timeout as e:
            self.adicionar_log(f"✗ ERRO DE TIMEOUT: {str(e)}")
            return None
        except Exception as e:
            self.adicionar_log(f"✗ ERRO DURANTE UPLOAD: {str(e)}")
            return None

    def processar_ocr_arquivo(self, file_id, api_key):
        """Processar OCR do arquivo"""
        self.adicionar_log("=== INICIANDO PROCESSAMENTO OCR ===")
        self.adicionar_log(f"File ID: {file_id}")
        
        session = self.criar_sessao_robusta()
        url = "https://api.mistral.ai/v1/ocr"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-ocr-latest",
            "document": {
                "type": "file",
                "file_id": file_id
            }
        }

        self.adicionar_log(f"URL OCR: {url}")
        self.adicionar_log(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            self.adicionar_log("Enviando requisição OCR...")
            response = session.post(url, headers=headers, json=payload, timeout=300)

            self.adicionar_log(f"Status OCR: {response.status_code}")
            self.adicionar_log(f"Tamanho da resposta: {len(response.text)} chars")

            if response.status_code == 200:
                self.adicionar_log("✓ OCR processado com sucesso!")
                return response.json()
            else:
                self.adicionar_log(f"✗ ERRO NO OCR: Status {response.status_code}")
                self.adicionar_log(f"Resposta completa: {response.text}")
                return None
        except Exception as e:
            self.adicionar_log(f"✗ ERRO DURANTE PROCESSAMENTO OCR: {str(e)}")
            return None

    def salvar_resultados(self, ocr_result, nome_arquivo_original):
        """Salvar resultados na pasta de destino"""
        try:
            self.adicionar_log("=== SALVANDO RESULTADOS ===")
            
            # Criar nome base a partir do arquivo original
            nome_base = os.path.splitext(os.path.basename(nome_arquivo_original))[0]
            nome_base = nome_base.replace(" ", "_")
            self.adicionar_log(f"Nome base para arquivos: {nome_base}")

            # Garantir que a pasta de destino existe
            os.makedirs(self.pasta_destino, exist_ok=True)
            self.adicionar_log(f"Pasta de destino verificada: {self.pasta_destino}")

            # Salvar JSON completo
            json_filename = os.path.join(self.pasta_destino, f"{nome_base}_OCR_completo.json")
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(ocr_result, f, indent=2, ensure_ascii=False)
            self.adicionar_log(f"✓ JSON salvo: {json_filename}")

            # Salvar Markdown
            pages = ocr_result.get("pages", [])
            self.adicionar_log(f"Páginas encontradas: {len(pages)}")
            
            if pages:
                md_filename = os.path.join(self.pasta_destino, f"{nome_base}_OCR.md")
                with open(md_filename, "w", encoding="utf-8") as f:
                    f.write(f"# Resultado OCR - {nome_base}\n")
                    f.write(f"**Data:** {time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                    
                    for i, page in enumerate(pages, 1):
                        markdown_content = page.get("markdown", "")
                        if markdown_content:
                            f.write(f"## Página {i}\n\n")
                            f.write(markdown_content)
                            f.write("\n\n" + "="*60 + "\n\n")
                            self.adicionar_log(f"  Página {i}: {len(markdown_content)} caracteres")

                self.adicionar_log(f"✓ Markdown salvo: {md_filename}")
                return True
            else:
                self.adicionar_log("⚠ Nenhuma página encontrada no resultado")
                self.adicionar_log(f"Estrutura do resultado: {list(ocr_result.keys())}")
                return False

        except Exception as e:
            self.adicionar_log(f"✗ ERRO AO SALVAR: {str(e)}")
            return False

    def atualizar_status(self, mensagem):
        """Atualizar label de status"""
        self.status_label.config(text=mensagem)
        self.root.update_idletasks()

    def processar_ocr_thread(self):
        """Executar OCR em thread separada para não travar a interface"""
        thread = threading.Thread(target=self.processar_ocr)
        thread.daemon = True
        thread.start()

    def processar_ocr(self):
        """Função principal para processar OCR"""
        self.adicionar_log("=== INICIANDO PROCESSO COMPLETO ===")
        
        # Validar entradas
        api_key = self.api_key_entry.get().strip()
        file_path = self.file_path_entry.get().strip()

        if not api_key:
            self.adicionar_log("✗ ERRO: API Key não fornecida")
            messagebox.showerror("Erro", "Por favor, insira a API Key.")
            return

        if not file_path or not os.path.isfile(file_path):
            self.adicionar_log("✗ ERRO: Arquivo PDF não selecionado ou inválido")
            messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF válido.")
            return

        self.adicionar_log(f"API Key: {'*' * (len(api_key)-4) + api_key[-4:]}")  # Mostrar apenas últimos 4 chars
        self.adicionar_log(f"Arquivo: {file_path}")

        # Desabilitar botão durante processamento
        self.processar_button.config(state=tk.DISABLED, text="PROCESSANDO...")
        
        try:
            # Etapa 1: Upload
            self.atualizar_status("Fazendo upload...")
            upload_result = self.upload_arquivo(file_path, api_key)
            
            if not upload_result:
                self.adicionar_log("✗ FALHA NO UPLOAD - Processo interrompido")
                messagebox.showerror("Erro", "Falha no upload do arquivo. Verifique o log para detalhes.")
                return

            file_id = upload_result.get("id")
            if not file_id:
                self.adicionar_log("✗ ERRO: ID do arquivo não encontrado na resposta")
                self.adicionar_log(f"Resposta completa: {upload_result}")
                messagebox.showerror("Erro", "ID do arquivo não encontrado.")
                return

            self.adicionar_log(f"✓ File ID obtido: {file_id}")

            # Etapa 2: Processar OCR
            self.atualizar_status("Processando OCR...")
            ocr_result = self.processar_ocr_arquivo(file_id, api_key)
            
            if not ocr_result:
                self.adicionar_log("✗ FALHA NO PROCESSAMENTO OCR")
                messagebox.showerror("Erro", "Falha no processamento OCR. Verifique o log para detalhes.")
                return

            # Etapa 3: Salvar resultados
            self.atualizar_status("Salvando resultados...")
            if self.salvar_resultados(ocr_result, file_path):
                self.adicionar_log("=== PROCESSO CONCLUÍDO COM SUCESSO! ===")
                messagebox.showinfo("Sucesso!", 
                                   f"OCR processado com sucesso!\n\n"
                                   f"Arquivos salvos em:\n{self.pasta_destino}")
                self.atualizar_status("✓ Processo concluído com sucesso!")
            else:
                self.adicionar_log("✗ FALHA AO SALVAR RESULTADOS")
                messagebox.showerror("Erro", "Falha ao salvar os resultados.")

        except Exception as e:
            self.adicionar_log(f"✗ ERRO INESPERADO: {str(e)}")
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            self.atualizar_status(f"Erro: {str(e)}")
        
        finally:
            # Reabilitar botão
            self.processar_button.config(state=tk.NORMAL, text="PROCESSAR OCR")

def main():
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
