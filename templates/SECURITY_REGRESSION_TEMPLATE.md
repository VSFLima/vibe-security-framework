# Security Regression — template v1.0

Arquivo de referência: `baseline/SECURITY_BASELINE.md`

Este template também conversa com `SECURITY_AUDIT_RESULTS.md`, `THREAT_MODEL.md` e `RELEASE_SECURITY_GATE.md`.

A proposta é simples: quando uma vulnerabilidade, bypass ou falha de segurança já foi encontrada e corrigida, vale transformar esse aprendizado em um teste que possa ser repetido e ligado à evidência.

> Uma vulnerabilidade corrigida não deve depender da memória humana — nem da memória da IA — para continuar corrigida.

# 1. Por que regressão importa

Quando uma falha de segurança for confirmada, corrigida e retestada com sucesso, avalie se ela pode virar uma regressão permanente.

A regressão precisa mostrar duas coisas:

-   NEGATIVO: o comportamento indevido continua bloqueado;
-   POSITIVO: o fluxo legítimo equivalente continua funcionando.

Uma correção que bloqueia o ataque, mas também quebra o usuário
legítimo, não é uma correção validada.

# 2. O que merece virar regressão

Sempre que tecnicamente viável, criar regressão para:

-   bypass de autenticação;
-   IDOR/BOLA;
-   cross-tenant;
-   escalada horizontal ou vertical;
-   falha de RLS/RBAC;
-   mass assignment;
-   alteração de campo sensível;
-   delete indevido;
-   SQL/command injection;
-   XSS;
-   SSRF;
-   path traversal;
-   upload/download indevido;
-   exposição de segredo;
-   enumeração relevante;
-   rate-limit bypass;
-   replay/idempotência;
-   OAuth/OIDC;
-   WebSocket/realtime;
-   GraphQL;
-   cache leakage/poisoning;
-   RAG/vector cross-tenant;
-   tool/agent authorization;
-   AI output handling;
-   configurações críticas;
-   qualquer vulnerabilidade que já tenha chegado a produção;
-   qualquer falha que possa reaparecer por refatoração ou geração de
    código por IA.

Nem toda evidência pode ser automatizada. Quando não for possível,
registre uma regressão MANUAL ou HÍBRIDA.

# 3. Tipos de regressão

Use uma destas classificações:

-   AUTOMÁTICA — executável por teste/script/pipeline sem
    intervenção humana.
-   MANUAL — exige inspeção ou execução humana.
-   HÍBRIDA — parte automatizada + confirmação humana.
-   INFRA — depende de estado/configuração externa.
-   BUILD/ARTEFATO — verifica APK/AAB/container/bundle/binário
    gerado.
-   LIVE — precisa validar comportamento do ambiente implantado.

A classificação não determina qualidade. O importante é que a evidência
seja adequada ao risco.

# 4. Identificação da suíte

-   Projeto:
-   Repositório:
-   Ambiente(s):
-   Baseline: v1.3 — 99 controles
-   Threat Model:
-   Audit Results:
-   Última execução completa:
-   Commit/tag testado:
-   Build/artefato testado:
-   Responsável:

# 5. Resumo

  Métrica                    Quantidade
  ------------------------ ------------
  Regressões cadastradas
  Automáticas
  Manuais
  Híbridas
  Infra
  Build/artefato
  Live
  PASS
  FAIL
  BLOQUEADAS
  NÃO EXECUTADAS

### Resultado geral

-   PASS — todas as regressões obrigatórias para o escopo
    passaram.
-   FAIL — pelo menos uma regressão obrigatória falhou.
-   BLOQUEADO — não foi possível executar evidência necessária.
-   PARCIAL — somente parte da suíte foi executada; não equivale a
    PASS completo.

# 6. Catálogo de regressões

  -------------------------------------------------------------------------------------------
  ID            Controle Vulnerabilidade   Tipo      Prioridade   Automatizada?   Último
                         original                                                 resultado
  --------- ------------ ----------------- --------- ------------ --------------- -----------
  SR-001

  -------------------------------------------------------------------------------------------

