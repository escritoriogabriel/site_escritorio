#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

# Conteúdos específicos para cada página - REESCRITO COM 60% TEXTO E 40% CARDS
PAGE_CONTENTS = {
    'criminal.html': {
        'badge': 'Direito Criminal',
        'badge_icon': 'fas fa-gavel',
        'title': 'Quando você está em perigo jurídico, <span>nós defendemos sua liberdade</span>.',
        'subtitle': 'Acusações criminais, prisão, processos complexos... Situações que podem mudar sua vida para sempre. Você precisa de alguém que não apenas conheça a lei, mas que realmente lute pelos seus direitos e liberdade.',
        'intro_text': 'O sistema criminal é complexo e intimidador. Quando você enfrenta uma acusação ou está preso, cada minuto conta. Você tem direitos fundamentais que precisam ser protegidos desde o primeiro momento. Nossa abordagem combina conhecimento profundo da lei penal com uma defesa agressiva dos seus interesses. Entendemos que por trás de cada caso existe uma pessoa com medo, com família, com futuro em jogo. Por isso, não apenas seguimos procedimentos legais — nós realmente lutamos pela sua liberdade e pelo seu futuro.',
        'scenarios': [
            {
                'icon': 'fas fa-handcuffs',
                'title': 'Você foi preso ou está sendo investigado',
                'description': 'Não sabe quais são seus direitos? Está assustado? Precisa de representação imediata?',
                'solution': 'Agimos rápido para proteger seus direitos desde o primeiro momento'
            },
            {
                'icon': 'fas fa-exclamation-triangle',
                'title': 'Acusações graves contra você',
                'description': 'Está sendo acusado de crime que não cometeu? Precisa de uma defesa forte?',
                'solution': 'Construímos defesas sólidas baseadas em provas e estratégia jurídica'
            },
            {
                'icon': 'fas fa-ban',
                'title': 'Risco de condenação',
                'description': 'Quer evitar a prisão? Busca redução de pena? Precisa de alternativas?',
                'solution': 'Negociamos as melhores soluções para minimizar consequências'
            },
            {
                'icon': 'fas fa-shield-alt',
                'title': 'Vítima de crime',
                'description': 'Sofreu crime e quer justiça? Não sabe como proceder?',
                'solution': 'Representamos você como vítima e buscamos reparação'
            },
            {
                'icon': 'fas fa-lock',
                'title': 'Prisão preventiva ou medidas cautelares',
                'description': 'Está preso e quer liberdade? Precisa questionar a prisão?',
                'solution': 'Impugnamos prisões injustificadas e buscamos liberdade'
            },
            {
                'icon': 'fas fa-file-contract',
                'title': 'Processo criminal complexo',
                'description': 'Processo complicado com muitas etapas? Não entende o que está acontecendo?',
                'solution': 'Orientamos e representamos em todas as fases do processo'
            }
        ],
        'solutions': [
            {
                'title': 'Defesa em Crimes Graves',
                'description': 'Crimes como homicídio, roubo, tráfico e outros delitos graves exigem defesa especializada. Trabalhamos para proteger seus direitos constitucionais. Cada caso é único e merece estratégia própria. Investigamos a fundo, questionamos provas, identificamos inconsistências e construímos defesa sólida. Não aceitamos condenações injustas.',
                'steps': [
                    'Análise imediata do caso e avaliação de riscos',
                    'Coleta de provas e investigação defensiva',
                    'Preparação de estratégia de defesa',
                    'Representação em audiências e julgamentos',
                    'Recursos em todas as instâncias se necessário'
                ]
            },
            {
                'title': 'Liberdade Provisória e Habeas Corpus',
                'description': 'Se você foi preso, pode ter direito à liberdade provisória. Atuamos rapidamente para conseguir sua soltura. A prisão preventiva deve ser exceção, não regra. Analisamos se há motivo legal para sua prisão e, se não houver, pedimos imediatamente sua libertação. Cada dia preso é um dia a menos com sua família.',
                'steps': [
                    'Avaliação imediata da legalidade da prisão',
                    'Preparação de petição de habeas corpus',
                    'Apresentação ao juiz com argumentos fortes',
                    'Acompanhamento até a concessão da liberdade',
                    'Proteção de seus direitos processuais'
                ]
            },
            {
                'title': 'Negociação de Penas e Acordos',
                'description': 'Nem sempre ir a julgamento é a melhor opção. Às vezes, um acordo bem negociado protege mais seus interesses do que um julgamento incerto. Analisamos as forças e fraquezas do caso e negociamos com a promotoria para reduzir penas, evitar prisão ou conseguir alternativas penais.',
                'steps': [
                    'Análise da força da acusação',
                    'Negociação com promotoria',
                    'Busca de alternativas penais',
                    'Acordo que proteja seus interesses',
                    'Cumprimento seguro das obrigações'
                ]
            },
            {
                'title': 'Crimes de Trânsito e Embriaguez',
                'description': 'Dirigir embriagado, causar acidente, suspensão de CNH. Defendemos seus direitos em crimes de trânsito. Questionamos testes de embriaguez, analisamos procedimentos policiais e construímos defesa baseada em evidências. Seu direito de dirigir é importante.',
                'steps': [
                    'Análise dos testes de embriaguez',
                    'Questionamento de procedimentos policiais',
                    'Defesa em julgamento',
                    'Busca de redução de pena',
                    'Proteção do direito de dirigir'
                ]
            }
        ],
        'faq': [
            {
                'q': 'Qual é meu direito se fui preso?',
                'a': 'Você tem direito a ser informado do motivo da prisão, ao silêncio, a um advogado e a ser apresentado a um juiz em até 24 horas. Esses direitos devem ser respeitados.'
            },
            {
                'q': 'Posso ser condenado sem julgamento?',
                'a': 'Não. Você tem direito a julgamento justo, a conhecer as acusações, a apresentar defesa e a questionar provas. Ninguém é condenado sem processo.'
            },
            {
                'q': 'O que é habeas corpus?',
                'a': 'É um recurso legal para questionar prisão ilegal ou abusiva. Se você foi preso sem motivo legal, pode pedir habeas corpus para ganhar liberdade.'
            },
            {
                'q': 'Quanto custa uma defesa criminal?',
                'a': 'Depende da complexidade do caso. Oferecemos diferentes formas de pagamento e podemos discutir honorários. Se não tiver recursos, pode pedir defensor público.'
            },
            {
                'q': 'Posso ser preso por dívida?',
                'a': 'Não. Prisão por dívida é proibida no Brasil. Você pode ser processado civilmente, mas não preso por dever dinheiro.'
            },
            {
                'q': 'O que acontece após condenação?',
                'a': 'Você pode recorrer da condenação, pedir revisão criminal ou progressão de regime. Existem várias opções para questionar uma condenação.'
            }
        ]
    },
    'contrato.html': {
        'badge': 'Contratos',
        'badge_icon': 'fas fa-file-contract',
        'title': 'Contratos bem feitos <span>protegem seu negócio e sua paz de espírito</span>.',
        'subtitle': 'Compra, venda, aluguel, parcerias, empréstimos... Cada acordo precisa estar claro e protegido. Um contrato bem elaborado evita conflitos futuros e garante que todos saibam seus direitos e deveres.',
        'intro_text': 'Contratos são a base de qualquer negócio ou acordo importante. Um contrato bem redigido protege você, deixa claro o que cada parte deve fazer e evita conflitos futuros. Mas muitas pessoas assinam contratos sem entender o que estão assinando, ou deixam de incluir proteções importantes. Nós ajudamos você a criar contratos que realmente protegem seus interesses, ou a revisar contratos antes de você assinar algo que possa prejudicá-lo.',
        'scenarios': [
            {
                'icon': 'fas fa-handshake',
                'title': 'Você quer fazer um acordo importante',
                'description': 'Vai comprar um imóvel? Fazer parceria? Emprestar dinheiro? Não sabe como documentar?',
                'solution': 'Elaboramos contratos claros que protegem você'
            },
            {
                'icon': 'fas fa-exclamation-circle',
                'title': 'Tem um contrato que não entende',
                'description': 'Recebeu um contrato para assinar? Acha que tem cláusulas injustas?',
                'solution': 'Analisamos e explicamos cada detalhe para você'
            },
            {
                'icon': 'fas fa-ban',
                'title': 'Alguém não está cumprindo o contrato',
                'description': 'A outra parte não está fazendo o que prometeu? Quer cobrar?',
                'solution': 'Executamos o contrato e garantimos seu cumprimento'
            },
            {
                'icon': 'fas fa-home',
                'title': 'Contrato de aluguel problemático',
                'description': 'Tem problemas com inquilino ou proprietário? Contrato confuso?',
                'solution': 'Resolvemos conflitos de aluguel e protegemos seus direitos'
            },
            {
                'icon': 'fas fa-building',
                'title': 'Compra e venda de imóvel',
                'description': 'Quer comprar ou vender imóvel? Precisa de segurança na transação?',
                'solution': 'Documentamos tudo corretamente para sua proteção'
            },
            {
                'icon': 'fas fa-coins',
                'title': 'Empréstimo entre pessoas',
                'description': 'Vai emprestar dinheiro a alguém? Quer garantia de recebimento?',
                'solution': 'Formalizamos empréstimos com segurança legal'
            }
        ],
        'solutions': [
            {
                'title': 'Elaboração de Contratos Personalizados',
                'description': 'Cada situação é única e merece um contrato feito especialmente para ela. Não usamos modelos genéricos. Conversamos com você, entendemos exatamente o que você quer, e criamos um contrato que reflete isso com clareza e proteção total. Incluímos cláusulas que protegem seus interesses e deixamos tudo bem documentado.',
                'steps': [
                    'Entendemos sua situação e necessidades',
                    'Redigimos contrato claro e completo',
                    'Incluímos cláusulas de proteção',
                    'Revisamos com você antes de assinar',
                    'Orientamos sobre direitos e deveres'
                ]
            },
            {
                'title': 'Análise e Revisão de Contratos',
                'description': 'Antes de assinar qualquer contrato, deixe um advogado revisar. Pode economizar muito dinheiro e evitar problemas futuros. Lemos tudo com atenção, identificamos cláusulas problemáticas ou injustas, explicamos em linguagem simples o que significa cada parte, e sugerimos modificações que protejam você melhor.',
                'steps': [
                    'Leitura completa e análise crítica',
                    'Identificação de cláusulas problemáticas',
                    'Explicação em linguagem simples',
                    'Sugestões de modificações',
                    'Negociação de termos melhores'
                ]
            },
            {
                'title': 'Execução de Contratos',
                'description': 'Se alguém não está cumprindo o contrato, podemos cobrar judicialmente. Primeiro tentamos resolver de forma amigável, mas se necessário, entramos com ação na justiça para garantir que você receba o que é devido ou que o contrato seja cumprido.',
                'steps': [
                    'Análise do contrato e do descumprimento',
                    'Tentativa de resolução amigável',
                    'Ação judicial se necessário',
                    'Execução da sentença',
                    'Cobrança de indenizações'
                ]
            },
            {
                'title': 'Contratos Imobiliários',
                'description': 'Transações imobiliárias envolvem valores grandes e precisam de cuidado extra. Revisamos toda a documentação, verificamos se o imóvel está regular, elaboramos contrato seguro e acompanhamos até o registro. Sua segurança é nossa prioridade.',
                'steps': [
                    'Revisão de toda documentação',
                    'Verificação de regularidade',
                    'Elaboração de contrato seguro',
                    'Acompanhamento até registro',
                    'Proteção de seus direitos'
                ]
            }
        ],
        'faq': [
            {
                'q': 'Um contrato verbal é válido?',
                'a': 'Depende. Alguns contratos precisam ser por escrito para serem válidos. É sempre mais seguro ter tudo documentado por escrito.'
            },
            {
                'q': 'Posso mudar um contrato depois de assinado?',
                'a': 'Sim, se ambas as partes concordarem. Qualquer mudança deve ser documentada por escrito e assinada por todos.'
            },
            {
                'q': 'O que fazer se alguém não cumpre o contrato?',
                'a': 'Primeiro tente resolver amigavelmente. Se não conseguir, pode processar judicialmente para cobrar indenização ou executar o contrato.'
            },
            {
                'q': 'Preciso de advogado para fazer um contrato?',
                'a': 'Não é obrigatório, mas é muito recomendado. Um advogado garante que você está protegido e não está abrindo mão de direitos importantes.'
            },
            {
                'q': 'Cláusulas abusivas são válidas?',
                'a': 'Não. Cláusulas muito injustas podem ser anuladas pelo juiz. Por isso é importante revisar contratos antes de assinar.'
            },
            {
                'q': 'Como proteger meu negócio com contratos?',
                'a': 'Tenha contratos claros com clientes, fornecedores e parceiros. Especifique prazos, valores, responsabilidades e consequências de descumprimento.'
            }
        ]
    },
    'busca-e-apreensao.html': {
        'badge': 'Busca e Apreensão',
        'badge_icon': 'fas fa-car',
        'title': 'O oficial de justiça bateu na sua porta? <span>Você tem direitos</span>.',
        'subtitle': 'Busca e apreensão de bens, veículos, imóveis... Situações que causam pânico. Mas você não está indefeso. Existem direitos que o protegem e formas de questionar uma apreensão injusta.',
        'intro_text': 'Quando o oficial de justiça chega para apreender seus bens, é uma situação assustadora. Mas você não está indefeso. A lei protege você de apreensões abusivas e garante que você tenha direitos mesmo quando deve. Você pode questionar a apreensão, negociar com o credor, recuperar seus bens ou proteger o que é essencial. Temos experiência em defender pessoas nessa situação e sabemos exatamente o que fazer para protegê-lo.',
        'scenarios': [
            {
                'icon': 'fas fa-car',
                'title': 'Seu carro foi apreendido',
                'description': 'O oficial de justiça pegou seu veículo? Não sabe como recuperar?',
                'solution': 'Recuperamos seu veículo e questionamos a apreensão se for injusta'
            },
            {
                'icon': 'fas fa-home',
                'title': 'Risco de perder seu imóvel',
                'description': 'Está atrasado em financiamento? Recebeu aviso de apreensão?',
                'solution': 'Negociamos com credor e evitamos perda do imóvel'
            },
            {
                'icon': 'fas fa-ban',
                'title': 'Apreensão sem aviso prévio',
                'description': 'Seus bens foram apreendidos sem você saber? Isso é legal?',
                'solution': 'Questionamos apreensões abusivas e recuperamos seus bens'
            },
            {
                'icon': 'fas fa-gavel',
                'title': 'Processo de execução',
                'description': 'Está sendo executado judicialmente? Não sabe como se defender?',
                'solution': 'Defendemos você no processo de execução'
            },
            {
                'icon': 'fas fa-file-invoice-dollar',
                'title': 'Dívida que levou à apreensão',
                'description': 'Tem dívida grande e teme perder tudo? Quer negociar?',
                'solution': 'Negociamos dívidas e evitamos apreensões'
            },
            {
                'icon': 'fas fa-shield-alt',
                'title': 'Proteção de bens essenciais',
                'description': 'Quer proteger sua casa ou carro de apreensão?',
                'solution': 'Usamos recursos legais para proteger bens essenciais'
            }
        ],
        'solutions': [
            {
                'title': 'Recuperação de Bens Apreendidos',
                'description': 'Se seu bem foi apreendido, podemos ajudar a recuperá-lo ou questionar a legalidade da apreensão. Analisamos todo o processo, verificamos se houve irregularidades, e se encontrarmos, pedimos ao juiz que devolva seu bem. Você pode pagar a dívida, negociar ou questionar a apreensão.',
                'steps': [
                    'Análise do processo de apreensão',
                    'Verificação de irregularidades',
                    'Petição para devolução do bem',
                    'Negociação com credor se necessário',
                    'Recuperação segura do bem'
                ]
            },
            {
                'title': 'Defesa em Execução Judicial',
                'description': 'Quando você está sendo executado, não está indefeso. Podemos apresentar defesa para proteger seus direitos, questionar a validade da dívida, apontar irregularidades no processo e proteger bens que são essenciais para sua sobrevivência.',
                'steps': [
                    'Análise da dívida e da execução',
                    'Apresentação de embargos à execução',
                    'Questionamento de irregularidades',
                    'Negociação de acordo',
                    'Proteção de bens essenciais'
                ]
            },
            {
                'title': 'Negociação de Dívidas',
                'description': 'Antes que seus bens sejam apreendidos, podemos negociar com credores para encontrar soluções. Às vezes é possível renegociar prazos, reduzir valores ou criar um plano de pagamento que você possa cumprir. Isso evita apreensão e protege seu patrimônio.',
                'steps': [
                    'Avaliação da situação financeira',
                    'Contato com credores',
                    'Proposta de renegociação',
                    'Acordo que você possa cumprir',
                    'Proteção de seus bens'
                ]
            },
            {
                'title': 'Proteção de Bens Essenciais',
                'description': 'A lei protege certos bens que são essenciais para sua vida. Sua casa de moradia, ferramentas de trabalho e alguns móveis não podem ser apreendidos. Usamos esses direitos para protegê-lo e garantir que você tenha o mínimo necessário para viver.',
                'steps': [
                    'Identificação de bens protegidos',
                    'Argumentação legal de proteção',
                    'Petições ao juiz',
                    'Garantia de que bens essenciais sejam preservados',
                    'Proteção de sua sobrevivência'
                ]
            }
        ],
        'faq': [
            {
                'q': 'O oficial de justiça pode entrar em minha casa sem permissão?',
                'a': 'Não. Ele precisa de mandado judicial. Mesmo com mandado, existem horários e procedimentos que devem ser respeitados.'
            },
            {
                'q': 'Meu carro pode ser apreendido por dívida?',
                'a': 'Sim, se você tem dívida e o credor consegue uma sentença judicial. Mas você tem direitos e pode questionar a apreensão.'
            },
            {
                'q': 'Posso recuperar meu bem após apreensão?',
                'a': 'Sim. Você pode pagar a dívida, questionar a apreensão ou negociar com o credor. Um advogado pode ajudar nessas negociações.'
            },
            {
                'q': 'Que bens não podem ser apreendidos?',
                'a': 'Bens essenciais como casa de moradia, ferramentas de trabalho e alguns móveis têm proteção legal e não podem ser apreendidos.'
            },
            {
                'q': 'O que fazer se receber aviso de apreensão?',
                'a': 'Procure um advogado imediatamente. Existem prazos para apresentar defesa e você pode ter direitos que não conhece.'
            },
            {
                'q': 'Posso evitar apreensão negociando?',
                'a': 'Sim. Muitas vezes é possível negociar com o credor antes que a apreensão aconteça. Quanto mais cedo agir, melhor.'
            }
        ]
    },
    'trabalhista.html': {
        'badge': 'Direito Trabalhista',
        'badge_icon': 'fas fa-briefcase',
        'title': 'Seus direitos trabalhistas <span>precisam ser respeitados</span>.',
        'subtitle': 'Demissão injusta, falta de pagamento, assédio, acidente de trabalho... O trabalho é essencial para sua vida, e você merece ser tratado com justiça e respeito. Defendemos seus direitos como trabalhador.',
        'intro_text': 'O trabalho ocupa a maior parte do nosso tempo e é essencial para nossa vida. Por isso, você merece ser tratado com respeito, receber tudo que é devido e ter um ambiente seguro. Infelizmente, nem sempre isso acontece. Demissões injustas, atrasos de salário, assédio, acidentes — essas situações são mais comuns do que deveriam ser. Mas você não está sozinho. Temos experiência em defender trabalhadores e sabemos exatamente quais são seus direitos e como cobrar por eles.',
        'scenarios': [
            {
                'icon': 'fas fa-ban',
                'title': 'Você foi demitido sem justa causa',
                'description': 'Perdeu o emprego do nada? Não recebeu aviso prévio? Quer suas verbas rescisórias?',
                'solution': 'Cobramos todas as verbas devidas e questionamos demissões injustas'
            },
            {
                'icon': 'fas fa-clock',
                'title': 'Horas extras não pagas',
                'description': 'Trabalha além do horário? Não recebe pelas horas extras?',
                'solution': 'Cobramos todas as horas extras com acréscimos legais'
            },
            {
                'icon': 'fas fa-exclamation-triangle',
                'title': 'Assédio moral ou sexual',
                'description': 'Está sendo assediado no trabalho? Sofre discriminação?',
                'solution': 'Agimos para proteger você e cobrar indenização'
            },
            {
                'icon': 'fas fa-heartbeat',
                'title': 'Acidente ou doença do trabalho',
                'description': 'Sofreu acidente? Tem doença ocupacional? Quer indenização?',
                'solution': 'Cobramos indenizações e benefícios previdenciários'
            },
            {
                'icon': 'fas fa-file-invoice-dollar',
                'title': 'Salário atrasado ou falta de pagamento',
                'description': 'Seu salário está atrasado? Não está recebendo direito?',
                'solution': 'Cobramos salários atrasados com juros e multa'
            },
            {
                'icon': 'fas fa-briefcase',
                'title': 'Questões de contrato e benefícios',
                'description': 'Dúvidas sobre contrato? Benefícios não estão sendo pagos?',
                'solution': 'Orientamos sobre direitos e cobramos benefícios devidos'
            }
        ],
        'solutions': [
            {
                'title': 'Cobrança de Verbas Rescisórias',
                'description': 'Quando você é demitido, tem direito a várias verbas: aviso prévio, décimo terceiro proporcional, férias não usadas, FGTS e mais. Cobramos tudo que é devido. Analisamos como você foi demitido, calculamos cada centavo que você tem direito, e se a empresa não pagar, entramos com ação na justiça.',
                'steps': [
                    'Análise de como você foi demitido',
                    'Cálculo de todas as verbas devidas',
                    'Tentativa de acordo com empresa',
                    'Ação judicial se necessário',
                    'Cobrança com juros e multa'
                ]
            },
            {
                'title': 'Ação por Horas Extras',
                'description': 'Você trabalhou além do horário? Tem direito a compensação — 50% de acréscimo sobre o valor normal. Cobramos tudo. Documentamos as horas que você trabalhou, calculamos com os acréscimos legais, reunimos provas, e se necessário, entramos com ação na justiça.',
                'steps': [
                    'Levantamento de horas trabalhadas',
                    'Cálculo com acréscimos legais',
                    'Documentação de provas',
                    'Ação judicial',
                    'Cobrança com juros e multa'
                ]
            },
            {
                'title': 'Proteção contra Assédio',
                'description': 'Ninguém merece ser assediado ou discriminado no trabalho. Protegemos você e cobramos indenização por danos morais. Documentamos o assédio, coletamos provas, comunicamos à empresa, e se necessário, entramos com ação na justiça para garantir que você seja indenizado.',
                'steps': [
                    'Documentação do assédio',
                    'Coleta de provas e testemunhas',
                    'Comunicação à empresa',
                    'Ação judicial se necessário',
                    'Indenização por danos morais'
                ]
            },
            {
                'title': 'Indenização por Acidente de Trabalho',
                'description': 'Se você sofreu acidente ou tem doença ocupacional, tem direitos. Além dos benefícios do INSS, você pode cobrar indenização da empresa por danos morais e materiais. Analisamos o acidente, coletamos provas, e se necessário, processamos a empresa.',
                'steps': [
                    'Análise do acidente ou doença',
                    'Comunicação ao INSS',
                    'Coleta de provas e laudos',
                    'Ação judicial contra empresa',
                    'Indenização por danos morais e materiais'
                ]
            }
        ],
        'faq': [
            {
                'q': 'Posso ser demitido sem motivo?',
                'a': 'Sim, mas você tem direito a verbas rescisórias. Se foi demitido por motivo discriminatório, pode questionar.'
            },
            {
                'q': 'Quanto tempo tenho para cobrar direitos trabalhistas?',
                'a': 'Você tem até 2 anos para cobrar direitos trabalhistas na justiça. Quanto mais cedo agir, melhor.'
            },
            {
                'q': 'Horas extras precisam ser pagas?',
                'a': 'Sim. Se você trabalha além do horário, tem direito a compensação ou pagamento em dinheiro com acréscimo.'
            },
            {
                'q': 'O que fazer se sofrer acidente no trabalho?',
                'a': 'Comunique imediatamente ao seu chefe, procure médico e registre boletim de ocorrência. Depois procure um advogado.'
            },
            {
                'q': 'Posso ser demitido por estar doente?',
                'a': 'Não. Demitir alguém por estar doente é discriminação. Você pode questionar e cobrar indenização.'
            },
            {
                'q': 'Como provar assédio moral no trabalho?',
                'a': 'Documente tudo: mensagens, testemunhas, datas, o que foi dito. Isso ajuda a provar o assédio na justiça.'
            }
        ]
    },
    'trabalhista-empregado.html': {
        'badge': 'Direito Trabalhista',
        'badge_icon': 'fas fa-hard-hat',
        'title': 'Como empregado, <span>seus direitos são sagrados</span>.',
        'subtitle': 'Você trabalha todos os dias para ganhar seu salário. Merece ser tratado com respeito, receber tudo que é devido e ter um ambiente seguro. Se seus direitos estão sendo violados, estamos aqui para defender você.',
        'intro_text': 'Você trabalha todos os dias, cumpre seu horário, faz seu trabalho. Merece ser tratado com respeito, receber tudo que é devido e ter um ambiente seguro. Infelizmente, muitos empregadores não respeitam esses direitos básicos. Demissões injustas, atrasos de salário, horas extras não pagas, assédio — essas violações prejudicam você e sua família. Mas você não está sozinho. Temos experiência em defender empregados e sabemos exatamente como cobrar por seus direitos.',
        'scenarios': [
            {
                'icon': 'fas fa-ban',
                'title': 'Demissão sem justa causa',
                'description': 'Perdeu o emprego do nada? Não sabe quais são seus direitos?',
                'solution': 'Cobramos todas as verbas e questionamos demissões injustas'
            },
            {
                'icon': 'fas fa-clock',
                'title': 'Horas extras não remuneradas',
                'description': 'Trabalha além do horário sem receber?',
                'solution': 'Cobramos todas as horas com acréscimos legais'
            },
            {
                'icon': 'fas fa-exclamation-triangle',
                'title': 'Assédio no ambiente de trabalho',
                'description': 'Sofre assédio moral ou sexual?',
                'solution': 'Protegemos você e cobramos indenização'
            },
            {
                'icon': 'fas fa-heartbeat',
                'title': 'Acidente ou doença ocupacional',
                'description': 'Sofreu acidente? Tem doença do trabalho?',
                'solution': 'Cobramos indenizações e benefícios'
            },
            {
                'icon': 'fas fa-file-invoice-dollar',
                'title': 'Salário atrasado',
                'description': 'Seu salário está atrasado?',
                'solution': 'Cobramos com juros e multa'
            },
            {
                'icon': 'fas fa-briefcase',
                'title': 'Direitos não respeitados',
                'description': 'Empresa não respeita seus direitos?',
                'solution': 'Orientamos e cobramos judicialmente'
            }
        ],
        'solutions': [
            {
                'title': 'Cobrança de Verbas Rescisórias',
                'description': 'Demitido? Você tem direito a: aviso prévio, 13º proporcional, férias não usadas, FGTS e mais. Cobramos tudo. Analisamos sua demissão, calculamos cada centavo que você tem direito, negociamos com a empresa, e se necessário, entramos com ação na justiça.',
                'steps': [
                    'Análise da demissão',
                    'Cálculo de todas as verbas',
                    'Negociação com empresa',
                    'Ação judicial se necessário',
                    'Recebimento com juros e multa'
                ]
            },
            {
                'title': 'Ação por Horas Extras',
                'description': 'Trabalhou além do horário? Tem direito a 50% de acréscimo. Cobramos tudo. Documentamos as horas, calculamos com os acréscimos, reunimos provas, e se necessário, processamos a empresa.',
                'steps': [
                    'Documentação das horas',
                    'Cálculo com acréscimos',
                    'Coleta de provas',
                    'Ação judicial',
                    'Cobrança com juros'
                ]
            },
            {
                'title': 'Proteção contra Assédio e Discriminação',
                'description': 'Ninguém merece ser assediado ou discriminado. Agimos rápido para protegê-lo e cobrar indenização. Documentamos tudo, coletamos provas, comunicamos à empresa, e se necessário, processamos para garantir sua indenização.',
                'steps': [
                    'Documentação do assédio',
                    'Coleta de provas',
                    'Comunicação à empresa',
                    'Ação judicial',
                    'Indenização por danos morais'
                ]
            },
            {
                'title': 'Benefícios Previdenciários',
                'description': 'Acidente de trabalho ou doença ocupacional? Tem direito a benefícios. Comunicamos ao INSS, coletamos laudos médicos, acompanhamos o processo, e se necessário, processamos a empresa para indenização adicional.',
                'steps': [
                    'Comunicação ao INSS',
                    'Coleta de laudos médicos',
                    'Acompanhamento do processo',
                    'Ação contra empresa se necessário',
                    'Indenização por danos'
                ]
            }
        ],
        'faq': [
            {
                'q': 'Quanto tempo tenho para cobrar direitos?',
                'a': 'Você tem até 2 anos para cobrar na justiça. Quanto mais cedo agir, melhor.'
            },
            {
                'q': 'Preciso pagar para processar a empresa?',
                'a': 'Não. Você pode pedir justiça gratuita se não tiver recursos. Também pode pagar com parte da indenização.'
            },
            {
                'q': 'Meu patrão pode me demitir por estar doente?',
                'a': 'Não. Isso é discriminação. Você pode questionar e cobrar indenização.'
            },
            {
                'q': 'Como provar horas extras?',
                'a': 'Documentos, testemunhas, registros de ponto, mensagens, emails. Tudo que prove que você trabalhou além do horário.'
            },
            {
                'q': 'Posso recusar fazer horas extras?',
                'a': 'Depende do seu contrato. Mas se fizer, tem direito a compensação ou pagamento.'
            },
            {
                'q': 'O que fazer se sofrer acidente no trabalho?',
                'a': 'Comunique imediatamente, procure médico, registre tudo e procure um advogado. Você tem direitos.'
            }
        ]
    },
    'trabalhista-empresa.html': {
        'badge': 'Direito Trabalhista',
        'badge_icon': 'fas fa-building',
        'title': 'Sua empresa protegida, <span>seus negócios seguros</span>.',
        'subtitle': 'No complexo mundo das relações de trabalho, a prevenção é a melhor estratégia. Oferecemos assessoria jurídica completa para empresas, garantindo conformidade com a legislação, minimizando riscos e protegendo seu patrimônio.',
        'intro_text': 'Gerenciar uma empresa envolve muitas responsabilidades legais. Contratos de trabalho, rescisões, fiscalizações, reclamações trabalhistas — tudo isso pode se tornar complicado e custoso se não for feito corretamente. A melhor estratégia é a prevenção: ter contratos bem feitos, políticas claras, compliance com a lei. Isso evita processos, protege seu patrimônio e deixa você tranquilo para focar no seu negócio. Oferecemos assessoria completa para empresas, desde a prevenção até a defesa em processos.',
        'scenarios': [
            {
                'icon': 'fas fa-shield-alt',
                'title': 'Você quer evitar processos trabalhistas',
                'description': 'Quer garantir que sua empresa está em conformidade com a lei?',
                'solution': 'Fazemos auditoria e implementamos compliance trabalhista'
            },
            {
                'icon': 'fas fa-gavel',
                'title': 'Recebeu uma reclamação trabalhista',
                'description': 'Um ex-funcionário está processando sua empresa?',
                'solution': 'Defendemos sua empresa com estratégia jurídica sólida'
            },
            {
                'icon': 'fas fa-file-contract',
                'title': 'Precisa de contratos de trabalho',
                'description': 'Quer contratos que protejam sua empresa?',
                'solution': 'Elaboramos contratos seguros e legais'
            },
            {
                'icon': 'fas fa-users',
                'title': 'Conflitos com funcionários',
                'description': 'Tem problemas com desempenho, comportamento ou demissão?',
                'solution': 'Orientamos sobre como agir legalmente'
            },
            {
                'icon': 'fas fa-file-invoice-dollar',
                'title': 'Fiscalização do Ministério do Trabalho',
                'description': 'Recebeu autuação? Está sendo investigado?',
                'solution': 'Representamos sua empresa na fiscalização'
            },
            {
                'icon': 'fas fa-briefcase',
                'title': 'Políticas e procedimentos internos',
                'description': 'Quer criar políticas que protejam sua empresa?',
                'solution': 'Elaboramos códigos de conduta e regimentos'
            }
        ],
        'solutions': [
            {
                'title': 'Consultoria Preventiva e Compliance',
                'description': 'Evitar problemas é mais barato que resolvê-los. Fazemos auditoria completa de conformidade, identificamos riscos, implementamos políticas, treinamos gestores e acompanhamos continuamente. Isso protege sua empresa e reduz drasticamente o risco de processos.',
                'steps': [
                    'Análise completa de conformidade',
                    'Identificação de riscos',
                    'Implementação de políticas',
                    'Treinamento de gestores',
                    'Acompanhamento contínuo'
                ]
            },
            {
                'title': 'Defesa em Reclamações Trabalhistas',
                'description': 'Se sua empresa está sendo processada, defendemos com estratégia sólida. Analisamos o processo, coletamos provas, preparamos defesa forte, representamos em audiências e recorremos em todas as instâncias se necessário.',
                'steps': [
                    'Análise do processo',
                    'Coleta de provas',
                    'Preparação da defesa',
                    'Representação em audiências',
                    'Recursos em todas as instâncias'
                ]
            },
            {
                'title': 'Elaboração de Contratos e Políticas',
                'description': 'Contratos bem feitos protegem sua empresa. Elaboramos com segurança jurídica, incluindo cláusulas que protegem seus interesses, deixando tudo claro para o funcionário. Também criamos políticas internas, códigos de conduta e regimentos que deixam claro como sua empresa funciona.',
                'steps': [
                    'Análise de necessidades',
                    'Redação de contratos',
                    'Inclusão de cláusulas protetoras',
                    'Revisão e ajustes',
                    'Implementação'
                ]
            },
            {
                'title': 'Gestão de Demissões e Rescisões',
                'description': 'Demitir é delicado e precisa ser feito corretamente. Orientamos sobre procedimentos legais, documentação correta, cálculo de verbas devidas e proteção contra futuras ações. Fazer isso certo evita processos e protege sua empresa.',
                'steps': [
                    'Análise da situação',
                    'Orientação sobre procedimentos',
                    'Documentação correta',
                    'Cálculo de verbas devidas',
                    'Proteção contra futuras ações'
                ]
            }
        ],
        'faq': [
            {
                'q': 'Como evitar processos trabalhistas?',
                'a': 'Compliance é essencial. Respeite direitos, pague em dia, mantenha registros corretos e tenha contratos claros.'
            },
            {
                'q': 'Posso demitir um funcionário sem motivo?',
                'a': 'Sim, mas deve pagar verbas rescisórias. Se for por motivo discriminatório, pode ser questionado.'
            },
            {
                'q': 'Quanto custa uma auditoria trabalhista?',
                'a': 'Depende do tamanho da empresa. É investimento que protege contra riscos muito maiores.'
            },
            {
                'q': 'Preciso de contrato escrito com todos os funcionários?',
                'a': 'Sim. Contrato escrito protege ambas as partes e é exigido por lei.'
            },
            {
                'q': 'O que fazer se receber autuação do Ministério do Trabalho?',
                'a': 'Procure um advogado imediatamente. Existem prazos para responder e você pode ter direitos de defesa.'
            },
            {
                'q': 'Como documentar corretamente as demissões?',
                'a': 'Tenha comunicação clara, cálculos corretos, assinaturas e registre tudo. Isso protege sua empresa.'
            }
        ]
    }
}

