# External Scanner Adapters — v0.3.0

Os adapters fazem a ponte entre ferramentas especializadas e o formato de evidência usado pelo framework. A ideia é aproveitar scanners maduros sem tratar a saída deles como uma resposta automática para os controles do baseline.

## Gitleaks

Execute:

``` bash
python checks/adapters/gitleaks_adapter.py --target . --json
```

O framework não instala o Gitleaks. Se o executável não estiver disponível, o resultado será `NOT_AVAILABLE`, nunca `PASS`.

Quando encontra `.git`, o adapter usa `git`. Nos demais casos, usa `dir`.

A evidência normalizada não copia `Secret`, `Match` nem `Line` do relatório.

Os status possíveis são:

`PASS`, `FAIL`, `WARN`, `ERROR`, `NOT_AVAILABLE`, `NOT_RUN`.

Um `PASS` informa somente que aquela execução do scanner não encontrou findings no escopo e na configuração utilizados. A Regra 99 continua valendo.

## Trivy

O adapter do Trivy normaliza findings de vulnerabilidades para o mesmo modelo de evidência.

``` bash
python checks/adapters/trivy_adapter.py --target . --mode fs --json
```

Para trabalhar com um SBOM já existente:

``` bash
python checks/adapters/trivy_adapter.py --target ./sbom.cdx.json --mode sbom --json
```

O framework também não instala nem atualiza o Trivy automaticamente. Se a ferramenta não estiver disponível, o resultado será `NOT_AVAILABLE`.

A evidência inclui ID da vulnerabilidade, severidade, pacote, versão instalada, versão corrigida quando disponível, target e URL primária.

Um `PASS` não prova que todas as dependências estão seguras. Cobertura de detecção, configuração e atualização da base continuam sendo limitações que precisam ser consideradas.