IDs são permanentes. Não reutilize um ID removido.

# 7. Modelo de caso de regressão

Copie este bloco para cada caso.

## SR-XXX — nome curto e específico

### Origem

-   Controle do baseline: XX
-   Finding/vulnerabilidade original:
-   Severidade/prioridade: P0 / P1 / P2 / INFRA
-   Data da descoberta:
-   Commit/build vulnerável:
-   Referência no Audit Results:
-   Incidente/ticket, se houver:

### Vulnerabilidade que este teste impede de voltar

Descreva objetivamente o comportamento vulnerável.

Exemplo:

`Usuário autenticado da Empresa A conseguia consultar o recurso da Empresa B alterando apenas o resource_id.`

### Causa raiz

Não registre somente o sintoma.

-   Falha de autorização?
-   Policy incorreta?
-   Identidade confiada ao cliente?
-   Validação ausente?
-   Configuração?
-   Biblioteca?
-   Cache?
-   Concorrência?
-   Prompt/tool?
-   Outra?

### Correção implementada

-   Arquivo/policy/configuração:
-   Commit:
-   Mudança:
-   Dependências:
-   Rollback relevante:

### Pré-condições do teste

-   Ambiente:
-   Fixtures/dados:
-   Usuários/perfis:
-   Tenant(s):
-   Tokens:
-   Feature flags:
-   Serviços externos:
-   Outras:

### Teste negativo — tentativa indevida

Objetivo: demonstrar que a vulnerabilidade continua bloqueada.

-   Passos:
    1.
    2.
    3.
-   Entrada/payload:
-   Resultado esperado:
-   Código HTTP/erro esperado, se aplicável:
-   Estado que NÃO pode mudar:
-   Dados que NÃO podem ser retornados:

### Teste positivo — fluxo legítimo

Objetivo: demonstrar que a proteção não quebrou a funcionalidade
válida.

-   Passos:
    1.
    2.
    3.
-   Entrada:
-   Resultado esperado:
-   Estado esperado:

### Evidência

-   Tipo: AUTOMÁTICA / MANUAL / HÍBRIDA / INFRA / BUILD/ARTEFATO / LIVE
-   Comando/teste:
-   Arquivo de teste:
-   Pipeline/job:
-   Screenshot/log/configuração:
-   Evidência de estado live:
-   Hash/versão do artefato:
-   Data:

### Resultado atual

-   [ ] PASS
-   [ ] FAIL
-   [ ] BLOQUEADO
-   [ ] NÃO EXECUTADO

Resultado real:

Diferenças em relação ao esperado:

### Quando revalidar

Marque tudo que invalida ou exige nova execução:

-   [ ] alteração de autenticação;
-   [ ] alteração de autorização/RBAC/RLS;
-   [ ] alteração do endpoint;
-   [ ] alteração de schema/query;
-   [ ] alteração de storage;
-   [ ] alteração de cache;
-   [ ] alteração de dependência crítica;
-   [ ] alteração de infraestrutura;
-   [ ] alteração de build mobile;
-   [ ] alteração de OAuth/SSO;
-   [ ] alteração de realtime;
-   [ ] alteração de IA/RAG/tool;
-   [ ] mudança no fluxo de dados;
-   [ ] outro:

### Frequência mínima

-   [ ] cada commit/PR;
-   [ ] cada merge na branch principal;
-   [ ] cada build;
-   [ ] antes de release;
-   [ ] após deploy;
-   [ ] periódico;
-   [ ] somente quando gatilho específico ocorrer.

### Responsável

-   Responsável:
-   Última execução:
-   Próxima revisão, se aplicável:

# 8. Como estruturar testes cross-tenant

Quando houver multi-tenancy, prefira matriz bidirecional.

  Origem     Alvo        Ação                   Esperado
  ---------- ----------- ---------------------- ----------
  Tenant A   Recurso A   leitura legítima       permitir
  Tenant A   Recurso B   leitura indevida       negar
  Tenant A   Recurso B   alteração indevida     negar
  Tenant A   Recurso B   exclusão indevida      negar
  Tenant B   Recurso A   operação equivalente   negar

