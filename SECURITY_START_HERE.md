# Comece por aqui — v1.0

Este é o ponto de entrada do Security Baseline para Vibe Coding.

Baseline compatível: `baseline/SECURITY_BASELINE.md` — 99 controles.

Se este arquivo foi entregue a uma IA ou agente, a primeira orientação é simples: leia tudo antes de alterar código, configuração, banco, infraestrutura ou qualquer artefato do projeto.

# 1. Para que este arquivo serve

Desenvolver com IA pode acelerar bastante o trabalho, mas também facilita uma armadilha: aceitar como seguro algo que apenas parece correto. Este protocolo existe para trocar essa impressão por um processo verificável.

A sequência é:

`Arquitetura → Threat Model → Profiles → Baseline 99 → Audit Results → Correção → Reteste → Security Regression → Release Security Gate`

O framework não promete invulnerabilidade, não substitui requisitos regulatórios específicos e não representa certificação OWASP.

# 2. A regra que vem antes de todas as outras

## Antes de criar, preserve. Antes de alterar, diagnostique. Antes de avançar, valide.

Não comece pela correção.

Antes, entenda:

-   o que existe;
-   como funciona;
-   o que está realmente implantado;
-   quais superfícies estão expostas;
-   quais controles se aplicam;
-   quais evidências já existem;
-   o que ainda não foi verificado.

Código que parece seguro ainda precisa de evidência.

# 3. Arquivos do framework

Ao começar, localize estes arquivos quando eles estiverem disponíveis:

``` text
SECURITY_START_HERE.md
baseline/SECURITY_BASELINE.md
THREAT_MODEL_TEMPLATE.md
SECURITY_AUDIT_RESULTS_TEMPLATE.md
SECURITY_REGRESSION_TEMPLATE.md
RELEASE_SECURITY_GATE.md

profiles/
├── PROFILES_INDEX.md
├── PROFILE_CORE.md
├── PROFILE_WEB.md
├── PROFILE_API.md
├── PROFILE_SAAS.md
├── PROFILE_MOBILE.md
├── PROFILE_AI_AGENT.md
├── PROFILE_FILES.md
├── PROFILE_REALTIME.md
├── PROFILE_OAUTH.md
└── PROFILE_INFRA.md
```

Se algum arquivo necessário estiver ausente, registre isso. Não tente preencher a lacuna inventando conteúdo.

# 4. Arquivos de trabalho do projeto

Os templates servem como ponto de partida. Em uma auditoria real, mantenha os originais e crie ou preencha:

``` text
THREAT_MODEL.md
SECURITY_AUDIT_RESULTS.md
SECURITY_REGRESSION.md
RELEASE_SECURITY_GATE_RESULT.md
```

Adapte o trabalho ao projeto, não o baseline.

Quando um controle não se aplicar, mantenha-o no documento e use `➖ N/A` somente depois de registrar a justificativa.

# 5. Fase 0 — Preserve e entenda o projeto

Antes de mexer em qualquer coisa:

1.  identifique repositório, branch, commit e ambiente;
2.  identifique stack e versões relevantes;
3.  identifique frontend, backend, banco, auth, storage e
    infraestrutura;
4.  identifique aplicações mobile;
5.  identifique integrações e serviços externos;
6.  identifique CI/CD e artefatos de release;
7.  identifique IA, RAG, agentes e tools;
8.  identifique fluxos de arquivos;
9.  identifique realtime;
10. identifique OAuth/OIDC/SSO;
11. identifique ambientes de desenvolvimento, homologação e produção;
12. identifique evidências/auditorias anteriores;
13. preserve estado suficiente para comparação/rollback conforme o
    contexto.

### O que deve sair desta etapa

``` text
INVENTÁRIO INICIAL
Projeto:
Commit/versão:
Ambiente:
Stack:
Componentes:
Serviços externos:
Dados sensíveis:
Superfícies públicas:
Artefatos:
Evidências existentes:
Lacunas conhecidas:
```

Nesta fase, ainda não marque controles como validados.

# 6. Fase 1 — Threat Model

Use `THREAT_MODEL_TEMPLATE.md`.

Mapeie:

-   ativos;
-   atores;
-   privilégios;
-   fronteiras de confiança;
-   fluxos críticos;
-   cenários de abuso;
-   piores impactos plausíveis;
-   hipóteses que precisam ser provadas;
-   superfícies do baseline.

Salve/preencha como:

`THREAT_MODEL.md`

