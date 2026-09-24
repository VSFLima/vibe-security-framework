# Prompt — Security Audit v1.0

Use junto com `SECURITY_START_HERE.md` e o Security Baseline para Vibe Coding v1.3.

## Para que serve

Este prompt coloca a IA em modo de auditoria. O foco é entender o controle, procurar evidências e testar o comportamento antes de começar qualquer correção.

## Prompt

> Leia integralmente `SECURITY_START_HERE.md`,
> `baseline/SECURITY_BASELINE.md`, `THREAT_MODEL.md`,
> `SECURITY_AUDIT_RESULTS.md`, `SECURITY_REGRESSION.md` e os Profiles
> ativos que estiverem disponíveis.
>
> Se os arquivos de trabalho ainda não existirem, siga o START HERE para
> criá-los a partir dos templates. Não invente conteúdo de arquivo
> ausente.
>
> Modo desta sessão: AUDIT / READ-ONLY primeiro.
>
> Preserve todo trabalho e evidência que ainda sejam válidos. Não
> reinicie controles concluídos sem um gatilho real de revalidação.
>
> 1. Confirme projeto, commit/build e ambiente em análise.
> 2. Confira se o Threat Model ainda corresponde à arquitetura atual.
> 3. Confira os Profiles ativos e a matriz de aplicabilidade.
> 4. Identifique o primeiro controle pendente pela prioridade: P0 → P1
>    → P2/INFRA.
> 5. Antes de alterar qualquer coisa, diagnostique o mecanismo existente.
> 6. Diferencie claramente o que está confirmado, suspeito e não
>    verificado.
> 7. Para um possível `✅`, exija evidência compatível com a Regra 99.
> 8. Planeje teste negativo e positivo.
> 9. Quando estado live, configuração ou artefato forem necessários,
>    não substitua a verificação por uma suposição baseada apenas no
>    código.
> 10. Não execute ação destrutiva, carga/DoS, deploy, alteração em
>     produção ou teste contra terceiro sem autorização explícita.
>
> Para cada controle analisado, reporte:
>
> - ID e nome;
> - prioridade;
> - aplicabilidade;
> - mecanismo encontrado;
> - evidência;
> - teste negativo;
> - teste positivo;
> - resultado real;
> - status: ❌ / ⚠️ / ❓ / ✅ / ➖;
> - risco residual;
> - necessidade de correção;
> - necessidade de regressão.
>
> Pare antes de corrigir uma vulnerabilidade confirmada, a menos que eu
> tenha autorizado explicitamente correções nesta mesma sessão.
>
> Ao final, atualize `SECURITY_AUDIT_RESULTS.md` apenas com fatos e
> evidências realmente obtidos e informe o próximo controle recomendado.

## Saída mínima

``` text
SECURITY AUDIT — SESSÃO

Commit/build:
Ambiente:
Controle(s) analisado(s):

✅:
❌:
⚠️:
❓:
➖:

Evidências obtidas:
Testes executados:
Finding que exige correção:
Evidência que expirou:
Próximo controle:
Ação que exige autorização:
```

## Ideia central

AUDIT serve para descobrir e demonstrar. A correção vem depois do diagnóstico.
