"""
F1 Analysis Crew - GUI com Seleção de Grande Prêmio
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from f1_agents import create_f1_crew

# Lista de Grandes Prêmios da temporada 2026
GRAND_PRIX_2026 = [
    "Bahrain", "Saudi Arabia", "Australia", "Japan", "China",
    "Miami", "Emilia Romagna", "Monaco", "Canada", "Spain",
    "Austria", "Great Britain", "Hungary", "Belgium", "Netherlands",
    "Italy", "Azerbaijan", "Singapore", "United States", "Mexico",
    "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"
]

class F1AnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏎️ F1 Analysis Crew - FastF1 Edition")
        self.root.geometry("980x780")
        
        self.crew = None
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        ttk.Label(self.root, text="🏎️ F1 Analysis Crew", font=("Arial", 22, "bold")).pack(pady=10)
        ttk.Label(self.root, text="Análise com FastF1 - Dados Reais", font=("Arial", 12)).pack()
        
        # === CONFIGURAÇÕES ===
        config_frame = ttk.LabelFrame(self.root, text="⚙️ Configurações FastF1", padding=15)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        # Linha 1
        row1 = ttk.Frame(config_frame)
        row1.pack(fill="x", pady=8)
        
        ttk.Label(row1, text="Ano:").pack(side="left", padx=5)
        self.year_var = tk.StringVar(value="2026")
        ttk.Entry(row1, textvariable=self.year_var, width=8).pack(side="left", padx=5)
        
        ttk.Label(row1, text="Grande Prêmio:").pack(side="left", padx=15)
        
        # DROPDOWN DE GRANDES PRÊMIOS
        self.gp_var = tk.StringVar(value="Monaco")
        gp_combo = ttk.Combobox(row1, textvariable=self.gp_var, values=GRAND_PRIX_2026, width=22, state="readonly")
        gp_combo.pack(side="left", padx=5)
        
        # Linha 2
        row2 = ttk.Frame(config_frame)
        row2.pack(fill="x", pady=8)
        
        ttk.Label(row2, text="Sessão:").pack(side="left", padx=5)
        self.session_var = tk.StringVar(value="Q")
        session_combo = ttk.Combobox(row2, textvariable=self.session_var, 
                                     values=["FP1", "FP2", "FP3", "Q", "R"], width=8, state="readonly")
        session_combo.pack(side="left", padx=5)
        
        ttk.Label(row2, text="(Q = Qualifying | R = Race)").pack(side="left", padx=10)
        
        # === BOTÕES ===
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=12)
        
        ttk.Button(btn_frame, text="📰 Relatório Diário", command=self.run_reporter, width=20).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="🔧 Análise Técnica (FastF1)", command=self.run_engineer, width=26).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="🏁 RODAR TUDO", command=self.run_full, width=18).pack(side="left", padx=8)
        
        # === LOG ===
        log_frame = ttk.LabelFrame(self.root, text="📋 Status e Resultados", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=24, font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True)
        
        ttk.Button(self.root, text="📂 Abrir Pasta de Relatórios", command=self.open_reports_folder).pack(pady=10)
        
        self.log("✅ Interface carregada com seleção de Grandes Prêmios!")
        self.log("Escolha a corrida no menu suspenso acima e clique em 'Análise Técnica'")
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def run_reporter(self):
        self.log("📰 Gerando relatório diário...")
        threading.Thread(target=self._run_reporter, daemon=True).start()
        
    def _run_reporter(self):
        if not self.crew:
            self.crew = create_f1_crew()
        report = self.crew['reporter'].generate_daily_report()
        self._save_report("daily", report)
        self.log("✅ Relatório diário gerado!")
        
    def run_engineer(self):
        year = int(self.year_var.get())
        gp = self.gp_var.get()
        session = self.session_var.get()
        
        self.log(f"🔧 Analisando {gp} {year} ({session}) com FastF1...")
        threading.Thread(target=self._run_engineer, args=(year, gp, session), daemon=True).start()
        
    def _run_engineer(self, year, gp, session):
        if not self.crew:
            self.crew = create_f1_crew()
        try:
            result = self.crew['engineer'].analyze_aerodynamics_and_speed(year=year, gp=gp, session=session)
            self._save_report("technical", result['text'])
            self.log("✅ Análise concluída com dados reais!")
        except Exception as e:
            self.log(f"❌ Erro: {str(e)}")
            
    def run_full(self):
        self.log("🏁 Executando análise completa...")
        threading.Thread(target=self._run_full, daemon=True).start()
        
    def _run_full(self):
        if not self.crew:
            self.crew = create_f1_crew()
        reporter = self.crew['reporter'].generate_daily_report()
        engineer = self.crew['engineer'].analyze_aerodynamics_and_speed(
            year=int(self.year_var.get()), gp=self.gp_var.get(), session=self.session_var.get()
        )
        regulator = self.crew['regulator'].get_weekend_schedule()
        final = self.crew['coordinator'].generate_final_report(reporter, engineer, regulator)
        self._save_report("full", final)
        self.log("✅ Relatório completo gerado!")
        
    def _save_report(self, prefix, content):
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/{prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        self.log(f"📄 Salvo: {filename}")
        
    def open_reports_folder(self):
        path = os.path.abspath("reports")
        if os.name == 'nt':
            os.startfile(path)
        else:
            os.system(f'xdg-open "{path}"')


if __name__ == "__main__":
    root = tk.Tk()
    app = F1AnalysisGUI(root)
    root.mainloop()