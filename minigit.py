"""Implementação didática de um histórico Git em memória."""

from collections import deque


class MiniGit:
    """Armazena commits, branches e relações de ancestralidade em memória.

    ``medir()`` e ``passos`` expõem o contador da última operação. A contagem
    representa visitas a registros/arestas relevantes, não tempo de execução.
    """

    __slots__ = ("__pais", "__mensagens", "__branches", "__branch_atual", "__contador", "__passos")

    def __init__(self):
        self.__pais = {}
        self.__mensagens = {}
        self.__branches = {"main": None}
        self.__branch_atual = "main"
        self.__contador = 0
        self.__passos = 0

    def _novo_commit(self, mensagem, pais):
        self.__contador += 1
        commit = f"c{self.__contador}"
        self.__mensagens[commit] = mensagem
        self.__pais[commit] = tuple(pais)
        return commit

    def _validar_commit(self, commit):
        if commit not in self.__mensagens:
            raise ValueError(f"Commit {commit!r} não encontrado.")

    def commitar(self, mensagem):
        if not isinstance(mensagem, str) or not mensagem.strip():
            raise ValueError("Mensagem de commit não pode ser vazia.")
        pai = self.__branches[self.__branch_atual]
        commit = self._novo_commit(mensagem, () if pai is None else (pai,))
        self.__branches[self.__branch_atual] = commit
        self.__passos = 2
        return commit

    def mensagem(self, commit):
        self._validar_commit(commit)
        self.__passos = 1
        return self.__mensagens[commit]

    def pais(self, commit):
        self._validar_commit(commit)
        self.__passos = 1
        return self.__pais[commit]

    @property
    def passos(self):
        """Número de passos registrados pela última operação."""
        return self.__passos

    def medir(self):
        """Retorna o número de passos registrados pela última operação."""
        return self.__passos

    def criar_branch(self, nome):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome da branch não pode ser vazio.")
        if nome in self.__branches:
            raise ValueError("Essa branch já existe.")
        cabeca = self.__branches[self.__branch_atual]
        if cabeca is None:
            raise ValueError("Não existem commits para criar uma branch.")
        self.__branches[nome] = cabeca
        self.__passos = 1

    def trocar_branch(self, nome):
        if nome not in self.__branches:
            raise ValueError("Essa branch não existe.")
        self.__branch_atual = nome
        self.__passos = 1

    def mesclar(self, nome):
        if nome not in self.__branches:
            raise ValueError("Essa branch não existe.")
        if nome == self.__branch_atual:
            raise ValueError("Não é possível mesclar a própria branch.")
        atual = self.__branches[self.__branch_atual]
        outro = self.__branches[nome]
        if atual is None or outro is None:
            raise ValueError("As duas branches precisam ter commits para mesclar.")
        commit = self._novo_commit(f"merge de {nome}", (atual, outro))
        self.__branches[self.__branch_atual] = commit
        self.__passos = 3
        return commit

    def log(self):
        """Retorna commits alcançáveis da branch atual, em busca por largura."""
        inicio = self.__branches[self.__branch_atual]
        if inicio is None:
            self.__passos = 0
            return ()
        fila = deque([inicio])
        visitados = set()
        resultado = []
        while fila:
            commit = fila.popleft()
            if commit in visitados:
                continue
            visitados.add(commit)
            resultado.append(commit)
            fila.extend(self.__pais[commit])
        self.__passos = len(resultado)
        return tuple(resultado)

    @property
    def branch_atual(self):
        return self.__branch_atual

    def buscar(self, texto):
        if not isinstance(texto, str):
            raise TypeError("O texto de busca deve ser uma string.")
        passos = 0
        for commit, mensagem in self.__mensagens.items():
            passos += 1
            if texto in mensagem:
                self.__passos = passos
                return commit
        self.__passos = passos
        return None

    def merges(self):
        """Retorna commits com mais de um pai, em ordem de criação."""
        resultado = []
        for commit, pais in self.__pais.items():
            if len(pais) > 1:
                resultado.append(commit)
        self.__passos = len(self.__pais)
        return tuple(resultado)
