# Security Baseline para Vibe Coding v1.3

Este baseline é um checklist de segurança pensado para projetos desenvolvidos com ajuda de IA.

A ideia é sair do “a IA disse que está seguro” e chegar a algo que possa ser verificado com evidência.

O documento nasceu de um baseline usado em um projeto real e depois foi generalizado para funcionar em diferentes stacks: web, mobile, APIs, SaaS multi-tenant, bancos relacionais, serverless/edge functions, object storage e aplicações com IA.

Ele não certifica que um sistema é seguro e não substitui pentest ou revisão profissional quando o risco justificar. O papel do baseline é oferecer um processo repetível para auditar, corrigir, testar de novo e registrar evidências.

## Como usar

1.  Salve este arquivo no repositório, por exemplo em
    `docs/SECURITY_BASELINE.md`.
2.  Entregue-o ao agente/IA que tenha acesso ao código.
3.  Informe a stack, o ambiente autorizado de teste, os perfis de
    usuário e as regras de acesso.
4.  Comece pela auditoria, não pela correção automática.
5.  Trabalhe item por item.
6.  Só marque um item como concluído depois de cumprir a Regra 99.
7.  Se um item não se aplicar à stack, marque N/A — NÃO APLICÁVEL,
    com justificativa. Não apague o item.
8.  Teste somente sistemas e ambientes que você possui ou tem autorização para avaliar.

## Princípios que orientam o baseline

-   Antes de criar, preserve.
-   Antes de alterar, diagnostique.
-   Antes de avançar, valide.
-   Não faça deploy, alterações de produção ou testes destrutivos/carga
    em produção durante a auditoria.
-   Não imprima nem envie segredos para a IA, logs ou relatórios.
-   Não encontrar algo em uma busca textual não prova que o sistema está seguro.
-   Prefira correções pequenas, compreensíveis e testáveis a grandes refatorações automáticas.
-   Proteção no frontend ajuda, mas não substitui autorização no backend.
-   UUID, CORS, CAPTCHA visual, botão escondido, rota difícil, `.env` e
    system prompt não são controles suficientes isoladamente.

## Como ler os status

-   ❌ VULNERÁVEL — falha comprovada.
-   ⚠️ SUSPEITO — indício relevante, ainda sem comprovação
    completa.
-   ❓ NÃO VERIFICADO — evidência insuficiente.
-   ✅ VALIDADO COM EVIDÊNCIA — passou pelos critérios da Regra
    99.
-   ➖ N/A — NÃO APLICÁVEL — controle realmente não existe
    naquela arquitetura, com justificativa registrada.

## Como funcionam as prioridades

-   🔴 P0 — Bloqueador de release/produção
-   🟠 P1 — Obrigatório antes de produção/piloto relevante
-   🟡 P2 — Hardening / defesa em profundidade
-   🔵 INFRA — depende de provedor/infraestrutura e exige evidência
    própria

## Cuidados ao testar

Use somente repositórios, contas, tenants, dispositivos e ambientes
locais/staging que você controla ou está autorizado a testar. Não faça
DDoS, varredura agressiva, exploração de terceiros ou coleta de
credenciais reais. Para SSRF e integrações externas, prefira
mocks/fixtures e ambientes isolados.

# 🔴 P0 — Bloqueadores de release / produção

## 01 — Segredos no frontend/build

Por que isso importa: uma variável em `.env` não é secreta se terminar no código
entregue ao navegador ou aplicativo. Chaves privadas, tokens
privilegiados e credenciais nunca podem ser incorporados ao frontend.

O que conferir: - `.env`, `.env.local`, arquivos de configuração; -
Dart/Flutter; - JavaScript/TypeScript; - bundles web; - source maps; -
respostas HTTP; - logs; - artefatos de build; - configurações de CI/CD.

Vale procurar especialmente: `service_role`, API keys privadas, tokens,
senhas, secrets de webhooks, credenciais de provedores e qualquer chave
com privilégio.

Quando considerar atendido: nenhum segredo privado alcança
cliente/browser/app. Chaves públicas por projeto devem ser
explicitamente classificadas como públicas e protegidas pelo modelo de
autorização correspondente.

## 02 — Segredos no Git/histórico

Por que isso importa: remover uma credencial do arquivo atual não a remove do
histórico Git.

O que conferir: - commits atuais e antigos; - branches; - tags; -
arquivos removidos; - diffs; - backups/exportações do repositório,
quando aplicável.

Quando considerar atendido: nenhum segredo válido permanece recuperável
no histórico; qualquer exposição anterior deve acionar o item 04.

## 03 — Segredos no APK/AAB

Por que isso importa: o aplicativo Android pode ser desmontado/inspecionado.
Strings, endpoints e credenciais incorporados podem ser recuperados.

No artefato RELEASE real, confira: - strings; - resources; -
`AndroidManifest.xml`; - assets; - configurações; - endpoints; -
tokens/chaves; - arquivos empacotados.

Quando considerar atendido: nenhuma credencial privada ou segredo
operacional recuperável do APK/AAB.

## 04 — Rotação/revogação de segredo exposto

Por que isso importa: apagar um segredo do código não invalida cópias já obtidas.

O que conferir: - se qualquer segredo encontrado nos itens 01--03 já
esteve exposto; - validade atual; - uso em logs/CI/CD; - escopo do
segredo.

Se a exposição for confirmada: revogar/rotacionar,
atualizar consumidores legítimos, verificar uso indevido e registrar
resposta ao incidente.

Quando considerar atendido: segredo antigo inválido + novo segredo
armazenado corretamente + consumidores atualizados + evidência de
rotação.

## 05 — Validação server-side de inputs

Por que isso importa: validação no frontend pode ser ignorada. Body, query, path,
headers, uploads e demais entradas são controláveis pelo cliente.

No servidor, valide: - tipo; - formato; - tamanho; - faixa; -
enum; - regras de negócio; - obrigatoriedade; - normalização quando
apropriada.

Testes negativos mínimos: tipo errado, campo vazio indevido, texto
acima do limite, valor fora da faixa, UUID inválido e estrutura JSON
inesperada.

Quando considerar atendido: entradas inválidas são rejeitadas antes de
atingir lógica sensível/persistência e entradas válidas continuam
funcionando.

## 06 — Mass assignment / campos extras

Por que isso importa: aceitar o body inteiro pode permitir alteração de campos
privilegiados.

Conforme o módulo, teste campos como: - `role`; - `admin`; -
`empresa_id`; - `user_id`; - `vigilante_id`; - `posto_id`; - `status`; -
`homologado`; - `owner_id`; - `created_by`; - campos equivalentes
sensíveis.

Como tratar: aceitar explicitamente apenas campos previstos
(allowlist/schema estrito). Nunca persistir `req.body`/payload completo
sem seleção.

Quando considerar atendido: campos extras são rejeitados/ignorados de
forma segura e não alteram estado protegido.

## 07 — SQL Injection

Por que isso importa: concatenação de entrada em SQL pode transformar dados em
comandos.

O que conferir: - SQL manual; - `raw`; - RPCs; - funções PostgreSQL; -
Edge Functions; - relatórios; - filtros/pesquisas; - qualquer
interpolação de string em consulta.

Como tratar: valores devem ser parametrizados.

Como testar: entradas com caracteres especiais/apóstrofos devem permanecer
dados e não alterar escopo/filtro.

Quando considerar atendido: nenhuma entrada controlada é concatenada como
SQL executável.

## 08 — SQL/RPC dinâmico e allowlists

Por que isso importa: nomes de tabela, coluna, ordenação ou operação geralmente não
podem ser tratados como parâmetros de valor.

O que conferir: - `ORDER BY` dinâmico; - coluna dinâmica; - tabela
dinâmica; - nome de função/operação; - SQL montado por string.

Como tratar: identificadores/opções dinâmicas devem vir de allowlist fixa
controlada pelo servidor.

Quando considerar atendido: usuário não consegue selecionar identificador
arbitrário ou alterar a estrutura da consulta.

## 09 — IDOR/BOLA — leitura

Por que isso importa: usuário autenticado pode trocar um identificador e ler
recurso de outro usuário/tenant.

Teste mínimo: Conta A tenta ler recurso pertencente à Conta/Tenant
B.

Como tratar: autorização deve considerar identidade autenticada + tenant +
objeto.

Quando considerar atendido: A não lê B; A continua lendo seu próprio
recurso.

## 10 — IDOR/BOLA — alteração

Teste mínimo: Conta A tenta atualizar recurso B, inclusive alterando
apenas campos aparentemente inofensivos.

Quando considerar atendido: alteração cross-tenant/cross-owner é negada
no backend/banco; operação legítima continua funcionando.

## 11 — IDOR/BOLA — exclusão

Teste mínimo: Conta A tenta excluir recurso B por endpoint, RPC, SDK
ou operação equivalente.