# Template base para cada página
PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Advogado Gabriel Corrêa</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="advogado, advocacia, direito trabalhista, previdenciário, civil, família, consumidor, empresarial, escritório de advocacia">
    <link rel="canonical" href="https://www.gabrielcorrea.adv.br/{filename}">
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/pages-style.css">
</head>
<body>

    <div class="top-bar">
        <i class="fas fa-envelope"></i> <a href="mailto:escritorio.gabrielcorrea@gmail.com">escritorio.gabrielcorrea@gmail.com</a> &nbsp;|&nbsp; <i class="fab fa-whatsapp"></i> <a href="https://wa.me/5547996756766">(47) 99675-6766</a> &nbsp;|&nbsp; <i class="fas fa-map-marker-alt"></i> Atendimento 100% Online em todo o Brasil
    </div>

    <header>
        <a href="index.html" class="logo"><img src="assets/img/logo.png" alt="Advogado Gabriel Corrêa"></a>
        <button class="hamburger" id="hamburgerBtn" aria-label="Abrir menu">
            <span></span><span></span><span></span>
        </button>
        <nav id="mainNav">
            <ul class="nav-links">
                <li><a href="index.html">Início</a></li>
                <li class="dropdown">
                    <a href="#">Áreas de Atuação <i class="fas fa-chevron-down" style="font-size: 0.7rem;"></i></a>
                    <div class="dropdown-content">
                        <a href="trabalhista-empregado.html"><i class="fas fa-hard-hat"></i> Trabalhista — Para Empregado</a>
                        <a href="trabalhista-empresa.html"><i class="fas fa-building"></i> Trabalhista — Para Empresa</a>
                        <a href="familia.html">Direito de Família</a>
                        <a href="criminal.html">Direito Criminal</a>
                        <a href="contrato.html">Contratos</a>
                        <a href="busca-e-apreensao.html">Busca e Apreensão</a>
                    </div>
                </li>
                <li><a href="sobre.html">Sobre</a></li>
                <li><a href="blog.html">Blog</a></li>
                <li><a href="contato.html">Contato</a></li>
            </ul>
            <a href="https://wa.me/5547996756766" class="btn-nav-whatsapp"><i class="fab fa-whatsapp"></i> Fale Conosco</a>
        </nav>
    </header>

    <main>
        
            <section class="page-hero">
                <div class="page-hero-content">
                    <span class="page-hero-badge"><i class="{badge_icon}"></i> {badge}</span>
                    <h1>{title}</h1>
                    <p class="page-hero-subtitle">{subtitle}</p>
                    <div class="page-hero-ctas">
                        <a href="https://wa.me/5547996756766" class="btn-primary">
                            <i class="fab fa-whatsapp"></i> Fale com um Especialista
                        </a>
                        <a href="#scenarios" class="btn-secondary">Conheça Nossas Soluções</a>
                    </div>
                </div>
            </section>

            <section class="content-section">
                <div class="content-wrapper">
                    <h2>Situações que você pode estar vivendo agora</h2>
                    <p>{intro_text}</p>

                    <div class="scenarios-grid" id="scenarios">
{scenarios_html}
                    </div>
                </div>
            </section>

            <section class="solutions-section">
                <div class="solutions-wrapper">
                    <h2>Como resolvemos seus problemas</h2>

