---
name: devto-answers
description: Pesquisa em dev.to (só leitura) via API/página pública, com score e comentários. Usar quando o Pedro pedir pesquisa em dev.to, o que devs escrevem sobre X, tutoriais e opinião técnica, ou validar um tema. Funciona em qualquer projeto.
---

# dev.to Answers (global)

Ferramenta local: `/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers` (um script, 5 sites; sem login nem chave).

## Regra

Só leitura. **Nunca postar, comentar nem votar.** Poucas buscas, espaçadas (o script espera 1s entre requisições).

## Uso

```bash
A="/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers"
"$A" devto "consulta em inglês" -d <pasta-de-saida>/ [-t 8]
```

- Saída em `<pasta>/`: `devto-top.tsv` (candidatos: score, n, data, título, url) e `devto-read.md` (os `-t` primeiros lidos, com comentários).
- Busca de texto real (`/api/articles/search`), ordenada por relevância. Score = reações; n = comentários. Consulta em inglês.
- `ERRO: ...` → o site mudou ou caiu; mostrar o erro ao Pedro, não insistir em loop.
- Leia `devto-read.md` e entregue um resumo (dores, números, ângulos), não o dump.
