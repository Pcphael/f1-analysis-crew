"""
F1 Analysis Crew - Script Principal
"""

from f1_agents import create_f1_crew
from datetime import datetime
import os

def run_f1_analysis(weekend_mode: bool = True):
    print("=" * 70)
    print("🏎️ F1 ANALYSIS CREW - INICIANDO ANÁLISE")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    crew = create_f1_crew()
    
    print("\n[1/4] Reporter Agent trabalhando...")
    reporter_report = crew['reporter'].generate_daily_report()
    
    engineer_report = ""
    regulator_report = ""
    
    if weekend_mode:
        print("\n[2/4] Engineer Agent analisando telemetria...")
        engineer_result = crew['engineer'].analyze_aerodynamics_and_speed()
        engineer_report = engineer_result['text']
        
        print("\n[3/4] Regulator Agent verificando regulamentos...")
        regulator_report = crew['regulator'].get_weekend_schedule()
    
    print("\n[4/4] Coordinator Agent gerando relatório final...")
    final_report = crew['coordinator'].generate_final_report(
        reporter_report, engineer_report, regulator_report
    )
    
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/f1_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_report)
    
    print(f"\n✅ Relatório salvo em: {filename}")
    print("=" * 70)
    print("\n" + final_report)
    
    return final_report


if __name__ == "__main__":
    run_f1_analysis(weekend_mode=True)