### Como decidir

Não trabalhe com uma arquitetura presumida quando ela puder ser verificada.

Se uma informação puder ser confirmada no projeto, na configuração ou no ambiente, confirme antes de assumir.

# 7. Fase 2 — Escolha dos Profiles

Leia `profiles/PROFILES_INDEX.md`.

Ative todos os perfis compatíveis com a arquitetura:

-   `CORE`
-   `WEB`
-   `API`
-   `SAAS`
-   `MOBILE`
-   `AI_AGENT`
-   `FILES`
-   `REALTIME`
-   `OAUTH`
-   `INFRA`

Os perfis se somam. Ative todos os que descrevem a arquitetura real.

## Precedência

Para cada controle:

`M > C > N`

Onde:

-   M — Mandatory
-   C — Conditional
-   N — Normally N/A

### Para não reduzir o escopo artificialmente

`N` não quer dizer `N/A` automaticamente.

O agente deve justificar tecnicamente todo `➖ N/A` usando a arquitetura
e o Threat Model.

Escolha os perfis pela arquitetura, não pelo tamanho da auditoria.

### O que deve sair desta etapa

``` text
PERFIS ATIVOS:
CORE:
WEB:
API:
SAAS:
MOBILE:
AI_AGENT:
FILES:
REALTIME:
OAUTH:
INFRA:

Controles M:
Controles C:
Controles N:
N/A já confirmáveis:
Aplicabilidade ainda não resolvida:
```

# 8. Fase 3 — Monte o Audit Results

Copie/use `SECURITY_AUDIT_RESULTS_TEMPLATE.md` como:

`SECURITY_AUDIT_RESULTS.md`

Registre os 99 controles.

Status permitidos:

-   ❌ VULNERÁVEL
-   ⚠️ SUSPEITO
-   ❓ NÃO VERIFICADO
-   ✅ VALIDADO COM EVIDÊNCIA
-   ➖ N/A JUSTIFICADO

### Como decidir

Se ainda faltar evidência, use `❓`.

Um controle assumidamente não verificado é melhor do que um falso verde.

# 9. Fase 4 — Defina a ordem de prioridade

Audite nesta ordem geral:

1.  P0
2.  P1
3.  P2
4.  INFRA, conforme criticidade e dependências

Dentro da mesma prioridade, comece pelas fronteiras de maior impacto:

-   secrets;
-   autenticação;
-   autorização;
-   cross-tenant;
-   administração;
-   dados sensíveis;
-   ações irreversíveis;
-   storage/uploads;
-   exposição pública;
-   IA/tools com capacidade de agir;
-   infraestrutura privilegiada.

A quantidade de controles verdes não substitui uma análise de risco.

# 10. Fase 5 — Comece pela auditoria read-only

Antes de corrigir qualquer item:

1.  leia código/configuração;
2.  identifique o mecanismo de proteção;
3.  identifique a fonte de identidade;
4.  identifique a fronteira de autorização;
5.  confira estado live quando necessário;
6.  procure bypasses;
7.  determine teste negativo;
8.  determine teste positivo;
9.  registre evidência disponível;
10. só então classifique o finding.

### O que evitar nesta fase

-   refatoração ampla;
-   deploy desnecessário;
-   alteração destrutiva;
-   carga/DoS;
-   exploração de terceiros;
-   mudanças em produção sem autorização;
-   "correções preventivas" antes de saber se há problema.

# 11. Fase 6 — Trabalhe com evidências

A Regra 99 governa o framework inteiro.

Um controle só recebe `✅` quando a evidência adequada mostrar que o comportamento esperado realmente acontece.

Para cada controle aplicável, procure:

1.  estado/implementação real;
2.  arquivo/linha/configuração/policy, quando relevante;
3.  teste negativo;
4.  resultado negativo real;
5.  teste positivo;
6.  resultado positivo real;
7.  correção, se necessária;
8.  reteste;
9.  risco residual;
10. regressão, quando aplicável.

Não encontrar algo em uma busca textual não prova que aquilo não exista no sistema.

Mock ajuda no teste, mas não comprova uma configuração externa real.

O código-fonte, sozinho, também não prova o estado do artefato que será distribuído.

# 12. Fase 7 — Corrija o que foi confirmado

Quando uma vulnerabilidade estiver confirmada:

