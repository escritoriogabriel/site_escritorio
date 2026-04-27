# Guia de Geração de Posts de Blog Local com Ollama

Este guia detalha como configurar e usar o Ollama para gerar posts de blog localmente, de forma gratuita e com controle total sobre o processo. Os posts gerados serão compatíveis com o seu site estático no GitHub Pages.

## 1. O que é Ollama?

O [Ollama](https://ollama.com/) é uma ferramenta que permite rodar modelos de linguagem grandes (LLMs) localmente no seu computador. Isso significa que você pode usar IAs como Llama 3, Mistral, Gemma, entre outros, sem precisar de uma conexão com a internet (após o download inicial do modelo) e sem custos de API. É ideal para geração de conteúdo em massa, pois o processamento é feito na sua máquina.

## 2. Instalação do Ollama

### 2.1. Baixar e Instalar o Ollama

1.  Acesse o site oficial do Ollama: [https://ollama.com/download](https://ollama.com/download)
2.  Baixe o instalador para o seu sistema operacional (Windows, macOS, Linux).
3.  Siga as instruções de instalação. É um processo simples de "próximo, próximo, finalizar".

### 2.2. Baixar um Modelo de Linguagem

Após instalar o Ollama, você precisará baixar um modelo de linguagem para usar. Sugiro o `llama3` ou `mistral`, que são excelentes para geração de texto.

1.  Abra o **Terminal** (macOS/Linux) ou **Prompt de Comando/PowerShell** (Windows).
2.  Execute o comando para baixar o modelo:
    ```bash
    ollama run llama3
    ```
    ou
    ```bash
    ollama run mistral
    ```
    O Ollama fará o download do modelo (pode levar alguns minutos, dependendo da sua conexão e do tamanho do modelo). Após o download, ele iniciará uma sessão de chat com o modelo. Você pode digitar ` /bye` para sair da sessão.

## 3. Usando o Script de Geração de Posts

Você tem um script Python chamado `generate_blog_post_ollama.py` no diretório `scripts/` do seu repositório. Este script se conecta ao Ollama que está rodando localmente e gera um post de blog completo.

### 3.1. Pré-requisitos

Certifique-se de ter o Python 3 instalado no seu sistema. Você também precisará instalar a biblioteca `requests`:

```bash
pip install requests
```

### 3.2. Executando o Script

1.  **Certifique-se de que o Ollama está rodando:** O Ollama deve estar ativo em segundo plano. Se você acabou de baixar um modelo com `ollama run <modelo>`, ele já estará rodando. Caso contrário, você pode iniciá-lo (geralmente ele inicia automaticamente com o sistema ou você pode abri-lo como um aplicativo).
2.  **Navegue até o diretório do seu site:**
    ```bash
    cd /caminho/para/seu/site_escritorio
    ```
3.  **Execute o script:**
    ```bash
    python scripts/generate_blog_post_ollama.py
    ```

O script selecionará um tópico do arquivo `scripts/blog_config.json`, gerará o conteúdo usando o Ollama e criará um novo arquivo `.md` na pasta `blog/posts/` e um `index.json` atualizado.

### 3.3. Personalizando o Script (Opcional)

Você pode editar o arquivo `scripts/blog_config.json` para adicionar mais tópicos, palavras-chave e públicos-alvo. Quanto mais detalhado for o tópico, melhor será a qualidade do post gerado.

Você também pode editar o `generate_blog_post_ollama.py` para mudar o `OLLAMA_MODEL` (linha 30) para o modelo que você baixou (ex: `mistral`).

## 4. Publicando os Posts no GitHub Pages

Após gerar os posts localmente, você precisará adicioná-los ao seu repositório e fazer o push para o GitHub:

1.  **Adicione os novos arquivos:**
    ```bash
    git add blog/posts/*.md blog/images/* blog/posts/index.json
    ```
2.  **Faça o commit:**
    ```bash
    git commit -m "feat: Novo post de blog gerado localmente com Ollama"
    ```
3.  **Faça o push:**
    ```bash
    git push origin main
    ```

O GitHub Pages detectará as mudanças e publicará automaticamente os novos posts no seu blog. Lembre-se de que o `blog-loader.js` (que já está no seu site) é responsável por ler o `index.json` e exibir os posts dinamicamente.

## 5. Próximos Passos (Melhorias)

*   **Geração de Imagens:** Você pode integrar APIs de geração de imagens (como DALL-E ou Stable Diffusion) ao script para gerar imagens automaticamente para cada post, ou usar APIs de bancos de imagens gratuitos (Unsplash, Pexels) para buscar imagens relevantes.
*   **Revisão e Otimização:** Sempre revise os posts gerados pela IA para garantir a precisão jurídica, a qualidade e a otimização para SEO antes de publicar. O script é uma ferramenta de produtividade, mas a curadoria humana é essencial.
*   **Agendamento:** Você pode criar um script de automação no seu próprio computador (usando `cron` no Linux/macOS ou `Task Scheduler` no Windows) para rodar o `generate_blog_post_ollama.py` em intervalos regulares, automatizando ainda mais o processo.
