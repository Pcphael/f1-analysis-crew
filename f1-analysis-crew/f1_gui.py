"""
F1 Analysis Crew - Interface Gráfica (GUI)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from f1_agents import create_f1_crew

class F1AnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏎️ F1 Analysis Crew - Interface Gráfica")
        self.root.geometry("900x700")
        
        self.crew = None
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        ttk.Label(self.root, text="🏎️ F1 Analysis Crew", font=("Arial", 20, "bold")).pack(pady=15)
        ttk.Label(self.root, text="Sistema Inteligente de Análise de Fórmula 1", font=("Arial", 11)).pack()
        
        # Timeline
        etapas_frame = ttk.LabelFrame(self.root, text="📅 Etapas da Semana de Corrida", padding=15)
        etapas_frame.pack(fill="x", padx=20, pady=10)
        
        timeline = ttk.Frame(etapas_frame)
        timeline.pack()
        
        etapas = [
            ("Quinta", "FP1", "#3B82F6"),
            ("Sexta", "FP2", "#10B981"),
            ("Sábado", "FP3 + Classificação", "#F59E0B"),
            ("Domingo", "Grande Prêmio", "#EF4444")
        ]
        
        for dia, desc, color in etapas:
            box = tk.Frame(timeline, bg=color, padx=15, pady=8)
            box.pack(side="left", padx=8)
            tk.Label(box, text=dia, font=("Arial", 11, "bold"), bg=color, fg="white").pack()
            tk.Label(box, text=desc, font=("Arial", 9), bg=color, fg="white").pack()
        
        # Botões
        acoes_frame = ttk.LabelFrame(self.root, text="🚀 Executar Análises", padding=15)
        acoes_frame.pack(fill="x", padx=20, pady=10)
        
        btn_frame = ttk.Frame(acoes_frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="📰 Relatório Diário", command=self.run_reporter, width=22).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="🔧 Análise Técnica", command=self.run_engineer, width=22).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="🏁 RODAR TUDO", command=self.run_full, width=22).pack(side="left", padx=8)
        
        # Log
        log_frame = ttk.LabelFrame(self.root, text="📋 Status", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True)
        
        ttk.Button(self.root, text="📂 Abrir Pasta de Relatórios", command=self.open_reports).pack(pady=10)
        
        self.log("✅ Interface carregada com sucesso!")
        
    def log(self, msg):
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def run_reporter(self):
        self.log("📰 Gerando relatório diário...")
        threading.Thread(target=self._run_reporter, daemon=True).start()
        
    def _run_reporter(self):
        if not self.crew:
            self.crew = create_f1_crew()
        report = self.crew['reporter'].generate_daily_report()
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/daily_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        self.log(f"✅ Relatório salvo: {filename}")
        
    def run_engineer(self):
        self.log("🔧 Executando análise técnica...")
        threading.Thread(target=self._run_engineer, daemon=True).start()
        
    def _run_engineer(self):
        if not self.crew:
            self.crew = create_f1_crew()
        result = self.crew['engineer'].analyze_aerodynamics_and_speed()
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/technical_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result['text'])
        self.log("✅ Análise técnica concluída com gráficos!")
        
    def run_full(self):
        self.log("🏁 Executando análise completa...")
        threading.Thread(target=self._run_full, daemon=True).start()
        
    def _run_full(self):
        if not self.crew:
            self.crew = create_f1_crew()
        reporter = self.crew['reporter'].generate_daily_report()
        engineer = self.crew['engineer'].analyze_aerodynamics_and_speed()
        regulator = self.crew['regulator'].get_weekend_schedule()
        final = self.crew['coordinator'].generate_final_report(reporter, engineer, regulator)
        
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/full_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final)
        self.log(f"✅ Relatório completo salvo: {filename}")
        
    def open_reports(self):
        path = os.path.abspath("reports")
        if os.name == 'nt':
            os.startfile(path)
        else:
            os.system(f'xdg-open "{path}"')


if __name__ == "__main__":
    root = tk.Tk()
    app = F1AnalysisGUI(root)
    root.mainloop()