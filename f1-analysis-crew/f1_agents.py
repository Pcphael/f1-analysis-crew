"""
F1 Analysis Crew - Versão Final Corrigida
"""

import os
import fastf1
import fastf1.plotting
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')


class BaseAgent:
    def __init__(self, name):
        self.name = name

    def log(self, message):
        print(f"[{self.name}] {message}")


class ReporterAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reporter Agent")

    def generate_daily_report(self):
        news = [
            "McLaren lidera desenvolvimento para 2026",
            "Verstappen comenta sobre o novo regulamento",
            "Ferrari apresenta atualizações no SF-25",
            "Mercedes trabalha em nova suspensão traseira"
        ]
        report = f"""# 🏎️ INFORMATIVO DIÁRIO F1
**Data:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}

## Principais destaques da semana

"""
        for i, title in enumerate(news, 1):
            report += f"**{i}.** {title}\n\n"
        return report


class EngineerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Engineer Agent")

    def analyze_aerodynamics_and_speed(self, year=2025, gp="Monaco", session="Q"):
        self.log(f"Carregando {gp} {year} - {session}...")

        try:
            session_data = fastf1.get_session(year, gp, session)
            session_data.load()

            laps = session_data.laps.pick_quicklaps().reset_index(drop=True)
            fastest = laps.loc[laps.groupby('Driver')['LapTime'].idxmin()]

            drivers = ['VER', 'NOR', 'LEC', 'PIA', 'HAM']
            telemetry_data = []

            for driver in drivers:
                try:
                    lap = session_data.laps.pick_driver(driver).pick_fastest()
                    tel = lap.get_car_data().add_distance()
                    max_speed = tel['Speed'].max()
                    telemetry_data.append({
                        'driver': driver,
                        'team': lap['Team'],
                        'top_speed': max_speed
                    })
                except:
                    continue

            df = pd.DataFrame(telemetry_data)

            import os
            os.makedirs("reports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")

            plt.figure(figsize=(10, 6))
            plt.bar(df['driver'], df['top_speed'], color='#1E40AF')
            plt.title(f'Top Speed Real - {gp} {year} ({session})', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            plt.tight_layout()
            speed_path = f"reports/real_speed_{timestamp}.png"
            plt.savefig(speed_path, dpi=150, bbox_inches='tight')
            plt.close()

            analysis = f"""# 🔧 ANÁLISE TÉCNICA REAL (FastF1)

**Sessão:** {gp} {year} - {session}

## Velocidade Máxima Real (km/h)
"""
            for _, row in df.iterrows():
                analysis += f"- **{row['driver']}** ({row['team']}): {row['top_speed']:.1f} km/h\n"

            analysis += f"\n**Gráfico:** {speed_path}\n"
            return {'text': analysis, 'charts': {'speed': speed_path}}

        except Exception as e:
            self.log(f"Erro: {e} → Usando dados simulados")
            return self._get_simulated_data()

    def _get_simulated_data(self):
        data = {
            'driver': ['VER', 'NOR', 'LEC', 'PIA', 'HAM'],
            'team': ['Red Bull', 'McLaren', 'Ferrari', 'McLaren', 'Mercedes'],
            'top_speed': [345, 342, 338, 341, 336]
        }
        df = pd.DataFrame(data)

        import os
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        plt.figure(figsize=(10, 6))
        plt.bar(df['driver'], df['top_speed'], color='#1E40AF')
        plt.title('Top Speed (Simulado)', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = f"reports/sim_speed_{timestamp}.png"
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()

        analysis = f"""# 🔧 ANÁLISE TÉCNICA (Fallback)

## Velocidade Máxima (km/h)
- VER (Red Bull): 345 km/h
- NOR (McLaren): 342 km/h
- PIA (McLaren): 341 km/h

**Gráfico:** {path}
"""
        return {'text': analysis, 'charts': {'speed': path}}


class RegulatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Regulator Agent")

    def get_weekend_schedule(self):
        return """# 📋 PASSO A PASSO - FINAL DE SEMANA DE GRANDE PRÊMIO

## Quinta-feira → FP1
## Sexta-feira → FP2
## Sábado → FP3 + Classificação
## Domingo → Largada 14h

**Regras importantes:**
- Parque Fechado
- Modos de Power Unit
- DRS
- Alocação de pneus
"""


class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Coordinator Agent")   # ← CORRIGIDO

    def generate_final_report(self, reporter, engineer, regulator):
        return f"""# 🏁 RELATÓRIO COMPLETO F1 ANALYSIS CREW (FastF1)
**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

---

{reporter}

---

{engineer['text']}

---

{regulator}

---
*Powered by FastF1 + Grok (xAI)*
"""


def create_f1_crew():
    return {
        'reporter': ReporterAgent(),
        'engineer': EngineerAgent(),
        'regulator': RegulatorAgent(),
        'coordinator': CoordinatorAgent()
    }