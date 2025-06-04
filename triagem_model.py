import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class TriagemMedica:
    def __init__(self):
        """Inicializa o modelo de triagem médica"""
        self.base_conhecimento = self._carregar_base_conhecimento()
        self.historico_file = 'historico_atendimentos.json'
        self.historico = self._carregar_historico()
    
    def _carregar_base_conhecimento(self):
        """Carrega a base de conhecimento médico baseada nos dados fornecidos"""
        return {
            'doencas': {
                'leptospirose': {
                    'eventos_climaticos': ['enchentes', 'chuvas_intensas'],
                    'sintomas': ['febre', 'dor_muscular', 'dor_cabeca', 'nausea', 'vomito', 'ictericia', 'dor_abdominal'],
                    'sintomas_especificos': ['ictericia', 'oliguria', 'hemorragia'],
                    'medicamentos': {
                        'adulto': {'nome': 'Doxiciclina', 'dosagem': '100mg', 'frequencia': '2x/dia'},
                        'crianca': {'nome': 'Amoxicilina', 'dosagem': '50mg/kg', 'frequencia': '3x/dia'}
                    },
                    'incidencia_max': 0.02,
                    'populacao_risco': ['criancas', 'idosos', 'ribeirinhos'],
                    'gravidade': 'alta',
                    'tempo_incubacao': '2-30 dias'
                },
                'diarreia_infecciosa': {
                    'eventos_climaticos': ['enchentes', 'secas', 'chuvas_intensas'],
                    'sintomas': ['diarreia', 'vomito', 'febre', 'desidratacao', 'dor_abdominal', 'sangue_fezes'],
                    'sintomas_especificos': ['sangue_fezes', 'muco_fezes', 'tenesmo'],
                    'medicamentos': {
                        'adulto': {'nome': 'Sais de reidratação + Zinco', 'dosagem': '1 sachê + 20mg', 'frequencia': 'conforme necessário'},
                        'crianca': {'nome': 'Sais de reidratação + Zinco', 'dosagem': '1/2 sachê + 10mg', 'frequencia': 'conforme necessário'}
                    },
                    'incidencia_max': 0.15,
                    'populacao_risco': ['criancas', 'idosos', 'desnutridos'],
                    'gravidade': 'media',
                    'tempo_incubacao': '1-3 dias'
                },
                'malaria': {
                    'eventos_climaticos': ['calor_umidade', 'chuvas_intensas'],
                    'sintomas': ['febre', 'calafrios', 'sudorese', 'dor_cabeca', 'nausea', 'vomito', 'fadiga'],
                    'sintomas_especificos': ['febre_ciclica', 'esplenomegalia', 'anemia'],
                    'medicamentos': {
                        'adulto': {'nome': 'Cloroquina/Artesunato', 'dosagem': '600mg/120mg', 'frequencia': 'conforme protocolo'},
                        'crianca': {'nome': 'Cloroquina/Artesunato', 'dosagem': '10mg/kg', 'frequencia': 'conforme protocolo'}
                    },
                    'incidencia_max': 0.05,
                    'populacao_risco': ['comunidades_ribeirinhas', 'criancas'],
                    'gravidade': 'alta',
                    'tempo_incubacao': '7-30 dias'
                },
                'dengue': {
                    'eventos_climaticos': ['calor_umidade', 'chuvas_intensas'],
                    'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'manchas_pele', 'nausea', 'vomito', 'dor_retro_orbital'],
                    'sintomas_especificos': ['dor_retro_orbital', 'petequias', 'prova_laco_positiva'],
                    'medicamentos': {
                        'adulto': {'nome': 'Paracetamol + Hidratação', 'dosagem': '750mg', 'frequencia': '6/6h'},
                        'crianca': {'nome': 'Paracetamol + Hidratação', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                    },
                    'incidencia_max': 0.20,
                    'populacao_risco': ['criancas', 'idosos', 'comunidades_urbanas'],
                    'gravidade': 'alta',
                    'tempo_incubacao': '3-14 dias'
                },
                'infeccao_respiratoria': {
                    'eventos_climaticos': ['frio', 'umidade', 'ondas_calor'],
                    'sintomas': ['tosse', 'febre', 'dificuldade_respirar', 'dor_peito', 'fadiga', 'expectoracao'],
                    'sintomas_especificos': ['dispneia', 'cianose', 'tiragem'],
                    'medicamentos': {
                        'adulto': {'nome': 'Amoxicilina/Azitromicina', 'dosagem': '875mg/500mg', 'frequencia': '2x/dia'},
                        'crianca': {'nome': 'Amoxicilina/Azitromicina', 'dosagem': '45mg/kg', 'frequencia': '2x/dia'}
                    },
                    'incidencia_max': 0.30,
                    'populacao_risco': ['lactentes', 'idosos', 'desnutridos'],
                    'gravidade': 'media',
                    'tempo_incubacao': '1-7 dias'
                },
                'chikungunya': {
                    'eventos_climaticos': ['calor_umidade', 'chuvas_intensas'],
                    'sintomas': ['febre', 'dor_articular_intensa', 'dor_muscular', 'dor_cabeca', 'manchas_pele', 'fadiga'],
                    'sintomas_especificos': ['artralgia_simetrica', 'edema_articular', 'rigidez_matinal'],
                    'medicamentos': {
                        'adulto': {'nome': 'Paracetamol + Anti-inflamatório', 'dosagem': '750mg + 400mg', 'frequencia': '6/6h'},
                        'crianca': {'nome': 'Paracetamol', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                    },
                    'incidencia_max': 0.15,
                    'populacao_risco': ['adultos', 'idosos'],
                    'gravidade': 'media',
                    'tempo_incubacao': '2-12 dias'
                },
                'zika': {
                    'eventos_climaticos': ['calor_umidade', 'chuvas_intensas'],
                    'sintomas': ['febre_baixa', 'manchas_pele', 'conjuntivite', 'dor_articular', 'dor_cabeca'],
                    'sintomas_especificos': ['conjuntivite_nao_purulenta', 'exantema_pruriginoso'],
                    'medicamentos': {
                        'adulto': {'nome': 'Paracetamol + Hidratação', 'dosagem': '750mg', 'frequencia': '6/6h'},
                        'crianca': {'nome': 'Paracetamol + Hidratação', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                    },
                    'incidencia_max': 0.10,
                    'populacao_risco': ['gestantes', 'criancas'],
                    'gravidade': 'baixa',
                    'tempo_incubacao': '3-12 dias'
                },
                'febre_amarela': {
                    'eventos_climaticos': ['calor_umidade', 'chuvas_intensas'],
                    'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'nausea', 'vomito', 'ictericia', 'hemorragia'],
                    'sintomas_especificos': ['ictericia_progressiva', 'hemorragia_gengival', 'oliguria'],
                    'medicamentos': {
                        'adulto': {'nome': 'Suporte clínico + Hidratação', 'dosagem': 'Conforme necessário', 'frequencia': 'Contínuo'},
                        'crianca': {'nome': 'Suporte clínico + Hidratação', 'dosagem': 'Conforme necessário', 'frequencia': 'Contínuo'}
                    },
                    'incidencia_max': 0.01,
                    'populacao_risco': ['nao_vacinados', 'viajantes'],
                    'gravidade': 'critica',
                    'tempo_incubacao': '3-6 dias'
                },
                'hepatite_a': {
                    'eventos_climaticos': ['enchentes', 'secas', 'falta_saneamento'],
                    'sintomas': ['febre', 'fadiga', 'nausea', 'vomito', 'dor_abdominal', 'ictericia', 'urina_escura'],
                    'sintomas_especificos': ['ictericia_progressiva', 'acolia', 'coluria'],
                    'medicamentos': {
                        'adulto': {'nome': 'Suporte clínico + Repouso', 'dosagem': 'Conforme necessário', 'frequencia': 'Contínuo'},
                        'crianca': {'nome': 'Suporte clínico + Repouso', 'dosagem': 'Conforme necessário', 'frequencia': 'Contínuo'}
                    },
                    'incidencia_max': 0.08,
                    'populacao_risco': ['criancas', 'comunidades_sem_saneamento'],
                    'gravidade': 'media',
                    'tempo_incubacao': '15-50 dias'
                },
                'tuberculose': {
                    'eventos_climaticos': ['frio', 'umidade', 'aglomeracao'],
                    'sintomas': ['tosse_persistente', 'febre', 'sudorese_noturna', 'perda_peso', 'fadiga', 'expectoracao_sangue'],
                    'sintomas_especificos': ['tosse_mais_3_semanas', 'hemoptise', 'emagrecimento_progressivo'],
                    'medicamentos': {
                        'adulto': {'nome': 'RIPE (Rifampicina+Isoniazida+Pirazinamida+Etambutol)', 'dosagem': 'Conforme peso', 'frequencia': '1x/dia'},
                        'crianca': {'nome': 'RIP (Rifampicina+Isoniazida+Pirazinamida)', 'dosagem': 'Conforme peso', 'frequencia': '1x/dia'}
                    },
                    'incidencia_max': 0.05,
                    'populacao_risco': ['desnutridos', 'imunodeprimidos', 'idosos'],
                    'gravidade': 'alta',
                    'tempo_incubacao': '2-10 semanas'
                },
                'leishmaniose_visceral': {
                    'eventos_climaticos': ['secas', 'calor', 'areas_rurais'],
                    'sintomas': ['febre_prolongada', 'perda_peso', 'fadiga', 'aumento_baço', 'aumento_figado', 'anemia'],
                    'sintomas_especificos': ['esplenomegalia', 'hepatomegalia', 'pancitopenia'],
                    'medicamentos': {
                        'adulto': {'nome': 'Anfotericina B', 'dosagem': '3-5mg/kg', 'frequencia': 'Conforme protocolo'},
                        'crianca': {'nome': 'Anfotericina B', 'dosagem': '3-5mg/kg', 'frequencia': 'Conforme protocolo'}
                    },
                    'incidencia_max': 0.02,
                    'populacao_risco': ['criancas', 'desnutridos', 'imunodeprimidos'],
                    'gravidade': 'critica',
                    'tempo_incubacao': '2-8 meses'
                },
                'esquistossomose': {
                    'eventos_climaticos': ['enchentes', 'chuvas_intensas', 'areas_endemicas'],
                    'sintomas': ['febre', 'dor_abdominal', 'diarreia', 'sangue_fezes', 'fadiga', 'dor_muscular'],
                    'sintomas_especificos': ['hematuria', 'disuria', 'hepatomegalia'],
                    'medicamentos': {
                        'adulto': {'nome': 'Praziquantel', 'dosagem': '40mg/kg', 'frequencia': 'Dose única'},
                        'crianca': {'nome': 'Praziquantel', 'dosagem': '40mg/kg', 'frequencia': 'Dose única'}
                    },
                    'incidencia_max': 0.06,
                    'populacao_risco': ['criancas', 'comunidades_ribeirinhas'],
                    'gravidade': 'media',
                    'tempo_incubacao': '4-12 semanas'
                },
                'meningite_bacteriana': {
                    'eventos_climaticos': ['secas', 'aglomeracao', 'baixa_umidade'],
                    'sintomas': ['febre_alta', 'dor_cabeca_intensa', 'rigidez_nuca', 'vomito', 'confusao_mental', 'convulsoes'],
                    'sintomas_especificos': ['rigidez_nucal', 'kernig_positivo', 'brudzinski_positivo'],
                    'medicamentos': {
                        'adulto': {'nome': 'Ceftriaxona', 'dosagem': '2g', 'frequencia': '2x/dia EV'},
                        'crianca': {'nome': 'Ceftriaxona', 'dosagem': '100mg/kg', 'frequencia': '2x/dia EV'}
                    },
                    'incidencia_max': 0.01,
                    'populacao_risco': ['criancas', 'idosos', 'imunodeprimidos'],
                    'gravidade': 'critica',
                    'tempo_incubacao': '1-10 dias'
                },
                'covid19': {
                    'eventos_climaticos': ['aglomeracao', 'baixa_ventilacao'],
                    'sintomas': ['febre', 'tosse_seca', 'fadiga', 'dor_cabeca', 'perda_olfato', 'perda_paladar', 'dificuldade_respirar'],
                    'sintomas_especificos': ['anosmia', 'ageusia', 'dispneia_progressiva'],
                    'medicamentos': {
                        'adulto': {'nome': 'Suporte clínico + Isolamento', 'dosagem': 'Conforme necessário', 'frequencia': 'Contínuo'},
                        'crianca': {'nome': 'Suporte clínico + Isolamento', 'dosagem': 'Conforme necessário', 'frequencia': 'Contínuo'}
                    },
                    'incidencia_max': 0.25,
                    'populacao_risco': ['idosos', 'comorbidades', 'imunodeprimidos'],
                    'gravidade': 'alta',
                    'tempo_incubacao': '2-14 dias'
                },
                'doenca_chagas_aguda': {
                    'eventos_climaticos': ['areas_rurais', 'habitacoes_precarias'],
                    'sintomas': ['febre', 'fadiga', 'dor_cabeca', 'dor_muscular', 'aumento_figado', 'aumento_baço'],
                    'sintomas_especificos': ['chagoma', 'sinal_romana', 'linfadenopatia'],
                    'medicamentos': {
                        'adulto': {'nome': 'Benznidazol', 'dosagem': '5-7mg/kg', 'frequencia': '2x/dia'},
                        'crianca': {'nome': 'Benznidazol', 'dosagem': '10mg/kg', 'frequencia': '2x/dia'}
                    },
                    'incidencia_max': 0.03,
                    'populacao_risco': ['comunidades_rurais', 'habitacoes_precarias'],
                    'gravidade': 'alta',
                    'tempo_incubacao': '5-14 dias'
                }
            }
        }
    
    def _carregar_historico(self):
        """Carrega histórico de atendimentos"""
        if os.path.exists(self.historico_file):
            try:
                with open(self.historico_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _salvar_historico(self):
        """Salva histórico de atendimentos"""
        with open(self.historico_file, 'w', encoding='utf-8') as f:
            json.dump(self.historico, f, ensure_ascii=False, indent=2)
    
    def calcular_score_sintomas(self, sintomas_paciente, sintomas_doenca, sintomas_especificos=None):
        """Calcula score de compatibilidade entre sintomas do paciente e da doença"""
        if not sintomas_paciente or not sintomas_doenca:
            return 0.0
        
        sintomas_comuns = set(sintomas_paciente).intersection(set(sintomas_doenca))
        score_base = len(sintomas_comuns) / len(sintomas_doenca)
        
        # Bonus para sintomas específicos (patognomônicos)
        bonus_especifico = 0.0
        if sintomas_especificos:
            sintomas_especificos_presentes = set(sintomas_paciente).intersection(set(sintomas_especificos))
            if sintomas_especificos_presentes:
                bonus_especifico = len(sintomas_especificos_presentes) * 0.3
        
        # Penalidade se tem muitos sintomas não relacionados
        sintomas_nao_relacionados = set(sintomas_paciente) - set(sintomas_doenca)
        penalidade = len(sintomas_nao_relacionados) * 0.1
        
        score_final = min(1.0, score_base + bonus_especifico - penalidade)
        return max(0.0, score_final)
    
    def calcular_score_climatico(self, evento_climatico, eventos_doenca):
        """Calcula score baseado no evento climático"""
        if not evento_climatico or not eventos_doenca:
            return 0.0
            
        if evento_climatico in eventos_doenca:
            return 1.0
        
        # Score parcial para eventos relacionados
        eventos_relacionados = {
            'enchentes': ['chuvas_intensas', 'falta_saneamento'],
            'chuvas_intensas': ['enchentes', 'calor_umidade'],
            'secas': ['ondas_calor', 'falta_saneamento'],
            'calor_umidade': ['chuvas_intensas', 'ondas_calor']
        }
        
        if evento_climatico in eventos_relacionados:
            for evento_relacionado in eventos_relacionados[evento_climatico]:
                if evento_relacionado in eventos_doenca:
                    return 0.5
        
        return 0.0
    
    def calcular_score_populacao(self, dados_paciente, populacao_risco):
        """Calcula score baseado na população de risco"""
        score = 0.0
        idade = dados_paciente.get('idade', 0)
        
        # Scores mais específicos por faixa etária
        if 'lactentes' in populacao_risco and idade < 2:
            score += 0.5
        elif 'criancas' in populacao_risco and idade < 12:
            score += 0.4
        elif 'adultos' in populacao_risco and 18 <= idade <= 65:
            score += 0.3
        elif 'idosos' in populacao_risco and idade > 65:
            score += 0.4
        
        # Fatores de risco específicos
        if dados_paciente.get('populacao_vulneravel', False):
            score += 0.3
        
        # Condições especiais
        if 'gestantes' in populacao_risco and dados_paciente.get('sexo') == 'Feminino' and 15 <= idade <= 45:
            score += 0.4
        
        if 'desnutridos' in populacao_risco and dados_paciente.get('peso', 70) < (idade * 2 + 8):  # Fórmula simplificada
            score += 0.3
        
        if 'imunodeprimidos' in populacao_risco:
            historico = dados_paciente.get('historico_medico', [])
            if any(cond in ['hiv', 'cancer', 'diabetes', 'imunossupressao'] for cond in historico):
                score += 0.4
        
        return min(score, 1.0)
    
    def calcular_score_gravidade(self, dados_paciente, gravidade):
        """Calcula score baseado na gravidade da doença e sinais vitais"""
        temperatura = dados_paciente.get('temperatura', 36.5)
        pressao_sistolica = dados_paciente.get('pressao_sistolica', 120)
        frequencia_cardiaca = dados_paciente.get('frequencia_cardiaca', 70)
        
        score_gravidade = 0.0
        
        # Ajuste baseado na gravidade da doença
        if gravidade == 'critica':
            score_gravidade = 0.3
        elif gravidade == 'alta':
            score_gravidade = 0.2
        elif gravidade == 'media':
            score_gravidade = 0.1
        else:  # baixa
            score_gravidade = 0.05
        
        # Ajuste baseado nos sinais vitais alterados
        if temperatura >= 39.0 or temperatura <= 35.0:
            score_gravidade += 0.2
        elif temperatura >= 38.0 or temperatura <= 36.0:
            score_gravidade += 0.1
        
        if pressao_sistolica >= 180 or pressao_sistolica <= 90:
            score_gravidade += 0.2
        elif pressao_sistolica >= 160 or pressao_sistolica <= 100:
            score_gravidade += 0.1
        
        if frequencia_cardiaca >= 120 or frequencia_cardiaca <= 50:
            score_gravidade += 0.2
        elif frequencia_cardiaca >= 100 or frequencia_cardiaca <= 60:
            score_gravidade += 0.1
        
        return min(score_gravidade, 1.0)
    
    def calcular_urgencia(self, dados_paciente, diagnostico):
        """Calcula nível de urgência baseado nos sinais vitais e sintomas"""
        temperatura = dados_paciente.get('temperatura', 36.5)
        pressao_sistolica = dados_paciente.get('pressao_sistolica', 120)
        frequencia_cardiaca = dados_paciente.get('frequencia_cardiaca', 70)
        sintomas = dados_paciente.get('sintomas', [])
        
        score_urgencia = 0
        
        # Temperatura
        if temperatura >= 39.0:
            score_urgencia += 3
        elif temperatura >= 38.0:
            score_urgencia += 2
        elif temperatura <= 35.0:
            score_urgencia += 2
        
        # Pressão arterial
        if pressao_sistolica >= 180 or pressao_sistolica <= 90:
            score_urgencia += 3
        elif pressao_sistolica >= 160 or pressao_sistolica <= 100:
            score_urgencia += 2
        
        # Frequência cardíaca
        if frequencia_cardiaca >= 120 or frequencia_cardiaca <= 50:
            score_urgencia += 2
        elif frequencia_cardiaca >= 100 or frequencia_cardiaca <= 60:
            score_urgencia += 1
        
        # Sintomas graves
        sintomas_graves = ['dificuldade_respirar', 'dor_peito', 'desidratacao', 'convulsoes']
        for sintoma in sintomas_graves:
            if sintoma in sintomas:
                score_urgencia += 2
        
        # Classificação
        if score_urgencia >= 7:
            return "CRÍTICA"
        elif score_urgencia >= 4:
            return "ALTA"
        elif score_urgencia >= 2:
            return "MÉDIA"
        else:
            return "BAIXA"
    
    def verificar_paciente_saudavel(self, dados_paciente):
        """Verifica se o paciente apresenta sinais de estar saudável"""
        temperatura = dados_paciente.get('temperatura', 36.5)
        pressao_sistolica = dados_paciente.get('pressao_sistolica', 120)
        pressao_diastolica = dados_paciente.get('pressao_diastolica', 80)
        frequencia_cardiaca = dados_paciente.get('frequencia_cardiaca', 70)
        sintomas = dados_paciente.get('sintomas', [])
        
        # Verifica se sinais vitais estão normais
        temperatura_normal = 36.0 <= temperatura <= 37.5
        pressao_normal = 90 <= pressao_sistolica <= 140 and 60 <= pressao_diastolica <= 90
        frequencia_normal = 60 <= frequencia_cardiaca <= 100
        
        # Verifica se não há sintomas ou apenas sintomas muito leves
        sintomas_graves = ['febre', 'dor_cabeca', 'dor_muscular', 'nausea', 'vomito', 
                          'diarreia', 'tosse', 'dificuldade_respirar', 'dor_peito',
                          'calafrios', 'sudorese', 'manchas_pele', 'dor_abdominal', 
                          'desidratacao', 'convulsoes']
        
        tem_sintomas_significativos = any(sintoma in sintomas_graves for sintoma in sintomas)
        
        # Paciente é considerado saudável se:
        # - Sinais vitais normais E
        # - Sem sintomas significativos (lista vazia ou apenas fadiga)
        if (temperatura_normal and pressao_normal and frequencia_normal):
            # Se não tem sintomas nenhum, é saudável
            if not sintomas or len(sintomas) == 0:
                return True
            # Se tem apenas fadiga, ainda é considerado saudável
            if len(sintomas) == 1 and 'fadiga' in sintomas:
                return True
            # Se não tem sintomas graves, é saudável
            if not tem_sintomas_significativos:
                return True
        
        return False

    def processar_triagem(self, dados_paciente):
        """Processa a triagem médica e retorna diagnóstico"""
        sintomas = dados_paciente.get('sintomas', [])
        temperatura = dados_paciente.get('temperatura', 36.5)
        pressao_sistolica = dados_paciente.get('pressao_sistolica', 120)
        pressao_diastolica = dados_paciente.get('pressao_diastolica', 80)
        frequencia_cardiaca = dados_paciente.get('frequencia_cardiaca', 70)
        
        # VERIFICAÇÃO CRÍTICA: Febre alta sempre indica doença, mesmo sem outros sintomas
        if temperatura >= 38.0:
            # Adiciona febre aos sintomas se não estiver presente
            if 'febre' not in sintomas:
                sintomas = sintomas + ['febre']
                dados_paciente['sintomas'] = sintomas
        
        # PRIORIDADE MÁXIMA: Se não tem sintomas E sinais vitais normais, é paciente saudável
        if (not sintomas or len(sintomas) == 0):
            # Verifica se sinais vitais estão REALMENTE normais
            temperatura_normal = 36.0 <= temperatura <= 37.5
            pressao_normal = 90 <= pressao_sistolica <= 140 and 60 <= pressao_diastolica <= 90
            frequencia_normal = 60 <= frequencia_cardiaca <= 100
            
            if temperatura_normal and pressao_normal and frequencia_normal:
                # Paciente completamente saudável
                resultado = {
                    'diagnostico_principal': 'Paciente Saudável',
                    'probabilidade': 95.0,
                    'medicamentos': 'Não necessário',
                    'dosagem': 'N/A',
                    'frequencia': 'N/A',
                    'nivel_urgencia': 'BAIXA',
                    'observacoes': ['Sinais vitais dentro dos parâmetros normais', 'Ausência de sintomas significativos', 'Paciente em bom estado geral'],
                    'recomendacoes': ['Manter hábitos saudáveis de vida', 'Hidratação adequada', 'Alimentação balanceada', 'Retornar se desenvolver sintomas']
                }
                
                # Salva no histórico
                self._salvar_atendimento(dados_paciente, resultado)
                return resultado
            else:
                # Sinais vitais alterados - NÃO é saudável, precisa investigar
                # Continua para diagnóstico normal
                pass
        
        # Se tem apenas fadiga, também é saudável (mas só se sinais vitais normais)
        if (len(sintomas) == 1 and 'fadiga' in sintomas and 
            36.0 <= temperatura <= 37.5 and 
            90 <= pressao_sistolica <= 140 and 60 <= pressao_diastolica <= 90 and
            60 <= frequencia_cardiaca <= 100):
            
            resultado = {
                'diagnostico_principal': 'Paciente Saudável - Fadiga Leve',
                'probabilidade': 90.0,
                'medicamentos': 'Repouso',
                'dosagem': 'N/A',
                'frequencia': 'Conforme necessário',
                'nivel_urgencia': 'BAIXA',
                'observacoes': ['Apenas fadiga leve', 'Sinais vitais estáveis'],
                'recomendacoes': ['Repouso adequado', 'Hidratação', 'Retorno se piorar']
            }
            
            # Salva no histórico
            self._salvar_atendimento(dados_paciente, resultado)
            return resultado
        
        # Continua com o processo normal de triagem para pacientes com sintomas ou sinais vitais alterados
        resultados = {}
        
        for nome_doenca, info_doenca in self.base_conhecimento['doencas'].items():
            # Calcula scores
            score_sintomas = self.calcular_score_sintomas(
                dados_paciente.get('sintomas', []), 
                info_doenca['sintomas'],
                info_doenca.get('sintomas_especificos', [])
            )
            
            score_climatico = self.calcular_score_climatico(
                dados_paciente.get('evento_climatico', ''),
                info_doenca['eventos_climaticos']
            )
            
            score_populacao = self.calcular_score_populacao(
                dados_paciente,
                info_doenca['populacao_risco']
            )
            
            score_gravidade = self.calcular_score_gravidade(
                dados_paciente,
                info_doenca.get('gravidade', 'media')
            )
            
            # Score final ponderado com nova fórmula mais assertiva
            score_final = (score_sintomas * 0.45) + (score_climatico * 0.25) + (score_populacao * 0.15) + (score_gravidade * 0.15)
            
            # Bonus para doenças com sintomas muito específicos presentes
            if score_sintomas > 0.7 and info_doenca.get('sintomas_especificos'):
                sintomas_especificos_presentes = set(dados_paciente.get('sintomas', [])).intersection(set(info_doenca['sintomas_especificos']))
                if sintomas_especificos_presentes:
                    score_final += 0.2
            
            resultados[nome_doenca] = {
                'score': score_final,
                'info': info_doenca,
                'detalhes_score': {
                    'sintomas': score_sintomas,
                    'climatico': score_climatico,
                    'populacao': score_populacao,
                    'gravidade': score_gravidade
                }
            }
        
        # Seleciona diagnóstico mais provável
        diagnostico_principal = max(resultados.items(), key=lambda x: x[1]['score'])
        nome_diagnostico = diagnostico_principal[0]
        info_diagnostico = diagnostico_principal[1]
        
        # Verifica se há diagnósticos alternativos próximos (diagnóstico diferencial)
        diagnosticos_ordenados = sorted(resultados.items(), key=lambda x: x[1]['score'], reverse=True)
        diagnosticos_diferenciais = []
        
        for nome, dados in diagnosticos_ordenados[1:4]:  # Top 3 alternativos
            if dados['score'] > 0.3 and (info_diagnostico['score'] - dados['score']) < 0.3:
                diagnosticos_diferenciais.append({
                    'nome': nome.replace('_', ' ').title(),
                    'probabilidade': round(dados['score'] * 100, 1)
                })
        
        # Se o score mais alto for muito baixo, pode indicar paciente saudável (mas só se sinais vitais normais)
        if (info_diagnostico['score'] < 0.25 and 
            36.0 <= temperatura <= 37.5 and 
            90 <= pressao_sistolica <= 140 and 60 <= pressao_diastolica <= 90 and
            60 <= frequencia_cardiaca <= 100):
            
            resultado = {
                'diagnostico_principal': 'Paciente Saudável - Sintomas Inespecíficos',
                'probabilidade': 85.0,
                'medicamentos': 'Observação clínica',
                'dosagem': 'N/A',
                'frequencia': 'N/A',
                'nivel_urgencia': 'BAIXA',
                'observacoes': ['Sintomas muito leves ou inespecíficos', 'Sinais vitais dentro da normalidade'],
                'recomendacoes': ['Retorno se houver piora dos sintomas', 'Manter hidratação adequada', 'Repouso se necessário'],
                'diagnosticos_diferenciais': diagnosticos_diferenciais,
                'detalhes_score': info_diagnostico.get('detalhes_score', {}),
                'tempo_incubacao': info_diagnostico['info'].get('tempo_incubacao', 'Não especificado'),
                'gravidade_doenca': info_diagnostico['info'].get('gravidade', 'media').title()
            }
            
            # Salva no histórico
            self._salvar_atendimento(dados_paciente, resultado)
            return resultado
        
        # Determina medicação baseada na idade
        idade = dados_paciente.get('idade', 0)
        tipo_paciente = 'crianca' if idade < 12 else 'adulto'
        medicamento = info_diagnostico['info']['medicamentos'][tipo_paciente]
        
        # Calcula nível de urgência
        urgencia = self.calcular_urgencia(dados_paciente, nome_diagnostico)
        
        # Monta resultado
        resultado = {
            'diagnostico_principal': nome_diagnostico.replace('_', ' ').title(),
            'probabilidade': round(info_diagnostico['score'] * 100, 1),
            'medicamentos': medicamento['nome'],
            'dosagem': medicamento['dosagem'],
            'frequencia': medicamento['frequencia'],
            'nivel_urgencia': urgencia,
            'observacoes': self._gerar_observacoes(dados_paciente, nome_diagnostico),
            'recomendacoes': self._gerar_recomendacoes(dados_paciente, nome_diagnostico, urgencia),
            'diagnosticos_diferenciais': diagnosticos_diferenciais,
            'detalhes_score': info_diagnostico.get('detalhes_score', {}),
            'tempo_incubacao': info_diagnostico['info'].get('tempo_incubacao', 'Não especificado'),
            'gravidade_doenca': info_diagnostico['info'].get('gravidade', 'media').title()
        }
        
        # Salva no histórico
        self._salvar_atendimento(dados_paciente, resultado)
        
        return resultado
    
    def _gerar_observacoes(self, dados_paciente, diagnostico):
        """Gera observações específicas baseadas no diagnóstico"""
        observacoes = []
        
        if diagnostico == 'leptospirose':
            observacoes.append("Monitorar função renal e hepática")
            observacoes.append("Isolamento não necessário")
            observacoes.append("Atenção para sinais de icterícia")
        elif diagnostico == 'diarreia_infecciosa':
            observacoes.append("Monitorar sinais de desidratação")
            observacoes.append("Manter isolamento de contato")
            observacoes.append("Observar presença de sangue nas fezes")
        elif diagnostico == 'malaria':
            observacoes.append("Confirmar com teste rápido se disponível")
            observacoes.append("Monitorar sinais de malária grave")
            observacoes.append("Atenção para febre cíclica")
        elif diagnostico == 'dengue':
            observacoes.append("NÃO usar AAS ou anti-inflamatórios")
            observacoes.append("Monitorar sinais de alarme")
            observacoes.append("Prova do laço se suspeita de dengue")
        elif diagnostico == 'infeccao_respiratoria':
            observacoes.append("Avaliar necessidade de oxigenoterapia")
            observacoes.append("Isolamento respiratório se necessário")
            observacoes.append("Monitorar saturação de oxigênio")
        elif diagnostico == 'chikungunya':
            observacoes.append("Dor articular pode persistir por meses")
            observacoes.append("Evitar aspirina e anti-inflamatórios na fase aguda")
            observacoes.append("Fisioterapia pode ser necessária")
        elif diagnostico == 'zika':
            observacoes.append("Orientar sobre prevenção de mosquitos")
            observacoes.append("Se gestante, acompanhamento pré-natal rigoroso")
            observacoes.append("Sintomas geralmente leves e autolimitados")
        elif diagnostico == 'febre_amarela':
            observacoes.append("EMERGÊNCIA MÉDICA - Encaminhar imediatamente")
            observacoes.append("Monitorar função hepática e renal")
            observacoes.append("Isolamento para evitar transmissão")
        elif diagnostico == 'hepatite_a':
            observacoes.append("Repouso absoluto durante fase aguda")
            observacoes.append("Evitar álcool e medicamentos hepatotóxicos")
            observacoes.append("Isolamento entérico")
        elif diagnostico == 'tuberculose':
            observacoes.append("Iniciar tratamento DOTS imediatamente")
            observacoes.append("Isolamento respiratório até negativação")
            observacoes.append("Investigar contatos domiciliares")
        elif diagnostico == 'leishmaniose_visceral':
            observacoes.append("EMERGÊNCIA - Hospitalização necessária")
            observacoes.append("Monitorar hemograma e função hepática")
            observacoes.append("Investigar outros casos na família")
        elif diagnostico == 'esquistossomose':
            observacoes.append("Evitar contato com águas contaminadas")
            observacoes.append("Tratar todos os familiares")
            observacoes.append("Monitorar função hepática")
        elif diagnostico == 'meningite_bacteriana':
            observacoes.append("EMERGÊNCIA CRÍTICA - UTI imediata")
            observacoes.append("Punção lombar para confirmação")
            observacoes.append("Quimioprofilaxia para contatos")
        elif diagnostico == 'covid19':
            observacoes.append("Isolamento domiciliar por 10 dias")
            observacoes.append("Monitorar saturação de oxigênio")
            observacoes.append("Orientar sinais de gravidade")
        elif diagnostico == 'doenca_chagas_aguda':
            observacoes.append("Investigar forma de transmissão")
            observacoes.append("Monitorar função cardíaca")
            observacoes.append("Tratamento específico obrigatório")
        
        return observacoes
    
    def _gerar_recomendacoes(self, dados_paciente, diagnostico, urgencia):
        """Gera recomendações baseadas no diagnóstico e urgência"""
        recomendacoes = []
        
        if urgencia in ['CRÍTICA', 'ALTA']:
            recomendacoes.append("Encaminhar para unidade de referência URGENTE")
            recomendacoes.append("Manter monitorização contínua")
        
        recomendacoes.append("Retorno em 24-48h se não houver melhora")
        recomendacoes.append("Orientar sinais de alarme para retorno imediato")
        
        if diagnostico in ['diarreia_infecciosa', 'dengue']:
            recomendacoes.append("Manter hidratação adequada")
        
        return recomendacoes
    
    def _gerar_observacoes_saudavel(self, dados_paciente):
        """Gera observações para paciente saudável"""
        observacoes = [
            "Sinais vitais dentro dos parâmetros normais",
            "Ausência de sintomas significativos",
            "Paciente em bom estado geral"
        ]
        
        # Adiciona observações específicas baseadas na idade
        idade = dados_paciente.get('idade', 0)
        if idade < 2:
            observacoes.append("Manter acompanhamento pediátrico regular")
        elif idade > 65:
            observacoes.append("Manter acompanhamento geriátrico preventivo")
        
        return observacoes
    
    def _gerar_recomendacoes_saudavel(self, dados_paciente):
        """Gera recomendações para paciente saudável"""
        recomendacoes = [
            "Manter hábitos saudáveis de vida",
            "Hidratação adequada",
            "Alimentação balanceada",
            "Retornar se desenvolver sintomas"
        ]
        
        # Recomendações baseadas no contexto ambiental
        evento_climatico = dados_paciente.get('evento_climatico', '')
        if evento_climatico in ['enchentes', 'chuvas_intensas']:
            recomendacoes.append("Evitar contato com água contaminada")
            recomendacoes.append("Manter cuidados com higiene pessoal")
        elif evento_climatico in ['secas', 'ondas_calor']:
            recomendacoes.append("Aumentar ingestão de líquidos")
            recomendacoes.append("Evitar exposição solar excessiva")
        elif evento_climatico == 'calor_umidade':
            recomendacoes.append("Usar repelente contra mosquitos")
            recomendacoes.append("Eliminar água parada ao redor da residência")
        
        return recomendacoes
    
    def _salvar_atendimento(self, dados_paciente, resultado):
        """Salva atendimento no histórico"""
        atendimento = {
            'timestamp': datetime.now().isoformat(),
            'dados_paciente': dados_paciente,
            'resultado': resultado
        }
        
        self.historico.append(atendimento)
        self._salvar_historico()
    
    def obter_historico(self):
        """Retorna histórico de atendimentos"""
        return self.historico
    
    def obter_estatisticas(self):
        """Calcula estatísticas dos atendimentos"""
        if not self.historico:
            return {}
        
        df = pd.DataFrame([
            {
                'diagnostico': item['resultado']['diagnostico_principal'],
                'urgencia': item['resultado']['nivel_urgencia'],
                'idade': item['dados_paciente']['idade'],
                'evento_climatico': item['dados_paciente'].get('evento_climatico', 'Não informado')
            }
            for item in self.historico
        ])
        
        return {
            'total_atendimentos': len(self.historico),
            'diagnosticos_frequentes': df['diagnostico'].value_counts().to_dict(),
            'urgencia_distribuicao': df['urgencia'].value_counts().to_dict(),
            'eventos_climaticos': df['evento_climatico'].value_counts().to_dict(),
            'idade_media': df['idade'].mean()
        } 