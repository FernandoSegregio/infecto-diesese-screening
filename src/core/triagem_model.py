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
        """Carrega a base de conhecimento médico regionalizada"""
        return {
            'regioes': {
                'brasil_norte': {
                    'nome': 'Norte do Brasil (Amazônia)',
                    'caracteristicas': ['enchentes_frequentes', 'clima_tropical', 'areas_rurais', 'rios_abundantes'],
                    'doencas': {
                        'leptospirose': {
                            'eventos_climaticos': ['enchentes', 'chuvas_intensas'],
                            'sintomas': ['febre', 'dor_muscular', 'dor_cabeca', 'nausea', 'vomito', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Doxiciclina', 'dosagem': '100mg', 'frequencia': '2x/dia por 7 dias'},
                                'crianca': {'nome': 'Amoxicilina', 'dosagem': '50mg/kg/dia', 'frequencia': '3x/dia por 7 dias'}
                            },
                            'incidencia_max': 0.15,
                            'populacao_risco': ['trabalhadores_rurais', 'ribeirinhos', 'criancas'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '2-30 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'hepatite_a': {
                            'eventos_climaticos': ['enchentes', 'falta_saneamento', 'secas'],
                            'sintomas': ['febre', 'nausea', 'vomito', 'dor_abdominal', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'dor_abdominal'],
                            'medicamentos': {
                                'adulto': {'nome': 'Suporte clínico + Repouso', 'dosagem': 'Hidratação + Sintomáticos', 'frequencia': 'Conforme necessário'},
                                'crianca': {'nome': 'Suporte clínico + Repouso', 'dosagem': 'Hidratação + Sintomáticos', 'frequencia': 'Conforme necessário'}
                            },
                            'incidencia_max': 0.20,
                            'populacao_risco': ['criancas', 'comunidades_sem_saneamento'],
                            'gravidade': 'media',
                            'tempo_incubacao': '15-50 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'diarreia_infecciosa': {
                            'eventos_climaticos': ['enchentes', 'secas', 'falta_saneamento'],
                            'sintomas': ['diarreia', 'vomito', 'febre', 'dor_abdominal', 'sangue_fezes'],
                            'sintomas_especificos': ['sangue_fezes', 'diarreia'],
                            'medicamentos': {
                                'adulto': {'nome': 'Sais de reidratação + Zinco', 'dosagem': '1 sachê + 20mg', 'frequencia': 'Conforme perda'},
                                'crianca': {'nome': 'Sais de reidratação + Zinco', 'dosagem': '75ml/kg + 10mg', 'frequencia': 'Nas primeiras 4h'}
                            },
                            'incidencia_max': 0.25,
                            'populacao_risco': ['criancas', 'idosos', 'desnutridos'],
                            'gravidade': 'media',
                            'tempo_incubacao': '1-5 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'febre_tifoide': {
                            'eventos_climaticos': ['enchentes', 'falta_saneamento'],
                            'sintomas': ['febre_alta', 'dor_cabeca', 'dor_abdominal', 'manchas_pele', 'diarreia'],
                            'sintomas_especificos': ['febre_alta', 'manchas_pele'],
                            'medicamentos': {
                                'adulto': {'nome': 'Ciprofloxacino', 'dosagem': '500mg', 'frequencia': '2x/dia por 10 dias'},
                                'crianca': {'nome': 'Ceftriaxona', 'dosagem': '75mg/kg/dia', 'frequencia': '1x/dia EV por 10 dias'}
                            },
                            'incidencia_max': 0.10,
                            'populacao_risco': ['adolescentes', 'adultos_jovens'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '7-21 dias',
                            'prevalencia_regional': 'media'
                        },
                        'malaria': {
                            'eventos_climaticos': ['chuvas_intensas', 'calor_umidade', 'areas_endemicas'],
                            'sintomas': ['febre', 'calafrios', 'dor_cabeca', 'nausea', 'vomito'],
                            'sintomas_especificos': ['calafrios', 'febre'],
                            'medicamentos': {
                                'adulto': {'nome': 'Artemeter + Lumefantrina', 'dosagem': '80mg + 480mg', 'frequencia': '2x/dia por 3 dias'},
                                'crianca': {'nome': 'Artemeter + Lumefantrina', 'dosagem': 'Conforme peso', 'frequencia': '2x/dia por 3 dias'}
                            },
                            'incidencia_max': 0.30,
                            'populacao_risco': ['criancas', 'gestantes', 'nao_imunes'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '7-30 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'dengue': {
                            'eventos_climaticos': ['chuvas_intensas', 'calor_umidade'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'manchas_pele', 'nausea', 'vomito'],
                            'sintomas_especificos': ['manchas_pele', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Paracetamol + Hidratação', 'dosagem': '750mg', 'frequencia': '6/6h (nunca AAS)'},
                                'crianca': {'nome': 'Paracetamol + Hidratação', 'dosagem': '15mg/kg', 'frequencia': '6/6h (nunca AAS)'}
                            },
                            'incidencia_max': 0.25,
                            'populacao_risco': ['criancas', 'adultos_jovens'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '3-14 dias',
                            'prevalencia_regional': 'media'
                        },
                        'zika': {
                            'eventos_climaticos': ['chuvas_intensas', 'calor_umidade'],
                            'sintomas': ['febre', 'manchas_pele', 'conjuntivite', 'dor_articular', 'dor_cabeca'],
                            'sintomas_especificos': ['conjuntivite', 'dor_articular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Paracetamol + Hidratação', 'dosagem': '750mg', 'frequencia': '6/6h'},
                                'crianca': {'nome': 'Paracetamol + Hidratação', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                            },
                            'incidencia_max': 0.15,
                            'populacao_risco': ['gestantes', 'mulheres_idade_fertil'],
                            'gravidade': 'baixa',
                            'tempo_incubacao': '3-12 dias',
                            'prevalencia_regional': 'media'
                        },
                        'chikungunya': {
                            'eventos_climaticos': ['chuvas_intensas', 'calor_umidade'],
                            'sintomas': ['febre', 'dor_articular', 'dor_muscular', 'dor_cabeca', 'manchas_pele'],
                            'sintomas_especificos': ['dor_articular', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Paracetamol + Dipirona', 'dosagem': '750mg + 500mg', 'frequencia': '6/6h'},
                                'crianca': {'nome': 'Paracetamol', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                            },
                            'incidencia_max': 0.20,
                            'populacao_risco': ['adultos', 'idosos'],
                            'gravidade': 'media',
                            'tempo_incubacao': '2-12 dias',
                            'prevalencia_regional': 'media'
                        },
                        'febre_amarela': {
                            'eventos_climaticos': ['areas_endemicas', 'calor_umidade'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'nausea', 'vomito', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'febre_alta'],
                            'medicamentos': {
                                'adulto': {'nome': 'Suporte intensivo', 'dosagem': 'UTI + Hemodiálise', 'frequencia': 'Contínuo'},
                                'crianca': {'nome': 'Suporte intensivo', 'dosagem': 'UTI + Hemodiálise', 'frequencia': 'Contínuo'}
                            },
                            'incidencia_max': 0.05,
                            'populacao_risco': ['nao_vacinados', 'trabalhadores_rurais'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '3-6 dias',
                            'prevalencia_regional': 'media'
                        },
                        'leishmaniose_cutanea': {
                            'eventos_climaticos': ['areas_rurais', 'calor_umidade'],
                            'sintomas': ['manchas_pele', 'febre'],
                            'sintomas_especificos': ['manchas_pele'],
                            'medicamentos': {
                                'adulto': {'nome': 'Antimoniato pentavalente', 'dosagem': '20mg/kg/dia', 'frequencia': 'Por 20 dias'},
                                'crianca': {'nome': 'Antimoniato pentavalente', 'dosagem': '20mg/kg/dia', 'frequencia': 'Por 20 dias'}
                            },
                            'incidencia_max': 0.08,
                            'populacao_risco': ['trabalhadores_rurais', 'homens_adultos'],
                            'gravidade': 'media',
                            'tempo_incubacao': '2-8 semanas',
                            'prevalencia_regional': 'alta'
                        },
                        'leishmaniose_visceral': {
                            'eventos_climaticos': ['areas_rurais', 'secas'],
                            'sintomas': ['febre', 'dor_abdominal'],
                            'sintomas_especificos': ['febre', 'dor_abdominal'],
                            'medicamentos': {
                                'adulto': {'nome': 'Anfotericina B lipossomal', 'dosagem': '3mg/kg/dia', 'frequencia': 'EV por 5 dias'},
                                'crianca': {'nome': 'Anfotericina B lipossomal', 'dosagem': '3mg/kg/dia', 'frequencia': 'EV por 5 dias'}
                            },
                            'incidencia_max': 0.05,
                            'populacao_risco': ['criancas', 'desnutridos', 'imunodeprimidos'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '2-8 meses',
                            'prevalencia_regional': 'media'
                        },
                        'doenca_chagas': {
                            'eventos_climaticos': ['habitacoes_precarias', 'areas_rurais'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_abdominal'],
                            'sintomas_especificos': ['febre', 'dor_abdominal'],
                            'medicamentos': {
                                'adulto': {'nome': 'Benznidazol', 'dosagem': '5-7mg/kg/dia', 'frequencia': '2x/dia por 60 dias'},
                                'crianca': {'nome': 'Benznidazol', 'dosagem': '10mg/kg/dia', 'frequencia': '2x/dia por 60 dias'}
                            },
                            'incidencia_max': 0.05,
                            'populacao_risco': ['criancas', 'moradores_rurais'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '5-14 dias',
                            'prevalencia_regional': 'media'
                        }
                    }
                },
                'africa': {
                    'nome': 'África Subsaariana',
                    'caracteristicas': ['epidemias_frequentes', 'saneamento_precario', 'clima_tropical', 'desnutricao'],
                    'doencas': {
                        'colera': {
                            'eventos_climaticos': ['enchentes', 'falta_saneamento', 'secas'],
                            'sintomas': ['diarreia', 'vomito', 'dor_abdominal'],
                            'sintomas_especificos': ['diarreia', 'vomito'],
                            'medicamentos': {
                                'adulto': {'nome': 'Sais de reidratação + Doxiciclina', 'dosagem': 'SRO + 300mg', 'frequencia': 'SRO contínuo + dose única'},
                                'crianca': {'nome': 'Sais de reidratação + Azitromicina', 'dosagem': 'SRO + 20mg/kg', 'frequencia': 'SRO contínuo + dose única'}
                            },
                            'incidencia_max': 0.40,
                            'populacao_risco': ['criancas', 'idosos', 'desnutridos'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '2 horas-5 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'febre_tifoide': {
                            'eventos_climaticos': ['enchentes', 'falta_saneamento'],
                            'sintomas': ['febre_alta', 'dor_cabeca', 'dor_abdominal', 'diarreia', 'manchas_pele'],
                            'sintomas_especificos': ['febre_alta', 'manchas_pele'],
                            'medicamentos': {
                                'adulto': {'nome': 'Ceftriaxona', 'dosagem': '2g', 'frequencia': '1x/dia EV por 10 dias'},
                                'crianca': {'nome': 'Ceftriaxona', 'dosagem': '75mg/kg/dia', 'frequencia': '1x/dia EV por 10 dias'}
                            },
                            'incidencia_max': 0.30,
                            'populacao_risco': ['adolescentes', 'adultos_jovens'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '7-21 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'hepatite_e': {
                            'eventos_climaticos': ['enchentes', 'falta_saneamento'],
                            'sintomas': ['febre', 'nausea', 'vomito', 'dor_abdominal', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'dor_abdominal'],
                            'medicamentos': {
                                'adulto': {'nome': 'Suporte clínico', 'dosagem': 'Hidratação + Sintomáticos', 'frequencia': 'Conforme necessário'},
                                'crianca': {'nome': 'Suporte clínico', 'dosagem': 'Hidratação + Sintomáticos', 'frequencia': 'Conforme necessário'}
                            },
                            'incidencia_max': 0.25,
                            'populacao_risco': ['gestantes', 'adultos_jovens'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '15-60 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'malaria': {
                            'eventos_climaticos': ['chuvas_intensas', 'calor_umidade'],
                            'sintomas': ['febre', 'calafrios', 'dor_cabeca', 'nausea', 'vomito'],
                            'sintomas_especificos': ['calafrios', 'febre'],
                            'medicamentos': {
                                'adulto': {'nome': 'Artesunato + Amodiaquina', 'dosagem': '200mg + 540mg', 'frequencia': '1x/dia por 3 dias'},
                                'crianca': {'nome': 'Artesunato + Amodiaquina', 'dosagem': 'Conforme peso', 'frequencia': '1x/dia por 3 dias'}
                            },
                            'incidencia_max': 0.50,
                            'populacao_risco': ['criancas', 'gestantes', 'menores_5_anos'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '7-30 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'febre_amarela': {
                            'eventos_climaticos': ['areas_endemicas', 'calor_umidade'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'nausea', 'vomito', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'febre_alta'],
                            'medicamentos': {
                                'adulto': {'nome': 'Suporte intensivo', 'dosagem': 'UTI + Hemodiálise', 'frequencia': 'Contínuo'},
                                'crianca': {'nome': 'Suporte intensivo', 'dosagem': 'UTI + Hemodiálise', 'frequencia': 'Contínuo'}
                            },
                            'incidencia_max': 0.15,
                            'populacao_risco': ['nao_vacinados', 'viajantes'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '3-6 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'dengue': {
                            'eventos_climaticos': ['chuvas_intensas', 'calor_umidade'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'manchas_pele', 'nausea', 'vomito'],
                            'sintomas_especificos': ['manchas_pele', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Paracetamol + Hidratação', 'dosagem': '750mg', 'frequencia': '6/6h'},
                                'crianca': {'nome': 'Paracetamol + Hidratação', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                            },
                            'incidencia_max': 0.20,
                            'populacao_risco': ['criancas', 'adultos_jovens'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '3-14 dias',
                            'prevalencia_regional': 'media'
                        },
                        'febre_vale_rift': {
                            'eventos_climaticos': ['chuvas_intensas', 'enchentes'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'nausea', 'vomito'],
                            'sintomas_especificos': ['febre', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Ribavirina', 'dosagem': '15mg/kg', 'frequencia': '4x/dia por 10 dias'},
                                'crianca': {'nome': 'Suporte clínico', 'dosagem': 'Sintomáticos', 'frequencia': 'Conforme necessário'}
                            },
                            'incidencia_max': 0.10,
                            'populacao_risco': ['pastores', 'trabalhadores_rurais'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '2-6 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'tripanossomiase_africana': {
                            'eventos_climaticos': ['areas_rurais', 'proximidade_rios'],
                            'sintomas': ['febre', 'dor_cabeca', 'confusao_mental'],
                            'sintomas_especificos': ['confusao_mental', 'febre'],
                            'medicamentos': {
                                'adulto': {'nome': 'Fexinidazol', 'dosagem': '1800mg', 'frequencia': '1x/dia por 10 dias'},
                                'crianca': {'nome': 'Melarsoprol', 'dosagem': '2.2mg/kg/dia', 'frequencia': 'EV por 10 dias'}
                            },
                            'incidencia_max': 0.05,
                            'populacao_risco': ['trabalhadores_rurais', 'pescadores'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '1-3 semanas',
                            'prevalencia_regional': 'media'
                        },
                        'meningite_meningococica': {
                            'eventos_climaticos': ['secas', 'aglomeracao', 'baixa_umidade'],
                            'sintomas': ['febre_alta', 'dor_cabeca', 'rigidez_nuca', 'vomito', 'manchas_pele'],
                            'sintomas_especificos': ['rigidez_nuca', 'manchas_pele'],
                            'medicamentos': {
                                'adulto': {'nome': 'Ceftriaxona + Dexametasona', 'dosagem': '4g + 10mg', 'frequencia': '2x/dia EV'},
                                'crianca': {'nome': 'Ceftriaxona + Dexametasona', 'dosagem': '100mg/kg + 0.6mg/kg', 'frequencia': '2x/dia EV'}
                            },
                            'incidencia_max': 0.15,
                            'populacao_risco': ['criancas', 'adolescentes', 'adultos_jovens'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '1-10 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'esquistossomose': {
                            'eventos_climaticos': ['enchentes', 'chuvas_intensas', 'contato_agua'],
                            'sintomas': ['febre', 'dor_abdominal', 'diarreia', 'sangue_fezes'],
                            'sintomas_especificos': ['sangue_fezes', 'dor_abdominal'],
                            'medicamentos': {
                                'adulto': {'nome': 'Praziquantel', 'dosagem': '40mg/kg', 'frequencia': 'Dose única'},
                                'crianca': {'nome': 'Praziquantel', 'dosagem': '40mg/kg', 'frequencia': 'Dose única'}
                            },
                            'incidencia_max': 0.35,
                            'populacao_risco': ['criancas', 'pescadores', 'lavadeiras'],
                            'gravidade': 'media',
                            'tempo_incubacao': '4-12 semanas',
                            'prevalencia_regional': 'muito_alta'
                        }
                    }
                },
                'asia': {
                    'nome': 'Ásia (Sul e Sudeste)',
                    'caracteristicas': ['monsoes', 'densidade_populacional', 'resistencia_medicamentosa', 'areas_rurais'],
                    'doencas': {
                        'colera': {
                            'eventos_climaticos': ['enchentes', 'monsoes', 'falta_saneamento'],
                            'sintomas': ['diarreia', 'vomito', 'dor_abdominal'],
                            'sintomas_especificos': ['diarreia', 'vomito'],
                            'medicamentos': {
                                'adulto': {'nome': 'Sais de reidratação + Azitromicina', 'dosagem': 'SRO + 1g', 'frequencia': 'SRO contínuo + dose única'},
                                'crianca': {'nome': 'Sais de reidratação + Azitromicina', 'dosagem': 'SRO + 20mg/kg', 'frequencia': 'SRO contínuo + dose única'}
                            },
                            'incidencia_max': 0.35,
                            'populacao_risco': ['criancas', 'idosos', 'comunidades_costeiras'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '2 horas-5 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'febre_tifoide': {
                            'eventos_climaticos': ['monsoes', 'enchentes', 'falta_saneamento'],
                            'sintomas': ['febre_alta', 'dor_cabeca', 'dor_abdominal', 'diarreia', 'manchas_pele'],
                            'sintomas_especificos': ['febre_alta', 'manchas_pele'],
                            'medicamentos': {
                                'adulto': {'nome': 'Ceftriaxona', 'dosagem': '2g', 'frequencia': '1x/dia EV por 14 dias'},
                                'crianca': {'nome': 'Ceftriaxona', 'dosagem': '75mg/kg/dia', 'frequencia': '1x/dia EV por 14 dias'}
                            },
                            'incidencia_max': 0.40,
                            'populacao_risco': ['criancas', 'adolescentes'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '7-21 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'hepatite_a': {
                            'eventos_climaticos': ['monsoes', 'enchentes', 'falta_saneamento'],
                            'sintomas': ['febre', 'nausea', 'vomito', 'dor_abdominal', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'dor_abdominal'],
                            'medicamentos': {
                                'adulto': {'nome': 'Suporte clínico', 'dosagem': 'Hidratação + Sintomáticos', 'frequencia': 'Conforme necessário'},
                                'crianca': {'nome': 'Suporte clínico', 'dosagem': 'Hidratação + Sintomáticos', 'frequencia': 'Conforme necessário'}
                            },
                            'incidencia_max': 0.30,
                            'populacao_risco': ['criancas', 'adultos_jovens'],
                            'gravidade': 'media',
                            'tempo_incubacao': '15-50 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'hepatite_e': {
                            'eventos_climaticos': ['monsoes', 'enchentes', 'falta_saneamento'],
                            'sintomas': ['febre', 'nausea', 'vomito', 'dor_abdominal', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'dor_abdominal'],
                            'medicamentos': {
                                'adulto': {'nome': 'Ribavirina (casos graves)', 'dosagem': '800mg', 'frequencia': '2x/dia por 3 meses'},
                                'crianca': {'nome': 'Suporte clínico', 'dosagem': 'Hidratação + Sintomáticos', 'frequencia': 'Conforme necessário'}
                            },
                            'incidencia_max': 0.25,
                            'populacao_risco': ['gestantes', 'imunodeprimidos'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '15-60 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'dengue': {
                            'eventos_climaticos': ['monsoes', 'chuvas_intensas', 'calor_umidade'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'manchas_pele', 'nausea', 'vomito'],
                            'sintomas_especificos': ['manchas_pele', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Paracetamol + Hidratação', 'dosagem': '750mg', 'frequencia': '6/6h (nunca AAS)'},
                                'crianca': {'nome': 'Paracetamol + Hidratação', 'dosagem': '15mg/kg', 'frequencia': '6/6h (nunca AAS)'}
                            },
                            'incidencia_max': 0.45,
                            'populacao_risco': ['criancas', 'adultos_jovens'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '3-14 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'chikungunya': {
                            'eventos_climaticos': ['monsoes', 'chuvas_intensas'],
                            'sintomas': ['febre', 'dor_articular', 'dor_muscular', 'dor_cabeca', 'manchas_pele'],
                            'sintomas_especificos': ['dor_articular', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Paracetamol + Anti-inflamatório', 'dosagem': '750mg + 400mg', 'frequencia': '6/6h'},
                                'crianca': {'nome': 'Paracetamol', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                            },
                            'incidencia_max': 0.35,
                            'populacao_risco': ['adultos', 'idosos'],
                            'gravidade': 'media',
                            'tempo_incubacao': '2-12 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'malaria': {
                            'eventos_climaticos': ['monsoes', 'chuvas_intensas', 'areas_rurais'],
                            'sintomas': ['febre', 'calafrios', 'dor_cabeca', 'nausea', 'vomito'],
                            'sintomas_especificos': ['calafrios', 'febre'],
                            'medicamentos': {
                                'adulto': {'nome': 'Artesunato + Mefloquina', 'dosagem': '200mg + 500mg', 'frequencia': 'Conforme protocolo'},
                                'crianca': {'nome': 'Artesunato + Mefloquina', 'dosagem': 'Conforme peso', 'frequencia': 'Conforme protocolo'}
                            },
                            'incidencia_max': 0.30,
                            'populacao_risco': ['criancas', 'gestantes', 'trabalhadores_rurais'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '7-30 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'encefalite_japonesa': {
                            'eventos_climaticos': ['monsoes', 'areas_rurais', 'criacao_suinos'],
                            'sintomas': ['febre', 'dor_cabeca', 'vomito', 'confusao_mental', 'rigidez_nuca'],
                            'sintomas_especificos': ['confusao_mental', 'rigidez_nuca'],
                            'medicamentos': {
                                'adulto': {'nome': 'Suporte intensivo', 'dosagem': 'UTI + Anticonvulsivantes', 'frequencia': 'Conforme necessário'},
                                'crianca': {'nome': 'Suporte intensivo', 'dosagem': 'UTI + Anticonvulsivantes', 'frequencia': 'Conforme necessário'}
                            },
                            'incidencia_max': 0.10,
                            'populacao_risco': ['criancas', 'trabalhadores_rurais'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '5-15 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'zika': {
                            'eventos_climaticos': ['monsoes', 'chuvas_intensas'],
                            'sintomas': ['febre', 'manchas_pele', 'conjuntivite', 'dor_articular', 'dor_cabeca'],
                            'sintomas_especificos': ['conjuntivite', 'dor_articular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Paracetamol + Hidratação', 'dosagem': '750mg', 'frequencia': '6/6h'},
                                'crianca': {'nome': 'Paracetamol + Hidratação', 'dosagem': '15mg/kg', 'frequencia': '6/6h'}
                            },
                            'incidencia_max': 0.20,
                            'populacao_risco': ['gestantes', 'mulheres_idade_fertil'],
                            'gravidade': 'baixa',
                            'tempo_incubacao': '3-12 dias',
                            'prevalencia_regional': 'alta'
                        },
                        'leptospirose': {
                            'eventos_climaticos': ['monsoes', 'enchentes', 'areas_urbanas'],
                            'sintomas': ['febre', 'dor_muscular', 'dor_cabeca', 'nausea', 'vomito', 'ictericia'],
                            'sintomas_especificos': ['ictericia', 'dor_muscular'],
                            'medicamentos': {
                                'adulto': {'nome': 'Doxiciclina', 'dosagem': '100mg', 'frequencia': '2x/dia por 7 dias'},
                                'crianca': {'nome': 'Amoxicilina', 'dosagem': '50mg/kg/dia', 'frequencia': '3x/dia por 7 dias'}
                            },
                            'incidencia_max': 0.25,
                            'populacao_risco': ['trabalhadores_urbanos', 'criancas'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '2-30 dias',
                            'prevalencia_regional': 'muito_alta'
                        },
                        'tifo': {
                            'eventos_climaticos': ['aglomeracao', 'habitacoes_precarias'],
                            'sintomas': ['febre', 'dor_cabeca', 'dor_muscular', 'manchas_pele', 'confusao_mental'],
                            'sintomas_especificos': ['manchas_pele', 'confusao_mental'],
                            'medicamentos': {
                                'adulto': {'nome': 'Doxiciclina', 'dosagem': '100mg', 'frequencia': '2x/dia por 7 dias'},
                                'crianca': {'nome': 'Cloranfenicol', 'dosagem': '50mg/kg/dia', 'frequencia': '4x/dia por 7 dias'}
                            },
                            'incidencia_max': 0.15,
                            'populacao_risco': ['refugiados', 'populacao_carente'],
                            'gravidade': 'alta',
                            'tempo_incubacao': '6-14 dias',
                            'prevalencia_regional': 'media'
                        },
                        'influenza_aviaria': {
                            'eventos_climaticos': ['proximidade_aves', 'mercados_animais'],
                            'sintomas': ['febre', 'tosse', 'dificuldade_respirar', 'dor_cabeca', 'dor_muscular'],
                            'sintomas_especificos': ['tosse', 'dificuldade_respirar'],
                            'medicamentos': {
                                'adulto': {'nome': 'Oseltamivir', 'dosagem': '75mg', 'frequencia': '2x/dia por 5 dias'},
                                'crianca': {'nome': 'Oseltamivir', 'dosagem': 'Conforme peso', 'frequencia': '2x/dia por 5 dias'}
                            },
                            'incidencia_max': 0.05,
                            'populacao_risco': ['trabalhadores_aves', 'criancas_rurais'],
                            'gravidade': 'critica',
                            'tempo_incubacao': '2-8 dias',
                            'prevalencia_regional': 'media'
                        }
                    }
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
        
        # Lista simplificada de sintomas significativos
        sintomas_significativos = [
            'febre', 'febre_alta', 'dor_cabeca', 'dor_muscular', 'dor_articular', 
            'nausea', 'vomito', 'diarreia', 'tosse', 'dificuldade_respirar', 
            'calafrios', 'manchas_pele', 'conjuntivite', 'dor_abdominal', 
            'ictericia', 'sangue_fezes', 'rigidez_nuca', 'confusao_mental'
        ]
        
        tem_sintomas_significativos = any(sintoma in sintomas_significativos for sintoma in sintomas)
        
        # Paciente é considerado saudável se:
        # - Sinais vitais normais E
        # - Sem sintomas significativos
        if (temperatura_normal and pressao_normal and frequencia_normal):
            # Se não tem sintomas nenhum, é saudável
            if not sintomas or len(sintomas) == 0:
                return True
            # Se não tem sintomas significativos, é saudável
            if not tem_sintomas_significativos:
                return True
        
        return False

    def processar_triagem(self, dados_paciente):
        """Processa triagem médica com sistema regionalizado"""
        try:
            # Verificar se o paciente está realmente saudável
            if self.verificar_paciente_saudavel(dados_paciente):
                return self._gerar_resultado_saudavel(dados_paciente)
            
            # Obter região selecionada
            regiao = dados_paciente.get('regiao_geografica', 'brasil_norte')
            doencas_regiao = self.base_conhecimento['regioes'][regiao]['doencas']
            
            scores_doencas = {}
            
            # Calcular scores para cada doença da região
            for nome_doenca, dados_doenca in doencas_regiao.items():
                # Score base dos sintomas (45%)
                score_sintomas = self.calcular_score_sintomas(
                    dados_paciente['sintomas'], 
                    dados_doenca['sintomas'],
                    dados_doenca.get('sintomas_especificos', [])
                )
                
                # Score do evento climático (25%)
                score_climatico = self.calcular_score_climatico(
                    dados_paciente.get('evento_climatico', ''),
                    dados_doenca['eventos_climaticos']
                )
                
                # Score da população vulnerável (15%)
                score_populacao = self.calcular_score_populacao_regionalizado(
                    dados_paciente,
                    dados_doenca['populacao_risco']
                )
                
                # Score de gravidade e prevalência regional (15%)
                score_gravidade = self.calcular_score_gravidade_regionalizado(
                    dados_paciente,
                    dados_doenca['gravidade'],
                    dados_doenca['prevalencia_regional']
                )
                
                # Score final ponderado
                score_final = (
                    score_sintomas * 0.45 +
                    score_climatico * 0.25 + 
                    score_populacao * 0.15 +
                    score_gravidade * 0.15
                )
                
                scores_doencas[nome_doenca] = {
                    'score_total': score_final,
                    'score_sintomas': score_sintomas,
                    'score_climatico': score_climatico,
                    'score_populacao': score_populacao,
                    'score_gravidade': score_gravidade,
                    'dados_doenca': dados_doenca
                }
            
            # Ordenar por score
            doencas_ordenadas = sorted(
                scores_doencas.items(), 
                key=lambda x: x[1]['score_total'], 
                reverse=True
            )
            
            # Diagnostico principal
            diagnostico_principal = doencas_ordenadas[0]
            nome_doenca = diagnostico_principal[0]
            dados_score = diagnostico_principal[1]
            dados_doenca = dados_score['dados_doenca']
            
            # Calcular probabilidade
            probabilidade = min(int(dados_score['score_total'] * 100), 95)
            
            # Determinar urgência
            urgencia = self.calcular_urgencia_regionalizada(dados_paciente, dados_doenca)
            
            # Selecionar medicamento baseado na idade
            idade = dados_paciente['idade']
            if idade < 12:
                medicamento_info = dados_doenca['medicamentos']['crianca']
            else:
                medicamento_info = dados_doenca['medicamentos']['adulto']
            
            # Diagnósticos diferenciais (top 3)
            diagnosticos_diferenciais = []
            for i in range(1, min(4, len(doencas_ordenadas))):
                diag = doencas_ordenadas[i]
                prob_diff = min(int(diag[1]['score_total'] * 100), probabilidade - 5)
                if prob_diff > 15:  # Só incluir se probabilidade > 15%
                    diagnosticos_diferenciais.append({
                        'nome': self._formatar_nome_doenca(diag[0]),
                        'probabilidade': prob_diff
                    })
            
            # Resultado final
            resultado = {
                'diagnostico_principal': self._formatar_nome_doenca(nome_doenca),
                'probabilidade': probabilidade,
                'nivel_urgencia': urgencia,
                'medicamentos': medicamento_info['nome'],
                'dosagem': medicamento_info['dosagem'],
                'frequencia': medicamento_info['frequencia'],
                'observacoes': self._gerar_observacoes_regionalizadas(dados_paciente, nome_doenca, dados_doenca),
                'recomendacoes': self._gerar_recomendacoes_regionalizadas(dados_paciente, nome_doenca, urgencia, regiao),
                'diagnosticos_diferenciais': diagnosticos_diferenciais,
                'detalhes_score': {
                    'sintomas': dados_score['score_sintomas'],
                    'climatico': dados_score['score_climatico'],
                    'populacao': dados_score['score_populacao'],
                    'gravidade': dados_score['score_gravidade']
                },
                'tempo_incubacao': dados_doenca['tempo_incubacao'],
                'gravidade_doenca': dados_doenca['gravidade'],
                'regiao_diagnostico': self.base_conhecimento['regioes'][regiao]['nome']
            }
            
            # Salvar atendimento
            self._salvar_atendimento(dados_paciente, resultado)
            
            return resultado
            
        except Exception as e:
            print(f"Erro no processamento: {str(e)}")
            return {
                'diagnostico_principal': 'Erro no processamento',
                'probabilidade': 0,
                'nivel_urgencia': 'MÉDIA',
                'medicamentos': 'Consultar médico',
                'dosagem': 'N/A',
                'frequencia': 'N/A',
                'observacoes': [f'Erro no sistema: {str(e)}'],
                'recomendacoes': ['Buscar atendimento médico imediato'],
                'diagnosticos_diferenciais': [],
                'detalhes_score': {'sintomas': 0, 'climatico': 0, 'populacao': 0, 'gravidade': 0}
            }
    
    def _gerar_observacoes_regionalizadas(self, dados_paciente, diagnostico, dados_doenca):
        """Gera observações específicas baseadas no diagnóstico regionalizado"""
        observacoes = []
        
        # Observações sobre gravidade
        gravidade = dados_doenca['gravidade']
        if gravidade == 'critica':
            observacoes.append("⚠️ DOENÇA CRÍTICA - Requer atenção médica imediata")
        elif gravidade == 'alta':
            observacoes.append("🔶 Doença de alta gravidade - Acompanhamento rigoroso necessário")
        
        # Observações sobre tempo de incubação
        tempo_incubacao = dados_doenca['tempo_incubacao']
        observacoes.append(f"📅 Tempo de incubação típico: {tempo_incubacao}")
        
        # Observações sobre sintomas específicos
        sintomas_paciente = dados_paciente.get('sintomas', [])
        sintomas_especificos = dados_doenca.get('sintomas_especificos', [])
        
        sintomas_graves_presentes = set(sintomas_paciente).intersection(set(sintomas_especificos))
        if sintomas_graves_presentes:
            observacoes.append(f"⚠️ Sintomas específicos presentes: {', '.join(sintomas_graves_presentes)}")
        
        # Observações sobre sinais vitais
        temperatura = dados_paciente.get('temperatura', 36.5)
        if temperatura >= 39.0:
            observacoes.append("🌡️ Febre alta - Monitorar hidratação")
        elif temperatura >= 37.8:
            observacoes.append("🌡️ Febre presente - Controle térmico")
        
        return observacoes
    
    def _gerar_recomendacoes_regionalizadas(self, dados_paciente, diagnostico, urgencia, regiao):
        """Gera recomendações baseadas no diagnóstico, urgência e região"""
        recomendacoes = []
        
        # Recomendações baseadas na urgência
        if urgencia == 'CRÍTICA':
            recomendacoes.append("🚨 BUSCAR ATENDIMENTO MÉDICO IMEDIATO")
            recomendacoes.append("📞 Considerar transferência para centro especializado")
        elif urgencia == 'ALTA':
            recomendacoes.append("🏥 Procurar atendimento médico em até 2 horas")
            recomendacoes.append("📋 Monitorar sinais vitais de perto")
        elif urgencia == 'MÉDIA':
            recomendacoes.append("👨‍⚕️ Procurar atendimento médico em 24 horas")
            recomendacoes.append("🏠 Repouso domiciliar adequado")
        
        # Recomendações específicas da região
        nome_regiao = self.base_conhecimento['regioes'][regiao]['nome']
        
        if regiao == 'brasil_norte':
            recomendacoes.append("🦟 Usar repelente e eliminar criadouros de mosquitos")
            recomendacoes.append("💧 Evitar contato com águas contaminadas")
            if diagnostico in ['malaria', 'leishmaniose_visceral']:
                recomendacoes.append("🏥 Notificar vigilância epidemiológica")
        
        elif regiao == 'africa':
            recomendacoes.append("💧 Ferver ou tratar toda água para consumo")
            recomendacoes.append("🧼 Higiene rigorosa das mãos")
            if diagnostico == 'colera':
                recomendacoes.append("⚠️ ISOLAMENTO e notificação obrigatória")
            elif diagnostico == 'meningite_meningococica':
                recomendacoes.append("💊 Profilaxia para contatos próximos")
        
        elif regiao == 'asia':
            recomendacoes.append("🌧️ Precauções especiais durante época de monções")
            recomendacoes.append("🍖 Cuidados com alimentos de origem animal")
            if diagnostico == 'dengue':
                recomendacoes.append("🩸 Monitorar contagem de plaquetas")
        
        # Recomendações gerais
        recomendacoes.append("💧 Manter hidratação adequada")
        recomendacoes.append("🌡️ Retornar se febre persistir ou piorar")
        
        return recomendacoes
    
    def _gerar_resultado_saudavel(self, dados_paciente):
        """Gera resultado para paciente saudável"""
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
    
    def calcular_score_populacao_regionalizado(self, dados_paciente, populacao_risco):
        """Calcula score baseado na população de risco regionalizada"""
        score = 0.0
        
        idade = dados_paciente.get('idade', 0)
        historico = dados_paciente.get('historico_medico', [])
        sexo = dados_paciente.get('sexo', '')
        populacao_vulneravel = dados_paciente.get('populacao_vulneravel', False)
        
        for grupo_risco in populacao_risco:
            if grupo_risco == 'criancas' and idade < 12:
                score += 0.3
            elif grupo_risco == 'menores_5_anos' and idade < 5:
                score += 0.4
            elif grupo_risco == 'idosos' and idade > 65:
                score += 0.3
            elif grupo_risco == 'gestantes' and 'gestante' in historico:
                score += 0.4
            elif grupo_risco == 'desnutridos' and 'desnutricao' in historico:
                score += 0.3
            elif grupo_risco == 'imunodeprimidos' and any(x in historico for x in ['hiv', 'cancer', 'imunossupressao']):
                score += 0.4
            elif grupo_risco == 'trabalhadores_rurais' and populacao_vulneravel:
                score += 0.3
            elif grupo_risco == 'ribeirinhos' and populacao_vulneravel:
                score += 0.3
            elif grupo_risco == 'nao_vacinados' and 'vacinacao_incompleta' in historico:
                score += 0.3
            elif grupo_risco == 'homens_adultos' and sexo == 'Masculino' and 18 <= idade <= 60:
                score += 0.2
            elif grupo_risco == 'mulheres_idade_fertil' and sexo == 'Feminino' and 15 <= idade <= 45:
                score += 0.2
        
        return min(score, 1.0)
    
    def calcular_score_gravidade_regionalizado(self, dados_paciente, gravidade, prevalencia_regional):
        """Calcula score de gravidade considerando prevalência regional"""
        score_base = {
            'baixa': 0.2,
            'media': 0.4,
            'alta': 0.7,
            'critica': 1.0
        }.get(gravidade, 0.4)
        
        # Modificador de prevalência regional
        modificador_prevalencia = {
            'baixa': 0.5,
            'media': 0.7,
            'alta': 0.9,
            'muito_alta': 1.2
        }.get(prevalencia_regional, 0.7)
        
        # Considera sinais vitais alterados
        temperatura = dados_paciente.get('temperatura', 36.5)
        pressao_sistolica = dados_paciente.get('pressao_sistolica', 120)
        
        modificador_clinico = 1.0
        if temperatura >= 39.0:
            modificador_clinico += 0.3
        elif temperatura >= 37.8:
            modificador_clinico += 0.2
        
        if pressao_sistolica < 90:
            modificador_clinico += 0.3
        elif pressao_sistolica > 160:
            modificador_clinico += 0.2
        
        return min(score_base * modificador_prevalencia * modificador_clinico, 1.0)
    
    def calcular_urgencia_regionalizada(self, dados_paciente, dados_doenca):
        """Calcula urgência baseada em dados regionalizados"""
        urgencia_base = dados_doenca['gravidade']
        
        # Modificadores baseados em sinais vitais
        temperatura = dados_paciente.get('temperatura', 36.5)
        pressao_sistolica = dados_paciente.get('pressao_sistolica', 120)
        
        if urgencia_base == 'critica':
            return 'CRÍTICA'
        elif temperatura >= 40.0 or pressao_sistolica < 80:
            return 'CRÍTICA'
        elif urgencia_base == 'alta' or temperatura >= 39.0:
            return 'ALTA'
        elif urgencia_base == 'media' or temperatura >= 38.0:
            return 'MÉDIA'
        else:
            return 'BAIXA'
    
    def _formatar_nome_doenca(self, nome_doenca):
        """Formata nome da doença para exibição"""
        formatacao = {
            'leptospirose': 'Leptospirose',
            'hepatite_a': 'Hepatite A',
            'hepatite_e': 'Hepatite E',
            'diarreia_infecciosa': 'Diarreia Infecciosa',
            'febre_tifoide': 'Febre Tifoide',
            'malaria': 'Malária',
            'dengue': 'Dengue',
            'zika': 'Zika',
            'chikungunya': 'Chikungunya',
            'febre_amarela': 'Febre Amarela',
            'leishmaniose_cutanea': 'Leishmaniose Cutânea',
            'leishmaniose_visceral': 'Leishmaniose Visceral',
            'doenca_chagas': 'Doença de Chagas',
            'colera': 'Cólera',
            'febre_vale_rift': 'Febre do Vale do Rift',
            'tripanossomiase_africana': 'Doença do Sono',
            'meningite_meningococica': 'Meningite Meningocócica',
            'esquistossomose': 'Esquistossomose',
            'encefalite_japonesa': 'Encefalite Japonesa',
            'tifo': 'Tifo',
            'influenza_aviaria': 'Influenza Aviária'
        }
        
        return formatacao.get(nome_doenca, nome_doenca.replace('_', ' ').title())

    def calcular_necessidades_medicamentos(self, periodo_dias=30, projecao_dias=30):
        """
        Calcula necessidades de medicamentos baseado no histórico de triagens
        
        Args:
            periodo_dias: Período para análise do histórico (padrão 30 dias)
            projecao_dias: Período para projeção futura (padrão 30 dias)
            
        Returns:
            dict: Relatório completo de necessidades de medicamentos
        """
        try:
            historico = self.obter_historico()
            
            if not historico:
                return {
                    'erro': 'Nenhum histórico de triagens disponível',
                    'medicamentos_necessarios': {},
                    'estatisticas': {}
                }
            
            # Filtrar triagens do período especificado
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=periodo_dias)
            
            triagens_periodo = []
            for triagem in historico:
                triagem_date = datetime.fromisoformat(triagem['timestamp'])
                if triagem_date >= cutoff_date:
                    triagens_periodo.append(triagem)
            
            if not triagens_periodo:
                return {
                    'erro': f'Nenhuma triagem encontrada nos últimos {periodo_dias} dias',
                    'medicamentos_necessarios': {},
                    'estatisticas': {}
                }
            
            # Contar medicamentos prescritos
            medicamentos_count = {}
            diagnosticos_count = {}
            urgencia_count = {}
            
            for triagem in triagens_periodo:
                resultado = triagem['resultado']
                medicamento = resultado.get('medicamentos', 'Não especificado')
                diagnostico = resultado.get('diagnostico_principal', 'Não especificado')
                urgencia = resultado.get('nivel_urgencia', 'BAIXA')
                
                # Contar medicamentos
                if medicamento != 'Observação clínica' and medicamento != 'Não especificado':
                    medicamentos_count[medicamento] = medicamentos_count.get(medicamento, 0) + 1
                
                # Contar diagnósticos
                diagnosticos_count[diagnostico] = diagnosticos_count.get(diagnostico, 0) + 1
                
                # Contar urgências
                urgencia_count[urgencia] = urgencia_count.get(urgencia, 0) + 1
            
            # Calcular projeção baseada na média diária
            total_triagens = len(triagens_periodo)
            media_diaria = total_triagens / periodo_dias
            projecao_total = int(media_diaria * projecao_dias)
            
            # Calcular necessidades projetadas de medicamentos
            medicamentos_necessarios = {}
            
            for medicamento, count in medicamentos_count.items():
                # Calcular frequência relativa
                frequencia = count / total_triagens
                
                # Projetar necessidade
                necessidade_projetada = int(frequencia * projecao_total)
                
                # Adicionar margem de segurança (20%)
                margem_seguranca = int(necessidade_projetada * 0.2)
                total_necessario = necessidade_projetada + margem_seguranca
                
                medicamentos_necessarios[medicamento] = {
                    'usado_periodo': count,
                    'frequencia_percent': round(frequencia * 100, 1),
                    'projecao_base': necessidade_projetada,
                    'margem_seguranca': margem_seguranca,
                    'total_necessario': total_necessario,
                    'prioridade': self._calcular_prioridade_medicamento(medicamento, frequencia, urgencia_count, triagens_periodo)
                }
            
            # Estatísticas gerais
            estatisticas = {
                'periodo_analise_dias': periodo_dias,
                'projecao_dias': projecao_dias,
                'total_triagens_periodo': total_triagens,
                'media_triagens_dia': round(media_diaria, 1),
                'projecao_triagens': projecao_total,
                'diagnosticos_mais_comuns': dict(sorted(diagnosticos_count.items(), key=lambda x: x[1], reverse=True)[:5]),
                'distribuicao_urgencia': urgencia_count,
                'medicamentos_mais_usados': dict(sorted(medicamentos_count.items(), key=lambda x: x[1], reverse=True)[:5])
            }
            
            return {
                'medicamentos_necessarios': medicamentos_necessarios,
                'estatisticas': estatisticas,
                'periodo_analise': f"{cutoff_date.strftime('%d/%m/%Y')} a {datetime.now().strftime('%d/%m/%Y')}",
                'projecao_para': f"{datetime.now().strftime('%d/%m/%Y')} a {(datetime.now() + timedelta(days=projecao_dias)).strftime('%d/%m/%Y')}"
            }
            
        except Exception as e:
            return {
                'erro': f'Erro ao calcular necessidades: {str(e)}',
                'medicamentos_necessarios': {},
                'estatisticas': {}
            }
    
    def _calcular_prioridade_medicamento(self, medicamento, frequencia, urgencia_count, triagens_periodo):
        """Calcula prioridade do medicamento baseado em critérios clínicos"""
        
        # Medicamentos críticos (sempre alta prioridade)
        medicamentos_criticos = [
            'Artesunato', 'Quinina', 'Ceftriaxona', 'Soro de reidratação oral',
            'Anfotericina B', 'Penicilina G', 'Doxiciclina'
        ]
        
        # Verificar se é medicamento crítico
        for critico in medicamentos_criticos:
            if critico.lower() in medicamento.lower():
                return 'CRÍTICA'
        
        # Calcular prioridade baseada na frequência e urgência
        urgencia_critica = urgencia_count.get('CRÍTICA', 0)
        urgencia_alta = urgencia_count.get('ALTA', 0)
        total_urgente = urgencia_critica + urgencia_alta
        
        # Verificar se o medicamento está associado a casos urgentes
        casos_urgentes_medicamento = 0
        for triagem in triagens_periodo:
            resultado = triagem['resultado']
            if (resultado.get('medicamentos') == medicamento and 
                resultado.get('nivel_urgencia') in ['CRÍTICA', 'ALTA']):
                casos_urgentes_medicamento += 1
        
        # Critérios de prioridade
        if frequencia >= 0.15 or casos_urgentes_medicamento >= 3:  # 15% ou mais, ou 3+ casos urgentes
            return 'ALTA'
        elif frequencia >= 0.05 or casos_urgentes_medicamento >= 1:  # 5% ou mais, ou 1+ caso urgente
            return 'MÉDIA'
        else:
            return 'BAIXA'
    
    def gerar_lista_compras_medicamentos(self, periodo_dias=30, projecao_dias=30, incluir_detalhes=True):
        """
        Gera lista de compras formatada para medicamentos
        
        Args:
            periodo_dias: Período para análise
            projecao_dias: Período para projeção
            incluir_detalhes: Se deve incluir detalhes técnicos
            
        Returns:
            dict: Lista de compras formatada
        """
        necessidades = self.calcular_necessidades_medicamentos(periodo_dias, projecao_dias)
        
        if 'erro' in necessidades:
            return necessidades
        
        # Organizar por prioridade
        medicamentos_por_prioridade = {
            'CRÍTICA': [],
            'ALTA': [],
            'MÉDIA': [],
            'BAIXA': []
        }
        
        for medicamento, dados in necessidades['medicamentos_necessarios'].items():
            prioridade = dados['prioridade']
            medicamentos_por_prioridade[prioridade].append({
                'medicamento': medicamento,
                'quantidade': dados['total_necessario'],
                'frequencia': dados['frequencia_percent'],
                'usado_periodo': dados['usado_periodo']
            })
        
        # Ordenar por quantidade dentro de cada prioridade
        for prioridade in medicamentos_por_prioridade:
            medicamentos_por_prioridade[prioridade].sort(
                key=lambda x: x['quantidade'], reverse=True
            )
        
        lista_compras = {
            'medicamentos_por_prioridade': medicamentos_por_prioridade,
            'resumo': {
                'total_medicamentos_diferentes': len(necessidades['medicamentos_necessarios']),
                'total_unidades_estimadas': sum(dados['total_necessario'] for dados in necessidades['medicamentos_necessarios'].values()),
                'periodo_cobertura': f"{projecao_dias} dias",
                'baseado_em': f"{necessidades['estatisticas']['total_triagens_periodo']} triagens"
            },
            'estatisticas': necessidades['estatisticas'] if incluir_detalhes else None,
            'periodo_analise': necessidades['periodo_analise'],
            'projecao_para': necessidades['projecao_para']
        }
        
        return lista_compras 