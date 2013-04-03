CDN Dinámico de imágenes para Google App Engine
===============================================

Proyecto con el que se almacenan imágenes en App Engine como datos Blob, se categorizan y se obtiene un url de acceso público a ella. 
Se utiliza el servicio de Memcache para almacenar en caché todas las imágenes, para el ahorro de las cuotas de acceso y lectura del almacen de datos.

Básicamente se consulta la imagen en la memoria caché, si ésta no está disponible la consulta en el almacen de datos, y la agrega a la memcache. Cuando se llega al limite de la memoria, ésta elimina los valores más viejos y menos solicitados, ó las borra por expiración.

Mas información:

    + Twitter: @c_samiro
    + GitHub: @samiro