Não testar apenas A → B quando a arquitetura permite assimetria.

# 9. Como estruturar testes de papéis

Quando houver RBAC/perfis:

  Papel            Recurso                  Ação                Esperado
  ---------------- ------------------------ ------------------- ----------
  usuário comum    próprio recurso          ação permitida      permitir
  usuário comum    recurso administrativo   ação privilegiada   negar
  admin limitado   escopo permitido         ação permitida      permitir
  admin limitado   escopo superior          ação indevida       negar

Inclua escalada horizontal e vertical.

# 10. Como tratar IA e agentes

Para regressões envolvendo IA, não valide apenas texto da resposta.

Teste também a ação efetiva.

Exemplos:

-   prompt injection tenta alterar autorização;
-   documento RAG contém instrução maliciosa;
-   agente tenta tool fora do escopo;
-   tool recebe `tenant_id` adulterado;
-   modelo gera URL interna para SSRF;
-   saída gera HTML/SQL/shell;
-   agente entra em loop;
-   documento de A tenta aparecer para B.

A camada determinística deve bloquear o comportamento indevido mesmo que
o modelo coopere com o ataque.

# 11. Regressões de segredos

Quando um segredo for encontrado:

1.  remover da origem;
2.  verificar histórico/build/log quando aplicável;
3.  rotacionar/revogar se houve exposição;
4.  criar teste que impeça reincidência quando tecnicamente possível.

Possíveis regressões:

-   secret scanning;
-   pattern scanning;
-   inspeção de bundle;
-   inspeção de APK/AAB;
-   bloqueio de commit;
-   verificação de variáveis públicas;
-   checagem de imagem/container.

Remover do código não prova que o segredo deixou de ser válido.

# 12. Regressões de build e artefato

Código-fonte correto não garante artefato correto.

Quando aplicável, testar o artefato efetivamente distribuído:

-   bundle web;
-   APK/AAB;
-   container image;
-   binário;
-   pacote;
-   arquivo de configuração empacotado.

Registrar:

-   versão;
-   hash quando útil;
-   ambiente;
-   data;
-   origem do artefato.

# 13. Regressões que dependem de estado live

Algumas proteções só podem ser comprovadas no ambiente real/configurado.

Exemplos:

-   headers;
-   CORS;
-   WAF;
-   TLS;
-   bucket público;
-   RLS/policies live;
-   IAM;
-   rate limits;
-   redirects OAuth;
-   configuração de produção.

Cuidado: teste live deve ser autorizado, controlado e não
destrutivo.

Não executar carga, exploração destrutiva ou ações contra terceiros sem
autorização explícita.

# 14. Mock não prova controle externo

Mocks são úteis para lógica interna, mas não provam:

-   policy real;
-   IAM real;
-   WAF real;
-   bucket real;
-   configuração real;
-   artefato real;
-   comportamento real do provedor.

Quando o controle depende de infraestrutura/serviço externo, mantenha
evidência apropriada para essa camada.

# 15. O que fazer quando uma regressão falha

Quando uma regressão que antes passava falhar:

1.  marcar imediatamente como `FAIL`;
2.  identificar o controle relacionado;
3.  invalidar o `✅` correspondente no `SECURITY_AUDIT_RESULTS.md`;
4.  avaliar prioridade/severidade;
5.  impedir `PASS` no Release Security Gate se o caso for bloqueador;
6.  diagnosticar antes de corrigir;
7.  aplicar correção mínima;
8.  executar teste negativo;
9.  executar teste positivo;
10. executar regressões relacionadas;
11. atualizar evidências.

Nunca apagar ou enfraquecer o teste apenas para o pipeline voltar a
ficar verde.

# 16. Quando uma regressão pode ser removida

Somente quando:

-   a funcionalidade/superfície deixou de existir; ou
-   a arquitetura tornou o cenário tecnicamente impossível; ou
-   o teste foi substituído por outro comprovadamente
    equivalente/superior.

Registrar:

