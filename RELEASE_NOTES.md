# Vibe Security Framework 1.0.0

Primeira release estável do Vibe Security Framework.

Esta versão promove o RC9 validado em CI real e inclui um hardening final identificado durante a inspeção das próprias evidências do pipeline: o scanner nativo de histórico Git agora diferencia fixtures sintéticas históricas conhecidas de findings desconhecidos, e um `FAIL` nativo passa a bloquear o CI.

Validações confirmadas:

- Gitleaks PASS;
- canário Gitleaks PASS;
- Trivy PASS;
- native checks PASS;
- evidence mapping PASS;
- SARIF gerado com 0 findings no candidato validado;
- strict release gate PASS;
- artifact de evidências PASS;
- suíte automatizada com 35 testes de regressão;
- pipeline GitHub Actions concluído com sucesso.

O baseline permanece com 99 controles.

O upload SARIF para GitHub Code Scanning é uma integração best-effort quando esse recurso não estiver disponível no repositório. Isso não altera nem enfraquece o strict release gate.

Nenhuma validação externa obrigatória permanece pendente.
# Vibe Security Framework 1.0.0-rc9

RC9 finaliza a validação do pipeline após testes reais no GitHub Actions.

Validado em CI real:

- Gitleaks PASS;
- canário Gitleaks PASS;
- Trivy PASS;
- native checks PASS;
- evidence mapping PASS;
- SARIF gerado com 0 findings;
- strict release gate PASS;
- artifact de evidências PASS.

O repositório privado usado para validação não oferece GitHub Code Scanning. Por isso, o upload SARIF é tratado como integração best-effort.

Essa condição não enfraquece o release gate: findings reais em Gitleaks ou Trivy continuam bloqueando a release.

O SARIF continua sempre sendo gerado e incluído nas evidências.

Nenhuma validação externa obrigatória permanece pendente.
# Vibe Security Framework 1.0.0-rc8

RC8 é uma correção mínima da integração GitHub Code Scanning.

O RC7 já comprovou em CI real:

- Gitleaks PASS;
- canário Gitleaks PASS;
- Trivy PASS;
- evidence mapping PASS;
- SARIF gerado com 0 findings;
- strict release gate PASS;
- artifact de evidências PASS.

O upload SARIF falhou porque o workflow não concedia `actions: read`, permissão exigida pelo GitHub para esse fluxo em repositório privado.

RC8 adiciona somente essa permissão.

Pendência final:

- upload SARIF aceito pelo GitHub Code Scanning.
# Vibe Security Framework 1.0.0-rc7

RC7 corrige o self-finding identificado na execução real do RC6.

Mudanças:

- fixture do canário Gitleaks não fica mais armazenada completa no código;
- `.gitleaks.toml` estende as regras padrão do Gitleaks;
- apenas o commit histórico que introduziu a fixture sintética é allowlistado;
- nenhuma regra real de detecção foi desativada;
- nenhuma allowlist ampla de arquivo ou diretório foi criada.

O strict gate já foi comprovado em CI real ao bloquear corretamente o finding do RC6.

Pendências finais:

- strict gate PASS;
- upload SARIF aceito pelo GitHub Code Scanning.
# Vibe Security Framework 1.0.0-rc6

RC6 reorganiza a etapa final do CI após a validação real do RC5.

Já validados em GitHub Actions real:

- Gitleaks 8.30.1;
- canário Gitleaks;
- Trivy 0.74.0;
- native checks;
- adapters;
- evidence mapping;
- geração do SARIF;
- upload do artifact de evidências.

O strict release gate agora executa antes do upload SARIF.

Permanecem pendentes:

- execução completa do strict gate;
- upload SARIF aceito pelo GitHub Code Scanning.
# Vibe Security Framework 1.0.0-rc5

RC5 corrige o primeiro defeito encontrado durante a execução real do GitHub Actions.

## Correções

- canário do Gitleaks usa agora uma fixture sintética que o scanner deve detectar;
- uploads de SARIF e evidências só são executados quando os respectivos arquivos existem;
- falhas iniciais não geram mais ruído secundário enganoso no pipeline.

## Estado

- baseline de 99 controles inalterado;
- 33 testes locais do RC4 haviam passado;
- GitHub Actions real executado no RC4;
- Gitleaks 8.30.1 instalado e checksum validado no runner real;
- Trivy real, SARIF real e strict gate completo ainda aguardam nova execução com RC5.
# Vibe Security Framework 1.0.0-rc4

RC4 consolida correções de empacotamento, metadados e portabilidade encontradas durante a validação real do RC3.

## Correções

- `RELEASE.json` alinhado integralmente com `1.0.0-rc4`;
- `.gitignore` ampliado;
- leituras JSON relevantes passam a usar UTF-8 explícito;
- fixtures de Gitleaks e Trivy corrigidos para Windows/Linux/macOS.

## Validação local

- 33/33 testes PASS;
- sintaxe Python PASS;
- baseline estrutural PASS: controles 1–98 + Regra 99;
- nenhum `__pycache__`;
- nenhum `*.pyc` / `*.pyo`.

O baseline de 99 controles permanece inalterado.

A release pública continua bloqueada até validação real de Gitleaks, Trivy, GitHub Actions e upload SARIF.
# Vibe Security Framework 1.0.0-rc3

RC3 is a packaging-hygiene release candidate derived from RC2. It removes generated Python bytecode/cache artifacts and adds ignore rules to prevent recurrence. Security controls and CI semantics are unchanged from RC2.

# Release 1.0.0

Primeira release pública congelada do Vibe Security Framework.

## Cadeia

Threat Model → Profiles → Baseline 99 → Audit Results → Correção/Reteste → Security Regression → Release Security Gate.

## Incluído

Baseline de 99 controles, 10 profiles cumulativos, templates, prompts especializados, checks locais, adapters Gitleaks/Trivy, evidência normalizada, SARIF, CI e Evidence → Baseline mapping.

## Como esta release foi fechada

Nenhum scanner, adapter, CI ou mapper promove sozinho um controle para `✅`. A Regra 99 permanece obrigatória.

## O que foi validado nesta release

Integridade ZIP, estrutura, sintaxe Python, suíte de testes, 99 controles, 10 profiles × 99 classificações, links locais, referências internas, evidence map e estrutura CI.

Isso valida o pacote e os contratos testados do framework; não é certificação de segurança nem garantia de ausência de vulnerabilidades.
