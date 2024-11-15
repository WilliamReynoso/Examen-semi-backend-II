# Examen semi backend II
## Instrucciones:
**Cobratron**
*mysql, mariadb o postgresql
*lenguaje a su eleccion

-Crear base de datos con tablas para registrar la fecha inicial de los cobros al cliente

-Una tabla con la fecha final y las fechas de los cobros, todo dependiendo de la elecion de la frecuencia de los pagos (Semanal, Mensual, Trimestral, Semestral y Anual)

-Debera existir una funcion para aplicar los pagos

-Funcion para crear cliente y su datos de fecha inicial , final y pago en cantidad

-Reporte por usuario el cual muestra las fechas que debera pagar o son de cobro

#Que pasa si el dia de pago es Domingo????? Se pasa el dia de pago al dia siguiente
#Deberan realizar un analisis de las necesidades que ocupara solicitar extras al cliente y en el sistema

pago("pako",cuantos_pagos)
fecha inicial 12 enero del 2023 -> mensual, 12 meses
12 enero, pagado
12 febrero
....
12 de diciembre
todo del 2023
## Resultados
Se creo un docker compose con un contenedor de postgreSQL para el manejo de la base de datos y un contenedor para el backend con python usando la libreria Flask.
El proyecto cuenta con la funcionalidad descrita por las instrucciones de la siguiente manera:
### Crear cliente y sus datos de fecha inicial, final, la cantidad de pago y si esta pendiente o ya fue pagado.
Ademas de esto se generan todas las fechas de pago en base a la frecuencia de pago que el cliente eliga.
![imagen](https://github.com/user-attachments/assets/4897df20-145e-4e25-851e-d8b995460d30)

### Aplicar el pago de uno o mas fechas de pago del cliente.
En este ejemplo, pagar("Juan Perez", 3) resulta en que juan perez tendra 3 fechas de sus pagos pendientes marcados como pagados. Una vez toda la lista de fechas de pagos esten pagados entonces el pago asociado al cliente se marcara como completado y sin adeudos.
![imagen](https://github.com/user-attachments/assets/9e802619-2f70-4ab9-b122-e6a35b61dc64)


### Generar un reporte con las fechas de pago del cliente
Aqui tambien se muestra cuales de estas fechas se encuentran pagadas o pendientes.
![imagen](https://github.com/user-attachments/assets/3b8ae23c-6d8e-4f91-bbba-0ee4dc922f18)

