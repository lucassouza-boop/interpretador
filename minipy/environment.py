"""Ambiente de execução: cadeia de escopos para variáveis."""

from minipy.errors import RuntimeMiniPyError


class Environment:
    def __init__(self, parent: "Environment | None" = None):
        self.vars: dict[str, object] = {}
        self.parent = parent

    def get(self, name: str) -> object:
        env: Environment | None = self
        while env is not None:
            if name in env.vars:
                return env.vars[name]
            env = env.parent
        raise RuntimeMiniPyError(f"nome '{name}' não definido")

    def set(self, name: str, value: object) -> None:
        """Atribui no escopo atual."""
        self.vars[name] = value

    def child(self) -> "Environment":
        return Environment(parent=self)
