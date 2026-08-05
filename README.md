# TP Integrador: Agente Racional para el Mundo del Wumpus

Trabajo Práctico Integrador para la cátedra de Inteligencia Artificial (5° Año - UTN FRSR).

Implementación de un agente autónomo para el entorno del Mundo del Wumpus (tablero de 4x4) utilizando arquitectura de sistemas expertos. El agente toma decisiones mediante un motor de inferencia por encadenamiento hacia adelante a partir de percepciones acumuladas en una base de conocimientos.

## Estructura del repositorio

* `tablero.py`: Simulación del entorno y cálculo de percepciones en cada casilla.
* `agente.py`: Definición del estado del agente (posición, inventario) y ejecución de acciones.
* `base_conocimiento.py`: Almacenamiento de percepciones, casillas visitadas y estados deducidos (seguras/peligrosas).
* `reglas.py`: Conjunto de reglas de producción condicionales (SI... ENTONCES...).
* `motor_inferencia.py`: Motor de encadenamiento hacia adelante para deducción de nuevos hechos.
* `main.py`: Loop principal de simulación e impresión de la traza de razonamiento.
* `visualizacion.py`: Módulo para la representación gráfica o ASCII del tablero.

## Ejecución

```bash
python main.py

## 👥 Organización del Equipo y División de Trabajo

| Integrante | Módulos a cargo | Responsabilidades principales |
| :--- | :--- | :--- |
| **Belén Saromé** | `tablero.py`<br>`agente.py` | Modelado del mundo real y control del estado físico del agente. |
| **Guadalupe Cuártara** | `reglas.py` | Traducción del razonamiento lógico del Wumpus a reglas de producción SI-ENTONCES. |
| **Julieta Chaki** | `base_conocimiento.py`<br>`motor_inferencia.py` | Implementación de la base de hechos y motor de encadenamiento hacia adelante (*Forward Chaining*). |
| **Dana Guzmán** | `main.py`<br>`visualizacion.py` | Orquestación del ciclo principal, política de decisión, traza de consola y visualización. |