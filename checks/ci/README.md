# CI / SARIF — v0.3.2

O framework inclui um workflow de referência em:

`.github/workflows/vibe-security.yml`

Ele executa os checks, reúne as evidências normalizadas, gera SARIF e preserva os relatórios como artifact.

## Pontos importantes

- `NOT_AVAILABLE`, `NOT_RUN` e `ERROR` nunca são convertidos em `PASS`.
- O SARIF funciona como superfície de visualização e integração; ele não é a fonte da verdade do Audit Results.
- O workflow usa `fetch-depth: 0` para permitir análise do histórico Git.
- As evidências ficam preservadas por tempo limitado no artifact do CI.
- O gate falha em `FAIL` ou `ERROR`. `NOT_AVAILABLE` continua visível e exige decisão ou configuração, sem ser mascarado como sucesso.

Este workflow é um template de referência. Dependendo do projeto, pode ser necessário instalar Gitleaks ou Trivy antes de executar os adapters. Se as ferramentas não estiverem disponíveis, os adapters registram `NOT_AVAILABLE`.
