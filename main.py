import mysql.connector
import psycopg2
import json
import argparse
import re
import getpass
from colorama import Fore, Style, init

init(autoreset=True)

def get_database_info():
    print(Fore.CYAN + "Detalhes da conexão com o banco de dados" + Style.RESET_ALL)
    print(Fore.CYAN + "----------------------------" + Style.RESET_ALL)

    host = input(Fore.YELLOW + "Insira o endereço do seu banco de dados: (padrão: localhost)" + Style.RESET_ALL)  or "localhost"
    user = input(Fore.YELLOW + "Insira o nome de usuário: " + Style.RESET_ALL) or "root"
    password = getpass.getpass(Fore.YELLOW + "Insira a senha: " + Style.RESET_ALL)

    while not password:
        print(Fore.RED + "A senha é obrigatória!" + Style.RESET_ALL)
        password = input(Fore.YELLOW + "Insira a senha: " + Style.RESET_ALL)

    #database = input(Fore.YELLOW + "Insira o nome do banco de dados: " + Style.RESET_ALL)
#
    #while not database:
    #    print(Fore.RED + "O nome do banco de dados é obrigatório" + Style.RESET_ALL)
    #    database = input(Fore.YELLOW + "Insira o nome do banco de dados: " + Style.RESET_ALL)
    return host, user, password

def fetch_all_databases(host, user, password, db_type):
    if db_type.lower() == 'postgres':
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES;")
            databases = [row[0] for row in cursor.fetchall()]
            return databases
        
        except Exception as e:
            print(Fore.RED + f"Erro ao buscar os databases: {e}" + Style.RESET_ALL)
            return []
        finally:
            if connection:
                connection.close()
    elif db_type.lower() == 'mysql':
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            schemas = [row[0] for row in cursor.fetchall()]
            return schemas
        except Exception as e:
            print(Fore.RED + f"Erro ao buscar os databases: {e}" + Style.RESET_ALL)
            return []
        finally:
            if connection:
                connection.close()
    else:
        print(Fore.RED + "Ainda não temos suporte a: " + db_type + Style.RESET_ALL)
        return []
    
def fetch_all_tables(host, user, password, database, db_type):
    if db_type.lower() == 'postgres':
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                dbname=database
            )
            cursor = connection.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except Exception as e:
            print(Fore.RED + f"Erro ao buscar as tabelas: {e}" + Style.RESET_ALL)
            return []
        finally:
            if connection:
                connection.close()
    elif db_type.lower() == 'mysql':
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except Exception as e:
            print(Fore.RED + f"Erro ao buscar as tabelas: {e}" + Style.RESET_ALL)
            return []
        finally:
            if connection:
                connection.close()
    else:
        print(Fore.RED + "Ainda não temos suporte para este Banco de Dados." + Style.RESET_ALL)
        return []
    
def get_databases_to_include(databases):
    if len(databases) > 2:
        for i, database in enumerate(databases, start=1):
            print(f"{i}. {database}")

        while True:
            try:
                choice = int(input("Escolha o número do database que deseja mapear: "))
                if 1 <= choice <= len(databases):
                    selected_database = databases[choice - 1]
                    return selected_database
                    break
                else:
                    print(Fore.RED + "Escolha inválida. Por favor, insira um número entre 1 e " + {len(databases)} + "." + Style.RESET_ALL)
            
            except ValueError:
                print(Fore.RED + "Entrada inválida. Por favor, insira um número." + Style.RESET_ALL)
        
            else:
                print(Fore.RED + "Nenhum esquema encontrado." + Style.RESET_ALL)

    else: return databases[1]

def get_tables_to_include(tables):
    print(Fore.CYAN + "Selecione as tabelas que deseja incluir em seu mapeamento" + Style.RESET_ALL)
    print(Fore.CYAN + "------------------------" + Style.RESET_ALL)
    for i, table in enumerate(tables, start=1):
        print(Fore.YELLOW + f"{i}. {table}" + Style.RESET_ALL)
    
    while True:
        selected_tables_input = input(Fore.YELLOW + "Insira o numero das tabelas (separados por virgula) ou " + Fore.MAGENTA + "* para selecionar todas as tabelas: " + Style.RESET_ALL)
        
        if selected_tables_input.strip().lower() == "*":
            selected_tables = tables
            break

        if not selected_tables_input.strip():
            print(Fore.RED + "Selecione pelo menos uma tabela" + Style.RESET_ALL)
            continue
        
        selected_indices = [int(index) - 1 for index in selected_tables_input.split(',')]
        
        valid_indices = [index for index in selected_indices if 0 <= index < len(tables)]
        
        if not valid_indices:
            print(Fore.RED + "Tabela inválida. Insira um numero de tabela válido." + Style.RESET_ALL)
            continue
        
        selected_tables = [tables[index] for index in valid_indices]
        break
    
    return selected_tables



def connect_to_postgresql(host, user, password, database):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
        )
        return connection
    except psycopg2.Error as err:
        print("Algo deu errado: {}".format(err))
        return None

