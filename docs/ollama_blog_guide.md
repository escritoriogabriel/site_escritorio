# Guia de Geração de Posts de Blog Local com Ollama (Versão PRO)

Este guia detalha como usar o novo script altamente configurável para gerar posts de blog usando o Ollama localmente. Agora você pode definir temas, usar links de referência e dar instruções específicas para a IA.

## 1. Instalação e Requisitos

Certifique-se de ter o Ollama instalado e rodando (veja a versão básica deste guia se precisar de ajuda com a instalação).

Além do Python 3, instale as bibliotecas necessárias para o novo script:

```bash
pip install requests beautifulsoup4
```

## 2. Como usar o Script PRO

O script `generate_blog_post_ollama.py` agora aceita comandos via terminal. Abra o terminal na pasta do seu projeto e use os seguintes comandos:

### 2.1. Gerar por Tema Específico
Se você já sabe sobre o que quer escrever:
```bash
python scripts/generate_blog_post_ollama.py --tema "Como funciona a Revisão da Vida Toda no INSS"
```

### 2.2. Usar um Link de Referência
Se você viu uma notícia ou artigo e quer que a IA use como base (ela vai ler o link e criar um post novo baseado nele):
```bash
python scripts/generate_blog_post_ollama.py --tema "Novas regras da Aposentadoria" --link "https://g1.globo.com/economia/noticia/link-da-noticia"
```

### 2.3. Dar Instruções Personalizadas
Se você quer que a IA foque em algo específico ou use um tom de voz diferente:
```bash
python scripts/generate_blog_post_ollama.py --tema "Pensão Alimentícia" --instrucoes "Foque nos direitos dos pais e explique como o cálculo é feito na prática."
```

### 2.4. Combinar Tudo (Poder Total)
Você pode usar todos os argumentos juntos para um resultado perfeito:
```bash
python scripts/generate_blog_post_ollama.py --tema "Indenização por Atraso de Voo" --link "https://www.anac.gov.br/noticia" --instrucoes "Cite exemplos de valores de indenização e mencione que atendemos casos em todo o Brasil."
```

## 3. Parâmetros Disponíveis

| Parâmetro | Descrição | Obrigatório |
| :--- | :--- | :--- |
| `--tema` | O título ou assunto principal do post. | **Sim** |
| `--link` | URL de um site para a IA ler e usar como contexto. | Não |
| `--instrucoes` | Comandos extras para a IA (ex: "seja formal", "use listas"). | Não |
| `--modelo` | Mudar o modelo do Ollama (ex: `--modelo mistral`). | Não |

## 4. O que acontece após rodar o comando?

1.  **Leitura:** O script lê o link (se fornecido) e prepara o comando para a IA.
2.  **Geração:** O Ollama processa o pedido e gera o texto em Markdown.
3.  **Arquivos:** O script cria o arquivo `.md` em `blog/posts/` e atualiza o `index.json`.
4.  **Imagem:** Um "espaço reservado" para imagem é criado em `blog/images/`.

## 5. Publicando no Site

Após gerar o post no seu computador:
1.  Substitua a imagem na pasta `blog/images/` por uma foto real (opcional, mas recomendado).
2.  No terminal, envie para o GitHub:
    ```bash
    git add .
    git commit -m "Novo post: [Título do Post]"
    git push origin main
    ```

Seu novo post aparecerá no carrossel da página inicial e na página do blog automaticamente!
