# La Coil (PEMF) — límites reales y shell recomendado

## Qué es

Puck magnético, cara `BN` contra la piel, alimentado directo de **Out1**. El campo magnético
atraviesa tejido; la corriente eléctrica no.

- **No tiene split kill/heal.** A diferencia de Contact o Plasma, no es un modo de "matar".
- La guía lo describe como *relaxation, circulation, regeneration* (p22).

---

## ⚠️ Usá el shell de Johannes D, no el de fábrica

**`Spooky Coil (Generator Direct) - JW` usa señal senoidal BIPOLAR.**

Con bipolar, el polo alterna: da igual cómo se sostenga la bobina contra el cuerpo.

> *"Es ist voellig egal, wie rum man die PEMF am Koerper haelt."* — Johannes D
> **Traducción:** "Es completamente indiferente cómo pongas la PEMF sobre el cuerpo."

**O sea: la instrucción "BN contra el cuerpo" no tiene efecto con ese shell.** No es una cuestión de
orientación — una onda bipolar no puede sostener un polo fijo.

Según Nesterov, el **polo sur** es el que produce efecto terapéutico, porque sólo él genera un campo
de torsión dextrógiro. Para aprovechar eso hace falta señal **unipolar** con el sur en BN, y ése es
el motivo de los shells propios de Johannes D.

**Los shells de Johannes D, presentes en el corpus:**

```
Preset Collections\Shell (Empty) Presets\Coil\
   Spooky2 Single PEMF (Coil )  - JD.txt        ← un solo canal
   Spooky2 Double PEMF (Coil) - JD.txt          ← dos canales, Ch1/Ch2
   MW Emulate 20v (Coil) - JD.txt
```

Su forma de onda:

> *"meine Lieblingswellenform polares asymmetrisches Rechteck"* — **rectángulo polar asimétrico**
> **Traducción:** "mi waveform favorita: rectángulo polar asimétrico."

Es el `MM_ModSquare` con +Spike y −Spike. En el shell doble **no apila BN sobre BN**, a propósito,
para no tener que decidir qué bobina va en Ch1.

Y también hay presets suyos para bobina:

```
Preset Collections\Miscellaneous\Johannes_D\Coil\
   Antimicrobial (MW) (Coil) - JD.txt
   Oncomodulin-1 V3 DC17 (Coil) - JD.txt
```

### Problema abierto en el shell de JD

Su shell **no tiene offset (0%)**, lo que choca con su propia explicación de "unipolar". O el
spike genera el sesgo, o la versión del corpus es anterior al 10-04-2024. **Sin osciloscopio no se
puede verificar.** Decilo como límite, no como certeza.

### El Boost queda fuera

Al conectar la PEMF al High Power del Boost, **se apagan los LEDs** [22686]. Johannes D preguntó
si se le caía la potencia y **no hay respuesta en el hilo**. **Nunca tapes la Coil al Boost.**

---

## El rango de frecuencias que realmente maneja

Medido sobre las **34.527 ocurrencias** de frecuencia en los 6.954 presets de Coil del corpus:

| percentil | Hz |
|---|---|
| p5 | 15 |
| p25 | 77 |
| **p50 (mediana)** | **513** |
| p75 | 1.865 |
| p90 | 72.609 |
| p95 | 81.241 |
| p99 | 87.841 |

| umbral | share |
|---|---|
| sobre 1 MHz | **0,58 %** |
| sobre 100 kHz | **0,85 %** |
| sobre 10 kHz | 23,71 % |

**La banda de trabajo de la Coil es 1 Hz – 100 kHz.** Por encima de 100 kHz quedan casos
atípicos, y el máximo del corpus (5,6 GHz) son seis valores sueltos, no una banda.

### Y lo que dice Johannes D que NO funciona

> *"**Nur mit den MWs und DNA Programmen**, d.h. Frequenzen >1 MHz da bin ich nicht sicher."* [33190]
> **Traducción:** "Sólo con los programas MW y DNA — o sea, frecuencias >1 MHz — no estoy seguro."

> **"Peptide-Presets im Coil Modus funktionieren nicht."** [45173]
> **Traducción:** "Los presets de péptidos no funcionan en modo Coil." — 
> es análisis de **JD** sobre la waveform senoidal del shell deJW, no una advertencia
> textual de JW.

Los programas DNA/MW en MHz son el grupo más raro del catálogo Coil. **No los pases a Coil.**

---

## El manufacturer's mistake: misma lista para todos los modos

**No hay una lista de frecuencias por modo.** El mismo número aparece en los seis modos.

`Ropeworm` = `1359=360`, idéntico en Coil, Contact, Laser, Plasma, Remote y Scalar.

`Parasites & Lymph` = `9.6, 15, 26, 35, 48, 60, 95, 125, 160, 200, 230`:

| modo | shell | dwell |
|---|---|---|
| Coil | Healing (Coil) | 85 |
| Remote | Healing (R) | 78 W4 |
| Plasma | Advanced (P) | 85 |
| Scalar | Healing (S) | 85 |

**Mismos números, mismo orden, todos los modos.** Cambiaron el shell y dejaron la lista. Eso no
significa que la Coil sea el vehículo correcto para cada lista: significa que nadie revalidó.

**Consecuencia práctica:** no tomes listas de Contact o Remote y las pases a Coil por suposición. Si querés Coil, usá una lista que ya esté en Coil, o justificá el traslado.

---

## Patrón de uso que recomienda Johannes D

Ante *"connective tissue, ¿PEMF o Cold Laser?"* [22530]:

> *"Hat man ein bestimmtes problematisches Areal wuerde ich eher zu PEMF neigen, aber jedenfalls
> **Traducción:** "Si tenés un área problemática puntual, me inclino más por PEMF, pero de todos modos corré la paleta por Remote y PEMF20-30 min diarios sobre esa zona."
> die ganze Palette via Remote parallel dazu laufen lassen und **jeden Tag mit PEMF 20-30 min**
> auf besagte Stelle"*

Traducción operational:

- **PEMF 20–30 min diarios sobre el área concreta.**
- **El resto de la paleta en paralelo por Remote**, no en vez de.

---

## Nota sobre datos corregidos

Las cifras "66,9 % bajo 100 Hz" y "0,2 % sobre 100 kHz" que aparecen en
`teoria-JD/KNOWLEDGE-JD.md` **no son reproducibles** con ningún método de conteo sobre este
corpus: por ocurrencia dan 31,8 % y 0,85 %, y por valor único 7,9 % y 2,0 %. Los números de esta
página son los medidos. Usá estos.