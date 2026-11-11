'''
Módulo: modulo_maglev.py 
Descrição: Modela o veículo MagLev-Cobra, integrando os sistemas de levitação (CriostatoHTS) e propulsão (MotorLinear) via Composição. 
''' 

try: 
    from src.criostato import CriostatoHTS 
    from src.motor import MotorLinear 
except ModuleNotFoundError: 
    from criostato import CriostatoHTS 
    from motor import MotorLinear 

class ModuloMagLev: 
    PESO_MEDIO_PASSAGEIRO_KG = 70.0 

    def __init__(self, id_modulo: str = "Cobra-01", massa_vazia_kg: float = 1200.0, capacidade_max: int = 30): 
        ''' 
        Inicializa o módulo do veículo. 
        :param id_modulo: Identificador do módulo (ex: "Cobra-01") 
        :param massa_vazia_kg: Massa do veículo sem passageiros (Padrão: 1200 kg) 
        :param capacidade_max: Lotação máxima de passageiros (Padrão: 30) 
        '''
        self.id_modulo = id_modulo 
        self.massa_vazia_kg = massa_vazia_kg 
        self.capacidade_max = capacidade_max 
        self.passageiros_atuais = 0 
        self.velocidade_kmh = 0.0 
        
        # COMPOSIÇÃO: O veículo tem um Criostato e um Motor Linear 
        self.criostato = CriostatoHTS() 
        self.motor = MotorLinear() 

    @property 
    def massa_total_kg(self) -> float: 
        '''
        Calcula a massa total do veículo (massa vazia + peso dos passageiros)
        ''' 
        return self.massa_vazia_kg + (self.passageiros_atuais * self.PESO_MEDIO_PASSAGEIRO_KG) 

    def embarcar_passageiros(self, quantidade: int) -> int: 
        '''
        Embarca passageiros respeitando a capacidade máxima
        ''' 
        espaco_disponivel = self.capacidade_max - self.passageiros_atuais 
        embarcados = min(quantidade, espaco_disponivel) 
        self.passageiros_atuais += embarcados 
        
        if embarcados < quantidade: 
            print(f"Lotação máxima atingida! {quantidade - embarcados} passageiros aguardam o próximo módulo.") 
        
        print(f"{embarcados} passageiros embarcaram no {self.id_modulo}. (Total: {self.passageiros_atuais}/{self.capacidade_max})") 
        return embarcados 

    def desembarcar_passageiros(self, quantidade: int) -> int: 
        '''
        Desembarca passageiros do veículo
        ''' 
        desembarcados = min(quantidade, self.passageiros_atuais) 
        self.passageiros_atuais -= desembarcados 
        
        print(f"{desembarcados} passageiros desembarcaram do {self.id_modulo}. (Restantes: {self.passageiros_atuais})") 
        return desembarcados 

    def mover_trecho(self, distancia_m: float, velocidade_alvo_kmh: float) -> dict: 
        ''' 
        Simula o movimento do módulo em um trecho entre estações. 
        :param distancia_m: Distância em metros 
        :param velocidade_alvo_kmh: Velocidade de cruzeiro no trecho 
        :return: Dicionário com a telemetria do percurso 
        ''' 
        if not self.criostato.esta_supercondutendo(): 
            print(f"ERRO DE SEGURANÇA: {self.id_modulo} não pode operar sem supercondutividade!") 
            return {"sucesso": False, "motivo": "Perda de levitação magnética"} 
            
        self.velocidade_kmh = velocidade_alvo_kmh 
        tempo_segundos = (distancia_m / (velocidade_alvo_kmh / 3.6)) # t = d / v 
        
        # Chama os métodos dos componentes do veículo 
        consumo_kwh = self.motor.calcular_consumo_kwh(velocidade_alvo_kmh, tempo_segundos) 
        self.criostato.simular_consumo_evaporacao(tempo_segundos) 
        altura_levitacao_mm = self.criostato.calcular_altura_levitacao_mm(self.massa_total_kg) 
        
        self.velocidade_kmh = 0.0 # Veículo para ao chegar na próxima estação 
        
        telemetria = { 
            "sucesso": True, 
            "distancia_m": distancia_m, 
            "tempo_s": round(tempo_segundos, 1), 
            "velocidade_kmh": velocidade_alvo_kmh, 
            "consumo_kwh": consumo_kwh, 
            "altura_levitacao_mm": altura_levitacao_mm, 
            "nivel_ln2_restante_l": round(self.criostato.nivel_ln2_l, 1), 
            "massa_total_kg": self.massa_total_kg 
        } 
        return telemetria 

    def __str__(self) -> str: 
        altura = self.criostato.calcular_altura_levitacao_mm(self.massa_total_kg) 
        return (f"[{self.id_modulo}] Carga: {self.passageiros_atuais}/{self.capacidade_max} pax " 
                f"({self.massa_total_kg:.0f} kg) | Altura Levitação: {altura} mm") 

# --- Bloco de Testes Rápidos --- 
if __name__ == "__main__": 
    print("=== TESTANDO A CLASSE MODULO MAGLEV ===") 
    modulo = ModuloMagLev("Cobra-Fundão", massa_vazia_kg=1300.0, capacidade_max=30) 
    print(modulo) 
    
    print("\n1. Embarcando passageiros no CT:") 
    modulo.embarcar_passageiros(22) 
    print(modulo) 
    
    print("\n2. Executando trecho CT -> Hospital Universitário (1200m a 40 km/h):") 
    res = modulo.mover_trecho(distancia_m=1200.0, velocidade_alvo_kmh=40.0) 
    print("Telemetria do Trecho:", res) 
    print(modulo)