Quando considerar atendido: exclusão indevida é negada independentemente
da interface.

## 12 — IDOR/BOLA — anexos e listagens

Por que isso importa: proteger o registro principal e esquecer
relações/listagens/anexos.

O que testar: - fotos; - vídeos; - documentos; - relatórios; -
histórico; - listagens; - URLs; - recursos filhos; - metadados; - anexos
de ocorrências; - qualquer recurso relacionado.

Quando considerar atendido: nenhuma rota/listagem/anexo permite
atravessar o limite de usuário/tenant.

## 13 — RLS/isolamento no banco em tabelas expostas (quando aplicável)

Por que isso importa: tabelas expostas pelo Supabase/PostgREST sem RLS podem vazar
dados.

O que conferir: todas as tabelas expostas e todas as tabelas
multiempresa/sensíveis.

Quando considerar atendido: RLS habilitada onde necessária, com evidência
no estado LIVE.

## 14 — RLS/controle de dados deny-by-default

Por que isso importa: políticas excessivamente permissivas ou desenho que dependa
de o cliente "se comportar".

Como tratar: acesso deve existir apenas quando uma policy explicitamente o
autoriza.

Quando considerar atendido: usuário sem vínculo/permissão não obtém
acesso; ausência de regra de permissão não vira acesso acidental.

## 15 — Isolamento cross-tenant no banco / RLS

Teste em matriz A/B: - Tenant A → dados A: permitido conforme perfil. -
Tenant A → dados B: negado. - Tenant B → dados B: permitido conforme
perfil. - Tenant B → dados A: negado.

Quando fizer sentido, execute em: SELECT, INSERT, UPDATE e DELETE.

Quando considerar atendido: isolamento multiempresa comprovado com duas
identidades/tenants reais de teste.

## 16 — Policies/regras de autorização no INSERT

Por que isso importa: usuário cria registro apontando `empresa_id`, proprietário ou
relação para outro tenant.

Como testar: alterar identificadores sensíveis no payload de criação.

Quando considerar atendido: `WITH CHECK`/controle equivalente impede
inserção fora do escopo autorizado.

## 17 — Policies/regras de autorização no UPDATE / campos sensíveis

Por que isso importa: usuário pode ter direito de editar um objeto, mas não de
mudar seu proprietário/tenant/status privilegiado.

Teste alterações de: - `empresa_id`; - owner/user; - vínculo; -
role/perfil; - campos administrativos; - status protegido; - campos de
auditoria.

Quando considerar atendido: campos sensíveis não podem ser
promovidos/trocados pelo cliente sem autorização específica.

## 18 — Policies/regras de autorização no DELETE

Por que isso importa: exclusão física indevida, inclusive de recursos de outro
tenant ou registros que deveriam ser imutáveis.

Quando considerar atendido: DELETE permitido somente onde explicitamente
definido; bloqueios/soft-delete/proteções funcionam conforme regra de
negócio.

## 19 — Funções privilegiadas / SECURITY DEFINER / permissões (quando aplicável)

Por que isso importa: funções privilegiadas podem contornar RLS ou executar objetos
inesperados.

O que conferir: - todas as `SECURITY DEFINER`; - owner; -
`search_path`; - EXECUTE grants; - argumentos controláveis; - SQL
dinâmico; - chamadas internas; - possibilidade de cross-tenant.

Quando considerar atendido: privilégio mínimo, `search_path` seguro,
permissões restritas e autorização explícita dentro da função quando
necessária.

## 20 — Chaves administrativas/backend privilegiado (`service_role` ou equivalente)

Por que isso importa: `service_role` contorna RLS e possui alto privilégio.

Como tratar: - nunca no Flutter/browser; - nunca em APK/AAB; - nunca em
resposta/log; - apenas backend confiável; - uso mínimo e justificado.

Quando considerar atendido: todos os usos inventariados e necessários;
nenhum caminho cliente → `service_role`.

## 21 — Serverless/Edge/API Functions — autenticação/JWT

Confira por função: - exige autenticação? - configuração
`verify_jwt`; - validação de JWT; - token ausente; - token inválido; -
token expirado; - token válido.

Quando considerar atendido: cada função tem política de autenticação
documentada e testada; função privada não executa sem identidade válida.

## 22 — Serverless/Edge/API Functions — autorização

Por que isso importa: JWT válido prova identidade, não autorização para qualquer
objeto/ação.

O que conferir: - tenant; - perfil; - propriedade do recurso; - ação
solicitada; - campos sensíveis; - uso de `service_role` após a
autenticação.

Quando considerar atendido: função autenticada ainda nega
objeto/tenant/operação não autorizados.

## 23 — Identidade confiável

Por que isso importa: aceitar do cliente a própria identidade/autorização.

Não use apenas o payload como fonte de confiança para: - `user_id`; -
`empresa_id`; - perfil/role; - owner; - permissões.

A fonte confiável deve ser: sessão/JWT validado + banco/vínculos autorizados.

Quando considerar atendido: alterar identidade declarada no body/query
não concede privilégio nem troca tenant.

## 24 — Object Storage / arquivos — isolamento cross-tenant

O que testar: usuário/tenant A tenta abrir/listar arquivo de B por caminho
conhecido ou obtido em teste.

Inclua: fotos, vídeos, documentos, relatórios e demais objetos
privados.

Quando considerar atendido: objeto de outro tenant não é acessível apenas
por conhecer path/nome/UUID.

## 25 — Object Storage — policies/regras de SELECT/INSERT/UPDATE/DELETE

Confira separadamente: - leitura; - upload; -
substituição/atualização; - exclusão.

Quando considerar atendido: cada operação respeita usuário, tenant e
recurso; nenhuma policy ampla invalida isolamento.

## 26 — Buckets públicos

Por que isso importa: bucket público torna irrelevante uma policy de leitura para
objetos publicamente acessíveis.

O que conferir: inventário de buckets e justificativa de exposição.

Quando considerar atendido: conteúdo privado/sensível não está em bucket
público; qualquer bucket público contém somente material
intencionalmente público.

## 27 — Signed URLs / links temporários — expiração e autorização

Por que isso importa: signed URL pode ser criada para objeto que o solicitante não
deveria acessar ou durar tempo excessivo.

O que conferir: - autorização antes da assinatura; - duração; -
reutilização; - logging indevido; - escopo/path.

Quando considerar atendido: somente usuário autorizado obtém URL e
validade é mínima compatível com o uso.

## 28 — Autorização de upload

Por que isso importa: usuário envia arquivo para pasta/recurso/tenant arbitrário.

Como testar: alterar path, `empresa_id`, `ocorrencia_id`, `ronda_id` ou
equivalente.

Quando considerar atendido: upload só é aceito para recurso que o usuário
pode realmente modificar.

## 29 — Upload malicioso

O que conferir: - extensão; - MIME declarado; - MIME/assinatura real
quando aplicável; - tamanho; - quantidade; - nome/path; - conteúdo
ativo; - processamento posterior; - arquivos inesperados.

Como tratar: extensão ou `Content-Type` enviado pelo cliente não é prova
suficiente.

Quando considerar atendido: tipos/tamanhos não permitidos são rejeitados;
processamento não executa conteúdo enviado como código.

## 30 — Autenticação / armazenamento de senhas

Abordagem recomendada: nenhum módulo deve criar armazenamento
improvisado de senha.

O que conferir: - tabelas com `senha`, `password`, `passwd`; - logs; -
analytics; - exports; - respostas; - recuperação de senha.

Quando considerar atendido: preferencialmente utilizar
provedor/biblioteca de autenticação confiável. Se a aplicação armazenar
credenciais, nunca usar texto puro ou criptografia reversível; usar
mecanismo de hashing de senha apropriado e mantido.

# 🟠 P1 — Antes de piloto ou produção comercial

## 31 — Rate limit no login

Por que isso importa: brute force e credential stuffing.

O que conferir: limite por identidade/IP/contexto, janela, resposta ao
excesso e recuperação após a janela.

Quando considerar atendido: excesso é limitado sem bloquear
permanentemente fluxo legítimo.

## 32 — Rate limit por usuário

Por que isso importa: IP isolado não representa identidade, especialmente atrás de
NAT/proxy.

Quando considerar atendido: operações relevantes possuem limitação
associada à identidade autenticada quando apropriado.

## 33 — Rate limit por endpoint

Como tratar: endpoints com custos e riscos diferentes não devem
compartilhar cegamente o mesmo limite.

Quando considerar atendido: limites documentados por classe de
rota/operação.

## 34 — Proteção de rotas caras / abuso financeiro-computacional

Exemplos úteis: - geração de PDF; - IA; - processamento de vídeo/imagem; -
WhatsApp; - e-mail; - consulta VIN; - integrações pagas; - relatórios.

Por que isso importa: atacante pode causar indisponibilidade ou conta financeira
elevada.

