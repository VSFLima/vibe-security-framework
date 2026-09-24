# Security Prompts — índice v1.0

Compatível com o Security Baseline para Vibe Coding v1.3.

Os prompts desta pasta ajudam a mudar o modo de trabalho da IA de acordo com a etapa da análise. Eles não substituem o `SECURITY_START_HERE.md`, o baseline ou as regras de autorização do ambiente.

## Qual prompt usar

  -----------------------------------------------------------------------
  Prompt                              Quando usar
  ----------------------------------- -----------------------------------
  `PROMPT_AUDIT.md`                   investigar controles e reunir
                                      evidências antes de corrigir

  `PROMPT_FIX.md`                     corrigir um finding já
                                      diagnosticado e retestar

  `PROMPT_REGRESSION.md`              executar ou manter testes
                                      permanentes de segurança

  `PROMPT_RELEASE.md`                 executar o Release Security Gate
  -----------------------------------------------------------------------

## Ordem mais comum

``` text
AUDIT
  ↓
finding confirmado
  ↓
FIX
  ↓
REGRESSION
  ↓
RELEASE GATE
```

Se a auditoria não encontrar uma vulnerabilidade, não há motivo para executar FIX só para completar a sequência.

## O que vem primeiro

Se houver conflito entre instruções, siga esta ordem:

1. requisitos legais ou organizacionais aplicáveis;
2. autorização e segurança do ambiente;
3. `SECURITY_START_HERE.md`;
4. baseline e Regra 99;
5. templates e resultados do projeto;
6. prompt especializado.

## Para começar um projeto

Em um projeto novo, evite abrir diretamente um prompt especializado. Primeiro peça:

> Leia `SECURITY_START_HERE.md` e execute somente preservação,
> inventário, Threat Model e Profiles.

Depois escolha o prompt da etapa em que o trabalho realmente está.

## Ações que continuam exigindo autorização

Nenhum prompt autoriza por conta própria:

- produção;
- deploy;
- exclusão;
- carga ou DoS;
- pentest em terceiros;
- rotação de credencial;
- alteração destrutiva;
- publicação de release.

Os prompts ajudam a organizar o trabalho. A evidência continua decidindo o status.
