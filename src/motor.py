'''
Módulo: motor.py
Descrição: Modela o Motor de Indução Linear (LIM) do MagLev-Cobra, responsável pela propulsão e pelo consumo de energia elétrica
'''

class MotorLinear: 
    def __init__(self, potencia_nominal_kw: float = 120.0, eficiencia: float = 0.88): 
        '''
        Inicializa o motor linear
        :param potencia_nominal_kw: Potência máxima em kW (Padrão: 120 kW) 
        :param eficiencia: Eficiência energética do motor (0 a 1, Padrão: 88%) 
        '''
        self.potencia_nominal_kw = potencia_nominal_kw 
        self.eficiencia = eficiencia 
        self.frequencia_hz = 0.0 
        self.em_operacao = False 

    def ajustar_velocidade_frequencia(self, velocidade_alvo_kmh: float): 
        '''
        Ajusta a frequência do inversor para controlar a velocidade do veículo
        ''' 
        if velocidade_alvo_kmh <= 0: 
            self.frequencia_hz = 0.0 
            self.em_operacao = False 
        else: 
            self.em_operacao = True 
            # Relação entre frequência de alimentação e velocidade do campo magnético 
            self.frequencia_hz = round(velocidade_alvo_kmh * 1.2, 2) 

    def calcular_consumo_kwh(self, velocidade_kmh: float, tempo_segundos: float) -> float: 
        '''
        Calcula a energia elétrica consumida (kWh) em um trecho de simulação.
        '''
        if velocidade_kmh <= 0 or tempo_segundos <= 0: 
            return 0.0 
        
        self.ajustar_velocidade_frequencia(velocidade_kmh) 
        
        # Potência consumida proporcional à velocidade de operação e à eficiência 
        fator_carga = min(1.0, velocidade_kmh / 70.0) # 70 km/h como velocidade máx nominal 
        potencia_efetiva_kw = (self.potencia_nominal_kw * fator_carga) / self.eficiencia 
        horas = tempo_segundos / 3600.0 
        consumo_kwh = potencia_efetiva_kw * horas 
        
        return round(consumo_kwh, 3) 

    def __str__(self) -> str: 
        status = f"EM OPERAÇÃO ({self.frequencia_hz} Hz)" if self.em_operacao else "DESLIGADO" 
        return f"[Motor Linear LIM] Potência: {self.potencia_nominal_kw} kW | Eficiência: {self.eficiencia*100:.0f}% | Status: {status}" 

# --- Bloco de Testes Rápidos --- 
if __name__ == "__main__": 
    print("=== TESTANDO A CLASSE MOTOR LINEAR ===") 
    motor = MotorLinear() 
    print(motor) 
    consumo = motor.calcular_consumo_kwh(velocidade_kmh=40.0, tempo_segundos=120) 
    print(f"Consumo em percurso de 120s a 40 km/h: {consumo} kWh") 
    print(motor)