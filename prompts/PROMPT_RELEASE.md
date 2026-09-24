# Prompt — Release Security Gate v1.0

## Para que serve

Este prompt conduz a checagem final de segurança de uma release usando somente evidências que ainda estejam válidas.

## Prompt

> Leia `SECURITY_START_HERE.md`, `THREAT_MODEL.md`,
> `SECURITY_AUDIT_RESULTS.md`, `SECURITY_REGRESSION.md` e
> `RELEASE_SECURITY_GATE.md`.
>
> Modo desta sessão: RELEASE GATE.
>
> Identifique exatamente:
>
> - versão;
> - commit/tag;
> - build/artefato;
> - ambiente;
> - mudanças desta release.
>
> Não assuma que uma evidência antiga continua válida. Compare as
> mudanças com os gatilhos de revalidação.
>
> Verifique os bloqueadores definidos no Release Security Gate,
> incluindo:
>
> - P0 aberto;
> - segredo exposto ativo;
> - bypass conhecido de autenticação/autorização;
> - regressão P0 obrigatória falhando, bloqueada ou não executada;
> - evidência crítica invalidada;
> - artefato diferente do testado.
>
> Confira também P1, riscos residuais, regressões, secrets, supply
> chain, auth/autorização, dados/arquivos, IA quando aplicável e
> infraestrutura/operação.
>
> O resultado deve ser exatamente um:
>
> - `PASS`
> - `FAIL`
> - `INCONCLUSIVO`
>
> Falta de evidência não deve virar PASS.
>
> Não declare o software “seguro” ou “invulnerável”. PASS significa
> somente que os critérios definidos para esta release foram satisfeitos
> com evidência atual.
>
> Preencha ou atualize `RELEASE_SECURITY_GATE_RESULT.md` com o resultado
> e as evidências usadas.
>
> Não publique nem faça deploy automaticamente da release, a menos que
> exista uma autorização explícita e separada para essa ação.

## Saída mínima

``` text
RELEASE SECURITY GATE

Versão:
Commit:
Artefato:
Ambiente:

Bloqueadores:
P0:
P1:
Regressões:
Evidências invalidadas:
Riscos residuais:

RESULTADO: PASS / FAIL / INCONCLUSIVO

Justificativa:
Pendências:
Ação necessária antes da release:
```

## Ideia central

O gate decide se os critérios definidos para a release foram atendidos. Ele não certifica invulnerabilidade.
