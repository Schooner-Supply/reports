# Käyttäjätason Claude Code -asetukset

Sama sallittujen/kysyttävien lista kuin repon `.claude/settings.json`,
mutta hook-polku osoittaa kotihakemistoon. Asenna omalle koneelle:

```bash
mkdir -p ~/.claude/hooks
cp .claude/user-level/settings.json ~/.claude/settings.json   # yhdistä käsin, jos sinulla on jo oma
cp .claude/hooks/guard.py ~/.claude/hooks/guard.py
```

Uudet repot perivät listan käyttäjätasolta; repokohtainen `.claude/settings.json`
voi lisätä tai kiristää sääntöjä.
