markdown_content = """
| Componente | Explicación | Valores Promedios Recomendados |
|------------|-------------|-------------------------------|
| **NOx** | Óxidos de nitrógeno, compuestos que incluyen NO (óxido nítrico) y NO₂ (dióxido de nitrógeno). | Concentraciones horarias no superiores a 200 µg/m³ más de 18 veces al año. |
| **CO** | Monóxido de carbono, gas producido por la combustión incompleta de carbono. | Concentraciones horarias no superiores a 10 mg/m³ más de 18 veces al año. |
| **SO₂** | Dióxido de azufre, gas emitido principalmente por la quema de combustibles fósiles. | Concentraciones horarias no superiores a 350 µg/m³ más de 24 veces al año. |
| **NO** | Óxido nítrico, un componente principal de los NOx. | No hay valores límite específicos; se regula como parte de los NOx. |
| **NO₂** | Dióxido de nitrógeno, otro componente de los NOx. | Concentraciones horarias no superiores a 200 µg/m³ más de 18 veces al año. |
| **O₃** | Ozono, gas presente en la atmósfera que puede ser tanto beneficioso (en la estratósfera) como dañino (en la troposfera). | Concentraciones horarias no superiores a 180 µg/m³ más de 18 veces al año. |
| **PM₁₀** | Partículas en suspensión con un diámetro menor a 10 micrómetros, causantes de problemas respiratorios. | Concentraciones diarias no superiores a 50 µg/m³ más de 35 veces al año. |
| **PM₂.₅** | Partículas en suspensión con un diámetro menor a 2.5 micrómetros, más finas que las PM₁₀, con mayor riesgo para la salud. | Concentraciones diarias no superiores a 25 µg/m³ más de 35 veces al año. |
| **PM₁** | Partículas en suspensión de tamaño aún más pequeño (menos de 1 micrómetro). | No hay valores límite específicos; se regulan como parte de las PM₂.₅. |
| **NH₃** | Amoníaco, gas que puede contribuir a la formación de partículas en el aire. | No hay valores límite específicos; se monitorea para evaluar la calidad del aire. |
| **C₆H₆** | Benceno, un compuesto químico volátil y cancerígeno. | Concentraciones anuales no superiores a 5 µg/m³. |
| **C₇H₈** | Tolueno, compuesto químico utilizado en solventes y pinturas. | No hay valores límite específicos; se monitorea para evaluar la calidad del aire. |
| **C₈H₁₀** | Xileno, compuesto químico usado en la industria de la pintura. | No hay valores límite específicos; se monitorea para evaluar la calidad del aire. |
| **Direc.** | Dirección del viento, expresada en grados. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **H.Rel.** | Humedad relativa, porcentaje de la cantidad máxima de vapor de agua que el aire puede contener. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **Precip.** | Precipitación, cantidad de lluvia o nieve caída en un período de tiempo. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **Pres.** | Presión atmosférica, la fuerza por unidad de área que ejerce el aire sobre la superficie terrestre. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **R.Sol.** | Radiación solar, cantidad de energía recibida del sol en un área dada. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **Ruido** | Nivel de ruido ambiental medido en decibelios. | Concentraciones horarias no superiores a 65 dB(A) más de 25 veces al año. |
| **Temp.** | Temperatura del aire, medida en grados Celsius. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **UV-B** | Radiación ultravioleta tipo B, perjudicial para la salud humana en grandes cantidades. | No tiene valores límite; se monitorea para evaluar la exposición solar. |
| **Veloc.** | Velocidad del viento. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **Veloc.max.** | Velocidad máxima del viento registrada. | No tiene valores límite; se utiliza para estudios meteorológicos. |
| **As** | Arsénico, metal pesado tóxico. | Concentraciones anuales no superiores a 6 ng/m³. |
| **BaA** | Benceno-antraceno, compuestos tóxicos derivados de la combustión. | No hay valores límite específicos; se monitorean para evaluar la calidad del aire. |
| **BaP** | Ben... |
"""

file_path = 'calidad_aire.md'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(markdown_content)
