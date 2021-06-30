# Proyecto Final AWS - M&T Bank
<p align="center">
  <img title="AWS" src="https://raw.githubusercontent.com/Thomas-George-T/Thomas-George-T/master/assets/aws.svg" width="60" height="40" />
</p>   

Miembros:

- _Alejandra Gabriela Chirinos Valle - 51132._

- _Fabian Andre Machicao Mercado - 51176._

- _Mikaela Maria Cardenas Rodriguez - 51108._

- _Miguel Ricardo Tejerina Flores - 51239._

## Pre - requisitos
Cosas que necesitas para poder ejecutar el código:
```
Necesitas una cuenta en Amazon Web Services.
```
```
Un ambiente en Cloud9 con un ssh key para GitHub
```
```
La aplicación "Insomnia" (Solo si quiere hacer pruebas)
```

## Pasos a seguir
Sigue esta serie de pasos para poder tener el código correctamente ejecutados:

1. En la consola ejecuta el comando "git clone git@github.com:AndreM22/ProyectoFinalAWS.git".
2. Dentro del archivo template.yaml necesitas cambiar el nombre del bucker (línea 10), el nombre debe ser único.
3. Dentro del archivo deployment.sh necesitas cambiar el nombre del bucker (línea 3), el nombre debe ser único.
4. En la consola ejecuta el comando "./deployment.sh -b".
5. En la consola ejecuta el comando "./deployment.sh -p".
6. En la consola ejecuta el comando "./deployment.sh -d".
7. En la consola ejecuta el comando "./deployment.sh -c".

## Pruebas
Sigue los pasos para poder hacer las puebas necesarias:

1. Entra a CloudFormation. 
2. Ve a la parte de Stacks y entra al último.
3. Ingresa a la pestaña de "Resources".
4. Ve hacia abajo en la columna de LogicalID hasta encontrar "MyAPI" e ingresa al link.
5. Entra a "Stages".
6. Entra a "prod".
7. Copia el link de "Invoke URL"
8. Copia el link anterior en la aplicación "Insomnia".

### Pruebas - Cuentas 

Una vez copiado el link en Insomnia, copiar "/account/account_01" (el "01" depende de la cuenta buscada).

Si quieres hacer un GET, no necesitas un body.

Si quieres hacer un PUT, copia:

>
{
   
    "name":"Hugoberto",
    
    "company_name": "INDUSTRIAS DE ACEITE SA FINO",
    
    "company_nit": 4581236,
    
    "company_type": "Harina de soya y otros",
    
    "money_amount":10000,
    
    "monthly_salary":2000,
    
    "daily_transactions":0
   
  }

### Pruebas - Transacciones 

Una vez copiado el link en Insomnia, copiar "/transaction/transaction_01" (el "01" depende de la transacción buscada).

Si quieres hacer un GET, no necesitas un body.

Si quieres hacer un PUT, copia:
>
{

    "sender": "account_01",
    
    "receiver": "account_02",
    
    "ammount": 400
    
}

## Diagrama

<img src="https://imgur.com/CrsbVk7">