1.  registre o finding antes da alteração;
2.  explique causa raiz;
3.  determine impacto;
4.  proponha a menor correção segura;
5.  registre trade-offs;
6.  preserve possibilidade de rollback quando relevante;
7.  aplique a correção;
8.  execute teste negativo;
9.  execute teste positivo;
10. execute regressões relacionadas;
11. atualize evidências.

## Evite misturar correção com refatoração desnecessária

Não misture correção de segurança com grande refatoração
estética/arquitetural sem necessidade.

Quanto menor e mais focado o diff, mais fácil entender o que foi corrigido e perceber uma regressão.

# 13. Fase 8 — Transforme correções em regressão

Use `SECURITY_REGRESSION_TEMPLATE.md`.

Quando uma vulnerabilidade confirmada for corrigida, avalie sua
transformação em teste permanente.

Salve/preencha:

`SECURITY_REGRESSION.md`

Uma regressão deve preservar:

-   teste negativo;
-   teste positivo;
-   causa raiz;
-   evidência;
-   gatilhos de revalidação;
-   ambiente/build;
-   histórico.

Nunca enfraqueça um teste apenas para o pipeline ficar verde.

# 14. Fase 9 — Lembre que evidência expira

Um `✅` não é permanente.

Mudanças no sistema podem invalidar evidências que antes eram suficientes.

Reavalie controles relacionados após alterações em:

-   auth;
-   RLS/RBAC;
-   schema;
-   API;
-   storage;
-   cache;
-   dependência crítica;
-   infraestrutura;
-   build mobile;
-   OAuth;
-   realtime;
-   IA/RAG/tools;
-   fluxos de dados;
-   secrets/configuração.

Quando a evidência não for mais suficiente:

`✅ → ❓`

até o reteste.

# 15. Fase 10 — Release Security Gate

Antes de release/deploy relevante, use `RELEASE_SECURITY_GATE.md`.

Gere/preencha:

`RELEASE_SECURITY_GATE_RESULT.md`

Resultados permitidos:

-   PASS
-   FAIL
-   INCONCLUSIVO

### O que bloqueia o gate

P0 conhecido aberto não recebe PASS.

Segredo exposto ativo não recebe PASS.

Bypass conhecido de autenticação/autorização não recebe PASS.

Regressão P0 obrigatória falhando/não executada não recebe PASS.

Evidência crítica invalidada e ainda não revalidada não recebe PASS.

Artefato diferente do que foi efetivamente testado não recebe PASS.

### O que esse resultado quer dizer

`PASS` significa:

> os critérios de segurança definidos para esta release foram
> satisfeitos com a evidência disponível.

Não significa:

> o software é invulnerável.

# 16. Como a IA deve trabalhar

Se você é um agente:

## O que fazer

-   cite arquivos/linhas/configurações reais;
-   diferencie confirmado, suspeito e não verificado;
-   mostre resultados de testes;
-   preserve evidências anteriores válidas;
-   invalide evidências afetadas por mudanças;
-   faça uma correção por vez quando possível;
-   pare diante de risco destrutivo ou falta de autorização;
-   peça autorização quando uma ação puder afetar
    produção/dados/terceiros.

## O que evitar

-   inventar estado live;
-   presumir que uma policy está implantada;
-   declarar "seguro" porque compilou;
-   marcar controle como ✅ por inspeção superficial;
-   esconder falha porque existe compensação;
-   reduzir escopo para melhorar métricas;
-   apagar teste que falhou;
-   colocar segredo em prompt/log;
-   executar pentest contra terceiro sem autorização;
-   realizar carga/DoS destrutivo;
-   fazer deploy silenciosamente.

# 17. O princípio “não confie em mim”

A IA que escreveu o código não é evidência independente de que o código
está seguro.

Sempre que possível, prefira evidência produzida por:

-   teste executado;
-   resposta real;
-   policy/configuração live;
-   estado do banco;
-   artefato compilado;
-   scanner apropriado;
-   log controlado;
-   pipeline;
-   revisão independente;
-   teste externo autorizado.

A IA pode interpretar evidências. Não deve inventá-las.

# 18. Quando parar antes de continuar

Pare e sinalize antes de continuar quando:

-   o teste pode destruir dados;
-   o teste pode afetar disponibilidade;
-   a ação alcança produção sem autorização;
-   a ação alcança terceiro;
-   seria necessário expor segredo;
-   não há rollback razoável para alteração crítica;
-   identidade/tenant do teste não está claro;
-   evidência necessária não está acessível;
-   há conflito entre documentação e estado live;
-   o artefato a liberar não é o artefato testado.

