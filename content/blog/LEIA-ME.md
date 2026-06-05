# Como criar um novo post de blog

Para criar um novo post de blog, siga os passos abaixo:

1.  **Crie um arquivo Markdown (.md)**: Dentro desta pasta (`content/blog`), crie um novo arquivo com a extensão `.md`. O nome do arquivo pode ser o título do seu post, por exemplo, `meu-primeiro-post.md`.

2.  **Adicione o Front Matter YAML**: No início do seu arquivo Markdown, adicione um bloco de *Front Matter* em formato YAML. Este bloco contém metadados sobre o post e é delimitado por três hífens (`---`) no início e no fim. Os campos obrigatórios são `title` e `date`. Outros campos úteis incluem `author`, `categories`, `tags` e `image`.

    **Exemplo de Front Matter:**
    ```yaml
    ---
    title: "Meu Primeiro Post no Novo Blog"
    date: "2026-06-05T10:00:00Z" # Formato ISO 8601
    author: "Gabriel Corrêa"
    categories: ["Direito Civil", "Notícias"]
    tags: ["advocacia", "blog", "direito"]
    image: "minha-imagem-principal.jpg" # Caminho relativo a /public/images ou URL externa
    excerpt: "Este é um breve resumo do meu primeiro post, que aparecerá na listagem do blog."
    ---
    ```

3.  **Escreva o conteúdo do post em Markdown**: Após o bloco de Front Matter, escreva o conteúdo do seu post usando a sintaxe Markdown padrão. Você pode usar títulos, parágrafos, listas, links, etc.

4.  **Adicione imagens**: Para incluir imagens no seu post, você pode:
    *   **Usar imagens locais**: Coloque suas imagens na pasta `/public/images`. No seu Markdown, referencie-as usando o nome do arquivo (ex: `![Descrição da Imagem](minha-imagem-no-post.png)`). O sistema irá automaticamente resolver o caminho para `/public/images/minha-imagem-no-post.png`.
    *   **Usar URLs externas**: Você pode referenciar imagens diretamente de URLs externas (ex: `![Logo Unsplash](https://images.unsplash.com/photo-12345.jpg)`).

    A imagem definida no campo `image` do Front Matter será usada como imagem principal (thumbnail) do post.

5.  **Execute o script de sincronização**: Após criar ou modificar seus arquivos Markdown, execute o script `scripts/sync_posts.py` para gerar os arquivos HTML e atualizar o `index.json` do blog.

    ```bash
    python3 scripts/sync_posts.py
    ```

6.  **Commit e Push**: Faça o commit das suas alterações e envie-as para o repositório GitHub para que o site seja atualizado.

    ```bash
    git add content/blog/ meu-primeiro-post.md public/images/minha-imagem-principal.jpg scripts/sync_posts.py
    git commit -m "Adiciona meu primeiro post de blog e atualiza script de sincronização"
    git push
    ```

## Exemplo de Post (exemplo-post.md)

```markdown
---
title: "A Importância do Direito Digital na Era Moderna"
date: "2026-06-05T11:30:00Z"
author: "Gabriel Corrêa"
categories: ["Direito Digital", "Tecnologia"]
tags: ["LGPD", "cibersegurança", "privacidade"]
image: "direito-digital.jpg"
excerpt: "Descubra como o Direito Digital protege seus dados e sua privacidade no mundo conectado de hoje."
---

## Introdução

A era digital trouxe consigo uma série de desafios e oportunidades. Com a crescente dependência da tecnologia, a necessidade de **leis e regulamentações** que protejam os indivíduos e as empresas no ambiente online tornou-se crucial. O Direito Digital surge como uma área fundamental para garantir a segurança jurídica neste novo cenário.

## O que é Direito Digital?

O Direito Digital é um ramo do direito que abrange todos os aspectos legais relacionados ao uso da tecnologia da informação e comunicação. Ele lida com questões como privacidade de dados, crimes cibernéticos, contratos eletrônicos, propriedade intelectual na internet e muito mais. Sua principal função é adaptar os princípios jurídicos tradicionais à realidade do mundo digital.

### LGPD e Proteção de Dados

No Brasil, a **Lei Geral de Proteção de Dados (LGPD)** é um marco importante do Direito Digital. Ela estabelece regras sobre a coleta, armazenamento, tratamento e compartilhamento de dados pessoais, visando proteger os direitos fundamentais de liberdade e de privacidade. Empresas que não cumprem a LGPD estão sujeitas a multas e sanções severas.

![Computador com cadeado](computador-seguro.jpg)

## Cibersegurança e Crimes Cibernéticos

Com o aumento das atividades online, os crimes cibernéticos também se tornaram mais sofisticados. Fraudes, roubo de dados, invasão de sistemas e difamação online são apenas alguns exemplos. O Direito Digital atua na prevenção e repressão desses crimes, buscando responsabilizar os infratores e proteger as vítimas.

### Dicas de Segurança Online

Para se proteger no ambiente digital, é fundamental adotar algumas práticas:

-   Use senhas fortes e únicas.
-   Mantenha seus softwares atualizados.
-   Desconfie de e-mails e mensagens suspeitas.
-   Faça backup de seus dados regularmente.

## Conclusão

O Direito Digital é uma área em constante evolução, essencial para a segurança e o desenvolvimento da sociedade na era da informação. Estar ciente de seus direitos e deveres no ambiente online é o primeiro passo para uma navegação segura e responsável.

**Precisa de ajuda profissional?** Fale agora com o Advogado Gabriel Corrêa pelo WhatsApp: [📞 (47) 98867-0233](https://wa.me/5547988670233?text=Olá%21%20Vim%20através%20do%20site%20e%20gostaria%20de%20resolver%20um%20problema%20que%20eu%20tenho%21%20%F0%9F%A4%9D)
```

```
