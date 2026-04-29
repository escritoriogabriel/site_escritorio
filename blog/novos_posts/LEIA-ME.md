# Como Publicar um Novo Post no Blog

## Passo a Passo

1. **Crie seu arquivo `.md`** nesta pasta (`blog/novos_posts/`)
2. **Copie o template abaixo** e preencha os campos
3. **Execute** o `sincronizar_posts.bat` (Windows) ou `sincronizar_posts.sh` (Linux/Mac)
4. O script processa o arquivo e **publica automaticamente** no GitHub Pages

---

## Template do Arquivo .md

Copie o conteúdo abaixo e salve como `NOME-DO-POST.md` nesta pasta:

```markdown
---
title: "Título do Post Aqui"
description: "Breve descrição do post para aparecer nos cards do blog (1-2 frases)."
date: 2026-04-29T00:00:00.000000
author: Gabriel Corrêa
category: Direito do Trabalho
tags:
  - palavra-chave-1
  - palavra-chave-2
  - palavra-chave-3
---

# Título do Post Aqui

Parágrafo de introdução...

## Seção 1

Conteúdo da seção...

## Seção 2

Conteúdo da seção...

## Conclusão

Texto de encerramento...
```

---

## Campos Obrigatórios

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `title` | Título completo do post | `"Direitos na Demissão"` |
| `description` | Resumo para o card do blog | `"Saiba seus direitos..."` |
| `date` | Data de publicação | `2026-04-29T00:00:00.000000` |
| `category` | Área do direito | `Direito do Trabalho` |

## Categorias Disponíveis

- `Direito do Trabalho`
- `Direito de Família`
- `Direito Criminal`
- `Direito Civil`
- `Busca e Apreensão`
- `Direito de Trânsito`
- `Direito`

---

## Atenção

- O arquivo **DEVE** começar com o bloco `---` (front matter YAML)
- O campo `title:` é **obrigatório** — sem ele o post é ignorado
- Após rodar o script, o post aparece no site em **1-2 minutos** (tempo do GitHub Pages)
