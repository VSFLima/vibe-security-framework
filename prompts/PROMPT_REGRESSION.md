# Prompt — Security Regression v1.0

## Para que serve

Este prompt orienta a execução e a manutenção das regressões de segurança. O objetivo é impedir que uma falha conhecida volte silenciosamente, sem enfraquecer testes apenas para deixar o pipeline verde.

## Prompt

> Leia `SECURITY_START_HERE.md`, `SECURITY_REGRESSION.md`,
> `SECURITY_AUDIT_RESULTS.md`, o Threat Model e os controles
> relacionados no baseline.
>
> Modo desta sessão: REGRESSION.
>
> Preserve todos os testes existentes.
>
> 1. Identifique commit/build/ambiente.
> 2. Identifique quais regressões são obrigatórias para as mudanças
>    atuais.
> 3. Execute primeiro sem modificar código ou testes.
> 4. Registre resultado esperado e resultado real.
> 5. Para cada caso, valide tanto o negativo quanto o positivo.
> 6. Se uma regressão anteriormente verde falhar, invalide o `✅`
>    relacionado no Audit Results.
> 7. Não remova, pule, relaxe ou reescreva a regressão só para fazê-la
>    passar.
> 8. Se o teste estiver incorreto, demonstre por que ele não representa
>    mais a ameaça antes de propor uma alteração.
> 9. Testes live, destrutivos, de carga ou contra terceiros exigem
>    autorização apropriada.
>
> Quando uma nova vulnerabilidade tiver sido corrigida e ainda não
> possuir regressão, crie um caso com ID permanente, causa raiz, teste
> negativo, teste positivo, gatilhos de revalidação e frequência.
>
> Ao final, diga claramente se alguma falha bloqueia o Release Security
> Gate.

## Saída mínima

``` text
SECURITY REGRESSION

Commit/build:
Ambiente:
Obrigatórias:
Executadas:
PASS:
FAIL:
BLOQUEADAS:
NÃO EXECUTADAS:

Controles invalidados:
Novas regressões:
Gate bloqueado?:
Motivo:
```

## Ideia central

Se uma vulnerabilidade já é conhecida, o processo deve conseguir perceber caso ela volte.
