---
name: huggingface-answers
description: Pesquisa em Hugging Face (só leitura) via API/página pública, com score e comentários. Usar quando o Pedro pedir pesquisa em Hugging Face, modelos, datasets, spaces e papers sobre X, o que está em alta, ou validar um tema. Funciona em qualquer projeto.
---

# Hugging Face Answers (global)

Ferramenta local: `/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers` (um script, 5 sites; sem login nem chave).

## Regra

Só leitura. **Nunca postar, comentar nem votar.** Poucas buscas, espaçadas (o script espera 1s entre requisições).

## Uso

```bash
A="/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers"
"$A" huggingface "consulta em inglês" -d <pasta-de-saida>/ [-t 8]
```

- Saída em `<pasta>/`: `huggingface-top.tsv` (candidatos: score, n, data, título, url) e `huggingface-read.md` (os `-t` primeiros lidos, com comentários).
- Traz modelos, datasets, spaces e papers juntos, ordenados por likes. n = downloads (ou comentários, em papers). Lê README e discussões abertas.
- `ERRO: ...` → o site mudou ou caiu; mostrar o erro ao Pedro, não insistir em loop.
- Leia `huggingface-read.md` e entregue um resumo (dores, números, ângulos), não o dump.
