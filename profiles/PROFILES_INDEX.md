# Security Profiles — índice v1.0

Baseline de referência: `baseline/SECURITY_BASELINE.md`

Os Profiles ajudam a aproximar o baseline da arquitetura real do projeto. Eles não substituem o Threat Model e não servem para diminuir artificialmente o número de controles.

Ative todos os perfis que realmente descrevem o sistema.

## Perfis disponíveis

  Perfil     Uso
  ---------- ---------------------------------
  CORE       Base transversal
  WEB        Navegador/frontend web
  API        Backend/API/serverless
  SAAS       Multiusuário/multi-tenant
  MOBILE     Android/iOS
  AI_AGENT   LLM/RAG/agentes/tools
  FILES      Upload/download/processamento
  REALTIME   WebSocket/pub-sub/subscriptions
  OAUTH      OAuth/OIDC/SSO
  INFRA      Cloud/runtime/CI-CD/IAM/backups

## Como combinar os perfis

Para cada controle, use a precedência:

`M > C > N`

Exemplo: CORE=C, API=M, SAAS=M, MOBILE=N → resultado final M.

`N` não significa N/A automático. O Threat Model ainda precisa justificar essa decisão.

## Fluxo

`Threat Model → ativar perfis → combinar matrizes → confirmar aplicabilidade → Baseline 99 → Audit Results`

## Resumo das matrizes

  Perfil        M    C    N
  ---------- ---- ---- ----
  CORE         50   49    0
  WEB          13   63   23
  API          38   55    6
  SAAS         30   65    4
  MOBILE       25   67    7
  AI_AGENT     24   62   13
  FILES        24   69    6
  REALTIME     26   65    8
  OAUTH        23   72    4
  INFRA        29   69    1

## Um cuidado importante

Os perfis devem nascer da arquitetura existente, não do desejo de reduzir o escopo da auditoria.

Se houver dúvida razoável sobre uma superfície, mantenha o controle como `C` ou `❓` até conseguir verificar.

## Regra 99

Independentemente dos perfis ativos, a Regra-Mestra de Evidência continua obrigatória.

Os Profiles ajudam a decidir o que merece atenção. A evidência é o que decide se um controle pode receber ✅.
