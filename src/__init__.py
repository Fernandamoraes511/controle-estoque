"""
Pacote `models`: reexporta as classes de domínio para facilitar o import.

Em vez de escrever:
    from src.models.produto import Produto
    from src.models.estoque import Estoque

é possível escrever:
    from src.models import Produto, Estoque
"""

from src.models.produto import Produto, ProdutoPerecivel, ProdutoNaoPerecivel
from src.models.fornecedor import Fornecedor
from src.models.movimentacao import MovimentacaoEstoque, TipoMovimentacao
from src.models.estoque import Estoque

__all__ = [
    "Produto",
    "ProdutoPerecivel",
    "ProdutoNaoPerecivel",
    "Fornecedor",
    "MovimentacaoEstoque",
    "TipoMovimentacao",
    "Estoque",
]