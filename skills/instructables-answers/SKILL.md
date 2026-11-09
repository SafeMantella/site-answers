---
name: instructables-answers
description: Pesquisa em Instructables (só leitura) via API/página pública, com score e comentários. Usar quando o Pedro pedir pesquisa em Instructables, projetos DIY/eletrônica sobre X, ideias de vídeo de projeto, ou validar um tema. Funciona em qualquer projeto.
---

# Instructables Answers (global)

Ferramenta local: `/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers` (um script, 5 sites; sem login nem chave).

## Regra

Só leitura. **Nunca postar, comentar nem votar.** Poucas buscas, espaçadas (o script espera 1s entre requisições).

## Uso

```bash
A="/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers"
"$A" instructables "consulta em inglês" -d <pasta-de-saida>/ [-t 8]
```

- Saída em `<pasta>/`: `instructables-top.tsv` (candidatos: score, n, data, título, url) e `instructables-read.md` (os `-t` primeiros lidos, com comentários).
- A busca deles é JS e a API exige chave, então o script renderiza a página (patchright). Score = favoritos; n = views; sem comentários.
- `ERRO: ...` → o site mudou ou caiu; mostrar o erro ao Pedro, não insistir em loop.
- Leia `instructables-read.md` e entregue um resumo (dores, números, ângulos), não o dump.
