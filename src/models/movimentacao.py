"""Modelagem do histórico de movimentações de estoque."""

from __future__ import annotations
from enum import Enum
from datetime import datetime


class TipoMovimentacao(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MovimentacaoEstoque:
    """Registra uma entrada ou saída de um produto no estoque."""

    _proximo_id = 1

    def __init__(self, produto_codigo: str, tipo: TipoMovimentacao,
                 quantidade: int, motivo: str = "", data: str | None = None,
                 id_mov: int | None = None):
        self.id = id_mov if id_mov is not None else MovimentacaoEstoque._gerar_id()
        self.produto_codigo = produto_codigo
        self.tipo = TipoMovimentacao(tipo)
        self.quantidade = quantidade
        self.motivo = motivo
        self.data = data or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def _gerar_id(cls) -> int:
        novo_id = cls._proximo_id
        cls._proximo_id += 1
        return novo_id

    @classmethod
    def ajustar_contador(cls, maior_id_existente: int):
        """Garante que novos IDs não colidam com os já carregados do arquivo."""
        cls._proximo_id = max(cls._proximo_id, maior_id_existente + 1)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "produto_codigo": self.produto_codigo,
            "tipo": self.tipo.value,
            "quantidade": self.quantidade,
            "motivo": self.motivo,
            "data": self.data,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "MovimentacaoEstoque":
        mov = cls(
            produto_codigo=dados["produto_codigo"],
            tipo=dados["tipo"],
            quantidade=dados["quantidade"],
            motivo=dados.get("motivo", ""),
            data=dados.get("data"),
            id_mov=dados.get("id"),
        )
        cls.ajustar_contador(mov.id)
        return mov

    def __str__(self):
        return (f"#{self.id} [{self.data}] {self.tipo.value} - "
                f"{self.produto_codigo} (qtd: {self.quantidade}) - {self.motivo}")