{solutions_html}
                </div>
            </section>

            <section class="faq-section">
                <div class="faq-wrapper">
                    <h2>Dúvidas Frequentes</h2>

{faq_html}
                </div>
            </section>

            <section class="related-posts-section">
                <div class="related-posts-wrapper">
                    <h2>Publicações Relacionadas</h2>
                    <p class="related-posts-subtitle">Confira artigos do nosso blog que podem te interessar.</p>
                    <div class="related-posts-grid">
{related_posts_html}
                    </div>
                </div>
            </section>

            <section class="contact-section-area">
                <div class="contact-content">
                    <h2>Pronto para resolver sua situação?</h2>
                    <p>Não deixe seus direitos para depois. Fale agora mesmo com um especialista e receba uma orientação personalizada.</p>
                    <a href="https://wa.me/5547996756766" class="btn-primary"><i class="fab fa-whatsapp"></i> Fale Conosco Agora</a>
                </div>
            </section>

    </main>

    <footer>
        <div class="footer-grid">
            <div class="footer-col">
                <h4>Advogado Gabriel Corrêa</h4>
                <p>OAB/SC 63.737</p>
                <p>Atendimento 100% Online em todo o Brasil</p>
            </div>
            <div class="footer-col">
                <h4>Links Úteis</h4>
                <a href="index.html">Início</a>
                <a href="sobre.html">Sobre</a>
                <a href="blog.html">Blog</a>
                <a href="contato.html">Contato</a>
            </div>
            <div class="footer-col">
                <h4>Contato</h4>
                <p>(47) 99675-6766</p>
                <p>escritorio.gabrielcorrea@gmail.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2026 Advogado Gabriel Corrêa. Todos os direitos reservados.
        </div>
    </footer>

    <a href="https://wa.me/5547996756766" class="whatsapp-float" aria-label="Falar pelo WhatsApp">
        <i class="fab fa-whatsapp"></i>
    </a>

    <script src="assets/js/main.js"></script>