Quando considerar atendido: autenticação/autorização +
limites/cotas/idempotência quando apropriados + monitoramento de
custo/abuso.

## 35 — Payload limits

Por que isso importa: corpos gigantes podem consumir memória/CPU/banda.

O que conferir: JSON, multipart, uploads e respostas.

Quando considerar atendido: limites coerentes com cada operação e
rejeição controlada de excesso.

## 36 — Timeouts externos

Por que isso importa: serviço externo lento prende recursos internos.

O que conferir: `fetch`, webhooks, APIs, downloads e integrações.

Quando considerar atendido: timeout explícito + tratamento seguro de
falha; retries controlados quando usados.

## 37 — DDoS / WAF / proteção de origem

Como tratar: rate limit na aplicação não equivale a proteção DDoS
volumétrica.

O que conferir: - provedor/borda; - WAF quando aplicável; - origem
exposta; - proxies confiáveis; - limites; - múltiplas instâncias.

Quando considerar atendido: controles de aplicação e infraestrutura
documentados separadamente. Não executar teste volumétrico em produção.

## 38 — Bots em login/cadastro

Por que isso importa: automação de tentativas, cadastros e abuso.

O que conferir: controles por conta/IP, detecção, desafio adaptativo
quando necessário e monitoramento.

Quando considerar atendido: automação básica abusiva é limitada e eventos
relevantes são observáveis.

## 39 — CAPTCHA/Turnstile validado no backend

Por que isso importa: widget visível não prova que o desafio foi validado.

No servidor, confira: - token ausente; - inválido; - expirado; -
reutilizado; - falha do provedor; - `hostname`; - `action`; - caso
válido.

Quando considerar atendido: operação protegida não acontece nos casos
inválidos; caso válido funciona.

## 40 — Enumeração de contas

Por que isso importa: respostas diferentes podem revelar CPF/e-mail/usuário
cadastrado.

O que conferir: login, recuperação, convite, cadastro e APIs correlatas.

Quando considerar atendido: respostas não revelam desnecessariamente
existência de conta; logs internos preservam diagnóstico sem vazar ao
cliente.

## 41 — Rotas administrativas

Mapeie: admin, debug, documentação interna, configuração,
relatórios privilegiados e operações sensíveis.

Matriz mínima de teste: - sem sessão → negar; - usuário comum → negar; -
admin correto → permitir conforme escopo; - admin de outro tenant →
negar quando aplicável.

Como tratar: URL escondida, botão oculto e CORS não são autorização.

## 42 — RBAC / perfis

Exemplos úteis: Usuário, operador, gestor, administrador do tenant,
administrador da plataforma e demais perfis do sistema.

Confira por recurso e operação: leitura, criação, alteração,
exclusão, homologação, administração.

Quando considerar atendido: matriz de acesso documentada e comprovada.

## 43 — Escalada horizontal

Por que isso importa: usuário com mesmo nível acessa recurso de outro
usuário/empresa sem direito.

Como testar: identidade A tenta agir como/contra identidade B do mesmo
nível.

Quando considerar atendido: limites de propriedade/tenant permanecem
ativos.

## 44 — Escalada vertical

Por que isso importa: usuário comum obtém ação de supervisor/admin/plataforma.

O que testar: manipulação de payload, rota, token/claims não confiáveis,
RPC e chamadas diretas.

Quando considerar atendido: privilégio só vem de fonte confiável e ação
privilegiada é negada ao perfil inferior.

## 45 — XSS

Em aplicações web, confira: - `innerHTML`; -
`dangerouslySetInnerHTML`; - templates sem escape; - conteúdo de
usuário; - resposta de IA; - nomes/observações/comentários.

Como testar: marcador HTML/JS inofensivo deve aparecer como texto quando
HTML não é necessário.

Quando considerar atendido: dados não confiáveis não viram conteúdo
executável.

## 46 — HTML/Markdown rico e sanitização

Por que isso importa: quando HTML/Markdown é necessário, renderização pode
introduzir scripts/eventos/URLs perigosas.

O que conferir: biblioteca de sanitização mantida, configuração
restritiva e contexto de saída.

Quando considerar atendido: payloads de teste perigosos são neutralizados
sem destruir conteúdo legítimo.

## 47 — SSRF

Mapeie: - `fetch`; - webhooks; - importadores; - URL de imagem; -
documentos remotos; - callbacks; - APIs cujo destino é controlável.

De preferência: cliente envia uma opção de negócio; servidor escolhe
destino conhecido.

Quando considerar atendido: usuário não induz servidor a acessar destino
arbitrário não autorizado.

## 48 — SSRF avançado

Teste apenas com ambiente ou mocks autorizados: - loopback; - IPv4 privado; -
IPv6; - destinos privados; - redirects; - resolução DNS/mudança de
DNS; - tamanho de resposta; - timeout.

Evite consultar metadados reais de nuvem como forma de teste.

Quando considerar atendido: controles abrangem destino final, não apenas
a string inicial da URL.

## 49 — Mensagens de erro sem vazamento

Não devolva ao usuário: - stack trace; - SQL; - caminhos
internos; - versões desnecessárias; - tokens; - credenciais; - dados
pessoais; - detalhes de infraestrutura.

Preserve: 4xx úteis para erros esperados e mensagem
genérica/request ID para falha inesperada.

Quando considerar atendido: exceção controlada não vaza detalhes
sensíveis.

## 50 — Logs sanitizados

Só registre com uma política explícita de mascaramento: - senhas; -
JWT; - `Authorization`; - cookies; - secrets; - corpos contendo dados
sensíveis; - PII desnecessária.

Quando considerar atendido: logs permitem investigação/correlação sem se
tornarem novo repositório de credenciais/dados sensíveis.

# 🟡 P2 — Hardening e defesa em profundidade

## 51 — Security headers web

Avalie de acordo com a arquitetura: - Content-Security-Policy (CSP); -
Strict-Transport-Security (HSTS); - `X-Content-Type-Options`; - política
de framing (`frame-ancestors`/equivalente); - Referrer-Policy; -
Permissions-Policy quando aplicável.

Quando considerar atendido: headers coerentes com o aplicativo e testados
sem quebrar funcionalidades legítimas.

## 52 — HTTPS/TLS obrigatório

O que conferir: aplicações web, APIs, callbacks, assets sensíveis e
integrações.

Quando considerar atendido: tráfego sensível não utiliza HTTP;
redirecionamentos/configuração não permitem downgrade indevido.

## 53 — CORS

Por que isso importa: CORS mal configurado amplia origens permitidas, mas CORS
também não substitui autenticação/autorização.

O que conferir: - origens necessárias; - métodos; - headers; -
credenciais; - wildcard incompatível com contexto.

Quando considerar atendido: somente origens necessárias quando aplicável;
endpoints permanecem seguros mesmo fora do navegador.

## 54 — Dependências vulneráveis

Escopo: - Flutter/Dart; - npm/Node; - SDKs Supabase; - bibliotecas
backend; - demais pacotes.

O que conferir: advisories conhecidos, versões abandonadas, atualizações
de segurança e dependências transitivas.

Quando considerar atendido: vulnerabilidades relevantes
tratadas/mitigadas e exceções documentadas.

## 55 — Supply-chain / lockfiles / origem e manutenção de pacotes

O que conferir: - lockfiles; - origem dos pacotes; - pacote
typosquatting/suspeito; - dependências desnecessárias; - manutenção; -
scripts de instalação/build; - integridade/reprodutibilidade quando
aplicável.

Quando considerar atendido: cadeia de dependências conhecida e
minimizada; inclusão de pacote novo é justificável.

## 56 — Mobile local storage

Por que isso importa: tokens/dados sensíveis podem ficar recuperáveis no aparelho,
backup, logs ou armazenamento inadequado.

O que conferir: - SharedPreferences; - arquivos locais; - SQLite; -
caches; - logs; - screenshots quando relevante; - clipboard quando
relevante; - armazenamento seguro/Keystore para segredos adequados.

Quando considerar atendido: apenas dados necessários persistem; material
sensível recebe armazenamento/proteção compatível e é removido quando
apropriado.

## 57 — Reverse engineering / APK/AAB release

Objetivo: avaliar o que um terceiro aprende ao desmontar o app.

O que conferir: - endpoints; - estrutura; - strings; - feature flags; -
chaves; - lógica sensível; - logs/debug; - artefatos desnecessários; -
configuração release.

Observação: ofuscação dificulta análise, mas não transforma segredo
cliente-side em segredo.

Quando considerar atendido: release não contém informação sensível
evitável e nenhuma proteção depende exclusivamente de esconder código.

## 58 — Prompt Injection / IA

Princípio importante: conteúdo externo lido pela IA é dado não
confiável. A saída do modelo também é não confiável.

