# Perfil FILES — v1.0

Baseline de referência: `baseline/SECURITY_BASELINE.md`\
Perfil: FILES

Sistemas com upload, download, mídia, documentos, anexos, conversão,
compactação ou processamento de arquivos.

## Como ler a matriz

- M — Mandatory: em geral, precisa ser verificado quando este perfil está ativo.
- C — Conditional: depende da arquitetura ou da funcionalidade; investigue antes de decidir.
- N — Normally N/A: em geral, não pertence a esta superfície, mas isso não transforma o controle em N/A automaticamente.

### Um cuidado importante

O perfil serve para organizar a triagem. Ele não é uma autorização para pular controles.

Um `N` só vira `➖ N/A` quando a arquitetura real e o Threat Model justificarem essa decisão. Se outro perfil ativo classificar o mesmo controle como `M`, prevalece `M`. Se nenhum perfil marcar `M`, mas algum marcar `C`, prevalece `C`.

A Regra 99 — Evidência continua valendo em todos os casos.

## Resumo do perfil

  Classificação        Quantidade
  ------------------ ------------
  Mandatory (M)                24
  Conditional (C)              69
  Normally N/A (N)              6
  Total                99

## Matriz dos 99 controles

  -----------------------------------------------------------------------------------------
                       ID Controle                                       Classe
  ----------------------- ----------------------------------- -----------------------------
                       01 Segredos no frontend/build                      C

                       02 Segredos no Git/histórico                       C

                       03 Segredos no APK/AAB                             N

                       04 Rotação/revogação de segredo                    C
                          exposto

                       05 Validação server-side de inputs                 M

                       06 Mass assignment / campos extras                 C

                       07 SQL Injection                                   C

                       08 SQL/RPC dinâmico e allowlists                   C

                       09 IDOR/BOLA — leitura                           M

                       10 IDOR/BOLA — alteração                         C

                       11 IDOR/BOLA — exclusão                          C

                       12 IDOR/BOLA — anexos e listagens                M

                       13 RLS/isolamento no banco em tabelas              C
                          expostas (quando aplicável)

                       14 RLS/controle de dados                           C
                          deny-by-default

                       15 Isolamento cross-tenant no banco /              C
                          RLS

                       16 Policies/regras de autorização no               C
                          INSERT

                       17 Policies/regras de autorização no               C
                          UPDATE / campos sensíveis

                       18 Policies/regras de autorização no               C
                          DELETE

                       19 Funções privilegiadas / SECURITY                N
                          DEFINER / permissões (quando
                          aplicável)

                       20 Chaves administrativas/backend                  C
                          privilegiado (`service_role` ou
                          equivalente)

                       21 Serverless/Edge/API Functions —               C
                          autenticação/JWT

                       22 Serverless/Edge/API Functions —               M
                          autorização

                       23 Identidade confiável                            M

                       24 Object Storage / arquivos —                   M
                          isolamento cross-tenant

                       25 Object Storage — policies/regras              M
                          de SELECT/INSERT/UPDATE/DELETE

                       26 Buckets públicos                                M

                       27 Signed URLs / links temporários —             M
                          expiração e autorização

                       28 Autorização de upload                           M

                       29 Upload malicioso                                M

                       30 Autenticação / armazenamento de                 C
                          senhas

                       31 Rate limit no login                             C

                       32 Rate limit por usuário                          C

                       33 Rate limit por endpoint                         C

                       34 Proteção de rotas caras / abuso                 C
                          financeiro-computacional

                       35 Payload limits                                  M

                       36 Timeouts externos                               M

                       37 DDoS / WAF / proteção de origem                 C

                       38 Bots em login/cadastro                          N

                       39 CAPTCHA/Turnstile validado no                   N
                          backend

                       40 Enumeração de contas                            C

                       41 Rotas administrativas                           C

                       42 RBAC / perfis                                   C

                       43 Escalada horizontal                             C

                       44 Escalada vertical                               C

                       45 XSS                                             C

                       46 HTML/Markdown rico e sanitização                C

                       47 SSRF                                            C

                       48 SSRF avançado                                   C

                       49 Mensagens de erro sem vazamento                 M

                       50 Logs sanitizados                                M

                       51 Security headers web                            C

                       52 HTTPS/TLS obrigatório                           C

                       53 CORS                                            C

                       54 Dependências vulneráveis                        M

                       55 Supply-chain / lockfiles / origem e             C
                          manutenção de pacotes

                       56 Mobile local storage                            C

                       57 Reverse engineering / APK/AAB                   C
                          release

                       58 Prompt Injection / IA                           C

                       59 Auditoria e Incident Response /                 C
                          trilha de eventos

                       60 Security Regression Suite /                     M
                          Security Gate

                       61 Threat modeling / design seguro /               M
                          regras de negócio

                       62 Criptografia e algoritmos seguros               C

                       63 Gestão de chaves criptográficas                 C

                       64 Sessão, tokens e ciclo de vida de               C
                          autenticação

                       65 MFA, recuperação de conta e                     C
                          operações de alto impacto

                       66 Configuração insegura, debug e                  C
                          defaults

                       67 Inventário de APIs, versões e                   C
                          endpoints esquecidos

                       68 Consumo seguro de APIs e dados de               C
                          terceiros

                       69 Webhooks: autenticidade, replay e               C
                          idempotência

                       70 Integridade de software, CI/CD e                C
                          artefatos

                       71 Falhas seguras e condições                      C
                          excepcionais

                       72 Concorrência, race conditions,                  C
                          replay e idempotência de negócio

                       73 Privacidade, minimização, retenção              M
                          e exclusão

                       74 Mobile: permissões, componentes,                N
                          deep links e IPC

                       75 Mobile: rede, atualização,                      N
                          plataforma e resiliência

                       76 \[API\]\[CORE\] Command Injection /             C
                          execução de comandos do sistema
                          operacional

                       77 \[API\]\[FILES\] Desserialização                M
                          insegura / XXE / parsers

                       78 \[FILES\]\[API\] Path Traversal /               M
                          LFI / manipulação de caminhos

                       79 \[FILES\]\[WEB\]\[API\] Download                M
                          seguro de arquivos

                       80 \[OAUTH\]\[WEB\]\[MOBILE\]\[API\]               C
                          OAuth 2.x / OpenID Connect / SSO

                       81 \[REALTIME\]\[WEB\]\[API\]                      C
                          WebSockets / realtime

                       82 \[API\] GraphQL                                 C

                       83 \[API\]\[INFRA\] Service-to-service             C
                          / machine-to-machine

                       84 \[FILES\]\[API\]\[WEB\] Malware,                M
                          arquivos comprimidos e
                          processamento de arquivos

                       85 \[AI\]\[CORE\] AI Sensitive                     C
                          Information Disclosure / exposição
                          de dados à IA

                       86 \[AI\]\[API\] AI Tool/Agent                     C
                          Permissions / Excessive Agency

                       87 \[AI\]\[SAAS\] RAG / Vector                     C
                          Database / Embeddings Isolation

                       88 \[AI\] Data / Model / Knowledge                 C
                          Poisoning

                       89 \[AI\]\[WEB\]\[API\] AI Output                  C
                          Handling

                       90 \[AI\] System Prompt / Agent                    C
                          Configuration / Secrets

                       91 \[AI\]\[API\] AI Cost / Token /                 C
                          Tool Budget / Unbounded Consumption

                       92 \[INFRA\]\[API\] Container /                    C
                          Runtime Hardening

                       93 \[INFRA\]\[API\] Cloud IAM /                    C
                          Service Accounts / Least Privilege

                       94 \[INFRA\]\[CORE\] Backup Security +             C
                          Restore Test

                       95 \[WEB\]\[API\] Prototype Pollution              C

                       96 \[WEB\]\[API\]\[SAAS\] Cache                    C
                          Security / Cache Poisoning /
                          Cross-user Leakage

                       97 \[CORE\]\[INFRA\] Security Kill                 C
                          Switch / Contenção de Emergência

                       98 \[CORE\]\[INFRA\]                               C
                          Dependency/Provider Failure &
                          Security Exit Strategy

                       99 REGRA-MESTRA DE EVIDÊNCIA                       M
  -----------------------------------------------------------------------------------------

## Como ativar este perfil

Quando este perfil estiver ativo:

1.  leia o `THREAT_MODEL.md`;
2.  combine esta matriz com todos os outros perfis ativos;
3.  aplique a precedência `M > C > N`;
4.  justifique todo controle marcado como `➖ N/A`;
5.  registre a matriz final no `SECURITY_AUDIT_RESULTS.md`;
6.  não altere o baseline para adaptar o projeto.

## O que a IA deve devolver

``` text
Perfil ativo: FILES
Mandatory:
Conditional:
Normally N/A:
Controles promovidos por outros perfis:
N/A confirmados após Threat Model:
Pendências de aplicabilidade:
```

A ideia é reduzir ruído sem reduzir o rigor da análise.
