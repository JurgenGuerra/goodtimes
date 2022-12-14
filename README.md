# goodtimes

### Arquitectura
La plataforma es básicamente un desarrollo web dividido en 3 capas, web tier, app tier y data tier, la capa web es donde se manejan las sesiones de cada usuario en esta primera capa se manejan aquellos procesos que no requieren muchos recursos computacionales, asimismo esta capa esta diseñada para poder escalar automáticamente ante una mayor demanda de usuarios. 
La segunda capa esta diseñada para poder manejar peticiones de manera asincrona, peticiones como la creación de NFTs, la transferencia o el envío de notificaciones a los usuarios, esta capa utiliza Lambdas en lugar de instancias debido a que esta clase de procesos no estan constantemente siendo ejecutados. La capa de datos esta compuesta por una base de datos Aurora que esta configurada con un read replica para poder aumentar su capacidad de lectura. Toda esta solución esta desplegada en 2 AZs distintos para proveer un mayor availability, la distribución de los request se hace mediante un Load Balancer. 
Para el acceso a la página web se utilizará Route53 y CloudFront junto con S3 para agilizar el consumo de archivos estáticos como imágenes o videos. Para la seguridad decidimos utilizar Secret Manager para almacenar de manera segura las credenciales de los recursos de AWS. 

![Arquitectura](https://raw.githubusercontent.com/JurgenGuerra/goodtimes/main/arquitectura.png)

### Flujo CI/CD
Adicionalmente se desplego un flujo CI/CD mediante una integración de github y AWS CodePipeline para ello se configuró un pipeline que ante cada commit que se hiciera en github este automáticamente trasladara estos cambios a las maquinas EC2 en las que se tiene el servicio web.
![Flujo_devops](https://raw.githubusercontent.com/JurgenGuerra/goodtimes/main/devops.png)
