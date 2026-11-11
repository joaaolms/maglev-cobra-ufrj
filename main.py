'''
Arquivo: main.py 
Descrição: Ponto de entrada principal da simulação do MagLev-Cobra (UFRJ). Integra os módulos de levitação, motorização, veículo e linha
'''

from src.modulo_maglev import ModuloMagLev 
from src.linha_maglev import LinhaMagLev 

def executar_simulacao(): 
    print("=" * 60) 
    print(" SIMULADOR DE OPERAÇÃO MAGLEV-COBRA (UFRJ - CAMPUS FUNDÃO)") 
    print("=" * 60) 
    
    # Instanciação do veículo e da linha de via única 
    cobra = ModuloMagLev(id_modulo="Cobra-01", massa_vazia_kg=1250.0, capacidade_max=30) 
    linha_fundao = LinhaMagLev(nome_linha="Linha 1 - Via Única Fundão") 
    
    # Execução da simulação de 1 ciclo completo (Ida: Reitoria -> HU | Volta: HU -> Reitoria) 
    velocidade_operacao_kmh = 45.0 
    df_resultado = linha_fundao.simular_ciclo_completo(cobra, num_ciclos=1, velocidade_kmh=velocidade_operacao_kmh) 
    
    # Exibição dos resultados
    print("\n" + "=" * 60) 
    print(" RESUMO EXECUTIVO DA VIAGEM DE TELEMETRIA") 
    print("=" * 60) 
    
    if not df_resultado.empty: 
        consumo_total_kwh = df_resultado["consumo_kwh"].sum() 
        distancia_total_km = df_resultado["distancia_m"].sum() / 1000.0 
        tempo_total_min = df_resultado["tempo_s"].sum() / 60.0 
        ln2_final_l = df_resultado["nivel_ln2_restante_l"].iloc[-1] 
        
        print(f"🔹 Percurso Total Percorrido: {distancia_total_km:.2f} km") 
        print(f"⏱️ Tempo Total em Movimento: {tempo_total_min:.1f} minutos") 
        print(f"⚡ Consumo Elétrico Total do Motor: {consumo_total_kwh:.3f} kWh") 
        print(f"❄️ Nível de LN2 Restante no Criostato: {ln2_final_l:.1f} Litros") 
        
        linha_fundao.salvar_telemetria_csv("data/telemetria_viagem.csv") 
    else: 
        print("A simulação foi encerrada prematuramente por falha técnica.") 

if __name__ == "__main__": 
    executar_simulacao()