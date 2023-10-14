# Desplegando la Imagen de Docker

## Carga la Imagen
Luego de obtener el archivo .tar, cárgalo en Docker con el siguiente coma
docker load -i mo_image.tar

## Configuración del Servidor Django

### Inicialización de la Base de Datos
Antes de empezar a usar el proyecto, es esencial que apliques las migraciones para configurar la base de datos:

docker run -it -p 8000:8000 mo_app:v1.0 python manage.py makemigrations

docker run -p 8000:8000 mo_app:v1.0 python manage.py migrate

### Creación de la API Key
Para generar una nueva API Key, ejecuta el siguiente comando:

docker run -it -p 8000:8000 mo_app:v1.0 python manage.py makemigrations

docker run -p 8000:8000 mo_app:v1.0 python manage.py migrate

### Creación de la API Key
Para generar una nueva API Key, ejecuta el siguiente comando:
docker run -p 8000:8000 mo_app:v1.0 python manage.py apikey_gen

### Ejecuta el Contenedor
docker run -p 8000:8000 mo_app:v1.0 python manage.py runserver 0.0.0.0:8000

## Uso de los Endpoints 
Para hacer peticiones a los endpoints, deberás incluir la API Key en las cabeceras de tus peticiones: `Authorization: Api-Key TU_API_KEY`.

### Servicios Customer

- **Url base**: http://127.0.0.1:8000/customers

  - **Crear un nuevo cliente (create_customer)** 
    - Endpoint: `/create_customer/` 
    - Método: POST
    - Cuerpo de la solicitud (JSON):
    ```json
    {
        "external_id": "550e8400-e29b-41d4-a716-446655440000",
        "score": 750.00,
        "status": 1
    }
    ```
    Uso: Para crear un nuevo cliente, debes hacer una solicitud POST al endpoint `/create_customer/` con los datos del cliente en formato JSON.

  - **Listar todos los clientes (list_customer)**
    - Endpoint: `/list_customer/`
    - Método: GET
    - Uso: Para obtener una lista de todos los clientes existentes, haz una solicitud GET al endpoint `/list_customer/`.

  - **Obtener el saldo y la deuda total de un cliente (get_balance)**
    - Endpoint: `/get_balance/`
    - Método: GET
    - Parámetros de consulta: `customer`: El ID externo (UUID) del cliente para el cual deseas obtener el saldo y la deuda total.

### Servicios Loans

- **Url base**: http://127.0.0.1:8000/loans

  - **Crear un nuevo préstamo (create_loan)**
    - Endpoint: `/create_loan/`
    - Método: POST
    - Cuerpo de la solicitud (JSON):
    ```json
    {
        "customer": "da6a1e82-8a50-40fc-af52-694f33eb37fb",
        "amount": 500.0,
        "outstanding": 500.0,
        "status": 1
    }
    ```

  - **Listar todos los préstamos (list_loans)**
    - Endpoint: `/list_loans/`
    - Método: GET

  - **Obtener detalles de un préstamo por ID externo (loan_by_id)**
    - Endpoint: `/loan_by_id/`
    - Método: GET
    - Parámetros de consulta: `external_id`: El ID externo (UUID) del préstamo que deseas consultar.

  - **Listar préstamos por cliente (customer_loans)**
    - Endpoint: `/customer_loans/`
    - Método: GET
    - Parámetros de consulta: `customer`: El ID externo (UUID) del cliente cuyos préstamos deseas listar.

### Servicios Payments

- **Url base**: http://127.0.0.1:8000/payments

  - **Registrar Pago (register_payment)**
    - URL: `/register_payment/`
    - Método: POST
    - Descripción: Permite registrar un nuevo pago para un cliente que tiene una deuda.
    - Cuerpo de la solicitud (JSON):
    ```json
    {
        "customer": "da6a1e82-8a50-40fc-af52-694f33eb37fb",
        "amount": 10.00,
        "status": 1,
        "payment_details": [
            {
                "loan_id": "78713851-6a3b-4cf8-a16b-2670ca53db24",
                "payment_amount": 5.00
            }
        ]
    }
    ```

