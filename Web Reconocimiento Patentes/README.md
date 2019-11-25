# WebReconocimientoPatentes

<h2>Ejecución:</h2>
<ul>
	<li>Crear entorno virtual en un directorio que contenga la carpeta proyecto y activarlo</li>
	<li>En consola/terminal ubicarse en carpeta Web Reconocimiento Patentes</li>
	<li>Para instalar/verificar las librerías necesarias ejecutar (con el entorno virtual activado y ubicado en carpeta Web Reconocimiento Patentes)</li>
	<ul>
		<li>pip3 install -r requirements.txt</li>
	</ul>
	<li>Si se está usando en Ubuntu ejecutar lo siguiente, de lo contrario continuar con el paso siguiente</li>
	<ul>
		<li>sudo lsof -t -i tcp:8000 | xargs kill -9</li>
	</ul>
	<li>En consola/terminal ubicarse en carpeta proyecto (la primera)</li>
	<li>Ejecutar</li>
	<ul>
		<li>python manage.py makemigrations</li>
		<li>python manage.py migrate</li>
		<li>python manage.py runserver</li>
	</ul>
	<li>Realizar login con los siguientes datos:</li>
	<ul>
		<li>Nombre de usuario: administrador</li>
		<li>Contraseña: asd123asd123</li>
	</ul>
	<li>Si el usuario no está registrado (no ingresa al hacer login) crear uno nuevo en botón Registrar</li>
</ul>
