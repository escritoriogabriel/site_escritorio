# Guia de Geração de Posts via IA (Modelo Mestre)

Este documento serve como o "Prompt Estrutural" para qualquer IA gerar um post de blog compatível com o sistema estático do Escritório Gabriel Corrêa.

---

## 1. Front Matter (Metadados Obrigatórios)
O bloco inicial deve seguir rigorosamente este formato para que o `sync_posts.py` processe o post corretamente.

```yaml
---
title: "TÍTULO IMPACTANTE E OTIMIZADO PARA SEO"
date: "2026-06-05T14:00:00Z"
author: "Advogado Gabriel Corrêa"
categories: ["CATEGORIA PRINCIPAL"]
tags: ["Tag 1", "Tag 2", "Tag 3", "Tag 4"]
image: "nome-da-imagem.jpg"
excerpt: "Um resumo de 2 a 3 linhas que instigue a curiosidade e contenha a palavra-chave principal."
---
```

---

## 2. Estrutura de Conteúdo (Markdown)

### Títulos e Hierarquia
- **H1**: Reservado apenas para o `title` no Front Matter (o sistema já renderiza automaticamente).
- **H2 (##)**: Use para as seções principais do artigo.
- **H3 (###)**: Use para subseções dentro dos H2.
- **Negrito**: Use `**texto**` para termos jurídicos ou pontos cruciais.

### Lógica de Imagens
Para que a imagem apareça no corpo do texto:
1. Se a imagem for local: `![Descrição Alt](nome-do-arquivo.jpg)` (Certifique-se de que o arquivo exista em `/public/images/`).
2. Se a imagem for externa: `![Descrição Alt](https://url-da-imagem.com/foto.jpg)`.

### Elementos Ricos (Tabelas e Listas)
Sempre que possível, a IA deve gerar uma tabela comparativa ou informativa para facilitar a leitura.

| Requisito | Descrição | Prazo |
| :--- | :--- | :--- |
| Item 1 | Detalhes do item 1 | 5 dias |
| Item 2 | Detalhes do item 2 | 15 dias |

---

## 3. Exemplo de Post Perfeito (Copie e Use como Prompt)

Abaixo está o conteúdo que você deve pedir para a IA gerar:

```markdown
---
title: "Como Reaver seu Veículo em 5 Dias após a Busca e Apreensão"
date: "2026-06-05T14:00:00Z"
author: "Advogado Gabriel Corrêa"
categories: ["Direito Bancário"]
tags: ["Busca e Apreensão", "Liminar", "Direito do Consumidor", "Veículos"]
image: "busca-e-apreensao-veiculo.jpg"
excerpt: "Entenda o processo de purgação da mora e como a defesa técnica pode anular a apreensão do seu carro por juros abusivos."
---

## O Choque da Busca e Apreensão

Perder o veículo para um oficial de justiça é um momento traumático. No entanto, o que muitos não sabem é que a lei brasileira oferece caminhos claros para a recuperação do bem.

### O Prazo de 5 Dias: A Purgação da Mora

De acordo com o Decreto-Lei 911/69, o devedor tem o prazo de **5 dias** após a execução da liminar para pagar a integralidade da dívida pendente.

![Oficial de Justiça](oficial-justica.jpg)

## Tabela de Custos e Prazos

| Etapa | Prazo Legal | Ação Necessária |
| :--- | :--- | :--- |
| Purgação da Mora | 5 Dias | Pagamento do valor integral |
| Contestação | 15 Dias | Apresentar defesa jurídica |
| Análise de Juros | Imediato | Cálculo pericial de abusividade |

## Estratégias de Defesa

Não se trata apenas de pagar. Muitas vezes, o contrato possui **cláusulas abusivas** que podem anular todo o processo de busca e apreensão.

1. **Notificação Inválida**: Se você não foi notificado corretamente, a busca é nula.
2. **Juros Abusivos**: Taxas acima da média do mercado permitem o questionamento judicial.
3. **Encargos Moratórios**: Cobranças indevidas no período de inadimplência.

> **Nota Importante**: "A falta de comprovação da mora é causa de extinção do processo sem julgamento do mérito." - Jurisprudência Consolidada.

## Conclusão e Próximos Passos

Se o seu veículo foi apreendido, não espere o prazo vencer. A agilidade na contratação de um especialista é o que define se você terá seu carro de volta ou se ele irá a leilão.

---

### Precisa de ajuda imediata?
Fale diretamente com o Dr. Gabriel Corrêa e proteja seu patrimônio.

[👉 Chamar no WhatsApp (47) 98867-0233](https://wa.me/5547988670233?text=Olá%21%20Meu%20veículo%20foi%20apreendido%20e%20preciso%20de%20ajuda%20urgente%21)
```

---

## 4. Checklist para a IA
Ao gerar o post, a IA deve garantir:
- [ ] **Slug Único**: O título deve ser claro para gerar um link amigável.
- [ ] **Breadcrumbs**: O sistema gera automaticamente baseado na categoria, então use apenas uma categoria principal no Front Matter.
- [ ] **Posts Relacionados**: O site já possui um script (`add_sections.py`) que lê o `index.json`. Para garantir que este post apareça como relacionado, use `tags` e `categories` consistentes com os posts antigos.
- [ ] **CTA no Final**: Sempre incluir o link do WhatsApp com a mensagem personalizada.
- [ ] **Formatação de Imagem**: Sempre sugerir um nome de arquivo lógico para a `image` (ex: `divorcio-consensual.jpg`).
