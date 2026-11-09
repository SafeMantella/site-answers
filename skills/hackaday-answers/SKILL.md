---
name: hackaday-answers
description: Pesquisa em Hackaday (só leitura) via API/página pública, com score e comentários. Usar quando o Pedro pedir pesquisa em Hackaday, projetos de hardware/hacking sobre X, ideias de vídeo de projeto, ou validar um tema. Funciona em qualquer projeto.
---

# Hackaday Answers (global)

Ferramenta local: `/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers` (um script, 5 sites; sem login nem chave).

## Regra

Só leitura. **Nunca postar, comentar nem votar.** Poucas buscas, espaçadas (o script espera 1s entre requisições).

## Uso

```bash
A="/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers"
"$A" hackaday "consulta em inglês" -d <pasta-de-saida>/ [-t 8]
```

- Saída em `<pasta>/`: `hackaday-top.tsv` (candidatos: score, n, data, título, url) e `hackaday-read.md` (os `-t` primeiros lidos, com comentários).
- O site não tem score: a ordem é a relevância da busca. Lê o texto do post e os comentários.
- `ERRO: ...` → o site mudou ou caiu; mostrar o erro ao Pedro, não insistir em loop.
- Leia `hackaday-read.md` e entregue um resumo (dores, números, ângulos), não o dump.
