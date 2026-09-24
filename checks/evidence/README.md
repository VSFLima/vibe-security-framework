# Evidence → Baseline Mapping — v1.0

Esta camada conecta as evidências produzidas por checks e adapters aos controles do baseline.

Ela não fecha controles automaticamente.

## Regra central

Um `PASS` de scanner informa apenas que aquela execução não encontrou findings dentro do escopo e da configuração utilizados.

Por isso, o mapper registra essa evidência como `REVIEW_REQUIRED` e `auto_validated: false`.

Para um controle receber `✅`, continuam valendo os requisitos da Regra 99: implementação ou configuração verificável, teste negativo, teste positivo, resultado real, correção e reteste quando aplicável e registro do risco residual.

## Mapeamentos iniciais

- Gitleaks → controles 1, 2, 3, 4 e 70.
- Trivy → controles 54, 55 e 70.

Esses vínculos representam evidência de apoio. Eles não significam equivalência lógica entre um scanner e um controle.

Checks desconhecidos são enviados para `unmapped_or_invalid`; eles não são descartados silenciosamente.

## Uso

``` bash
python checks/evidence/map_evidence.py   --evidence security-evidence/gitleaks.json   --evidence security-evidence/trivy.json   --output security-evidence/control-evidence.json
```
