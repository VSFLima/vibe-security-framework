## 1.0.0

- Promovido o RC9 validado para a primeira release estável do Vibe Security Framework.
- Hardening final do scanner nativo de histórico Git após inspeção das evidências do CI.
- Fixtures sintéticas históricas conhecidas passam a ser ignoradas somente por valor exato, sem allowlist ampla de commits ou arquivos.
- Findings diferentes continuam sendo detectados normalmente.
- `native checks` passam a bloquear o pipeline em caso de `FAIL`; removido o mascaramento por `|| true`.
- Adicionados testes de regressão para fixture sintética conhecida e valor credential-shaped não allowlisted.
- Suíte automatizada ampliada de 33 para 35 testes.
- Baseline preservado em 99 controles.
- Gitleaks, canário Gitleaks, Trivy, native checks, evidence mapping e strict release gate validados em CI real.
- SARIF permanece gerado e incluído no artifact de evidências.
- Upload ao GitHub Code Scanning permanece best-effort quando o recurso não está disponível no repositório.
- Nenhuma validação externa obrigatória permanece pendente.
## 1.0.0-rc9

- Preservado RC8 como evidência de validação real completa do strict release gate.
- Confirmados Gitleaks PASS, Trivy PASS, evidence mapping PASS, SARIF com 0 findings e strict release gate PASS.
- Confirmado que o repositório privado de validação não possui GitHub Code Scanning habilitado/disponível.
- O upload SARIF passa a ser uma integração best-effort e não interfere no resultado do strict release gate.
- O arquivo SARIF continua sendo gerado e preservado no artifact de evidências.
- Findings reais continuam bloqueando a release normalmente.
- Nenhuma alteração no baseline de 99 controles, scanners, adapters ou política de segurança.
- Nenhuma validação externa obrigatória permanece pendente.
## 1.0.0-rc8

- Preservado RC7 como release candidate com strict release gate PASS em CI real.
- Confirmados Gitleaks PASS, Trivy PASS, evidence mapping PASS e SARIF com 0 findings.
- Identificada permissão ausente no GitHub Actions para upload SARIF em repositório privado.
- Adicionada somente a permissão `actions: read`, mantendo princípio de menor privilégio.
- `contents: read` e `security-events: write` permanecem inalterados.
- Nenhuma alteração no baseline de 99 controles, adapters, evidências ou política do strict gate.
- Pendência final: validação real do upload SARIF.
## 1.0.0-rc7

- Preservado RC6 como evidência da terceira execução real do GitHub Actions.
- Confirmado que o strict gate executa corretamente e bloqueia findings reais.
- Identificado self-finding causado pela fixture sintética do próprio canário Gitleaks.
- A fixture passa a ser montada somente em runtime, sem armazenar o token sintético completo no código-fonte.
- Adicionada configuração `.gitleaks.toml` estendendo as regras padrão e allowlistando exclusivamente o commit histórico que introduziu a fixture sintética.
- Nenhuma allowlist de caminho ampla foi adicionada.
- Trivy real permanece PASS.
- Permanecem pendentes: strict gate PASS e upload SARIF aceito pelo GitHub Code Scanning.
- Nenhuma alteração no baseline de 99 controles.
## 1.0.0-rc6

- Preservado RC5 como evidência da segunda execução real do GitHub Actions.
- Confirmados Gitleaks 8.30.1 e Trivy 0.74.0 em runner real.
- Confirmados evidence mapping, geração de SARIF e upload do artifact de evidências em CI real.
- Movido o strict release gate para antes do upload SARIF.
- Isso impede que uma limitação externa do GitHub bloqueie a execução do gate do framework.
- Pendências externas: execução completa do strict gate e upload SARIF aceito pelo GitHub.
- Nenhuma alteração no baseline de 99 controles ou nos critérios de segurança dos adapters.
## 1.0.0-rc5

