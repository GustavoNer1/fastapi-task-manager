from pydantic import BaseModel, ConfigDict, EmailStr


# Classe base com os campos comuns de um usuário.
# Ela evita repetição entre os schemas de entrada e saída.
class UserBase(BaseModel):
    # Nome do usuário.
    # Precisa ser uma string.
    username: str

    # Telefone do usuário.
    # Usamos string porque telefone não deve ser tratado como número.
    # Exemplo: pode ter DDD, +55, zeros à esquerda ou máscara.
    phone: str

    # E-mail do usuário.
    # EmailStr valida se o valor tem formato de e-mail válido.
    email: EmailStr


# Schema usado para entrada de dados.
# Exemplo: criação ou atualização de usuário.
class UserIn(UserBase):
    # Senha do usuário.
    # Entra na API, mas não deve sair na resposta.
    password: str


# Schema usado para saída de dados.
# Define o que a API pode devolver para o cliente.
class UserOut(UserBase):
    # Permite que o Pydantic leia dados de objetos ORM,
    # como os objetos User retornados pelo SQLAlchemy.
    #
    # Exemplo:
    # db_user.username
    # db_user.phone
    # db_user.email
    #
    # Sem isso, o Pydantic esperaria algo mais parecido com dicionário:
    # db_user["username"]
    model_config = ConfigDict(from_attributes=True)


# Schema usado para listar vários usuários.
# A resposta da rota fica no formato:
#
# {
#     "users": [
#         {
#             "username": "gustavo",
#             "phone": "11999999999",
#             "email": "gustavo@email.com"
#         }
#     ]
# }
class UserList(BaseModel):
    # Lista de usuários no formato público UserOut.
    users: list[UserOut]


class Token(BaseModel):
    acess_token: str
    token_type: str