-   ID antigo;
-   motivo;
-   evidência;
-   substituto, se houver;
-   data;
-   responsável.

Não reutilizar o ID removido.

# 17. Quando executar cada regressão

Sugestão inicial; adapte ao projeto.

  -----------------------------------------------------------------------
  Evento                              Regressões mínimas
  ----------------------------------- -----------------------------------
  Pull Request                        automáticas rápidas relacionadas à
                                      mudança

  Merge principal                     suíte automática ampliada

  Build release                       build/artefato + regressões
                                      críticas

  Antes da release                    todas as regressões exigidas pelo
                                      Security Gate

  Após deploy                         smoke + live/configuração aplicável

  Mudança de auth/RLS/RBAC            autorização, IDOR/BOLA,
                                      cross-tenant

  Mudança de IA/RAG/tools             isolamento, tool auth, output
                                      handling, budgets

  Incidente                           cenário do incidente + casos
                                      relacionados
  -----------------------------------------------------------------------

# 18. Integração com o Security Gate

O `RELEASE_SECURITY_GATE.md` deve receber:

-   commit/build testado;
-   quantidade de regressões obrigatórias;
-   PASS/FAIL/BLOQUEADAS;
-   regressões P0/P1;
-   evidências invalidadas;
-   exceções formalmente registradas.

### Quando bloquear

Uma regressão obrigatória P0 em `FAIL`, `BLOQUEADO` ou `NÃO EXECUTADO`
impede `PASS`.

Para demais prioridades, siga a política de risco definida pelo projeto
e registre explicitamente qualquer exceção.

# 19. Registro de execução

Não sobrescreva silenciosamente o histórico relevante.

  -----------------------------------------------------------------------------------------------
  Data    Commit/build   Ambiente     Executadas       PASS       FAIL   Bloqueadas Responsável
  ------- -------------- ---------- ------------ ---------- ---------- ------------ -------------

  -----------------------------------------------------------------------------------------------

# 20. Prompt para executar regressões

Use como ponto de partida:

> Leia `baseline/SECURITY_BASELINE.md`, `THREAT_MODEL.md`,
> `SECURITY_AUDIT_RESULTS.md` e este arquivo antes de executar qualquer
> alteração.
>
> Preserve testes existentes. Não enfraqueça, remova, pule ou altere uma
> regressão apenas para fazê-la passar.
>
> Identifique quais regressões são afetadas pelas mudanças atuais.
> Execute primeiro os testes sem modificar o sistema.
>
> Para cada regressão, registre comando/procedimento, ambiente,
> commit/build, resultado esperado e resultado real.
>
> Um PASS exige que o teste negativo bloqueie o comportamento indevido e
> que o teste positivo preserve o fluxo legítimo.
>
> Se uma regressão falhar, pare de considerar o controle correspondente
> como validado. Diagnostique a causa raiz antes de propor correção.
>
> Não execute testes destrutivos, carga, exploração contra terceiros ou
> alterações em produção sem autorização explícita.
>
> Ao final, atualize o resultado da suíte e informe se o
> `RELEASE_SECURITY_GATE.md` pode prosseguir ou está bloqueado.

# 21. Quando uma regressão está pronta

Uma regressão só está pronta quando:

-   [ ] está ligada a um controle/finding real;
-   [ ] descreve a vulnerabilidade original;
-   [ ] registra a causa raiz conhecida;
-   [ ] possui teste negativo;
-   [ ] possui teste positivo;
-   [ ] define resultado esperado;
-   [ ] é reproduzível;
-   [ ] registra ambiente/versão;
-   [ ] possui evidência;
-   [ ] define gatilhos de revalidação;
-   [ ] define quando deve rodar;
-   [ ] possui owner quando aplicável;
-   [ ] integra-se ao Security Gate quando relevante.

# 22. Regra-mestra

> Uma vulnerabilidade que já conhecemos não deveria conseguir voltar
> silenciosamente.

A regressão existe para transformar conhecimento de segurança em uma
barreira permanente e verificável.

Nunca troque evidência por confiança no código, no desenvolvedor ou no
agente de IA.
