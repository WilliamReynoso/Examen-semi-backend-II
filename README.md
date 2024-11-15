# Dockerproxy-Endpoints

## Nuevos endpoints
### /usuarios
### /usuarios/torre
El api es la misma del docker nginx que ya cuenta con flask, donde se agregaron nuevos endpoints y con la ayuda de la libreria psycopg2 se realiza la conexion a la base de datos del contenedor de postgres.
![imagen](https://github.com/user-attachments/assets/529f14fb-6148-42de-93dc-83a4f0265029)


Al acceder al endpoint /usuarios regresa la informacion de una base de datos con informacion falsa almacenada en el docker de postgresql.
![imagen](https://github.com/user-attachments/assets/d2e79f4e-8876-4818-bde1-9cd65bf97a7a)


En este ejemplo el endpoint /usuarios/torre regresa los usuarios que cuentan con una torre o computadora de escritorio separandolos de los usuarios moviles.

![imagen](https://github.com/user-attachments/assets/f5a6aba6-7d78-402e-887e-f80b0ae5a245)


Podemos verificar la informacion recibida de los endpoints desde el navegador.
![imagen](https://github.com/user-attachments/assets/061ad37c-b00c-41a5-a08a-44254513168c)

![imagen](https://github.com/user-attachments/assets/a0ef3a56-f90b-4f0e-b8d7-97b49121b020)


Y tambien validamos con POSTMAN para mostrar que funciona.
/usuarios regresa los 20 usuarios de la base de datos falsa
![imagen](https://github.com/user-attachments/assets/71119bba-90cc-4118-b07c-ca6f28899ae9)


/usuarios/torre solo regresa los usuarios que cuenten con computadora de escritorio o torre.
![imagen](https://github.com/user-attachments/assets/ab0c2b28-6513-4424-8ac9-f11fbc14d2cf)

