'''
Módulo: criostato.py
Descrição: Modela o bloco supercondutor HTS (High-Temperature Superconductor) e o sistema de refrigeração por Nitrogênio Líquido (LN2) do MagLev-Cobra
'''

class CriostatoHTS:
    def __init__(self, temp_critica_k: float = 92.0, cap_max_ln2_l: float = 50.0):
        '''
        Inicializa o módulo de levitação supercondutora
        :param temp_critica_k: Temperatura crítica do supercondutor YBCO (Padrão: 92 K / ~-181 °C)
        :param cap_max_ln2_l: Capacidade máxima do reservatório de Nitrogênio Líquido (LN2) em Litros
        '''
        self.temp_critica_k = temp_critica_k
        self.cap_max_ln2_l = cap_max_ln2_l
        self.nivel_ln2_l = cap_max_ln2_l
        self.temperatura_k = 77.0 # Temperatura de ebulição do LN2 (77 Kelvin / -196 °C)
        self.altura_base_mm = 10.0

    def esta_supercondutendo(self) -> bool:
        '''
        Verifica se o bloco está na fase supercondutora (abaixo da Temp. Crítica com LN2)
        '''
        return (self.temperatura_k < self.temp_critica_k) and (self.nivel_ln2_l > 0)

    def calcular_altura_levitacao_mm(self, massa_total_kg: float) -> float:
        '''
        Calcula a altura de levitação (mm) considerando o aprisionamento de fluxo magnético. Quanto maior a carga, menor a distância do trilho. Se perder a supercondutividade, cai para 0 
        '''
        if not self.esta_supercondutendo(): return 0.0 # Perda de levitação (perigo de contato com o trilho) 
        
        # Redução da altura com base no peso embarcado (aproximação física simples)
        deformacao_mm = massa_total_kg / 250.0 
        altura_efetiva = self.altura_base_mm - deformacao_mm 
        # Limite mínimo de segurança mecânica (3.0 mm) 
        return max(3.0, round(altura_efetiva, 2))

    def refrigera_sistema(self, litros: float): 
        '''
        Reabastece o reservatório de Nitrogênio Líquido
        '''
        self.nivel_ln2_l = min(self.cap_max_ln2_l, self.nivel_ln2_l + litros)
        self.temperatura_k = 77.0
        print(f"Refrigeração concluída. Reservatório em {self.nivel_ln2_l:.1f}L ({self.temperatura_k}K).")

    def simular_consumo_evaporacao(self, tempo_segundos: float): 
        '''
        Simula a evaporação natural do LN2 e o aumento de temperatura se o reservatório esvaziar
        ''' 
        taxa_evaporacao_l_s = 0.05 # 0.05 L por segundo de operação
        consumido = tempo_segundos * taxa_evaporacao_l_s 
        self.nivel_ln2_l = max(0.0, self.nivel_ln2_l - consumido)

        # Se zerar o LN2, a temperatura sobe gradualmente para a ambiente (300K)
        if self.nivel_ln2_l == 0:
            self.temperatura_k += tempo_segundos * 0.5
            if self.temperatura_k > 300.0:
                self.temperatura_k = 300.0

    def __str__(self) -> str:
         status = "OPERANCIAL (SUPERCONDUTOR)" if self.esta_supercondutendo() else "FALHA DE LEVITAÇÃO" 
         return f"[Criostato HTS] Temp: {self.temperatura_k:.1f}K | Nível LN2: {self.nivel_ln2_l:.1f}L | Status: {status}"

# --- Bloco de Testes Rápidos --- 
if __name__ == "__main__": 
    print("=== TESTANDO A CLASSE CRATESTATO HTS ===") 
    criostato = CriostatoHTS() 
    print(criostato)
    print(f"Altura de levitação com 1500 kg: {criostato.calcular_altura_levitacao_mm(1500)} mm") 
    
    print("\\nSimulando evaporação de LN2 por 800 segundos...") 
    criostato.simular_consumo_evaporacao(800) 
    print(criostato) 
    print(f"Altura de levitação após evaporação: {criostato.calcular_altura_levitacao_mm(1500)} mm")