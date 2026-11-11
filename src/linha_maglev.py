'''
Módulo: linha_maglev.py 
Descrição: Gerencia a linha de via única (trilho único) do MagLev-Cobra no Fundão, executando o ciclo continuo de bate-e-volta (Reitoria <-> HU) e exportando os dados de telemetria para análise posterior
'''
import os
import pandas as pd 
from typing import List, Dict 

try: 
    from src.modulo_maglev import ModuloMagLev 
except ModuleNotFoundError: 
    from modulo_maglev import ModuloMagLev 

class LinhaMagLev: 
    def __init__(self, nome_linha: str = "Linha Via Única Fundão"): 
        self.nome_linha = nome_linha
        '''
        Inicializa o circuito com as estações e distâncias padrão da Cidade Universitária. 
        '''
        
        # Estações em ordem linear 
        self.estacoes = [ 
            {"nome": "Reitoria", "distancia_proxima_m": 2400.0}, # Reitoria -> CT
            {"nome": "Centro de Tecnologia (CT)", "distancia_proxima_m": 2600.0}, # CT -> EEFD
            {"nome": "EEFD / Educação Física", "distancia_proxima_m": 400.0}, # EEFD -> HU
            {"nome": "Hospital Universitário (HU)", "distancia_proxima_m": 0.0} # Estação Terminal
        ] 
        self.historico_telemetria: List[Dict] = []

    def executar_percurso_sentido(self, modulo: ModuloMagLev, sentido: str, velocidade_kmh: float): 
        '''
        Executa a viagem em um dos sentidos (IDA: Reitoria -> HU | VOLTA: HU -> Reitoria)
        ''' 
        estacoes_rota = self.estacoes.copy() if sentido == "IDA" else list(reversed(self.estacoes)) 
        
        print(f"\n[TRILHO ÚNICO - {sentido}] {modulo.id_modulo} partindo de {estacoes_rota[0]['nome']}...") 
        
        for i in range(len(estacoes_rota) - 1): 
            estacao_atual = estacoes_rota[i] 
            proxima_estacao = estacoes_rota[i + 1] 
            
            # Ajuste de distância dependendo da direção no trilho único 
            distancia_m = estacao_atual["distancia_proxima_m"] if sentido == "IDA" else proxima_estacao["distancia_proxima_m"] 
            
            print(f"\nParada em [{estacao_atual['nome']}]") 
            modulo.desembarcar_passageiros(5) 
            modulo.embarcar_passageiros(10) 
            print(f"⏩ Trecho [{estacao_atual['nome']}] -> [{proxima_estacao['nome']}] ({distancia_m}m)...") 
            
            telemetria = modulo.mover_trecho(distancia_m, velocidade_kmh) 
            
            if not telemetria["sucesso"]: 
                print(f"OPERAÇÃO INTERROMPIDA! Falha técnica no {modulo.id_modulo}.") 
                return False 
                
            telemetria["sentido"] = sentido 
            telemetria["estacao_origem"] = estacao_atual["nome"] 
            telemetria["estacao_destino"] = proxima_estacao["nome"] 
            telemetria["id_modulo"] = modulo.id_modulo 
            
            self.historico_telemetria.append(telemetria) 
            
        return True 

    def simular_ciclo_completo(self, modulo: ModuloMagLev, num_ciclos: int = 1, velocidade_kmh: float = 45.0): 
        '''
        Simula ciclos completos de Ida (Reitoria -> HU) e Volta (HU -> Reitoria) no mesmo trilho.
        '''
        print(f"\n=== INICIANDO OPERAÇÃO EM VIA ÚNICA (BATE-E-VOLTA) ===") 
        print(f"Veículo: {modulo.id_modulo} | Ciclos programados: {num_ciclos}\n" + "="*55) 
        
        for ciclo in range(1, num_ciclos + 1): 
            print(f"\n--- INICIANDO CICLO {ciclo}/{num_ciclos} ---") 
            
            # 1. Percurso de IDA (Reitoria -> HU) 
            ok_ida = self.executar_percurso_sentido(modulo, sentido="IDA", velocidade_kmh=velocidade_kmh) 
            if not ok_ida: 
                break 
                
            # 2. Percurso de VOLTA (HU -> Reitoria) pelo mesmo trilho 
            ok_volta = self.executar_percurso_sentido(modulo, sentido="VOLTA", velocidade_kmh=velocidade_kmh) 
            if not ok_volta: 
                break 
                
        print(f"\nOperação em via única finalizada.") 
        return self.obter_dataframe_telemetria() 

    def obter_dataframe_telemetria(self) -> pd.DataFrame: 
        return pd.DataFrame(self.historico_telemetria) 

    def salvar_telemetria_csv(self, caminho_arquivo: str = "data/telemetria_viagem.csv"): 
        df = self.obter_dataframe_telemetria() 
        if not df.empty: 
            pasta = os.path.dirname(caminho_arquivo) 
            if pasta: 
                os.makedirs(pasta, exist_ok=True) 
            df.to_csv(caminho_arquivo, index=False, encoding="utf-8") 
            print(f"\nTelemetria salva em: '{caminho_arquivo}'") 

# --- Teste do Ciclo em Trilho Único --- 
if __name__ == "__main__": 
    linha = LinhaMagLev() 
    cobra_01 = ModuloMagLev("Cobra-01", massa_vazia_kg=1250.0) 
    
    # Executa 1 ciclo completo de Ida e Volta 
    df_res = linha.simular_ciclo_completo(cobra_01, num_ciclos=1, velocidade_kmh=45.0) 
    
    print("\nTELEMETRIA REGISTRADA DO CICLO COMPLETO (PANDAS):") 
    print(df_res[["sentido", "estacao_origem", "estacao_destino", "consumo_kwh", "altura_levitacao_mm", "nivel_ln2_restante_l"]]) 
    
    linha.salvar_telemetria_csv()