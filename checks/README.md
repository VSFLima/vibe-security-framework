# Automated Checks — v0.2.2

Esta é a segunda camada executável do framework. Os checks continuam locais e read-only por padrão.

## Como executar

``` bash
python checks/run_checks.py --target .
```

Se precisar de uma saída estruturada, use `--json`.

## O que entrou nesta camada

`check_git_history_secrets.py` faz uma análise heurística de até 500 commits locais.

`check_sbom.py` procura SBOMs e lockfiles. Ele não consulta CVEs.

`check_artifact_contents.py` abre APK, AAB, JAR, WAR e ZIP com limites de leitura para procurar arquivos sensíveis e alguns padrões de credencial.

Os checks v0.1 de working tree, higiene, dependências e descoberta de artefatos continuam fazendo parte do conjunto.

## Como interpretar o resultado

`PASS` quer dizer apenas que aquele check não encontrou a condição que estava configurado para procurar.

`WARN` indica evidência parcial ou alguma limitação da verificação.

`FAIL` indica um finding.

Um `PASS` não promove automaticamente nenhum controle do baseline para ✅.

## Limitações atuais

A v0.2 ainda não consulta CVEs, não gera ou valida SBOM, não decompila Android, não interpreta `AndroidManifest.xml` binário, não valida assinatura ou exported components e não executa checks HTTP remotos.

Nas próximas camadas, a preferência é integrar ferramentas maduras quando isso fizer sentido, em vez de reimplementar scanners inteiros dentro do framework.

## Testes dos scanners

O arquivo principal de contrato pode ser executado com:

``` text
python checks/tests/test_checks.py
```

Na v0.2.2, esse arquivo possui 11 testes de contrato, incluindo regressões para o tratamento das fixtures sintéticas usadas no histórico de testes.

A suíte completa do framework possui 35 testes distribuídos pelos seis arquivos em `checks/tests/`, cobrindo checks nativos, adaptadores Gitleaks e Trivy, mapeamento de evidências, geração de SARIF e política do release gate.
