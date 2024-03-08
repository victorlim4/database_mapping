# Ferramenta de Mapeamento de Banco de Dados

Uma ferramenta projetada para extrair a estrutura de um banco de dados e convertê-la em um arquivo JSON ou em um arquivo de interfaces TypeScript.

## Dependências

Lista de libs que utilizei:

As seguintes bibliotecas fazem parte da biblioteca padrão do Python e não precisam ser instaladas separadamente:

- `json`: Para trabalhar com formato JSON.
- `argparse`: Adicionar comandos e argumentos.
- `re`: 'Útil para validação de entrada e manipulação de strings - Regex.
- `getpass`: Segurança das senhas.
- `colorama`: Melhorar aparência da ferramenta.

Para instalar a biblioteca externa `colorama`, você pode usar o seguinte comando:

```bash
pip install colorama
```

### Suporte de Banco de Dados

Este projeto suporta conexão com bancos de dados MySQL e PostgreSQL. Para trabalhar com esses bancos de dados, você precisará instalar as bibliotecas de conexão apropriadas:

- Para MySQL:

```bash
pip install mysql.connector
```

- Para PostgreSQL:

```bash
pip install psycopg2
```

## Instruções de Instalação

1. **Faça um Fork do Repositório**: Primeiro, faça um fork deste repositório.

2. **Clonar o Repositório**: Em seguida, clone este repositório para o seu ambiente de desenvolvimento local.

3. **Instalar Dependências**: Execute o comando `pip install <biblioteca>` para instalar a dependência

4. **Executar a Ferramenta**: Execute a ferramenta usando o comando `python main.py` seguido das opções e argumentos apropriados.

## Uso

A Ferramenta aceita argumentos de linha de comando para personalizar a extração e o processamento dos dados do banco de dados. Aqui estão os argumentos disponíveis:

#### `--exclude`

Este argumento permite especificar os campos que você deseja excluir do resultado final. Você pode fornecer múltiplos campos para excluir, separados por espaços.

**Sintaxe:**

```
--exclude <campo1> <campo2> ...
```

**Exemplo:**

```
--exclude id name created_at
```

#### `--db`

Este argumento é obrigatório e especifica o tipo de banco de dados (MySQL, PostgreSQL, etc.) com o qual você deseja trabalhar.

**Sintaxe:**

```
--db <tipo_do_banco_de_dados>
```

**Exemplo:**

```
--db mysql
```

```
--db postgres
```

#### `--type`

Este argumento é obrigatório e especifica o tipo de retorno desejado. Os valores possíveis são `json` para salvar a estrutura do banco de dados em um arquivo JSON, `interface` para gerar um arquivo de interfaces e tipos TypeScript, ou `block` para gerar um bloco sem formatação.

**Sintaxe:**

```
--type <tipo_de_retorno>
```

**Valores Possíveis:**

- `json`: Salva a estrutura do banco de dados em um arquivo JSON.
- `interface`: Gera um arquivo de interfaces e tipos TypeScript.
- `block`: Gera um bloco de propriedades e tabelas.

**Exemplo:**

```
--type interface
```

### Uso

Para usar a ferramenta com os argumentos especificados, você pode executar um comando como este:

```bash
python3 main.py --db postgres --type interface --exclude id name created_at
```

Este comando instrui a ferramenta a se conectar a um banco de dados PostgreSQL, gerar um arquivo de interfaces e tipos TypeScript, e excluir os campos `id`, `name`, e `created_at` do resultado final.

## Contribuição

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

**Observação: ( vou melhorar o código conforme o tempo, a ferramenta foi criada para uso próprio, mas resolvi adicionar aqui. Fique a vontade para contribuir😁 )**

## Licença

Esta ferramenta é distribuída sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
