# Threat Model — template v1.0

Arquivo de referência: `baseline/SECURITY_BASELINE.md`\
Este template existe para entender o sistema antes de aplicar os 99 controles.

## 1. Descreva o sistema em uma frase

O que o sistema faz, para quem e qual ação/dado mais importante ele
controla?

## 2. O que precisa ser protegido

  Ativo   Sensibilidade/impacto   Onde vive   Quem deveria acessar
  ------- ----------------------- ----------- ----------------------


Considere: credenciais, dados pessoais, dados empresariais, dinheiro,
documentos, localização, mídia, permissões administrativas, chaves,
código, modelos/RAG e disponibilidade.

## 3. Quem interage com o sistema

  Ator                  Legítimo?   Privilégios   O que NÃO pode fazer
  --------------------- ----------- ------------- ----------------------
  Usuário anônimo
  Usuário autenticado
  Administrador
  Serviço/worker
  Terceiro/integrador
  Agente de IA
  Atacante externo      não         nenhum

Adicione papéis específicos do projeto.

## 4. Onde a confiança muda

Liste cada ponto em que dados ou autoridade atravessam uma fronteira:

1.  Browser/app → API
2.  API → banco
3.  API → storage
4.  Serviço → serviço
5.  Aplicação → provedor externo
6.  Usuário → upload
7.  Aplicação → modelo de IA
8.  IA → tool/ação
9.  CI/CD → produção
10. Outros:

Para cada fronteira, registre autenticação, autorização, validação,
criptografia e logging existentes.

## 5. Fluxos que merecem mais atenção

### Fluxo A — nome

-   Entrada:
-   Identidade:
-   Autorização:
-   Dados acessados:
-   Ações irreversíveis:
-   Dependências:
-   Saída:
-   Falha segura esperada:

Repita para login, administração, pagamento, upload/download, exclusão,
mudança de privilégio, RAG/tools e demais fluxos críticos.

## 6. Como o sistema pode ser abusado

Pergunte explicitamente:

-   E se o usuário alterar IDs?
-   E se trocar tenant/empresa?
-   E se enviar campos extras?
-   E se repetir/reordenar a requisição?
-   E se automatizar milhares de chamadas?
-   E se o arquivo mentir sobre seu tipo?
-   E se uma URL apontar para rede interna?
-   E se um token for roubado/reutilizado?
-   E se um administrador abusar do próprio acesso?
-   E se um terceiro/provedor falhar ou for comprometido?
-   E se uma instrução maliciosa chegar via documento/RAG?
-   E se a IA tentar chamar uma tool não autorizada?
-   E se cache, fila, worker ou realtime misturar usuários/tenants?
-   E se a produção precisar ser contida imediatamente?

## 7. Piores impactos plausíveis

Classifique sem sensacionalismo:

  -----------------------------------------------------------------------------------------------------
  Cenário     Confidencialidade   Integridade   Disponibilidade   Privacidade/financeiro   Prioridade
  ----------- ------------------- ------------- ----------------- ------------------------ ------------

  -----------------------------------------------------------------------------------------------------

## 8. O que ainda precisa ser provado

Não trate suposição como fato.

  Hipótese                    Como validar      Evidência esperada   Resultado
  --------------------------- ----------------- -------------------- -----------
  "RLS impede cross-tenant"   teste A→B e B→A   negação real


## 9. Superfícies e tags do baseline

-   [ ] CORE
-   [ ] WEB
-   [ ] API
-   [ ] MOBILE
-   [ ] SAAS
-   [ ] AI
-   [ ] FILES
-   [ ] REALTIME
-   [ ] OAUTH
-   [ ] INFRA

Controles aplicáveis estimados:\
Controles N/A estimados:\
P0 a testar primeiro:

## 10. Quando revisar este Threat Model

-   novo papel/perfil;
-   nova integração;
-   novo endpoint/serviço;
-   mudança de autenticação/autorização;
-   novo tenant/modelo de isolamento;
-   upload/download;
-   IA/RAG/tool;
-   pagamento/ação irreversível;
-   nova infraestrutura;
-   mudança relevante de fluxo de dados.

Última revisão:\
Commit/versão:\
Responsável:

Regra final: primeiro entenda o que pode dar errado; depois use o
baseline para demonstrar quais barreiras realmente funcionam.
