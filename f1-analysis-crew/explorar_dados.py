import fastf1
import pandas as pd

# Carrega a sessão que está no cache
session = fastf1.get_session(2026, "Japanese Grand Prix", "Q")
session.load()

print("=== Informações da Sessão ===")
print(session)

print("\n=== Melhores voltas ===")
print(session.laps.pick_quicklaps().head(10))

print("\n=== Telemetria do Verstappen (primeira volta rápida) ===")
ver_lap = session.laps.pick_driver('VER').pick_fastest()
tel = ver_lap.get_car_data().add_distance()
print(tel[['Distance', 'Speed', 'Throttle', 'Brake']].head(20))