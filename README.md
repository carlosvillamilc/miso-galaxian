# miso-galaxian
## Integrantes
- Carlos Villamil
- Crhistian Suárez
- Daniel Babativa

## Arquitectura
El desarrollo del juego `miso-galaxian` como proyecto final del curso "Introducción al desarrollo de videojuegos" fue hecho haciendo uso de la arquitectura ECS, así como de los diversos patrones (game-loop, service-locator, steering-behaviours) vistos en las ocho semanas de clase.

## Dinámicas del videojuego
El videojuego se basa en el juego clásico "Galaxian" de la Nintento Entertainment System (NES) de Nintendo, por lo cual busca emular al máximo sus características. Entre estas encontramos:

- Un menú de inicio.
- La escena del juego que presenta al jugador y a los enemigos.
- Letrero de "start" al inicio de cada nivel a jugar.
- Disparo de jugador a enemigos.
- Disparo de aleatorios de enemigos a jugador.
- Lanzamiento aleatorio de enemigos hacia el jugador.
- Contador de puntaje de acuerdo con el valor obtenido al eliminar cada enemigo, sea disparando o chocando contra él.
- Puntaje récord que será actualizado si el puntaje del juego en curso lo supera.
- Un sistema de vidas que se va descontando a medida que el jugador va siendo atacado.
- Letrero de "game over" al finalizar el contador de vidas del jugador.
- Letrero de preparación antes del cambio de nivel cuando este es superado (se eliminaron todos los enemigos).

De igual manera, se incluyen dos modos adicionales, de acuerdo con el material del curso:

1. **Modo edición:** Se activa con la tecla `Tab` y permite crear, arrastrar y borrar enemigos, para luego almacenarlos en un archivo tipo .json.

    Dando por hecho que ya está en modo edición, se explicarán cada una de las posibles acciones a realizar.

- **Crear enemigo:** Ubicar el mouse en la parte del juego donde se desea crear el enemigo, luego dar clic derecho para cambiar entre los diferentes tipos de enemigo a crear hasta encontrar el deseado para luego hacer clic izquierdo y de esta manera crear el enemigo.

- **Arrastar enemigo:** Ubicar el mouse sobre el enemigo a arrastrar y con el clic izquierdo sostenido, arrastrarlo hasta la ubicación deseada.

- **Borrar enemigo:** Ubicar el mouse sobre el enemigo a borrar y dar clic medio del mouse.

2. **Modo debug:** Se activa con la tecla `Ctrl-Izq` y tiene dos sub-modos, el modo debug de posiciones-tamaños y el modo debud de velocidades, cada uno se activa volviendo a teclar la misma tecla referenciada anteriormente.

    Como tal ambos sub-modos presentan la respectiva información a las ques hacen referencia acerca de las entidades que tienen estos componentes. Lo importante a tener en cuenta es que para ambos, los enemigos que están en su movimiento regular no fue incluida esta información ya que al ser tantos se recargaba de mucha información la pantalla.