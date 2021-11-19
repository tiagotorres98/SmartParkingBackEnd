# Smart-Parking
APS CC8Q13

## Instruções de uso
Para executar o projeto será necessário realizar previamente a instalação do **Python na versão 3.9**

### Para iniciar o ambiente virtual siga os seguintes passos: 

    1- Inicie o ambiente virtual: 
        - Inicie um terminal Powershell
        - Execute o comando: ./env/Scripts/Activate.ps1

### Para criar uma instância de banco de dados baseado no Model siga os seguintes passos: 
    
    1- Abra o arquivo **config.py** e configure a string de conexão de acordo com o BD que desejar utilizar.
        Exemplos:
            - postgresql://postgres:admin@localhost/smartparking
            - sqlite:///db_smartparking.db

    1- Inicie uma instância de migrations
        - Execute o comando: python3 run.py db init
    
    2- Execute o comando para rastrear as alterações e gerar tabela alembic
        - Execute o comando: python3 run.py db migrate
    
    3- Efetive as alterações na base de dados
        - Execute o comando: python3 run.py db upgrade
    
    *OBS*: Para toda alteração realizada no banco de dados será necessário executar o passo 2 e 3, respectivamente para efetivar as alterações.

### Para executar a aplicação siga os seguintes passos:
    1- Inicie o servidor local: 
        - Execute o comando: python3 run.py runserver