Aplique a: - documentos; - páginas; - mensagens; - PDFs; -
e-mails; - resultados de ferramentas; - conteúdo de usuário; - respostas
de modelos.

Regras: - IA nunca decide autorização; - ferramentas validam
argumentos no backend; - sessão/tenant/perfil são revalidados fora do
modelo; - modelo recebe somente dados/segredos estritamente
necessários; - ações de alto impacto exigem confirmação/controle
adicional quando apropriado.

Como testar: documento malicioso pede para ignorar regras e acessar
recurso de outro tenant; backend deve negar mesmo que o modelo solicite.

Quando considerar atendido: barreira efetiva está no backend/controle de
ferramenta, não apenas no system prompt.

## 59 — Auditoria e Incident Response / trilha de eventos

Objetivo: permitir detectar e investigar ações sensíveis sem criar
vazamento adicional.

Quando necessário, registre: - quem; - tenant/empresa; - ação; -
recurso; - quando; - resultado; - request/correlation ID; -
origem/contexto necessário.

Eventos que podem entrar aqui: login relevante, mudança de perfil,
administração, homologação, alterações sensíveis, falhas de autorização,
abuso/rate limit e operações privilegiadas.

Quando considerar atendido: eventos críticos são rastreáveis, logs são
protegidos/sanitizados e existe procedimento mínimo de resposta a
incidente.

## 60 — Security Regression Suite / Security Gate

Objetivo: impedir que correções futuras reintroduzam
vulnerabilidades já eliminadas.

Transformar controles críticos em testes repetíveis, incluindo quando
aplicável: - cross-tenant; - RBAC; - campos sensíveis; -
autenticação; - Edge Functions; - Storage; - validação; - erros; - rate
limit; - uploads.

Antes de uma release ou piloto, use o Security Gate para: nenhuma falha P0 conhecida
aberta; P1 aplicável tratado ou risco formalmente documentado;
evidências atualizadas para componentes alterados.

Quando considerar atendido: suíte executada com resultados reais
registrados e regressões críticas bloqueiam a release.

# Controles adicionados na revisão v1.1

A revisão v1.1 cruzou o baseline com OWASP ASVS 5.0.0, OWASP Top
10:2025, OWASP API Security Top 10:2023 e OWASP MASVS 2.1.0.

Os controles abaixo foram adicionados porque o baseline original cobria
muito bem autorização, isolamento, secrets, abuso, storage e
vulnerabilidades clássicas, mas ainda não tratava com profundidade
suficiente criptografia, sessão, design, inventário de APIs, integridade
de pipeline, privacidade e superfícies específicas de mobile.

## 61 — Threat modeling / design seguro / regras de negócio

Por que isso importa: uma aplicação pode estar "correta no código" e ainda ser
insegura por desenho. Vulnerabilidades de fluxo de negócio
frequentemente não aparecem em scanners.

Mapeie: - ativos que precisam ser protegidos; - atores e perfis; -
fronteiras de confiança; - fluxos críticos; - operações irreversíveis; -
abuso economicamente interessante; - suposições de segurança; -
dependências externas; - cenários de fraude.

O que testar: formas de pular etapas, executar ações fora de ordem,
repetir operações, manipular estados e combinar funções legítimas para
obter resultado indevido.

Quando considerar atendido: fluxos críticos possuem invariantes/regras
server-side documentadas e testadas; segurança não depende apenas da
sequência apresentada pela interface.

## 62 — Criptografia e algoritmos seguros

Por que isso importa: criptografia própria, algoritmos obsoletos ou parâmetros
fracos podem dar falsa sensação de proteção.

O que conferir: - algoritmos; - modos; - tamanhos de chave; - geração de
IV/nonce; - aleatoriedade; - hashing; - assinatura; - comparação de
valores sensíveis quando relevante.

Como tratar: não inventar criptografia. Usar bibliotecas e primitivas
modernas e mantidas, adequadas ao objetivo.

Quando considerar atendido: nenhuma proteção crítica depende de algoritmo
obsoleto, implementação caseira ou parâmetro inseguro.

## 63 — Gestão de chaves criptográficas

Por que isso importa: criptografia forte perde valor se a chave estiver no código,
no mesmo arquivo do dado ou acessível ao cliente indevido.

O que conferir: - geração; - armazenamento; - acesso; - rotação; -
revogação; - separação por ambiente; - backup; - expiração; - exposição
em logs/builds.

Quando considerar atendido: ciclo de vida da chave é compatível com sua
sensibilidade e nenhum cliente recebe chave que deveria permanecer no
servidor/HSM/KMS/keystore equivalente.

## 64 — Sessão, tokens e ciclo de vida de autenticação

O que conferir: - expiração de access token; - refresh token; -
revogação; - logout; - rotação; - reutilização; - sessões simultâneas
quando relevante; - mudança de senha/perfil; - armazenamento do token; -
invalidação após evento de segurança.

Testes mínimos: token expirado, revogado, malformado, de outro
ambiente/audience quando aplicável e sessão após logout.

Quando considerar atendido: sessão inválida não continua autorizando
operações e o fluxo legítimo de renovação permanece funcional.

## 65 — MFA, recuperação de conta e operações de alto impacto

Por que isso importa: autenticação forte pode ser contornada pelo fluxo de
recuperação ou por operações sensíveis sem reautenticação.

Confira de acordo com o risco: - recuperação de senha; - troca de
e-mail/telefone; - mudança de MFA; - elevação de privilégio; - operações
administrativas; - ações financeiras/irreversíveis; - códigos de
recuperação.

Quando considerar atendido: recuperação não é mais fraca que o nível de
proteção necessário para a conta; ações críticas usam
step-up/reautenticação/MFA quando o risco justificar.

## 66 — Configuração insegura, debug e defaults

Mapeie por ambiente: - debug mode; - endpoints de
diagnóstico; - stack traces; - contas/senhas padrão; - painéis
administrativos; - documentação interativa; - flags experimentais; -
diretórios/listagens; - permissões padrão; - serviços/portas
desnecessários; - configurações permissivas.

Quando considerar atendido: produção usa configuração endurecida,
separada de desenvolvimento, sem funcionalidades de debug ou defaults
perigosos expostos.

## 67 — Inventário de APIs, versões e endpoints esquecidos

Por que isso importa: APIs antigas, beta, debug ou não documentadas podem
permanecer acessíveis e escapar dos controles atuais.

Mapeie: - hosts; - versões; - rotas; - RPCs; - GraphQL; -
webhooks; - funções serverless; - endpoints internos expostos; - versões
depreciadas.

Quando considerar atendido: existe inventário atual; versões antigas são
removidas/bloqueadas ou mantidas com os mesmos controles; nenhum
endpoint "órfão" relevante permanece exposto sem dono.

## 68 — Consumo seguro de APIs e dados de terceiros

Por que isso importa: dados vindos de outra API não são automaticamente confiáveis.

O que conferir: - validação de schema; - limites; - tipos; - conteúdo
inesperado; - timeouts; - redirects; - erros; - autenticação do
terceiro; - dados usados em SQL/HTML/comandos; - confiança excessiva em
respostas externas.

Quando considerar atendido: respostas externas atravessam validação
compatível com seu uso e falhas do terceiro não viram bypass de
segurança.

## 69 — Webhooks: autenticidade, replay e idempotência

O que conferir: - assinatura/HMAC ou mecanismo equivalente; -
segredo/chave; - timestamp; - janela anti-replay; - identificador único
do evento; - idempotência; - ordem de eventos; - retries; - autorização
da ação resultante.

Como testar: reenviar o mesmo evento e enviar evento adulterado.

Quando considerar atendido: evento forjado é rejeitado e replay não
duplica ação de negócio.

## 70 — Integridade de software, CI/CD e artefatos

Por que isso importa: código seguro pode ser comprometido entre commit, build e
deploy.

O que conferir: - permissões do CI/CD; - secrets do pipeline; - proteção
de branches; - dependências/actions; - origem do artefato; - assinatura
quando aplicável; - promoção entre ambientes; - quem pode publicar; -
alterações de pipeline.

Quando considerar atendido: caminho código → build → artefato → deploy
possui controles de integridade e privilégio mínimo compatíveis com o
risco.

## 71 — Falhas seguras e condições excepcionais

Por que isso importa: timeout, exceção, falha parcial ou dependência indisponível
pode colocar o sistema em estado inseguro.

O que testar: - banco indisponível; - API externa falhando; - timeout; -
resposta parcial; - exceção durante autorização; - falha durante
operação multi-etapa; - retry.

Como tratar: falha de componente de segurança deve tender a fail
closed, não conceder acesso por conveniência.

Quando considerar atendido: exceções não transformam "não sei se está
autorizado" em "permitido" e não deixam estado crítico inconsistente.

## 72 — Concorrência, race conditions, replay e idempotência de negócio

Por que isso importa: duas requisições simultâneas ou repetidas podem contornar
limites ou duplicar efeitos.

