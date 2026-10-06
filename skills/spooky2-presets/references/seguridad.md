# Seguridad — las prohibiciones verificadas

Reglas que **no se saltan**. Cada una está respaldada por la guía oficial de Spooky2 o por
propiedades medibles del aparato. La columna "Fuente" dice de dónde sale cada una.

> **Lo que la guía oficial declara como creencia, no como hecho:** la blacklist de 1840 y 1910 Hz
> dice literalmente *"these are **believed to** cause malignancy growth"* (guía p.140). Reportalo
> como belief del fabricante, nunca como hallazgo.

---

## 1. Nunca dos Contact a la vez

**Prohibido por el fabricante**, no es consejo de un autor.

Varios pads TENS en distintos generadores quedan conectados **indirectamente por el USB-ground**,
y por el cuerpo circulan corrientes de ecualización (*Ausgleichströme*).

> *"eine Betriebsart die auch vom Hersteller nicht gestattet ist"*
> **Traducción:** "un modo de funcionamiento que tampoco permite el fabricante."

**Contact + Laser simultáneos sí se puede**, con programas distintos.

## 2. El offset es corriente continua

**Offset 0 en Contact. Siempre.**

> *"Offset ist Gleichspannung und kann bei Contact zu Verbrennungen führen."*
> **Traducción:** "El offset es tensión continua y puede producir quemaduras en Contact."

El offset no es un ajuste de polaridad inocuo: es DC. Aplica cada vez que se cambia un shell de
Remote a Contact sin revisarlo.

### Y con offset alto el rango se desplaza entero

**Offset 100 % + amplitud 20 V NO da 20 V — da 0…10 V.** El rango completo se mueve al positivo.
Cualquier cálculo de "cuánta tensión entrega" con offset 100 % está mal.

Con Boost, para obtener −20…0 V en BN y 0…20 V en MN hay que poner **Out2 a −100 %**.

## 3. Polarizar con pads TENS quema

> *"Vorsicht dabei aber mit TENS-Pads. Da kann man sich recht schnell auch Verbrennungen
> **Traducción:** "Pero cuidado con los pads TENS: te dan quemaduras con bastante rapidez."
> zuziehen."*

## 4. El dolor es el único indicador, y llega tarde

**En frecuencias altas ya no se siente hormigueo.** Lo único que se nota al equivocarse es dolor,
y para entonces ya es tarde.

**La piel debe estar seca.** 20 V a 150 mA con piel húmeda son 3 W.

## 5. Cuatro pads: imposible

> *"Die Ausgänge sind nicht galvanisch getrennt, so können zwischen den Generatoren unerwünschte
> **Traducción:** "Las salidas no están aisladas galvánicamente, así que entre los generadores pueden circular corrientes no deseadas."
> Ströme fließen."*

**No es una recomendación: es una limitación del hardware.** No hay galvano con estos generadores.

## 6. No tapes los generadores

La riesgo no es la temperatura aislada sino la **acumulación de calor**.

> *"Wichtig ist die Teile so aufzustellen, dass kein Hitzestau entsteht. Also nicht zudecken."*
> **Traducción:** "Importante poner las partes de forma que no se acumule calor. No taparlos."

## 7. Nunca tapes el Laser al Boost

> *"dann können sie kaputt gehen."* — es riesgo para el aparato, no para vos. Si se conecta:
> **Traducción:** "se pueden romper."
**siempre Out1.**

## 8. Los láseres, Scalar y Plasma no son a prueba de tensión

| aparato | ¿aguanta fuera de rango? |
|---|---|
| **Remote** | **sí, a prueba de tensión** |
| **Plasma** | **no** — rompe la Central |
| **Scalar** | **no** — lo destruye |
| **Cold Laser** | **no** — muere a 10 V en Boost |

Este es el criterio de selección entre preset y salida, no una preferencia.

## 9. Cold Laser: nunca con offset −100 %

Quedaría en −5 V…−10 V, fuera de rango.

## 10. Las entradas de la Central son conmutadas

**0 V apagado · +5 V encendido.** Por eso sólo tiene sentido una onda cuadrada.
Umbrales TTL (`Vih ≥ 2 V` / `Vil ≤ 0,8 V`) y CMOS (`Vih ≥ 3,5 V` / `Vil ≤ 1,5 V`).

**10 V sobre la entrada es sobrecarga permanente, con riesgo de destruir la Central.**

## 11. El tubo de plasma: no lo abras

Si hay piezas metálicas adentro, los wires **jamás** deben tocarlas:

> *"Das könnte durchaus ernste Konsequenzen (**Bersten der Röhre**, Zerstörung der Endstufe) haben."*
> **Traducción:** "Eso puede tener consecuencias graves (reventar el tubo, destruir la etapa de salida)."

**Reventar el tubo o destruir la etapa de salida. Abrirlo pierde el gas.**

## 12. Los fusibles del Central: desenchufá antes

Hay fusibles accesibles desde fuera, y uno de 4 A escondido bajo el interruptor rojo.

> *"Dabei aber bitte den Stecker ziehen."*
> **Traducción:** "Pero desenchufá antes."

## 13. Nunca con el auto en marcha

Puesto a 12 V: **13,8 V parado · 14,4 V con el motor en marcha.** La norma VW80000 ensaya hasta
**27 V**. Los frigoríficos del auto también generan picos.

**Nunca conectar a la red de 12 V con el motor en marcha.**

## 14. Los adhesivos holográficos

- **Nunca plástico entre la etiqueta y la piel.**
- **Para uñas: papel blanco, nunca*Tesa.** El plástico entre medias atenúa el campo.
- El holograma es **sólo para imprinting**. Para el cuerpo, un pañuelo de papel también sirve.
- El pelo **no sirve**: es ARN, no ADN, y la raíz tiene que seguir pegada.
- **No mezclar ADN humano y animal** en una Remote.
- El **imán de la Remote borra los stickers**: hay que sacarlos **con el programa corriendo**.
  Para reimprimir hace falta un imán de **140 kg**.

## 15. Menores de 7 años

Prohibición del fabricante, textual en su documentación.

---

## La blacklist global

| frecuencia | qué hacer |
|---|---|
| **1840 Hz** | agregar a la blacklist |
| **1910 Hz** | agregar a la blacklist |

Es global: aplica a **todos** los generadores. La frase del fabricante es *"believed to cause
malignancy growth"* — **una creencia declarada, no un hecho establecido**.

En este corpus **1840 Hz aparece 83 veces en 22 presets distintos**; 1910 Hz no aparece.

### Las casillas que pueden saltear frecuencias

`Avoid Octaves` y `Avoid Decades` evitan armónicos de octava y década. La propia guía advierte:

> *"this can result in very important frequencies being skipped."*

Un preset scrolled onto uno de esos puede **saltarse frecuencias en silencio**.