- Corrigido o canário do Gitleaks: a fixture anterior (`AKIAIOSFODNN7EXAMPLE`) era explicitamente allowlisted pelo próprio Gitleaks e não podia provar detecção.
- Substituída por fixture sintética positiva reconhecida pela regra AWS do Gitleaks.
- Adicionados guards no workflow para evitar falhas secundárias de upload quando SARIF/evidências ainda não foram gerados.
- Mantido o strict gate.
- Nenhuma alteração no baseline de 99 controles.
- Nenhuma alteração na lógica dos adapters, evidence mapping ou política de validação.
- RC4 preservado como evidência da primeira execução real do GitHub Actions.
- Validação externa de Trivy real, SARIF real e strict gate completo continua pendente.
## 1.0.0-rc4

- Corrigido `RELEASE.json` para alinhar `release` e `version` em `1.0.0-rc4`.
- Expandido `.gitignore` para caches Python, ambientes virtuais, artefatos de build e arquivos sensíveis comuns.
- Corrigidas leituras de arquivos JSON para UTF-8 explícito em pontos relevantes.
- Corrigidos fixtures de Gitleaks e Trivy para execução cross-platform, incluindo Windows.
- Validado no Windows com Python 3.14:
  - 33/33 testes PASS;
  - sintaxe Python PASS;
  - baseline estrutural PASS: controles 1–98 + Regra 99;
  - 0 `__pycache__`;
  - 0 `*.pyc` / `*.pyo`.
- Nenhuma alteração no baseline de 99 controles.
- Nenhuma alteração na política de segurança, gate, SARIF ou evidence mapping além das correções de portabilidade.
- Validação externa real de Gitleaks, Trivy, GitHub Actions e SARIF continua pendente.
## 1.0.0-rc3

- Packaging hygiene: removed generated Python bytecode (`__pycache__` / `*.pyc`) from the release candidate.
- Added `.gitignore` rules to prevent Python bytecode/cache artifacts from being committed.
- No baseline control, adapter, CI gate, or security semantics changed from RC2.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.4.0\] — 2026-09-23

### Adicionado

-   camada Evidence → Baseline;
-   mapa inicial Gitleaks → controles 1,2,3,4,70;
-   mapa inicial Trivy → controles 54,55,70;
-   mapper gera `REVIEW_REQUIRED` e `auto_validated: false`;
-   checks desconhecidos permanecem visíveis como `unmapped_or_invalid`;
-   CI passa a produzir `control-evidence.json`.

### Segurança

-   scanner PASS nunca promove controle automaticamente para ✅;
-   mapeamento é evidência de apoio, não equivalência entre ferramenta e
    controle;
-   Regra 99 continua sendo requisito de fechamento.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.3.2\] — 2026-09-23

### Adicionado

-   workflow GitHub Actions de referência;
-   geração SARIF 2.1.0 a partir de evidência normalizada;
-   upload de SARIF e artifact de evidências;
-   gate CI para FAIL/ERROR;
-   teste do builder SARIF.

### Segurança

-   NOT_AVAILABLE/NOT_RUN/ERROR nunca são convertidos em PASS;
-   checkout usa histórico completo para checks Git;
-   CI preserva a distinção entre scanner ausente e scanner aprovado.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.3.1\] — 2026-09-23

### Adicionado

-   adapter externo para Trivy;
-   modos `fs` e `sbom`;
-   normalização de vulnerabilidade, severidade, pacote, versão
    instalada e versão corrigida;
-   testes fixture para PASS, FAIL, normalização e modo SBOM;
-   ferramenta ausente continua `NOT_AVAILABLE`, nunca PASS.

### Decisões de design

-   adapter usa relatório JSON temporário;
-   não instala nem atualiza scanner automaticamente;
-   resultado do scanner permanece evidência auxiliar, sem promover
    controles automaticamente para ✅.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.3.0\] — 2026-09-23

### Adicionado

-   contrato de evidência normalizada v1.0;
-   camada de adapters externos;
-   primeiro adapter: Gitleaks;
-   estados NOT_AVAILABLE e NOT_RUN;
-   redaction: Secret, Match e Line não entram na evidência normalizada;
-   testes do adapter com scanner fixture.

### Decisões de design