Isso merece atenção especial em: - pagamentos; - cupons; - estoque; -
criação de registros únicos; - aprovação/homologação; - alteração de
status; - envio de mensagens; - jobs; - operações irreversíveis.

Quando considerar atendido: invariantes críticas sobrevivem a
concorrência/repetição; operações que precisam ser únicas são
atômicas/idempotentes.

## 73 — Privacidade, minimização, retenção e exclusão

O que conferir: - quais dados são coletados; - necessidade real; -
finalidade; - tempo de retenção; - caches/backups; -
analytics/telemetria; - compartilhamento com terceiros; - exclusão; -
exportação quando aplicável; - transparência ao usuário.

Como tratar: coletar e conservar somente o necessário para a finalidade
legítima.

Quando considerar atendido: coleta e retenção são justificáveis, fluxos
de exclusão são conhecidos e telemetria não envia dados
desnecessários/sensíveis.

Observação: este controle é técnico e não substitui avaliação
jurídica/regulatória (LGPD, GDPR etc.).

## 74 — Mobile: permissões, componentes, deep links e IPC

Aplicável a apps mobile.

O que conferir: - permissões solicitadas; - componentes exportados; -
intents/URL schemes/deep links; - App Links/Universal Links; -
WebViews; - clipboard; - screenshots; - IPC; - arquivos
compartilhados; - interação com outros apps.

Quando considerar atendido: privilégio mínimo; entrada externa é tratada
como não confiável; componente sensível não fica exposto sem
necessidade/autorização.

## 75 — Mobile: rede, atualização, plataforma e resiliência

Aplicável a apps mobile.

O que conferir: - TLS e validação de certificado; - cleartext traffic; -
versões mínimas de SO suportadas; - bibliotecas nativas; - mecanismo
para responder a versão vulnerável; - atualização do app; -
release/debug; - reverse engineering/tampering conforme threat model; -
privacidade declarada versus comportamento real.

Ponto de atenção: pinning, root/jailbreak detection e anti-tamper não são
obrigatórios para todo app; devem ser decididos pelo threat model e não
podem substituir autorização server-side.

Quando considerar atendido: comunicação é protegida, plataforma suportada
é compatível com o risco, versão vulnerável pode ser tratada
operacionalmente e controles de resiliência são proporcionais ao threat
model.

# Controles adicionados na revisão v1.2

A v1.2 torna explícitas superfícies que antes estavam parcialmente
embutidas em controles mais amplos. Isso facilita a auditoria por
agentes de IA e reduz a chance de uma superfície específica passar
despercebida.

## Tags de aplicabilidade

Cada projeto deve classificar os controles antes da auditoria:

-   \[CORE\] — praticamente qualquer aplicação.
-   \[WEB\] — aplicações web/browser.
-   \[API\] — APIs, backends e serverless.
-   \[MOBILE\] — Android/iOS.
-   \[SAAS\] — multiusuário/multi-tenant.
-   \[AI\] — IA, LLMs, agentes e tools.
-   \[FILES\] — upload, download ou processamento de arquivos.
-   \[REALTIME\] — WebSocket/realtime/pub-sub.
-   \[OAUTH\] — OAuth 2.x, OpenID Connect e SSO.
-   \[INFRA\] — cloud, rede, CI/CD, runtime e infraestrutura.

Como tratar: uma tag ajuda a decidir aplicabilidade; não substitui análise
da arquitetura. Um item só pode ser `N/A` com justificativa.

## 76 — \[API\]\[CORE\] Command Injection / execução de comandos do sistema operacional

Por que isso importa: entrada controlada pelo usuário pode alcançar shell, processo
externo ou ferramenta de sistema e virar comando.

Mapeie: - `exec`, `spawn`, subprocessos e shell; -
FFmpeg/ImageMagick e ferramentas de mídia; - Git; - conversores; -
compactadores; - scripts; - CLIs; - qualquer processo construído a
partir de input.

Como tratar: evitar shell quando uma API segura/biblioteca resolve o
problema; passar argumentos separadamente; usar allowlists para opções;
nunca concatenar entrada não confiável em comando.

Teste negativo: valores com metacaracteres e argumentos inesperados
não podem alterar o comando/operação prevista.

Quando considerar atendido: dados do usuário permanecem dados e não
controlam comando, flags ou executáveis fora da allowlist.

## 77 — \[API\]\[FILES\] Desserialização insegura / XXE / parsers

Por que isso importa: parsers de XML, YAML, objetos serializados ou formatos
complexos podem executar comportamento inesperado, acessar recursos
externos ou reconstruir tipos perigosos.

O que conferir: - XML e entidades externas; - YAML; - serialização nativa
de linguagem; - objetos polimórficos; - bibliotecas de parsing; -
formatos recebidos de terceiros; - schemas e limites.

Como tratar: preferir formatos simples; desabilitar recursos perigosos;
não desserializar objetos arbitrários controlados pelo cliente; validar
schema antes do uso.

Quando considerar atendido: payload não confiável não instancia tipo
arbitrário, executa código, acessa recurso externo indevido ou ignora
validação.

## 78 — \[FILES\]\[API\] Path Traversal / LFI / manipulação de caminhos

Por que isso importa: nomes e caminhos controlados podem escapar do diretório
permitido ou atingir arquivos internos.

O que testar: - `../` e variantes; - caminhos absolutos; - encoding; -
separadores alternativos; - symlinks quando relevantes; - nomes de
ZIP; - extração de arquivos (ZIP Slip).

Como tratar: gerar nomes server-side quando possível,
resolver/canonicalizar o caminho e confirmar que o destino final
permanece dentro da raiz autorizada.

Quando considerar atendido: entrada controlada nunca permite leitura,
gravação, sobrescrita ou extração fora do diretório/recurso autorizado.

## 79 — \[FILES\]\[WEB\]\[API\] Download seguro de arquivos

Por que isso importa: um download pode contornar autorização, expor arquivos
internos ou fazer o navegador interpretar conteúdo perigoso.

O que conferir: - autorização por objeto/tenant; - path/ID; - filename; -
`Content-Type`; - `Content-Disposition`; - cache; - links temporários; -
arquivos não confiáveis; - headers relevantes.

Como testar: usuário A tenta baixar arquivo B; filename/conteúdo malicioso
não pode alterar headers nem execução prevista.

Quando considerar atendido: somente usuário autorizado recebe o arquivo
correto e a resposta não transforma conteúdo não confiável em execução
indevida.

## 80 — \[OAUTH\]\[WEB\]\[MOBILE\]\[API\] OAuth 2.x / OpenID Connect / SSO

Aplicável somente quando o projeto usa OAuth/OIDC/SSO.

Verificar conforme o fluxo: - redirect URIs estritas; - `state`; -
PKCE; - `nonce` em OIDC; - validação de assinatura; - `iss`; - `aud`; -
expiração; - scopes; - troca de código; - armazenamento de tokens; -
replay; - logout/revogação.

Como tratar: não implementar protocolo "de memória"; seguir
biblioteca/provedor mantido e o fluxo apropriado ao tipo de cliente.

Quando considerar atendido: callback/token de outro cliente, issuer,
audience, sessão ou fluxo não é aceito; fluxo legítimo funciona.

## 81 — \[REALTIME\]\[WEB\]\[API\] WebSockets / realtime

Por que isso importa: autenticar a conexão não significa autorizar todas as
mensagens posteriores.

O que conferir: - autenticação no handshake/conexão; - autorização por
canal, tópico, objeto e ação; - expiração/revogação da sessão; - origem
quando relevante; - tamanho/frequência das mensagens; - subscriptions; -
reconexão; - vazamento cross-tenant.

Como testar: cliente autenticado tenta assinar canal/objeto de outro
usuário/tenant e enviar ação não autorizada.

Quando considerar atendido: autorização é aplicada ao recurso/ação
realtime, não apenas à abertura da conexão.

## 82 — \[API\] GraphQL

Aplicável somente quando GraphQL existe.

O que conferir: - autorização por resolver/objeto; - field-level
access; - introspection conforme ambiente/política; - profundidade; -
complexidade/custo; - aliases; - batching; - paginação; - enumeração; -
erros.

Por que isso importa: uma única query pode atravessar relações protegidas ou gerar
custo muito maior do que aparenta.

Quando considerar atendido: GraphQL respeita os mesmos limites de
autorização e consumo da aplicação; query complexa não vira bypass ou
DoS barato.

## 83 — \[API\]\[INFRA\] Service-to-service / machine-to-machine

Por que isso importa: "rede interna" não é identidade nem autorização.

Aplique a: - microserviços; - workers; - filas; - jobs; - APIs
internas; - banco; - serviços serverless; - integrações internas.

