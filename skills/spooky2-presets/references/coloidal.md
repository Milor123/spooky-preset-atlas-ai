# Plata coloidal — cómo se hace y qué límites tiene

Fuente: guía oficial de Spooky2, páginas **205–207** (batch-197-244.md).

---

## ⚠️ Primero, la corrección

Una versión anterior de `electromecanica.md` decía:

> *"Colloidal Silver = BN + 10 kΩ en serie — lleva resistencia limitadora incorporada."*

**Eso es falso y estaba escrito sin fuente.** El resistor de 10 kΩ **no viene dentro del puerto
SILVER del Boost**: es un componente que vos agregás **a mano en tu equipo de fabricación**.

**Consecuencia práctica:** el puerto SILVER **no tiene limitador de corriente incorporado.** Eso
cambia cómo hay que usarlo. Ver "Límites" abajo.

---

## Qué es, según la definición de la guía

> *"colloidal silver is silver **particles** that are **suspended** in solution — only silver
> **ions** are **dissolved**."*

**Son dos cosas distintas:** partículas coloidales en suspensión, e iones disueltos.

> *"TDS meters will only measure the **ionic** silver strength, **not the colloidal strength**."*

**Consecuencia:** un TDS te mide una cosa y no la otra. La guia dice que la Spooky2 tiene
*"an exceptionally high ratio of CS to ionic silver"* — pero **no lo podés verificar con un TDS.**

La guía sí da un método mejor:

> *"A more accurate way of determining the ppm is to use a **multimeter set to milliamps**. Measure
> by putting the multimeter in series with one rod."*

---

## El montaje que describe la guía

```
laptop → Spooky2-XM → frasco (jar) sobre agitador magnético
                     + varillas de plata
                     + resistor de 10 kΩ
```

**Magnético stirrer a ~4 RPM.**

Tiempo de proceso:

> *"360,000 s (just over four days) for four litres"*

Y:

> *"current through the solution rises over time as more silver sloughs off the rods; the purpose
> of the 10k resistor is to **keep the current more constant and low**"*

---

## Cómo saber si está bien hecho

**Color:** amarillo claro / dorado = tamaño de partícula muy pequeño.

**Prueba:** *"shine a laser through it and see a visible red line"* — la línea roja de Tyndall
confirma partículas coloidales suspendidas.

---

## Los errores que la guía advierte

**1. Calor = partículas más grandes.**
> *"use **cold water** (hot water speeds it but increases particle size)"*

**2. Agitar cada hora, dejar reposar una hora antes de decantar.**

**3. Guardar en vidrio oscuro.**
> *"plastics and UV can cause ions to lose charge and clump"*

**4. Las varillas no se limpian.** Las inversiones de waveform
(*`Swap Waveform`*) convierten el buildup de hidróxido de plata del ánodo en plata depositada
que se sedimenta.

**5. El agua destilada debe dar TDS 1 o menos.** El starting point del cálculo.

---

## Para USAR la plata como salida

**El puerto SILVER del Boost** — p21 lo marca como **weak**. Para Contact se usa acero
inoxidable o pads TENS vía High Power, o el puerto de plata.

### El ajuste que la guía exige

| uso | `Swap Waveform Every` |
|---|---|
| Contact treatment | **60 segundos** |
| **silver** | **300 segundos** |

> *"used for Contact Mode to prevent **acid burns** on sensitive skin"*

**Ojo con esa frase: "acid burns".** Es la guía describiendo el daño por Contact, en sus
propios términos.

### Por qué el waveform alterna

La forma `Colloidal_Silver` es una de las **ocho** waveforms integradas:

```
Colloidal_Silver · Alpha-Stim · Beamwave · DC · GoldDoublnSaw
GoldWave17-29 · GoldWave17-29Tenth · H-Bomb_Sine
```

**Seis de las ocho no están definidas en ningún otro lado de la guía.** Alternar entre ellas es
lo que produce el "envoltura triangular con spikes" que muestra el osciloscopio del manual, y
lo que mantiene la reacción en el electrodo en lugar de acumular óxido.

---

## Límites y seguridad

**1. El puerto no tiene limitador de corriente.** El 10 kΩ es del equipo de fabricación, no del
puerto. Si vas a tratar con plata coloidal sobre la piel, **empezá con la amplitud más baja del
rango** y subí gradually.

**2. El `Reduce Amplitude <` está en 10 kHz por default** (p117), y la guía lo justifica así:
> *"because **low frequencies can sting and tingle uncomfortably**… 10 KHz is the default"*

Es exactamente el comportamiento que vos mediste: **las bajas molestan, las altas no.**

**3. `Spike Ratio` cambia el Vpp real.** spike V = Amplitude; el resto = Amplitude ÷ Ratio.
Con Ratio 2 y amplitud 20, el span es **30, no 20**. Combinado con offset, extends la trampa
del §9.3 — **calculá el rango total, no la amplitud.**

**4. Spike Length en Contact es molesto.** p162: un valor de 24 *"would be a good value to
[avoid]… likely to be painful for contact mode"*.

**5. El Boost no se usa con BFB.** La guía es explícita: *"Spooky Boost must NOT be used — it
interferes"*.

---

## Lo que JW hace con su plata

> *"I don't swallow my silver. I swish some in my mouth for two minutes, then spit it out."*

Registrado como **lo que el usuario hace**, no como recomendación.