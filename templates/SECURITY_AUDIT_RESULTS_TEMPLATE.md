# Security Audit Results — template v1.0

Arquivo de referência: `baseline/SECURITY_BASELINE.md`

Este documento serve para registrar o que foi realmente verificado durante a auditoria. Ele não substitui o baseline e também não prova que o sistema é invulnerável.

## 1. Identificação

- Projeto:
- Repositório / versão / commit:
- Ambiente auditado:
- Data de início:
- Data da última validação:
- Responsável pela auditoria:
- Agente/IA utilizado:
- Baseline: v1.3 — 99 controles

## 2. Arquitetura e escopo

### Tags aplicáveis

- [ ] CORE
- [ ] WEB
- [ ] API
- [ ] MOBILE
- [ ] SAAS
- [ ] AI
- [ ] FILES
- [ ] REALTIME
- [ ] OAUTH
- [ ] INFRA

### Componentes em escopo

- Frontend:
- Backend/API:
- Banco:
- Auth:
- Storage:
- Mobile:
- Realtime:
- IA/RAG/agentes:
- Infra/cloud:
- CI/CD:
- Terceiros críticos:

### O que ficou fora do escopo

Registre claramente o que não foi testado e o motivo.

## 3. Resumo da auditoria

  Métrica                        Quantidade
  ---------------------------- ------------
  Controles totais                       99
  Aplicáveis
  N/A justificados
  ❌ Vulneráveis
  ⚠️ Suspeitos
  ❓ Não verificados
  ✅ Validados com evidência
  P0 abertos
  P1 abertos
  P2/INFRA abertos

### Riscos que bloqueiam a release

- Nenhum / listar IDs.

### O que mudou desde a última auditoria

- Commit/deploy:
- Auth:
- Autorização/RLS/RBAC:
- Banco:
- Storage/uploads:
- Dependências:
- Infra:
- IA/tools:
- Outros:

## 4. Como usar os status

- ❌ VULNERÁVEL — falha reproduzida ou proteção ausente.
- ⚠️ SUSPEITO — existe um indício relevante, mas a confirmação ainda está pendente.
- ❓ NÃO VERIFICADO — a evidência ainda é insuficiente.
- ✅ VALIDADO COM EVIDÊNCIA — teste negativo, teste positivo e evidência real sustentam a validação.
- ➖ N/A — o controle não se aplica e existe justificativa técnica.

Não transforme um item em ✅ apenas porque o código parece correto.

## 5. Matriz dos 99 controles

Preencha uma linha por controle. Mesmo quando um item for N/A, mantenha-o na matriz.

  ---------------------------------------------------------------------------------------
            ID Controle       Prioridade   Status    Evidência   Última      Revalidar?
                                                                 validação
  ------------ -------------- ------------ --------- ----------- ----------- ------------
            01                             ❓

            02                             ❓

           ... ...            ...          ...       ...         ...         ...

            98                             ❓

            99 Regra-Mestra   —            ❓
               de Evidência
  ---------------------------------------------------------------------------------------

## 6. Registro detalhado de cada controle

Use este bloco para cada item aplicável:

### Item XX — nome

- Prioridade: P0 / P1 / P2 / INFRA
- Tags:
- Status: ❌ / ⚠️ / ❓ / ✅ / ➖ N/A
- Aplicabilidade / justificativa N/A:
- Ativo/fronteira protegida:
- Ameaça testada:
- Pré-condições:
- Evidência de implementação: arquivo/linha, policy, configuração, console, artefato ou estado live.
- Teste negativo: tentativa indevida/ataque.
- Resultado negativo esperado:
- Resultado negativo real:
- Teste positivo: fluxo legítimo equivalente.
- Resultado positivo esperado:
- Resultado positivo real:
- Correção aplicada: nenhuma / descrição + referência.
- Reteste: data + resultado.
- Regressão criada: teste/script/caso permanente.
- Risco residual:
- Dependências da evidência: auth, policy, biblioteca, infraestrutura etc.
- Validade da evidência: válida / revalidar após mudança X.
- Responsável/data:

## 7. Evidências que deixaram de valer

Um controle que estava em ✅ volta para ❓ quando uma mudança relevante invalida a evidência que sustentava aquela validação.

  --------------------------------------------------------------------------
  Controle       Mudança que    Evidência      Ação           Status
                 invalidou      anterior       necessária
  -------------- -------------- -------------- -------------- --------------

  --------------------------------------------------------------------------

Alguns gatilhos comuns são mudanças em auth, RLS/RBAC, endpoint, storage, biblioteca crítica, infraestrutura, fluxo de IA/tool, build mobile ou segredo.

## 8. Vulnerabilidades encontradas

  ----------------------------------------------------------------------------------
  ID         Severidade   Controle   Descrição   Exploração    Correção   Reteste
                                                 confirmada?
  ---------- ------------ ---------- ----------- ------------- ---------- ----------

  ----------------------------------------------------------------------------------

## 9. Risco aceito e exceções

Aceitar um risco não transforma uma falha em ✅.

  -----------------------------------------------------------------------------------
  Controle    Risco       Motivo      Compensação   Responsável   Expiração/revisão
                                                    pela decisão
  ----------- ----------- ----------- ------------- ------------- -------------------

  -----------------------------------------------------------------------------------

## 10. Resultado do Security Gate

- [ ] Nenhum P0 conhecido permanece aberto.
- [ ] P1 aplicáveis foram tratados ou possuem decisão formal documentada.
- [ ] Evidências dos componentes alterados estão atuais.
- [ ] Testes negativos passaram.
- [ ] Testes positivos passaram.
- [ ] Regressões relevantes passaram.
- [ ] Secrets/build/dependências foram rechecados conforme escopo.
- [ ] Riscos residuais foram registrados.
- [ ] Threat Model continua compatível com a arquitetura atual.

Resultado: PASS / FAIL / INCONCLUSIVO

Data:

Evidência/commit/build:

Observações:

O relatório deve mostrar o que foi testado e observado de verdade, não apenas descrever o que o código deveria fazer.
