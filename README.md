# lab2_redes
## Implementación de Fletcher y Viterbi. 
Se implementaron los algoritmos de Fletcher y Viterbi para detección y corrección de errores de bits. Además, se creó el envío de palabras por medio de bits (mediante conversión bits-ASCII) con un porcentaje de ruido; dependiendo del algoritmo (elegido por el usuario), este se envía, por medio del programa emisor (Python) al programa receptor (C), y se detecta o corrigen los errores.  


### Cómo correr el emisor: 
Dentro de la carpeta de "emisor", se debe colocar el siguiente comando:
`python main_emisor.py "MENSAJE" [FLETCHER/VITERBI] 0.01` , en donde en "MENSAJE" se coloca el mensaje que se quiera enviar, se debe seleccionar un único valor entre FLETCHER y VITERBI, y el último valor es cuántos errores habrán por cada 100 bits (o sea porcentaje de probabilidad de error).
>[!WARNING] 
>Este emisor debe de correrse solo cuando el receptor ya se esté ejecutando]  


### Cómo correr el receptor
Dentro de la carpeta de "receptor", se debe de colocar el siguiente comando: 
`make`, para compilar el código; y luego: 
`./receptor 6000`
Este código debe correrse antes que el emisor. 
>[!WARNING]
>El receptor debe correrse 100% en un ambiente de Linux. Utilizar WSL o VM.]
