"""
Exceções customizadas do sistema de controle de estoque.

Usar exceções específicas (em vez de Exception genérica) deixa o
código mais claro e permite tratar cada erro de forma adequada na
camada de interface (CLI).
"""


class EstoqueError(Exception):
    """Classe base para todas as exceções do domínio de estoque."""
    pass


class ProdutoNaoEncontradoError(EstoqueError):
    """Lançada quando se tenta operar sobre um produto que não existe."""
    def __init__(self, codigo: str):
        super().__init__(f"Produto com código '{codigo}' não encontrado.")
        self.codigo = codigo


class ProdutoJaExisteError(EstoqueError):
    """Lançada ao tentar cadastrar um produto com código já usado."""
    def __init__(self, codigo: str):
        super().__init__(f"Já existe um produto cadastrado com o código '{codigo}'.")
        self.codigo = codigo


class QuantidadeInvalidaError(EstoqueError):
    """Lançada quando uma quantidade informada é inválida (<= 0)."""
    def __init__(self, quantidade):
        super().__init__(f"Quantidade inválida: {quantidade}. Deve ser um número positivo.")


class PrecoInvalidoError(EstoqueError):
    """Lançada quando um preço informado é inválido (< 0)."""
    def __init__(self, preco):
        super().__init__(f"Preço inválido: {preco}. Deve ser maior ou igual a zero.")


class EstoqueInsuficienteError(EstoqueError):
    """Lançada quando uma saída de estoque excede a quantidade disponível."""
    def __init__(self, codigo: str, disponivel: int, solicitado: int):
        super().__init__(
            f"Estoque insuficiente para o produto '{codigo}': "
            f"disponível={disponivel}, solicitado={solicitado}."
        )
        self.codigo = codigo
        self.disponivel = disponivel
        self.solicitado = solicitado


class FornecedorNaoEncontradoError(EstoqueError):
    """Lançada quando se tenta operar sobre um fornecedor que não existe."""
    def __init__(self, codigo: str):
        super().__init__(f"Fornecedor com código '{codigo}' não encontrado.")
        self.codigo = codigo