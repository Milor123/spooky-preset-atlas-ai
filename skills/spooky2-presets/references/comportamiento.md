# Comportamiento — cómo funcionan de verdad

Lo que hay que saber para no afirmar algo falso sobre un preset. Sin esto, la AI repite el error
más común: **confundir la frecuencia que muestra el generador con la que sale.**

---

## El ARB: 1.024 muestras

Los generadores Spooky2 son generadores de forma de onda arbitraria. Guardan la forma en
**1.024 puntos de muestreo** y reciben amplitud y frecuencia por orden del PC.

**De ahí salen tres cosas:**

1. **No hay sweep.** En standalone se manda una lista de programas con nombre; un sweep la
   llenaría enseguida. El sweep lo hace el PC, no el generador.
2. **Si el PC se cuelga, sigue sonando la última frecuencia.** No hay reloj que lo detenga.
3. **La arquitectura real es** reloj → direccionamiento de memoria → **DAC** → **endstufe**.
   El cuello de botella **no es la memoria**: es el DAC y la etapa de salida. Tope de lectura
   **XM 5 MHz, GX 40 MHz**.

## WCM: por qué el generador nunca muestra la frecuencia del preset

**La waveform contiene varios ciclos por unidad de tiempo.** El WCM es ese número, y el generador
muestra **f ÷ WCM**.

```
Square-H-Bomb  →  WCM 16  →  el generador corre a 1/16 de lo que muestra
```

**A 1 MHz de programa el generador corre a 62,5 kHz.** No es un error, es el diseño.

El consequence práctica: **`Square H-Bomb` es un nombre distinto de `Square -H-Bomb`.** El guion
importa, y cambia la relación con el display.

Y el límite real del H-Bomb no es 1 MHz: XM llega a ~80 MHz teóricos, GX a ~640 MHz.

**El trap del WCM:** `WCM = 20 V ÷ nº de frecuencias simultáneas`. Con WCM=1024 la amplitud cae
de 20 V a **0,0195 V**. **Siempre el WCM más pequeño posible.** Y WCM tiene **dos significados
distintos** en el software, ambos introducidos por John White.

## El XM divide por octavas automáticamente

**Todo lo que pase de 5 MHz se divide en pasos de octava hasta llegar a 5 MHz.**
Con 5,01 MHz en el programa salen **2,505 MHz**.

Contra lo que se suele creer, **la exactitud del XM es similar o algo mejor que la del GX**, y su
forma de onda es mejor que la GX Pro en frecuencias altas — que el XM de todos modos no alcanza.

**Para MW y DNA: usá un GX.** Es lo que dice el autor que más midió.

## Los generadores SÍ precalculan

Las frecuencias se precalculan en el GX con un factor **siempre potencia de dos** (×2048, ×1024,
×512…). **Medir sin corregir ese factor da un error de 500× a 8.000×.**

## Biofeedback: qué mide y qué NO

**No diagnostica.** Eso lo dice el autor repetidas veces: *"der BFB ist kein Diagnosetool"*.

El número entre paréntesis **no es una medición**: es **`valor actual − media móvil`**
(`Current − PrevRA`). Ventana 2 por defecto, máximo 20.

**`Current` es la única de las tres con significado físico.** `Angle+Current` suma un ángulo con
una corriente. El autor **rectificó su propia recomendación** sobre esto.

**El cuerpo se comporta como carga capacitiva**, por eso los hits altos caen siempre en las
frecuencias altas. **Ésa es una de las dos razones del piso de 41 kHz** (la otra es que por
debajo la corriente cae y sube el error de medida, SNR).

**Con el XM es otra cosa por completo:** mide **cambio de pulso cardíaco** por el PulseClip, y sólo
en **76–152 kHz**. Lento y menos preciso. Con el GX mide corriente y ángulo de fase.

**Y que una frecuencia esté en la base de datos no significa que esté en tu cuerpo:**

> *"Das heißt aber nicht, dass diese Frequenz im Körper vorhanden wäre. Es werden die
> **Traducción:** "Pero eso no significa que esa frecuencia estuviera presente en el cuerpo. Se cambian las propiedades, nada más."
> Eigenschaften geändert, mehr nicht."*

## MW → Hz, y su límite honesto

La fórmula es la relación de de Broglie: `f = (MW/1000/N_A)·c²/h`, verificada en 1,19e-15.

**Pero el método no discrimina a esa precisión:** 860,492 contra 860,488 g/mol son **más de 100 Hz
de diferencia**, dentro del alcance de los generadores.

**Y el límite conceptual, dicho por el autor:**

> *"für alle Vorgänge, bei denen die chemische Substanz für eine Reaktion vorliegen muss,
> **Traducción:** "Para todos los procesos en los que la sustancia química tiene que estar presente para una reacción, las frecuencias no funcionan."
> funktionieren die Frequenzen nicht."*