-   ferramenta ausente nunca vira PASS;
-   o framework não instala scanners automaticamente;
-   integrações entram uma por vez, com testes.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.2.1\] — 2026-09-23

### Corrigido

-   falso positivo do detector de SBOM em documentação.

### Adicionado

-   suíte de 9 testes de contrato dos scanners com fixtures isoladas.

### Decisões de design

-   scanners passam a ser testados como código de segurança;
    PASS/WARN/FAIL têm regressões próprias.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.2.0\] — 2026-09-23

### Adicionado

-   checks v0.2.0;
-   scanner heurístico de secrets no histórico Git;
-   descoberta de SBOM;
-   inspeção estática inicial de APK/AAB/JAR/WAR/ZIP com limites contra
    arquivos abusivos.

### Decisões de design

-   sem rede e sem modificação do alvo por padrão;
-   finding histórico não presume credencial ativa;
-   SBOM não presume dependências seguras;
-   inspeção de arquivo não presume segurança do artefato.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.1.0\] — 2026-09-22

### Adicionado

-   primeira camada executável de checks locais e read-only (`checks`
    v0.1.0);
-   runner unificado com saída humana ou JSON;
-   heurística local de secrets;
-   higiene de repositório/arquivos sensíveis;
-   inventário de manifests e lockfiles;
-   descoberta de artefatos de release;
-   limitações explícitas para evitar falso PASS.

### Design de segurança

-   nenhum check faz rede por padrão;
-   nenhum check modifica o projeto;
-   PASS dos checks não promove automaticamente um controle para ✅;
-   vulnerabilidade de dependência, histórico Git e artefatos continuam
    exigindo ferramentas/evidências próprias.

# Changelog

Todas as mudanças relevantes do framework devem ser registradas neste
arquivo.

## \[1.0.0\] — 2026-09-22

### Adicionado

-   pacote público inicial do Vibe Security Framework;
-   `SECURITY_START_HERE.md` como porta de entrada;
-   baseline canônico v1.3 com 99 controles;
-   template de Threat Model;
-   template de Audit Results;
-   template de Security Regression;
-   Release Security Gate;
-   10 Profiles de aplicabilidade com matrizes M/C/N;
-   prompts especializados AUDIT, FIX, REGRESSION e RELEASE;
-   política de segurança do próprio repositório;
-   referências técnicas;
-   estrutura reservada para checks automatizados.

### Decisões de design decisions

-   baseline não é alterado durante uma auditoria;
-   resultados/evidências ficam separados do baseline;
-   `N` de Profile não vira N/A automaticamente;
-   evidência pode ser invalidada por mudanças;
-   vulnerabilidade corrigida deve virar regressão quando viável;
-   PASS do Release Gate não significa invulnerabilidade;
-   expansão horizontal do baseline foi congelada em 99 nesta fase;
-   próximas evoluções priorizam automação, evidência, mapeamento e
    adaptação por stack.

## Histórico do baseline

### Baseline v1.3

-   99 itens totais;
-   expansão para IA/agentes, RAG, excessive agency, poisoning, output
    handling, secrets de agente, consumo/custo;
-   hardening de runtime/cloud;
-   backup/restore;
-   prototype pollution;
-   cache security;
-   kill switch/contenção;
-   dependência/provedor e estratégia de saída;
-   Regra 99 de Evidência.

### Baseline v1.2

-   85 itens;
-   command injection;
-   unsafe deserialization/XXE;
-   path traversal;
-   secure file download;
-   OAuth/OIDC/SSO;
-   realtime/WebSocket;
-   GraphQL;
-   service-to-service;
-   malware/arquivos compactados;
-   tags de aplicabilidade.

### Baseline v1.1

-   76 itens;
-   revisão e expansão inspirada por referências OWASP;
-   secure design;
-   criptografia;
-   sessões;
-   MFA/recovery;
-   configuração;
-   inventário de API;
-   webhooks;
-   integridade/CI-CD;
-   concorrência/idempotência;
-   privacidade;
-   controles mobile.

### Baseline v1.0

-   primeira versão generalizada do baseline para projetos de vibe
    coding.
