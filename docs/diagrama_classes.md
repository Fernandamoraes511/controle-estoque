@'
# Diagrama de Classes — Sistema de Controle de Estoque

> O diagrama abaixo está em sintaxe **Mermaid**. Ele é renderizado
> automaticamente no GitHub, no GitLab, no VS Code (com a extensão
> "Markdown Preview Mermaid Support") e em https://mermaid.live
> (basta colar o bloco de código lá para visualizar/exportar como imagem).

```mermaid
classDiagram
    class Produto {
        -float _preco
        -int _quantidade
        +str codigo
        +str nome
        +str categoria
        +preco: float
        +quantidade: int
        +adicionar_quantidade(quantidade)
        +remover_quantidade(quantidade)
        +valor_total() float
        +esta_em_falta(minimo) bool
        +info_extra() str
        +to_dict() dict
        +from_dict(dados)$ Produto
    }

    class ProdutoPerecivel {
        +date data_validade
        +dias_para_vencer() int
        +esta_vencido() bool
        +esta_proximo_vencimento(dias) bool
        +info_extra() str
    }

    class ProdutoNaoPerecivel {
        +int garantia_meses
        +info_extra() str
    }

    class Fornecedor {
        +str codigo
        +str nome
        +str contato
        +list~str~ produtos_fornecidos
        +vincular_produto(codigo_produto)
        +to_dict() dict
        +from_dict(dados)$ Fornecedor
    }

    class TipoMovimentacao {
        <<enumeration>>
        ENTRADA
        SAIDA
    }

    class MovimentacaoEstoque {
        +int id
        +str produto_codigo
        +TipoMovimentacao tipo
        +int quantidade
        +str motivo
        +str data
        +to_dict() dict
        +from_dict(dados)$ MovimentacaoEstoque
    }

    class Estoque {
        -dict~str,Produto~ produtos
        -dict~str,Fornecedor~ fornecedores
        -list~MovimentacaoEstoque~ movimentacoes
        +adicionar_produto(produto)
        +buscar_produto(codigo) Produto
        +remover_produto(codigo)
        +listar_produtos() list
        +entrada_estoque(codigo, quantidade, motivo)
        +saida_estoque(codigo, quantidade, motivo)
        +adicionar_fornecedor(fornecedor)
        +buscar_fornecedor(codigo) Fornecedor
        +valor_total_estoque() float
        +produtos_em_falta(minimo) list
        +produtos_proximos_vencimento(dias) list
        +salvar(caminho)
        +carregar(caminho)$ Estoque
    }

    class Relatorio {
        -Estoque estoque
        +texto_produtos_em_falta(minimo) str
        +texto_proximos_vencimento(dias) str
        +texto_valor_total() str
        +totais_por_produto() dict
        +gerar_grafico_estoque_atual(caminho) str
        +gerar_grafico_movimentacoes(caminho) str
    }

    class EstoqueError {
        <<exception>>
    }
    class ProdutoNaoEncontradoError
    class ProdutoJaExisteError
    class QuantidadeInvalidaError
    class PrecoInvalidoError
    class EstoqueInsuficienteError
    class FornecedorNaoEncontradoError

    Produto <|-- ProdutoPerecivel : herda
    Produto <|-- ProdutoNaoPerecivel : herda
    EstoqueError <|-- ProdutoNaoEncontradoError
    EstoqueError <|-- ProdutoJaExisteError
    EstoqueError <|-- QuantidadeInvalidaError
    EstoqueError <|-- PrecoInvalidoError
    EstoqueError <|-- EstoqueInsuficienteError
    EstoqueError <|-- FornecedorNaoEncontradoError

    Estoque "1" o-- "*" Produto : compõe
    Estoque "1" o-- "*" Fornecedor : compõe
    Estoque "1" o-- "*" MovimentacaoEstoque : compõe
    MovimentacaoEstoque --> TipoMovimentacao : usa
    Relatorio --> Estoque : consulta
```

## Como explicar este diagrama na apresentação

1. **Herança/Polimorfismo:** `Produto` é a superclasse; `ProdutoPerecivel`
   e `ProdutoNaoPerecivel` sobrescrevem `info_extra()`. Cada um mostra
   uma informação diferente (validade vs. garantia), mesmo método,
   comportamentos diferentes.
2. **Composição:** `Estoque` **é dono** de `Produto`, `Fornecedor` e
   `MovimentacaoEstoque`. Se o objeto `Estoque` deixar de existir, essas
   listas também deixam (não fazem sentido isoladas).
3. **Responsabilidade única:** `Relatorio` não altera dados, apenas lê
   o `Estoque` e produz análises/gráficos, separando "regra de negócio"
   de "apresentação de dados".
4. **Hierarquia de exceções:** todas herdam de `EstoqueError`, o que
   permite tratar qualquer erro do domínio com um único `except EstoqueError`
   na CLI, ou tratar casos específicos separadamente quando necessário.
'@ | Set-Content -Path docs\diagrama_classes.md -Encoding utf8