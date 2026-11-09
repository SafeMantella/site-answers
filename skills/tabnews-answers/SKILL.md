---
name: tabnews-answers
description: Pesquisa em TabNews (só leitura) via API/página pública, com score e comentários. Usar quando o Pedro pedir pesquisa em TabNews, o que devs brasileiros discutem sobre X, dores do público BR, ou validar um tema. Funciona em qualquer projeto.
---

# TabNews Answers (global)

Ferramenta local: `/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers` (um script, 5 sites; sem login nem chave).

## Regra

Só leitura. **Nunca postar, comentar nem votar.** Poucas buscas, espaçadas (o script espera 1s entre requisições).

## Uso

```bash
A="/Volumes/1TB Mac/Desktop/social media/ferramentas/site-answers/answers"
"$A" tabnews "consulta em português" -d <pasta-de-saida>/ [-t 8]
```

- Saída em `<pasta>/`: `tabnews-top.tsv` (candidatos: score, n, data, título, url) e `tabnews-read.md` (os `-t` primeiros lidos, com comentários).
- Sem endpoint de busca: filtra o título nas 300 mais relevantes e 200 mais novas; tema de nicho pode voltar 0 resultados. Score = tabcoins; n = comentários.
- `ERRO: ...` → o site mudou ou caiu; mostrar o erro ao Pedro, não insistir em loop.
- Leia `tabnews-read.md` e entregue um resumo (dores, números, ângulos), não o dump.
