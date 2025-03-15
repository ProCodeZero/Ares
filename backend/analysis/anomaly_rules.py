# Простые правила для MVP
def detect_speed_anomaly(speed):
    # Аномалия: скорость > 100 км/ч
    return speed > 100

def detect_geofence_anomaly(latitude, longitude):
    # Аномалия: выход за пределы геозоны (пример для Москвы)
    return not (55.0 <= latitude <= 56.0 and 37.0 <= longitude <= 38.0)