</body>
</html>
'''

def generate_scenarios_html(scenarios):
    html = ""
    for scenario in scenarios:
        html += f'''
                        <div class="scenario-card">
                            <div class="scenario-icon">
                                <i class="{scenario['icon']}"></i>
                            </div>
                            <h3>{scenario['title']}</h3>
                            <p>{scenario['description']}</p>
                            <div class="scenario-solution">
                                <i class="fas fa-check-circle"></i> {scenario['solution']}
                            </div>
                        </div>
'''
    return html

def generate_solutions_html(solutions):
    html = ""
    for solution in solutions:
        steps_html = "\n".join([f"                                <li>{step}</li>" for step in solution['steps']])
        html += f'''
                    <div class="solution-item">
                        <h3><i class="fas fa-check"></i> {solution['title']}</h3>
                        <p>{solution['description']}</p>
                        <div class="solution-steps">
                            <h4>O que fazemos:</h4>
                            <ol>
{steps_html}
                            </ol>
                        </div>
                    </div>
'''
    return html

def generate_faq_html(faq_items):
    html = ""
    for item in faq_items:
        html += f'''
                    <div class="faq-item">
                        <button class="faq-question">
                            {item['q']}
                            <i class="fas fa-chevron-down"></i>
                        </button>
                        <div class="faq-answer">
                            <p>{item['a']}</p>
                        </div>
                    </div>
