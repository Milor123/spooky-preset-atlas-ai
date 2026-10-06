# Electromecánica — por qué las prohibiciones existen

Este archivo explica el **por qué** eléctrico detrás de cada prohibición. Sin esto, las reglas se
memorizan y se rompen cuando aparece un caso raro.

---

## El hecho que lo explica casi todo

> **Todas las salidas comparten masa**, referenciada a tierra por el PC a través del USB.

Con dos generadores conectados por USB, sus salidas quedan **potencialmente al mismo potencial**.
Se pueden cruzar Out1-Gen1 con Out1-Gen2 y Out2-Gen1 con Out2-Gen2.

**Por eso dos Contact sobre el mismo cuerpo hacen circular corriente entre generadores a través
de vos.** No es un detalle deNewswire, es tierra común.

### Y la tierra no siempre existe

- **Funcionar a batería no tiene conexión a tierra.**
- **Un cargador sin PE (protección) tampoco.**

Así que el consejo "tené earth connection" **es inalcanzable en un portátil**. Si el usuario
trabaja con el notebook desenchufado, esa protección no existe.

## Las salidas NO están aisladas galvánicamente

> *"Die Ausgänge sind nicht galvanisch getrennt, so können zwischen den Generatoren unerwünschte
> **Traducción:** "Las salidas no están aisladas galvánicamente, así que entre los generadores pueden circular corrientes no deseadas."
> Ströme fließen."*

**Ésta es la razón de fondo de por qué no se puede hacer galvano con estos generadores.** Cuatro
pads sobre dos generadores no es una elección de programación: es imposible con este hardware.

Sólo los generadores de laboratorio caros tienen aislamiento galvánico entre canales. Los ARB
comunes son de 50 Ω sin aislamiento.

---

## El Boost es una suma en serie

**BN y MN son las dos series de Out1 + Out2**, con los cables cruzados:

- **BN** → (Out1 + Out2) = **10 V + −10 V = 20 V**
- **MN** → (Out1 − Out2)

**High-Power es alias eléctrico de BN.**
**Colloidal Silver** — el Boost (p12) **cuadruplica la potencia de Contact**, duplica la de Remote, y tiene salida dedicada. Puertos: `OUT1, OUT2, PW_R, CONTACT 1, CONTACT 2, SILVER, BN, MN`.
La guia marca el puerto silver como **weak** (p21).

> **CORRECCIÓN:** una versión anterior de este archivo decía *"Colloidal Silver = BN + 10 kΩ
> en serie, lleva resistencia limitadora incorporada"*. **Eso es falso.** El resistor de 10 kΩ
> **no viene en el puerto**: es un componente que se agrega **a mano en el equipo casero** para
> fabricar la plata coloidal (p207). Ver `coloidal.md`.

Requiere **excitación en contrafase** en Out1 y Out2. `Follow Out` es **copia** de Out1, no
inversión — ese error cambia el resultado por completo.

**El generador nunca pasa de ±10 V por salida**, pidas lo que pidas. La "amplitud 20 V" es pico a
pico.

---

## Modo Dual: el precio

`Out2 Runs Every Second Frequency` reparte las frecuencias entre las dos salidas para ahorrar
tiempo. El precio:

- **la tensión en BN queda casi partida a la mitad**
- aparecen **productos de mezcla no deseados**

**No lo uses en Imprinting, en los MW-Presets de Johannes D, ni en Plasma** — esos necesitan
ambas salidas para tareas distintas.

**Y el flag `Repeat Chain` va en el ÚLTIMO preset de la cadena, no en el primero.** Es el bug más
reportado, y hay un fallo del Chain-Editor detrás: la solución es ponerlo a 0 en todos.

---

## Modo offline: lo que cambia

**En offline, Out2 es SIEMPRE inverso a Out1.** Eso **rompe los MW-Presets de Johannes D**, que
dependen de la relación entre las dos salidas.

Además, en standalone **la lista de programas se agota rápido**: cada programa ocupa una entrada
con nombre. Un sweep llenaría la lista enseguida — por eso no hay sweep.

## Los generadores NO tienen reloj

> *"Die Spooky2 Generatoren haben keine Uhr. Alle diese Scheduler Geschichten funktionieren nur mit
> **Traducción:** "Los generadores Spooky2 no tienen reloj. Todos estos temas de scheduler sólo funcionan con conexión constante al PC."
> ständiger Verbindung mit dem PC."*

**El Terrain Protocol de 11 días NO es autónomo.** Sin PC hay que arrancar y avanzar cada preset a
mano.

Y si el PC se cuelga, el generador **sigue emitiendo la última frecuencia** — no tiene reloj que
lo detenga.

## La Central genera ruido que tumba los generadores

El fallo más reportado del grupo. **No es del preset**: el chip USB del generador se cuelga por
interferencia EMI del tubo de plasma.

> *"zumeist der USB-Chip im Generator abstürzt"* · *"Das hat mit der Menge der Frequenzen nichts zu
> **Traducción:** "casi siempre el chip USB del generador se cuelga."
> tun."*

**El indicador no es un LED rojo.** Si ves `000000` en Out2 con Out1 activo, el generador no se
inicializó tras un corte de luz. **No hay error porque el generador sí responde — sólo no sale
señal.** Solución: `Utils | Rescan Devices`.

Lista anti-interferencia: Central y generador en enchufes separados (a ser posible otra fase),
ferritas en cables USB y BNC, separar los cables blancos de alta tensión, y separación espacial.

---

## El Crystal: qué lo rompe

- Entrada **square +5 V / GND**, sin valores intermedios. Techo de **50 kHz**.
- **Conmutar cuesta el 50% de fuerza** (duty).
- **Nunca a 5 V con el generador conectado en High-Power**: apaga los LEDs y daña el campo.
- **Nunca 27 V con el motor en marcha** (ver seguridad).
- El tope de frecuencia del Scalar viene de su reloj: el campo corre a ~6 MHz y se conmuta entero.
  **Por eso no hay armónicos útiles de MW o DNA.**