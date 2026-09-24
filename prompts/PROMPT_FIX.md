# Prompt — Security Fix v1.0

Use este prompt somente depois que o finding estiver suficientemente diagnosticado.

## Para que serve

O objetivo é corrigir uma vulnerabilidade confirmada com o menor diff seguro, testar a correção e garantir que o fluxo legítimo continue funcionando.

## Prompt

> Leia `SECURITY_START_HERE.md`, o controle correspondente no baseline,
> `THREAT_MODEL.md`, `SECURITY_AUDIT_RESULTS.md` e as regressões
> relacionadas.
>
> Modo desta sessão: FIX.
>
> Antes de alterar qualquer coisa, recapitule:
>
> - finding confirmado;
> - causa raiz;
> - impacto;
> - evidência que confirmou a falha;
> - componentes afetados;
> - comportamento legítimo que precisa ser preservado.
>
> Antes da mudança:
>
> 1. preserve o estado atual;
> 2. identifique o menor conjunto de arquivos, policies ou configurações
>    necessário;
> 3. explique o risco da alteração;
> 4. identifique rollback quando relevante;
> 5. identifique controles vizinhos que podem sofrer regressão.
>
> Durante a correção:
>
> - prefira o menor diff seguro;
> - não faça refatoração estética ou arquitetural que não seja necessária;
> - não mova autorização para o cliente;
> - não esconda o erro em vez de corrigir a causa raiz;
> - não desabilite uma proteção existente para fazer o fluxo funcionar;
> - não altere o teste para acomodar um comportamento vulnerável.
>
> Depois da mudança, execute:
>
> 1. o teste negativo que reproduzia a vulnerabilidade;
> 2. o teste positivo do fluxo legítimo;
> 3. as regressões relacionadas;
> 4. o reteste de autorização ou tenant quando aplicável;
> 5. a validação do estado live ou do artefato quando a correção depender
>    dele.
>
> Se qualquer teste falhar, não marque o controle como `✅`.
>
> Atualize `SECURITY_AUDIT_RESULTS.md` com a correção e o reteste. Se a
> falha puder reaparecer, crie ou atualize a entrada correspondente em
> `SECURITY_REGRESSION.md`.
>
> Não faça deploy ou alteração em produção sem autorização explícita.

## Saída mínima

``` text
SECURITY FIX

Finding:
Causa raiz:
Correção:
Arquivos/configurações alterados:
Diff conceitual:
Rollback:

Teste negativo:
Resultado:

Teste positivo:
Resultado:

Regressões:
Resultado:

Status final do controle:
Risco residual:
Evidências atualizadas:
Próxima ação:
```

## Ideia central

Uma correção sem reteste ainda é apenas uma mudança. A evidência vem do comportamento validado depois dela.