'''
    return html

def generate_related_posts_html(category):
    """Gera HTML para posts relacionados"""
    try:
        with open('blog/posts/index.json', 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
        
        related = [p for p in posts_data if category in p.get('categories', [])][:3]
        
        html = ""
        for post in related:
            html += f'''
                        <a href="{post['url']}" class="related-post-card">
                            <div class="related-post-image">
                                <img src="{post.get('image', 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80')}" alt="{post['title']}">
                            </div>
                            <div class="related-post-content">
                                <h3>{post['title']}</h3>
                                <p>{post.get('excerpt', '')}</p>
                                <div class="related-post-meta">
                                    <span><i class="far fa-calendar"></i> {post['date'][:10]}</span>
                                </div>
                            </div>
                        </a>
'''
        return html
    except:
        return ""

# Gerar páginas
pages_to_generate = ['criminal.html', 'contrato.html', 'busca-e-apreensao.html', 'trabalhista.html', 'trabalhista-empregado.html', 'trabalhista-empresa.html']

for page_file in pages_to_generate:
    if page_file not in PAGE_CONTENTS:
        print(f"⚠️  Conteúdo não definido para: {page_file}")
        continue
    
    content = PAGE_CONTENTS[page_file]
    
    # Gerar HTML das seções
    scenarios_html = generate_scenarios_html(content['scenarios'])
    solutions_html = generate_solutions_html(content['solutions'])
    faq_html = generate_faq_html(content['faq'])
    
    # Determinar categoria para posts relacionados
    category_map = {
        'criminal.html': 'Direito Criminal',
        'contrato.html': 'Contratos',
        'busca-e-apreensao.html': 'Busca e Apreensão',
        'trabalhista.html': 'Direito Trabalhista',
        'trabalhista-empregado.html': 'Direito Trabalhista',
        'trabalhista-empresa.html': 'Direito Trabalhista',
    }
    
    related_posts_html = generate_related_posts_html(category_map[page_file])
    
    # Gerar página
    page_html = PAGE_TEMPLATE.format(
        title=content['badge'],
        description=content['subtitle'],
        filename=page_file,
        badge=content['badge'],
        badge_icon=content['badge_icon'],
        title_main=content['title'],
        subtitle=content['subtitle'],
        intro_text=content['intro_text'],
        scenarios_html=scenarios_html,
        solutions_html=solutions_html,
        faq_html=faq_html,
        related_posts_html=related_posts_html
    )
    
    # Salvar página
    with open(page_file, 'w', encoding='utf-8') as f:
        f.write(page_html)
    
    print(f"✅ Gerada: {page_file}")

print("\n🎉 Todas as páginas foram geradas com conteúdo reescrito!")