O que conferir: - identidade do serviço; - autenticação; - autorização; -
credenciais temporárias quando possível; - privilégio mínimo; -
rotação; - TLS/rede; - segregação entre ambientes.

Quando considerar atendido: cada componente recebe somente o acesso
necessário e serviço não autorizado não consegue se passar por outro
apenas por estar na mesma rede.

## 84 — \[FILES\]\[API\]\[WEB\] Malware, arquivos comprimidos e processamento de arquivos

Por que isso importa: mesmo um arquivo com tipo permitido pode explorar parser,
carregar conteúdo ativo, esconder malware ou causar exaustão de
recursos.

Verificar conforme o risco: - tamanho após descompressão; -
profundidade/quantidade de arquivos; - ZIP bombs; - arquivos
aninhados; - reprocessamento seguro de imagem/documento; - bibliotecas
de parsing atualizadas; - macros/conteúdo ativo; - quarentena; -
antivírus/sandbox quando proporcional ao contexto; - armazenamento fora
da raiz pública antes da validação.

Como tratar: antivírus não substitui validação de tipo, autorização,
limites e isolamento.

Quando considerar atendido: processamento de arquivo não permite
execução, escape de diretório, exaustão previsível de recursos ou
publicação antes das validações exigidas.

# Controles adicionados na revisão v1.3

A v1.3 fecha a expansão horizontal do baseline em 99 controles. O
foco desta revisão é aprofundar segurança de IA/agentes, runtime/cloud,
recuperação operacional e duas superfícies web que merecem validação
explícita.

A partir desta versão, a recomendação é não aumentar a lista apenas
para aumentar cobertura nominal. Novas versões devem priorizar
qualidade dos testes, automação, evidências, mapeamento de requisitos e
adaptação por stack. Controles realmente novos só devem entrar quando
representarem uma classe de risco materialmente diferente.

## 85 — \[AI\]\[CORE\] AI Sensitive Information Disclosure / exposição de dados à IA

Por que isso importa: prompts, contexto, RAG, logs ou chamadas para modelos podem
enviar secrets, PII, documentos internos ou dados de outros
usuários/tenants sem necessidade.

Mapeie: - tudo que entra no prompt/contexto; - system/developer
prompts; - anexos; - memória; - RAG; - tool results; - logs de
prompts/respostas; - provedores/modelos externos; - retenção do
provedor; - dados de treinamento quando aplicável.

Como tratar: aplicar minimização. O modelo recebe somente os dados
necessários para executar aquela tarefa e somente dados que o
usuário/tenant está autorizado a usar.

Teste negativo: usuário/tenant A tenta provocar inclusão ou
recuperação de dado sensível de B ou de segredo operacional.

Quando considerar atendido: informação sensível desnecessária não alcança
o modelo e dados autorizados permanecem isolados por
identidade/tenant/finalidade.

## 86 — \[AI\]\[API\] AI Tool/Agent Permissions / Excessive Agency

Por que isso importa: um agente pode possuir ferramentas, permissões ou autonomia
maiores do que a tarefa exige.

Inventariar por agente: - tools disponíveis; - leitura/escrita; -
banco; - filesystem; - e-mail/mensageria; - pagamentos; - deploy; -
administração; - ações destrutivas; - capacidade de chamar outros
agentes.

Regras: - menor privilégio; - autorização server-side em cada
tool; - argumentos revalidados; - identidade/tenant derivados de fonte
confiável; - confirmação humana para ações de alto impacto quando
apropriado; - separar ferramentas de leitura e escrita quando útil.

Como testar: prompt malicioso solicita ação que excede a permissão do
usuário/agente.

Quando considerar atendido: o modelo pode pedir; a camada determinística
continua negando o que não é autorizado.

## 87 — \[AI\]\[SAAS\] RAG / Vector Database / Embeddings Isolation

Por que isso importa: filtros semânticos ou metadados incorretos podem recuperar
documentos de outro usuário/tenant.

O que conferir: - ingestão; - namespace/collection; - metadados; -
filtros; - autorização antes/depois da recuperação; - cache; -
embeddings; - exclusão; - reindexação; - documentos compartilhados.

Em SaaS, este teste é obrigatório: tenant A tenta recuperar semanticamente
conteúdo exclusivo de B, inclusive usando palavras conhecidas do
documento.

Quando considerar atendido: busca vetorial/semântica respeita os mesmos
limites de autorização do dado original.

## 88 — \[AI\] Data / Model / Knowledge Poisoning

Por que isso importa: conteúdo malicioso inserido em documentos, datasets, memória,
RAG ou fontes externas pode influenciar respostas e ações futuras.

O que conferir: - quem pode inserir/alterar conhecimento; -
procedência; - moderação/validação; - versionamento; - prioridade entre
fontes; - conteúdo recuperado; - memória persistente; - feedback usado
para melhorar comportamento; - rollback.

Como tratar: conteúdo recuperado é dado não confiável e não pode redefinir
políticas de autorização.

Quando considerar atendido: fonte maliciosa não ganha autoridade sobre
regras do sistema e alterações de conhecimento relevantes são
rastreáveis/reversíveis.

## 89 — \[AI\]\[WEB\]\[API\] AI Output Handling

Por que isso importa: saída do modelo pode conter SQL, HTML, Markdown ativo, URL,
shell, código ou argumentos de ferramenta perigosos.

Nunca tratar saída de IA como confiável apenas porque veio do próprio
modelo.

Confira para onde a saída vai: - HTML/DOM; - SQL; - shell; -
templates; - Markdown; - URLs; - APIs; - tools; - arquivos; -
mensagens; - código executado.

Como tratar: validar/sanitizar/parametrizar de acordo com o sink final.

Quando considerar atendido: resposta maliciosa do modelo permanece dado e
não vira execução/ação indevida.

## 90 — \[AI\] System Prompt / Agent Configuration / Secrets

Por que isso importa: system prompts, instruções ocultas, nomes de tools e
configurações podem ser parcialmente revelados por comportamento, logs,
erros ou ataques.

Como tratar: system prompt não é cofre nem mecanismo de autorização.

Não trate como “segredo protegido pela IA”: - API keys; -
senhas; - tokens; - credenciais; - dados que causariam impacto material
se extraídos.

Quando considerar atendido: eventual exposição parcial de instruções não
entrega credencial nem remove uma barreira de segurança real.

## 91 — \[AI\]\[API\] AI Cost / Token / Tool Budget / Unbounded Consumption

Por que isso importa: prompts gigantes, loops de agentes, geração ilimitada,
chamadas recursivas ou tools caras podem gerar DoS e custo financeiro
descontrolado.

Controle de acordo com a arquitetura: - tamanho de entrada; - tokens; -
duração; - número de iterações; - número de tools; - concorrência; -
custo por usuário/tenant; - retries; - contexto/RAG; - geração de
mídia; - quotas.

Como testar: requisição no limite e acima do limite; agente tentando
loop/repetição.

Quando considerar atendido: consumo possui limites previsíveis e
excedê-los falha de forma controlada sem comprometer outros usuários.

## 92 — \[INFRA\]\[API\] Container / Runtime Hardening

Aplicável a containers, VPS, Kubernetes, runtimes serverless
configuráveis e ambientes equivalentes.

Confira de acordo com a plataforma: - execução como root; - modo
privilegiado; - Linux capabilities; - filesystem gravável; - mounts; -
acesso ao socket do container; - CPU/memória/processos; - imagem base; -
patches; - debug tools; - secrets na imagem; - isolamento entre
workloads.

Quando considerar atendido: runtime usa privilégio mínimo, limites
adequados e não transforma comprometimento da aplicação automaticamente
em controle do host/ambiente.

## 93 — \[INFRA\]\[API\] Cloud IAM / Service Accounts / Least Privilege

Por que isso importa: credencial de aplicação excessivamente privilegiada amplia
drasticamente o impacto de uma invasão.

Mapeie: - IAM roles; - service accounts; - API keys; -
credenciais cloud; - permissões de banco/storage/filas; - ambientes; -
credenciais temporárias; - trust relationships.

Teste ou revisão: comparar cada permissão com as operações realmente
necessárias.

Quando considerar atendido: workload possui somente privilégios
necessários, ambientes são segregados e credenciais privilegiadas não
são compartilhadas sem necessidade.

## 94 — \[INFRA\]\[CORE\] Backup Security + Restore Test

Por que isso importa: backup pode vazar os mesmos dados da produção ou simplesmente
não restaurar quando necessário.

O que conferir: - conteúdo; - criptografia; - controle de acesso; -
localização; - segregação; - retenção; - imutabilidade quando
necessária; - secrets/PII presentes; - exclusão; - logs; - cópias
antigas; - procedimento de restore.

Teste essencial: executar restauração autorizada em ambiente isolado
e validar integridade/consistência sem sobrescrever produção.

Quando considerar atendido: backup é protegido proporcionalmente aos
dados originais e existe evidência recente de restauração funcional.

