# Política de CI — release candidate 2

O workflow de referência usa a política `strict`.

Nesse modo, `FAIL`, `ERROR`, `NOT_AVAILABLE` e `NOT_RUN` bloqueiam o job. Um `WARN` não é transformado silenciosamente em `PASS`.

Gitleaks e Trivy são instalados em versões fixas, e os archives são verificados por SHA-256 antes da instalação. Antes do scan do projeto, o Gitleaks executa um canário sintético.

Esse canário contém apenas uma credencial com formato de teste e deliberadamente inválida. Ele existe para mostrar que o mecanismo de detecção está realmente funcionando, em vez de devolver um falso “nenhum finding”.

As GitHub Actions usam as gerações atuais verificadas durante esta revisão:

`checkout@v7`, `setup-python@v7`, `upload-sarif@v4`, `upload-artifact@v7`.

Em ambientes de alta garantia, considere pin por SHA completo e uma atualização automatizada controlada.

A execução real no GitHub continua sendo evidência obrigatória antes da release pública.
