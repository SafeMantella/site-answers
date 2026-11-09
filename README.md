# site-answers

Pesquisa **só leitura** em dev.to, TabNews, Hugging Face, Hackaday e Instructables, no estilo do `reddit-answers`: um comando grava `<site>-top.tsv` (candidatos com score) e `<site>-read.md` (os primeiros lidos, com comentários). Sem login, sem chave, sem API paga.

```bash
./answers <devto|tabnews|huggingface|hackaday|instructables> "consulta" -d pasta/ [-t 8]
./answers --self-check
```

Skills (`skills/<site>-answers/SKILL.md`): `devto-answers`, `tabnews-answers`, `huggingface-answers`, `hackaday-answers`, `instructables-answers`. Instalar: `ln -s "$PWD"/skills/* ~/.claude/skills/`.

Limites: TabNews não tem busca: filtra o título nas 300 mais relevantes e 200 mais novas; Instructables renderiza a página (precisa de `patchright`, usa o venv do Scrapling se existir ao lado) e não traz comentários.