## 95 — \[WEB\]\[API\] Prototype Pollution

Especialmente relevante para ecossistemas JavaScript/Node e
manipulação dinâmica de objetos.

O que conferir: - merge profundo; - setters dinâmicos; - objetos
construídos a partir de chaves do usuário; - `__proto__`; -
`constructor`; - `prototype`; - bibliotecas historicamente afetadas.

Como tratar: rejeitar chaves perigosas, preferir estruturas
seguras/allowlists e manter bibliotecas corrigidas.

Quando considerar atendido: entrada controlada não modifica protótipos
globais nem altera autorização/configuração/comportamento de outros
objetos.

## 96 — \[WEB\]\[API\]\[SAAS\] Cache Security / Cache Poisoning / Cross-user Leakage

Mapeie: - CDN; - reverse proxy; - browser cache; - Redis/cache de
aplicação; - ISR/SSR cache; - edge cache; - cache de API; - cache de RAG
quando aplicável.

O que conferir: - `Cache-Control`; - `Vary`; - chave de cache; -
usuário/tenant; - autenticação; - headers não confiáveis; - query
params; - invalidação; - conteúdo sensível.

Como testar: respostas diferentes de usuários/tenants não podem
compartilhar entrada de cache quando deveriam permanecer isoladas.

Quando considerar atendido: cache não mistura identidade/tenant, não
armazena conteúdo sensível indevidamente e não pode ser envenenado por
entrada não confiável relevante.

## 97 — \[CORE\]\[INFRA\] Security Kill Switch / Contenção de Emergência

Objetivo: permitir conter rapidamente uma vulnerabilidade crítica
sem depender exclusivamente de nova release/deploy completo.

Planeje de acordo com a arquitetura: - revogar sessões/tokens; -
rotacionar segredo; - desativar integração; - bloquear endpoint; -
desligar feature flag; - suspender chave; - bloquear versão vulnerável
quando possível; - reduzir permissões; - identificar usuários/tenants
afetados.

Proteja também o próprio mecanismo: kill switch também precisa de
autenticação forte, autorização, auditoria e proteção contra acionamento
indevido.

Quando considerar atendido: existe procedimento documentado e testável
para conter classes críticas de incidente em tempo compatível com o
risco.

## 98 — \[CORE\]\[INFRA\] Dependency/Provider Failure & Security Exit Strategy

Por que isso importa: aplicação pode depender de um provedor, SDK, serviço de IA,
auth, storage, pacote ou API que seja comprometido, descontinuado,
bloqueado ou passe a apresentar risco inaceitável.

Para dependências críticas, confira: - inventário e owner; -
versão; - canal de advisories; - possibilidade de desabilitar; -
credenciais revogáveis; - exportação/recuperação de dados; - fallback
seguro quando necessário; - plano de atualização/substituição; -
comportamento quando o provedor falha.

Como tratar: não é necessário duplicar toda infraestrutura; é necessário
saber como conter e recuperar uma dependência crítica.

Quando considerar atendido: dependências críticas possuem caminho de
atualização, revogação ou desativação e sua falha não força o sistema a
operar de maneira insegura.

# 99 — Regra-mestra de evidência

## Nenhum item recebe ✅ apenas porque "o código parece protegido".

Esta regra governa os 98 controles anteriores.

Para declarar ✅ VALIDADO COM EVIDÊNCIA, registrar, conforme
aplicável:

1.  O que foi verificado.
2.  Onde: módulo, ambiente, arquivo, linha, migration, policy,
    função ou configuração.
3.  Fluxo dos dados: origem → validação/autorização →
    persistência/ação → saída.
4.  Condição de exploração ou cenário de abuso.
5.  Impacto potencial.
6.  Teste negativo: comportamento indevido/ataque deve ser
    rejeitado.
7.  Resultado real do teste negativo.
8.  Teste positivo: comportamento legítimo deve funcionar.
9.  Resultado real do teste positivo.
10. Correção aplicada, quando houver.
11. Reteste após correção.
12. Teste de regressão, quando aplicável.
13. Risco residual.
14. Dependências externas/infra não verificadas.
15. Data/evidência da validação.

### Proibições da Regra 99

Não aceitar como prova isolada:

-   "Existe uma policy."
-   "RLS está habilitada."
-   "Tem validação no formulário."
-   "Tem CAPTCHA na tela."
-   "Usamos UUID."
-   "Tem CORS."
-   "Tem CSP."
-   "Usamos Supabase."
-   "A função verifica JWT."
-   "A IA analisou e disse que está seguro."
-   "Procurei a string e não encontrei."
-   "O botão não aparece para esse usuário."
-   "A rota tem nome difícil."
-   "O `.env` não está no Git atual."
-   "O teste não deu erro."

A pergunta final é sempre:

> Qual evidência comprova que o ataque/uso indevido foi negado e que o
> uso legítimo continua funcionando?

# Fluxo adaptativo de auditoria

Antes de testar, o agente deve:

1.  Identificar a arquitetura e atribuir as tags aplicáveis.
2.  Marcar controles claramente não aplicáveis como `➖ N/A`, sempre com
    justificativa.
3.  Contar quantos dos 99 controles são realmente aplicáveis.
4.  Ordenar primeiro os controles P0, depois P1, depois
    P2/INFRA.
5.  Dentro da mesma prioridade, começar pelas fronteiras de maior
    impacto: autenticação, autorização, dados sensíveis, administração,
    pagamentos/ações irreversíveis, secrets e exposição pública.
6.  Não usar o número de itens verdes como substituto para análise de
    risco.

Exemplo de saída inicial:

``` text
Controles totais: 99
Aplicáveis: 61
N/A justificados: 38

P0 aplicáveis: 27
P1 aplicáveis: 22
P2/INFRA aplicáveis: 12

Primeiro bloco de auditoria:
01, 02, 03, 05, 06, 09, 10, 11...
```

Os números acima são apenas um exemplo de formato, não uma meta. Isso
evita tratar um site institucional simples como se tivesse a mesma
superfície de um SaaS financeiro multi-tenant com aplicativo mobile e
agentes de IA.

# Checklist de preparação do projeto

Antes dos 99 controles, documente:

-   Stack: frontend, backend, banco, mobile, serverless, storage,
    IA.
-   Ambientes: local, staging, produção.
-   Autenticação: provedor e fluxo.
-   Perfis: usuário, gestor, admin etc.
-   Tenancy: single-tenant ou multi-tenant.
-   Dados sensíveis: PII, documentos, localização, pagamentos, saúde
    etc.
-   Integrações externas: APIs, webhooks, e-mail, mensageria, IA.
-   Artefatos distribuídos: web bundle, APK/AAB/IPA, desktop.
-   Fronteiras de confiança: cliente → API → banco → storage →
    terceiros.
-   Ambiente autorizado para testes: registrar explicitamente.

# Prompt mestre para entregar ao agente/IA

Copie o texto abaixo junto com este arquivo:

``` text
Atue como revisor de segurança deste projeto.

Leia integralmente o baseline/SECURITY_BASELINE.md antes de propor qualquer alteração.

REGRAS:
1. Comece em modo AUDITORIA. Não altere arquivos, banco, infraestrutura ou produção até eu autorizar.
2. Identifique stack, versões, pontos de entrada, autenticação, perfis, tenants e fronteiras de confiança.
3. Primeiro classifique a arquitetura pelas tags [CORE], [WEB], [API], [MOBILE], [SAAS], [AI], [FILES], [REALTIME], [OAUTH] e [INFRA]. Depois avalie os 99 controles. Se um controle não se aplicar, marque N/A e justifique tecnicamente; não o remova.
4. Nunca marque um item como ✅ apenas porque encontrou uma função, policy, middleware, RLS, CAPTCHA, CORS, CSP ou configuração que parece correta.
5. Para cada achado, informe evidência concreta: arquivo/linha ou configuração, fluxo de dados, condição necessária e impacto.
6. Diferencie: vulnerável, suspeito, não verificado, validado com evidência e não aplicável.
7. Faça somente testes locais/staging/autorizados. Não faça carga em produção, DDoS, varredura de terceiros ou acesso a dados que não pertençam ao ambiente de teste.
8. Não imprima segredos. Mascare qualquer credencial encontrada.
9. Para correções, proponha a menor mudança segura possível antes de editar.
10. Depois da correção, execute teste negativo, teste positivo e regressão.
11. Ausência em busca textual não é prova de segurança.
12. Se algo depender de infraestrutura à qual você não tem acesso, mantenha como NÃO VERIFICADO/INFRA e diga exatamente o que um humano precisa conferir.

FORMATO:
Entregue uma matriz com:
ITEM | PRIORIDADE | STATUS | EVIDÊNCIA | RISCO | CORREÇÃO | TESTE NEGATIVO | TESTE POSITIVO | RETESTE | RISCO RESIDUAL

Comece pelo inventário da arquitetura, informe quantos dos 99 controles são aplicáveis e depois inicie pelos P0 aplicáveis.
```

