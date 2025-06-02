import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Definir Universos de Discurso
dist_universe = np.arange(0, 21, 1)  # 0 a 20 metros
vel_atual_universe = np.arange(0, 101, 1) # 0 a 100 km/h
vel_ajustada_universe = np.arange(0, 61, 1) # 0 a 60 km/h
direcao_universe = np.arange(-45, 46, 1) # -45 a 45 graus

# 2. Definir Variáveis Fuzzy (Antecedents & Consequents)
distancia = ctrl.Antecedent(dist_universe, 'distancia')
velocidade_atual = ctrl.Antecedent(vel_atual_universe, 'velocidade_atual')

velocidade_ajustada = ctrl.Consequent(vel_ajustada_universe, 'velocidade_ajustada', defuzzify_method='centroid')
direcao = ctrl.Consequent(direcao_universe, 'direcao', defuzzify_method='centroid')

# 3. Definir Funções de Pertinência
# Distância
distancia['Muito Perto'] = fuzz.trapmf(distancia.universe, [0, 0, 1, 2])
distancia['Moderada'] = fuzz.trapmf(distancia.universe, [1, 2, 5, 6])
distancia['Distante'] = fuzz.trapmf(distancia.universe, [5, 6, 20, 20])

# Velocidade Atual
velocidade_atual['Baixa'] = fuzz.trapmf(velocidade_atual.universe, [0, 0, 10, 20])
velocidade_atual['Média'] = fuzz.trapmf(velocidade_atual.universe, [10, 20, 40, 50])
velocidade_atual['Alta'] = fuzz.trapmf(velocidade_atual.universe, [40, 50, 100, 100])

# Velocidade Ajustada
velocidade_ajustada['Baixa'] = fuzz.trimf(velocidade_ajustada.universe, [0, 0, 10])
velocidade_ajustada['Média'] = fuzz.trimf(velocidade_ajustada.universe, [10, 25, 40])
velocidade_ajustada['Alta'] = fuzz.trimf(velocidade_ajustada.universe, [40, 60, 60])

# Direção
direcao['Esquerda'] = fuzz.trimf(direcao.universe, [-45, -30, 0])
direcao['Reto'] = fuzz.trimf(direcao.universe, [-15, 0, 15])
direcao['Direita'] = fuzz.trimf(direcao.universe, [0, 30, 45])

# 4. Definir Regras Fuzzy
# Regras para Velocidade Ajustada
rule1_vel = ctrl.Rule(distancia['Muito Perto'] & velocidade_atual['Alta'], velocidade_ajustada['Baixa'])
rule2_vel = ctrl.Rule(distancia['Moderada'] & velocidade_atual['Média'], velocidade_ajustada['Média'])
rule3_vel = ctrl.Rule(distancia['Distante'] & velocidade_atual['Baixa'], velocidade_ajustada['Média'])
rule4_vel = ctrl.Rule(distancia['Muito Perto'] & velocidade_atual['Baixa'], velocidade_ajustada['Baixa'])
rule5_vel = ctrl.Rule(distancia['Moderada'] & velocidade_atual['Alta'], velocidade_ajustada['Média'])

# Regras para Direção
rule1_dir = ctrl.Rule(distancia['Moderada'], direcao['Reto']) # Regra 6 original
rule2_dir = ctrl.Rule(distancia['Muito Perto'], direcao['Reto']) # Regra 7 original

# A Regra 8 original ("Se distância é moderada e velocidade é baixa, então direção deve ser Esquerda OU Direita (dependendo do obstáculo)")
# é ambígua para uma única saída determinística sem informação adicional sobre o obstáculo.
# Se interpretada como duas regras separadas (ativando Esquerda E Direita com a mesma premissa), seria:
# rule3_dir_esq = ctrl.Rule(distancia['Moderada'] & velocidade_atual['Baixa'], direcao['Esquerda'])
# rule3_dir_dir = ctrl.Rule(distancia['Moderada'] & velocidade_atual['Baixa'], direcao['Direita'])
# No entanto, para as entradas dadas (Velocidade Baixa = 0), estas regras não seriam ativadas.
# Para este exemplo, vamos nos ater às regras que podem ser diretamente implementadas e são ativadas.

# 5. Criar o Sistema de Controle
# Sistema de controle para velocidade
control_velocidade = ctrl.ControlSystem([rule1_vel, rule2_vel, rule3_vel, rule4_vel, rule5_vel])
simulacao_velocidade = ctrl.ControlSystemSimulation(control_velocidade)

# Sistema de controle para direção
# Adicionar rule3_dir_esq e rule3_dir_dir se a interpretação da Regra 8 for essa.
control_direcao = ctrl.ControlSystem([rule1_dir, rule2_dir])
simulacao_direcao = ctrl.ControlSystemSimulation(control_direcao)


# 6. Passar Entradas para o Sistema e Calcular Saída
# Entradas
input_distancia = 3  # metros
input_velocidade_atual = 20 # km/h

# Simulação para Velocidade Ajustada
simulacao_velocidade.input['distancia'] = input_distancia
simulacao_velocidade.input['velocidade_atual'] = input_velocidade_atual
simulacao_velocidade.compute()
output_velocidade_ajustada = simulacao_velocidade.output['velocidade_ajustada']
print(f"Velocidade Ajustada Calculada (Python): {output_velocidade_ajustada:.2f} km/h")
# velocidade_ajustada.view(sim=simulacao_velocidade) # Para visualizar

# Simulação para Direção
simulacao_direcao.input['distancia'] = input_distancia
# A velocidade atual só é necessária para a direção se a Regra 8 (ou suas variantes) for incluída
# simulacao_direcao.input['velocidade_atual'] = input_velocidade_atual
simulacao_direcao.compute()
output_direcao = simulacao_direcao.output['direcao']
print(f"Direção Calculada (Python): {output_direcao:.2f} graus")
# direcao.view(sim=simulacao_direcao) # Para visualizar

# plt.show() # Para exibir os gráficos se .view() for chamado