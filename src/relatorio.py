"""
Geração de relatórios e gráficos a partir do estado do Estoque.

Mantida como uma classe separada (Estoque não sabe nada sobre
relatórios) para respeitar responsabilidade única: Estoque cuida das
regras de negócio, Relatorio cuida de apresentação/análise dos dados.
"""

from __future__ import annotations
import os
from src.models import Estoque, TipoMovimentacao


class Relatorio:
    def __init__(self, estoque: Estoque):
        self.estoque = estoque

    def texto_produtos_em_falta(self, minimo: int = 5) -> str:
        produtos = self.estoque.produtos_em_falta(minimo)
        if not produtos:
            return f"Nenhum produto com estoque igual ou abaixo de {minimo} unidades."
        linhas = [f"Produtos com estoque <= {minimo} unidades:"]
        linhas += [f"  - {p}" for p in produtos]
        return "\n".join(linhas)

    def texto_proximos_vencimento(self, dias: int = 7) -> str:
        produtos = self.estoque.produtos_proximos_vencimento(dias)
        if not produtos:
            return f"Nenhum produto perecível vence nos próximos {dias} dias."
        linhas = [f"Produtos perecíveis próximos do vencimento ({dias} dias):"]
        linhas += [f"  - {p}" for p in produtos]
        return "\n".join(linhas)

    def texto_valor_total(self) -> str:
        total = self.estoque.valor_total_estoque()
        return f"Valor total imobilizado em estoque: R$ {total:.2f}"

    def totais_por_produto(self) -> dict[str, dict[str, int]]:
        """Soma quantidade de entrada e saída por produto, a partir do histórico."""
        totais: dict[str, dict[str, int]] = {}
        for mov in self.estoque.movimentacoes:
            registro = totais.setdefault(mov.produto_codigo, {"entrada": 0, "saida": 0})
            if mov.tipo == TipoMovimentacao.ENTRADA:
                registro["entrada"] += mov.quantidade
            else:
                registro["saida"] += mov.quantidade
        return totais

    def gerar_grafico_estoque_atual(self, caminho_saida: str = "data/grafico_estoque.png"):
        """Gráfico de barras com a quantidade atual de cada produto."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        produtos = self.estoque.listar_produtos()
        if not produtos:
            raise ValueError("Não há produtos cadastrados para gerar o gráfico.")

        nomes = [p.nome for p in produtos]
        quantidades = [p.quantidade for p in produtos]
        cores = ["#d9534f" if p.esta_em_falta() else "#5cb85c" for p in produtos]

        plt.figure(figsize=(8, max(4, len(nomes) * 0.4)))
        plt.barh(nomes, quantidades, color=cores)
        plt.xlabel("Quantidade em estoque")
        plt.title("Quantidade atual por produto (vermelho = estoque baixo)")
        plt.tight_layout()
        os.makedirs(os.path.dirname(caminho_saida) or ".", exist_ok=True)
        plt.savefig(caminho_saida)
        plt.close()
        return caminho_saida

    def gerar_grafico_movimentacoes(self, caminho_saida: str = "data/grafico_movimentacoes.png"):
        """Gráfico de barras comparando entradas x saídas por produto."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        totais = self.totais_por_produto()
        if not totais:
            raise ValueError("Não há movimentações registradas para gerar o gráfico.")

        codigos = list(totais.keys())
        entradas = [totais[c]["entrada"] for c in codigos]
        saidas = [totais[c]["saida"] for c in codigos]

        x = range(len(codigos))
        largura = 0.35

        plt.figure(figsize=(8, 5))
        plt.bar([i - largura / 2 for i in x], entradas, width=largura, label="Entradas", color="#5cb85c")
        plt.bar([i + largura / 2 for i in x], saidas, width=largura, label="Saídas", color="#d9534f")
        plt.xticks(list(x), codigos, rotation=45, ha="right")
        plt.ylabel("Quantidade")
        plt.title("Entradas x Saídas por produto")
        plt.legend()
        plt.tight_layout()
        os.makedirs(os.path.dirname(caminho_saida) or ".", exist_ok=True)
        plt.savefig(caminho_saida)
        plt.close()
        return caminho_saida