def connect_to_mysql(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as err:
        print("Algo deu errado: {}".format(err))
        return None

def connect_to_database(host, user, password, database, db_type):
    db_connection_functions = {
        'mysql': connect_to_mysql,
        'postgres': connect_to_postgresql
    }
    
    connection_function = db_connection_functions.get(db_type.lower())
    if connection_function:
        return connection_function(host, user, password, database)
    else:
        print("Ainda não temos suporte para este Banco de Dados")
        return None

def extract_base_mysql_type(mysql_type):
    match = re.match(r'(\w+)\s*\(\d+\)', mysql_type)
    if match:
        return match.group(1)
    else:
        return mysql_type
    
def postgresql_to_typescript_type(postgresql_type, db_type):
    if db_type.lower() == 'postgres':
        type_mapping = {
            'integer': 'number',
            'smallint': 'number',
            'bigint': 'number',
            'decimal': 'number',
            'numeric': 'number',
            'real': 'number',
            'double precision': 'number',
            'character varying': 'string',
            'varchar': 'string',
            'text': 'string',
            'date': 'Date',
            'timestamp': 'Date',
            'time': 'string',
            'boolean': 'boolean',
        }
    else:
        print("Este tipo de Banco de Dados não suporta conversão de tipo para Typescript")
        return 'any'
    return type_mapping.get(postgresql_type.lower(), 'any')

def mysql_to_typescript_type(mysql_type, db_type):
    base_type = extract_base_mysql_type(mysql_type)

    if db_type.lower() == 'mysql':
        type_mapping = {
            'int': 'number',
            'tinyint': 'number',
            'smallint': 'number',
            'mediumint': 'number',
            'bigint': 'number',
            'decimal': 'number',
            'float': 'number',
            'double': 'number',
            'char': 'string',
            'varchar': 'string',
            'text': 'string',
            'tinytext': 'string',
            'mediumtext': 'string',
            'longtext': 'string',
            'date': 'Date',
            'datetime': 'Date',
            'timestamp': 'Date',
            'time': 'string',
            'year': 'number',
            'binary': 'string',
            'varbinary': 'string',
            'blob': 'string',
            'tinyblob': 'string',
            'mediumblob': 'string',
            'longblob': 'string',
            'enum': 'string',
            'set': 'string',
            'boolean': 'boolean'
        }

    else:
        print("Este tipo de Banco de Dados não suporta conversão de tipo para Typescript")
        return 'any'
    
    if mysql_type.startswith('enum'):
        enum_values_str = mysql_type[5:-1]
        enum_values_list = enum_values_str.split(',')
        return [s.strip("'") for s in enum_values_list]
    
    else: return type_mapping.get(base_type.lower(), 'any')

def get_table_columns(connection, tables, exclude, prettify, db):
    mapping = {}
    cursor = connection.cursor()
    for table in tables:
        if db.lower() == 'mysql':
            cursor.execute(f"SHOW COLUMNS FROM {table}")
        elif db.lower() == 'postgres':
            cursor.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table.lower()}'")
        else:
            print("Ainda não temos suporte para este Banco de Dados")
            return {}
        
        columns = cursor.fetchall()
        
        if exclude:
            columns = [column for column in columns if column[0] not in exclude]

        if prettify:
            if db.lower() == 'mysql':
                mapping[table] = [{'property_name': column[0], 'type': mysql_to_typescript_type(column[1], db)} for column in columns]
            elif db.lower() == 'postgres':
                mapping[table] = [{'property_name': column[0], 'type': postgresql_to_typescript_type(column[1], db)} for column in columns]
        else:
            mapping[table] = [column[0] for column in columns]

    return mapping

def generate_mapping_file(mapping, filename):
    with open(filename, 'w') as file:
        json.dump(mapping, file, indent=4)
    print(Fore.GREEN + "Resultado de mapeamento concluido com sucesso: "+ filename + Style.RESET_ALL)

def generate_typescript_interfaces(database_schema, db_type):
    interfaces = []
    for table_name, columns in database_schema.items():
        interface_name = table_name.capitalize()
        properties = []
        for column in columns:
            type = column["type"]

            if isinstance(column["type"], list) and all(isinstance(item, str) for item in column["type"]):
                type = ' | '.join(f'"{value}"' for value in column["type"])

            properties.append(f'{column["property_name"]}: {type};')
        properties_str = '\n    '.join(properties)
        interface_definition = f'interface {interface_name} {{\n    {properties_str}\n}}'
        interfaces.append(interface_definition)
    return interfaces

def write_interfaces_to_file(interfaces, filename):
    with open(filename, 'w') as file:
        for interface in interfaces:
            file.write(interface + '\n\n')
    print(Fore.GREEN + "Arquivo de interfaces gerado com sucesso: "+ filename + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description='Faça um mapeamento completo de seu banco de dados')
    parser.add_argument('--exclude', nargs='+', help='Escolha os campos que deseja retirar de seu resultado')
    parser.add_argument('--db', required=True, help='Banco de Dados (MySQL, PostgreSQL, etc..)')
    parser.add_argument('--type', required=True, help='Tipo de retorno, em arquivo JSON, Arquivo de Interfaces & Tipos do Typescript para usar ou em bloco de properiedades e tabelas')
    args = parser.parse_args()

    host, user, password = get_database_info()
    databases = fetch_all_databases(host, user, password, args.db)
    selected_database = get_databases_to_include(databases)
    #print(selected_database)
    #schemas = fetch_all_schemas(host, user, password, database, args.db)
    #selected_schema = get_schemas_to_include(schemas)
    tables = fetch_all_tables(host, user, password, selected_database, args.db)
    selected_tables = get_tables_to_include(tables)
    
    if not selected_tables.count:
        print(Fore.RED + "No tables found in the database." + Style.RESET_ALL)

    connection = connect_to_database(host, user, password, selected_database, args.db)
    if connection:
        prettify = False if args.type == "block" else True
        mapping = get_table_columns(connection, selected_tables, args.exclude, prettify, args.db)

        if args.type == "json" or args.type == "block":
            generate_mapping_file(mapping, 'mapped_result.json')
            connection.close()

        elif args.type == "interface":
            interfaces = generate_typescript_interfaces(mapping, args.db)
            write_interfaces_to_file(interfaces, 'interfaces.ts')

            connection.close()

        else:
            print("Nenhum tipo de retorno escolhido")

if __name__ == "__main__":
    main()
