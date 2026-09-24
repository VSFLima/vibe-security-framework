# Release Security Gate — template v1.0

Arquivo de referência: `baseline/SECURITY_BASELINE.md`\
Este template ajuda a decidir se os critérios de segurança definidos para uma release foram atendidos com a evidência disponível.

> Um `PASS` não significa “software invulnerável”. Ele informa apenas que o gate abaixo foi atendido com evidência atual.

## 1. Release

-   Projeto:
-   Versão/build:
-   Commit/tag:
-   Ambiente:
-   Data:
-   Responsável:
-   Link/referência ao `SECURITY_AUDIT_RESULTS.md`:
-   Link/referência ao `THREAT_MODEL.md`:

## 2. O que mudou nesta release

-   [ ] Auth
-   [ ] Autorização/RBAC/RLS
-   [ ] Banco/schema
-   [ ] API/Edge Functions
-   [ ] Storage/uploads/downloads
-   [ ] Mobile
-   [ ] Web
-   [ ] Realtime
-   [ ] OAuth/SSO
-   [ ] IA/RAG/tools
-   [ ] Infra/cloud
-   [ ] Dependências
-   [ ] Secrets/configuração
-   [ ] Nenhuma das anteriores

Descreva mudanças relevantes:

## 3. O que bloqueia a release

Se qualquer condição abaixo for verdadeira, o resultado continua `FAIL` até que haja correção e reteste:

-   [ ] Existe P0 conhecido aberto.
-   [ ] Existe segredo exposto ativo.
-   [ ] Há evidência invalidada em componente crítico alterado e ainda
    não revalidada.
-   [ ] Teste negativo crítico falhou.
-   [ ] Fluxo legítimo crítico falhou após correção.
-   [ ] Há bypass conhecido de autenticação/autorização.
-   [ ] Build/deploy analisado não corresponde ao artefato que será
    liberado.
-   [ ] Risco crítico está apenas "aceito" sem mecanismo formal
    permitido pelo projeto.

## 4. Verificações que precisam estar em dia

### Evidência e regressão

-   [ ] Controles afetados pela mudança foram identificados.
-   [ ] Evidências afetadas foram revalidadas.
-   [ ] Testes negativos relevantes passaram.
-   [ ] Testes positivos relevantes passaram.
-   [ ] Regressões de segurança passaram.

### Secrets e supply chain

-   [ ] Secret scan aplicável executado.
-   [ ] Artefato/build aplicável inspecionado.
-   [ ] Dependências críticas verificadas conforme política.
-   [ ] Lockfiles/origens permanecem coerentes.

### Auth, autorização e isolamento

-   [ ] Fluxos de autenticação alterados foram testados.
-   [ ] IDOR/BOLA/cross-tenant relevante foi retestado.
-   [ ] Operações administrativas/sensíveis foram retestadas.

### Dados e arquivos

-   [ ] Inputs alterados possuem validação server-side.
-   [ ] Upload/download/storage alterados foram retestados.
-   [ ] Logs/erros não ganharam vazamento novo.

### IA, quando aplicável

-   [ ] Tools mantêm autorização determinística.
-   [ ] RAG/tenant isolation relevante foi retestado.
-   [ ] Saída da IA continua tratada como não confiável.
-   [ ] Limites de custo/tokens/tools permanecem adequados.

### Infra/operação

-   [ ] Configuração de produção corresponde ao esperado.
-   [ ] Kill switch/contenção continua disponível quando aplicável.
-   [ ] Backup/restore não foi impactado por mudança relevante.
-   [ ] Observabilidade necessária para detectar abuso está ativa.

## 5. P1, P2 e riscos residuais

  -----------------------------------------------------------------------------
  Controle    Status      Risco       Decisão     Responsável   Prazo/revisão
                          residual
  ----------- ----------- ----------- ----------- ------------- ---------------

  -----------------------------------------------------------------------------

Um P1 não tratado precisa seguir a política de risco do projeto. Não o esconda como ✅.

## 6. Resultado

Escolha um único resultado:

-   [ ] PASS — critérios do gate satisfeitos com evidência atual.
-   [ ] FAIL — existe bloqueador ou teste obrigatório falhou.
-   [ ] INCONCLUSIVO — evidência necessária não pôde ser obtida.

### Como registrar a decisão

-   Resultado:
-   Evidências principais:
-   Controles revalidados:
-   Pendências:
-   Risco residual:
-   Data:
-   Responsável:

## 7. Depois da release

-   [ ] Monitorar sinais relevantes de abuso/falha.
-   [ ] Registrar incidente ou regressão se algo escapar.
-   [ ] Invalidar evidências afetadas por hotfix/mudança emergencial.
-   [ ] Atualizar `SECURITY_AUDIT_RESULTS.md`.

A decisão de release deve se apoiar na evidência atual, não na confiança em quem ou no que escreveu o código.