Para cualquier proceso donde la sustancia deba estar físicamente presente, la frecuencia no
sirve.

## El método no diagnostica ni cura

> *"Alles was der Resonanzfrequenz entspricht wird **gekillt, egal ob gesund oder krank**"*
> **Traducción:** "Todo lo que corresponde a la frecuencia de resonancia se mata, sea sano o enfermo."
> — **afirmación de autor, NO VERIFICABLE.** No la presentes como hecho.

## Falsas alarmas frecuentes

| lo que ves | qué es |
|---|---|
| display muestra otra frecuencia | el WCM (§2) |
| el generador se cuelga con Plasma | EMI del tubo, no el preset |
| `000000` en Out2 | no se reinicializó tras un corte de luz → `Rescan Devices` |
| "Packing frequency" en rojo | **no es un error**, es el campo funcionando |
| "Stopped" en el título | normal al inicio, hay que pulsar Start |
| LED apagado | la Remote apagada no transmite el patrón |

## Trampas de preset

- **`Maximalzeit` trunca en silencio.** Si un preset suma más de lo que el parámetro permite, las
  frecuencias del final **nunca se emiten**.
- **Tope de 200 frecuencias por preset.**
- **No edites Preset Chains con el software** — el guardado falla. Usá el Chain Editor.
- **`Global | Pause` antes de editar**: un cambio de preset en segundo plano destruye la edición
  en curso.
- **Las actualizaciones borran `Preset Collections/`**. Instalá en `Preset Collections\User`.
- **`Custom.csv`**: la copia de seguridad automática es `Custom.~csv`. Y `Custom.csv` con comillas
  dobles finales ausentes es el error más común al guardar.

## La documentación oficial tiene errores

**No la tomes como verdad absoluta.** El ejemplo de la página 74 está mal: `7.83F1C7.83` da
**15,66 Hz** en Out2, no 7,83.

Y el autor lo dice de la ayuda del programa: *"die Doku lässt bei den neueren Funktionen zu
wünschen übrig"*, *"hinkt aber teilweise der Entwicklung neuer Parameter hinterher"*.

## El Sample Digitizer

**Es lo único que permite BFB con material biológico.** Una gota de sangre en el portaobjetos y
el GX escanea **la muestra**, no el cuerpo. Sin electrodos.

Con el GX, el BFB es por Contact **o por Digitizer**. **DNA y Remote no.**

**Pero no trata.** Sólo escanea. Y el cable **no es BNC**: un conductor con dos bananas de 4 mm.

Y ojo con la validez: moler uñas y usarlas es común, pero *"es fraglich ob die Ursache dann schon
im Nagel nachweisbar ist"* — que el aparato mida bien **no** es lo mismo que lo que mide
signifique algo.

## Cold Laser

**Techo de 1 MHz por hardware:** el diodo no conmuta más rápido. Por encima, el software **baja
la frecuencia y actúa más débil, sin avisar**.

**Sólo Out1.** Los MW-Presets de Johannes D necesitan Out1+Out2, así que son incompatibles, y el
Boost queda casi prohibido.

---

## Cómo leer un preset sin afirmar cosas falsas

1. **Nunca por el filename.** Hay filenames que dicen una cosa y el preset dentro es otra.
   Ejemplo real: un archivo titulado con "worms, hook, roundworm, filariasis" contiene 16 presets
   de **cromoterapia**.
2. **Mirá `Base_Preset`** para heredar la waveform del shell.
3. **Si el WCM no es 1, la frecuencia del display no es la del preset.**
4. **Los programas `MW` y `DNA` están cifrados.** No son números de Hz: son inútiles fuera del
   software. Y **no los trates como si fueran frecuencias medibles.**
5. **Reportá el veredicto de `screen` tal cual.** `OK-PARTIAL` y `NO-CHECK` **no** son `OK`:
| veredicto | qué significa | qué decís al usuario |
|---|---|---|
| `OK` | todas las frecuencias se resolvieron y la blacklist se aplicó | *"revisado y limpio"* |
| `OK-PARTIAL` | la blacklist se aplicó sólo a las resolubles | *"revisado en parte; N de M frecuencias no se pudieron comprobar"* |
| `NO-CHECK` | **no se pudo comprobar ninguna** | *"**sin verificar**: no sabés si tiene 1840"* |
| `FLAG` | un parámetro pide mirar más cerca | decí cuál y por qué |
| `REJECT` | hay una razón dura | no lo ofrezcas como opción limpia |

**Nunca conviertas `OK-PARTIAL` ni `NO-CHECK` en "está bien".** Decir "OK" cuando no se miró el
100% es exactamente el error que este veredicto existe para evitar.
