from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

# Cria o registrador dos modelos/tabelas do projeto.
# Ele guarda os metadados que o SQLAlchemy e o Alembic usam.
table_registry = registry()


@table_registry.mapped_as_dataclass
# Registra a classe User como uma tabela do banco
# e gera automaticamente um __init__ parecido com dataclass.
class User:
    # Nome real da tabela no banco de dados.
    __tablename__ = 'users'

    # Chave primária da tabela.
    # init=False porque o banco deve gerar esse valor automaticamente.
    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    # Nome de usuário.
    # unique=True impede nomes de usuário repetidos.
    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Telefone do usuário.
    # unique=True impede telefones repetidos.
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)

    # E-mail do usuário.
    # unique=True impede e-mails repetidos.
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Senha do usuário.
    # Em produção, o ideal é salvar hash, não texto puro.
    password: Mapped[str] = mapped_column(nullable=False)

    # Data de criação.
    # O banco preenche automaticamente com a data/hora atual.
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        nullable=False,
    )

    # Data de atualização.
    # O banco preenche na criação e o SQLAlchemy atualiza quando o
    # registro mudar.
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    todos: Mapped[list['Todo']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[TodoState] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