Use `❓ NÃO VERIFICADO` ou `INCONCLUSIVO` quando a evidência não puder
ser obtida com segurança.

# 19. Como fechar cada sessão

Ao final de cada sessão, deixe um resumo parecido com este:

``` text
AUDITORIA — ESTADO ATUAL

Baseline: v1.3
Commit/build:
Ambiente:

Controles aplicáveis:
✅ Validados:
❌ Vulneráveis:
⚠️ Suspeitos:
❓ Não verificados:
➖ N/A justificados:

P0 abertos:
P1 abertos:

Itens alterados nesta sessão:
Testes negativos executados:
Testes positivos executados:
Regressões criadas/atualizadas:
Evidências invalidadas:

Próximo controle recomendado:
Motivo:
Ação que exige autorização:
```

Não esconda pendências só para deixar a conclusão mais bonita.

# 20. Prompt curto para começar

O usuário pode entregar este repositório/framework a uma IA e dizer:

> Leia `SECURITY_START_HERE.md` integralmente e siga o protocolo.
>
> Antes de alterar qualquer coisa, faça somente a fase de preservação,
> inventário, Threat Model e seleção de Profiles.
>
> Não presuma que controles estão implementados. Não marque nada como
> validado sem evidência.
>
> Depois apresente o escopo encontrado, os perfis ativos, os controles
> aplicáveis, os P0 identificados e o plano de auditoria.
>
> Aguarde autorização antes de qualquer correção, deploy, teste
> destrutivo ou alteração em produção.

# 21. Prompt para continuar uma auditoria

> Leia `SECURITY_START_HERE.md`, `THREAT_MODEL.md`,
> `SECURITY_AUDIT_RESULTS.md` e `SECURITY_REGRESSION.md`.
>
> Preserve todo trabalho e evidência já válidos.
>
> Identifique o primeiro controle pendente pela prioridade definida no
> protocolo.
>
> Antes de alterar código, verifique se a evidência existente continua
> válida e diagnostique o estado atual.
>
> Continue do ponto exato em que a auditoria parou. Não reinicie
> controles concluídos sem motivo de revalidação.
>
> Ao terminar, atualize os arquivos de trabalho e informe o próximo
> controle.

# 22. Quando a auditoria pode ser considerada concluída

A ausência de `❌` não significa, sozinha, que a auditoria terminou.

Para o escopo declarado:

-   [ ] arquitetura inventariada;
-   [ ] Threat Model preenchido;
-   [ ] Profiles ativados e combinados;
-   [ ] todos os 99 controles classificados;
-   [ ] todo N/A justificado;
-   [ ] nenhum aplicável ficou sem status;
-   [ ] todo ✅ possui evidência compatível;
-   [ ] testes negativos executados quando exigidos;
-   [ ] testes positivos executados quando exigidos;
-   [ ] vulnerabilidades corrigidas foram retestadas;
-   [ ] regressões relevantes foram criadas;
-   [ ] riscos residuais foram registrados;
-   [ ] evidências invalidadas foram revalidadas ou voltaram para ❓;
-   [ ] Security Gate executado quando houver release.

# 23. O que 99/99 realmente significa

99/99 não significa "invulnerável".

Significa que:

-   os 99 controles foram considerados;
-   N/A foram justificados;
-   os aplicáveis classificados como `✅` possuem a evidência exigida;
-   findings e riscos residuais estão documentados;
-   o estado corresponde ao commit/build/ambiente declarado.

Se o sistema muda, a segurança precisa ser reavaliada junto.

# 24. Ordem do protocolo

``` text
┌───────────────────────────────┐
│  1. SECURITY_START_HERE       │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  2. INVENTÁRIO / PRESERVAÇÃO  │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  3. THREAT MODEL              │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  4. PROFILES                  │
│  M > C > N                    │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  5. BASELINE — 99 CONTROLES   │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  6. AUDIT RESULTS             │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  7. CORREÇÃO + RETESTE        │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  8. SECURITY REGRESSION       │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  9. RELEASE SECURITY GATE     │
└───────────────────────────────┘
```

# 25. Para fechar

> Não pergunte apenas "o código parece seguro?". Pergunte "qual
> evidência demonstra que o comportamento inseguro foi bloqueado e o
> comportamento legítimo continua funcionando?".

Esse princípio é o fio condutor do framework inteiro.

Preserve → diagnostique → teste → corrija → reteste → crie regressão →
valide a release.