# Modelo de registro por item

``` text
ITEM:
TÍTULO:
PRIORIDADE:
STATUS: ❌ / ⚠️ / ❓ / ✅ / ➖ N/A

STACK/MÓDULO:
AMBIENTE:

ESCOPO VERIFICADO:

EVIDÊNCIA:
- Arquivo/linha:
- Migration/policy/configuração:
- Comando/teste executado:
- Resultado observado:

FLUXO DOS DADOS:

CONDIÇÃO DE EXPLORAÇÃO:

IMPACTO:

TESTE NEGATIVO:
Esperado:
Observado:

TESTE POSITIVO:
Esperado:
Observado:

CORREÇÃO:
(nenhuma / descrição)

RETESTE:

REGRESSÃO:

DEPENDÊNCIA EXTERNA / INFRA:

RISCO RESIDUAL:

JUSTIFICATIVA N/A:
(se aplicável)

DATA:

CONCLUSÃO:
```

# Quando considerar o trabalho concluído

Um controle não está concluído porque foi "implementado".

Ele está concluído quando: - o escopo aplicável foi identificado; - o
estado real foi inspecionado; - a barreira de segurança foi
localizada; - o cenário indevido foi testado; - o cenário legítimo foi
testado; - a evidência foi registrada; - falhas foram corrigidas e
retestadas; - regressão foi considerada; - dependências não verificadas
ficaram explícitas; - risco residual foi documentado.

A meta não é fabricar 99/99 verdes. A meta é saber, com honestidade
técnica, o que está validado, vulnerável, pendente ou realmente não se
aplica.

# Notas de adaptação por stack

Supabase/PostgreSQL: dê atenção especial aos itens de RLS, policies,
`SECURITY DEFINER`, `service_role`, Edge Functions e Storage.

Firebase/Firestore: traduza os controles de RLS/policies para
Security Rules, custom claims, Cloud Functions e Storage Rules.

Node/Nest/Express/Django/Laravel/Rails/.NET/Spring: aplique os
mesmos princípios de autorização por objeto/tenant, validação
server-side, queries parametrizadas, middleware/guards e segredo somente
no backend.

Mobile: APK/AAB é aplicável a Android; para iOS, faça a verificação
equivalente no artefato distribuído. O cliente nunca é fronteira
confiável.

Single-tenant: testes cross-tenant podem ser N/A, mas IDOR entre
usuários/recursos e autorização por objeto continuam aplicáveis.

Sem IA/LLM: o item 58 pode ser N/A com justificativa. Se o sistema
começar a consumir conteúdo por IA ou expuser tools/agentes, reabra o
item.

Sem upload/storage: itens específicos de upload/object storage podem
ser N/A; documente.

Aplicação somente backend: XSS pode mudar de aplicabilidade, mas
qualquer saída HTML/web consumida por clientes precisa ser analisada.

# Revisão v1.3 — cobertura, IA, infra e resiliência

A v1.1 foi cruzada com referências OWASP; a v1.2 tornou explícitas
superfícies específicas de aplicação; e a v1.3 amplia a cobertura
prática para IA/agentes, RAG, runtime/cloud, backups, cache, contenção
de incidentes e dependências críticas.

## OWASP ASVS 5.0.0

O ASVS é uma base de requisitos verificáveis para controles técnicos de
segurança de aplicações. A revisão levou à expansão principalmente de: -
design/threat modeling; - criptografia e chaves; -
autenticação/sessão; - configuração; - integridade; - tratamento seguro
de falhas.

Referência oficial: https://owasp.org/projects/asvs

## OWASP Top 10:2025

Categorias consideradas: - A01 Broken Access Control; - A02 Security
Misconfiguration; - A03 Software Supply Chain Failures; - A04
Cryptographic Failures; - A05 Injection; - A06 Insecure Design; - A07
Authentication Failures; - A08 Software or Data Integrity Failures; -
A09 Security Logging & Alerting Failures; - A10 Mishandling of
Exceptional Conditions.

Referência oficial: https://top10.owasp.org/2025/

## OWASP API Security Top 10:2023

O baseline já cobria fortemente BOLA, autenticação, mass
assignment/property authorization, resource consumption, function-level
authorization e SSRF.

A revisão adicionou cobertura explícita para: - abuso de fluxos
sensíveis de negócio; - inventário/versionamento de APIs; - consumo
inseguro de APIs de terceiros; - webhooks/replay/idempotência.

Referência oficial:
https://api-security.owasp.org/editions/2023/en/0x11-t10/

## OWASP MASVS 2.1.0

Foram considerados os grupos: - STORAGE; - CRYPTO; - AUTH; - NETWORK; -
PLATFORM; - CODE; - RESILIENCE; - PRIVACY.

A revisão fortaleceu especialmente criptografia/chaves, ciclo de vida de
autenticação, permissões/componentes mobile, rede,
atualização/plataforma e privacidade.

Referência oficial: https://mas.owasp.org/MASVS/

## O que esta revisão NÃO significa

Este documento não afirma conformidade formal com ASVS, MASVS ou
qualquer certificação OWASP. Ele é um baseline prático inspirado e
cruzado com essas referências. Uma avaliação formal exige selecionar
requisitos/perfis aplicáveis e verificar cada requisito da norma
correspondente.

# Depois do baseline: profundidade, não contagem

A v1.3 encerra este baseline em 99 controles por decisão de design.
O objetivo não é competir em quantidade com padrões formais.

Depois de tratar os controles aplicáveis, projetos de maior risco devem
aprofundar a verificação com requisitos específicos das referências
adequadas, threat modeling detalhado, testes automatizados, revisão
independente e pentest autorizado quando proporcional ao risco.

99/99 não significa "invulnerável". Significa apenas que os 99
controles foram classificados e que todos os controles aplicáveis
marcados como `✅` possuem a evidência exigida pela Regra 99.

## Companion recomendado

Mantenha este baseline imutável durante a auditoria e registre
resultados em um arquivo separado, por exemplo:

`SECURITY_AUDIT_RESULTS.md`

Isso evita transformar o padrão em um relatório específico de um projeto
e facilita atualizar o baseline sem perder evidências históricas.

# AVISO

Este checklist é um baseline de engenharia, não uma garantia de ausência
de vulnerabilidades. Sistemas com dados críticos, pagamentos, saúde,
infraestrutura sensível, grande exposição pública ou alto impacto devem
considerar threat modeling, revisão independente, pentest autorizado,
monitoramento e resposta a incidentes compatíveis com o risco.

SECURITY BASELINE PARA VIBE CODING v1.3 — 99 CONTROLES

Regra final: segurança não é presumida; é demonstrada.

## Endurecimento v1.0.0-rc2 — browser, cookies, proxy e HTTP

Este endurecimento não cria novos controles. Ele torna explícitos critérios que devem ser avaliados dentro dos controles existentes conforme o Threat Model.

### Controle 64 — sessão, tokens, cookies e CSRF

Quando autenticação/sessão depender de cookies no navegador, verificar também:

- `Secure` e `HttpOnly` nos cookies de sessão quando aplicável;
- `SameSite=Strict` ou `Lax` escolhido conscientemente; `SameSite=None` somente com `Secure`;
- escopo mínimo de `Domain`/`Path`, preferindo prefixo `__Host-` quando compatível;
- nenhuma operação que altere estado por `GET` ou outro método considerado seguro;
- proteção CSRF apropriada ao desenho (token anti-CSRF, double-submit robusto, verificação de `Origin`/`Referer` e/ou Fetch Metadata como defesa adicional);
- subdomínios não devem ser presumidos confiáveis sem Threat Model.

Teste negativo: requisição cross-site ou sem prova anti-CSRF válida não altera estado.
Teste positivo: requisição legítima com sessão e proteção válidas continua funcionando.

### Controles 05, 37, 51, 66 e 68 — proxy, Host e parsing HTTP

Quando houver reverse proxy, CDN, load balancer, API gateway ou múltiplos parsers HTTP, verificar também:

- `Host`/`:authority` não controla redirects, links sensíveis, reset de senha ou seleção de tenant sem allowlist/normalização;
- `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto` e headers de identidade só são confiados quando inseridos por proxies explicitamente confiáveis;
- métodos HTTP desnecessários são desabilitados/rejeitados;
- divergências de parsing entre camadas (incluindo request smuggling/desync) são consideradas e testadas de forma segura quando aplicável;
- limites de tamanho, timeout e normalização são coerentes entre borda e aplicação.

Teste negativo: headers forjados diretamente pelo cliente não mudam identidade, origem confiável, tenant ou destino sensível.
Teste positivo: tráfego legítimo através do proxy confiável preserva IP/protocolo/host necessários.
