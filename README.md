# Práctica 1: WebScraping

## Descripción:

En esta práctica se ha llevado a cabo un proceso de web scraping para obtener información valiosa de la página web de [doctorados](https://genealogy.math.ndsu.nodak.edu/). En dicha página se puede encontrar información relativa a todas las tesis doctorales realizadas a lo largo de la historia y, más en concreto, a todos los doctores que las realizaron y el grado de relación profesional entre ellos.

## Realizada en solitario por:

- Juan María Guerrero Carrasco

## Ficheros:

- **[chromedriver.exe](https://github.com/jmguerreroca/WebScraping/blob/main/source/chromedriver.exe)** se ha obtenido de [chromedriver](https://chromedriver.chromium.org/downloads). A partir de este podemos definir la configuración necesaria que nos otorga permisos para navegar por la web. Conviene señalar que cada versión de Chrome necesita de una versión específica y adaptada a dicha versión, por lo que conviene comprobar esto antes de continuar. Este fichero en concreto será el ChromeDriver 107.0.5304.62.

- **[scraper.py](https://github.com/jmguerreroca/WebScraping/blob/main/source/scraper.py)** es el ejecutable principal del código y en el que se encuentran los métodos necesarios para llevar a cabo nuestro web scraping de manera correcta y eficiente.

- **[memoria.pdf](https://github.com/jmguerreroca/WebScraping/blob/main/memoria.pdf)** será el PDF donde se den las respuestas a las cuestiones planteadas en la práctica y se explique en profundidad la motivación y funcionamiento del proyecto.

- **[historical_spanish_PhD_computer_scientist](https://doi.org/10.5281/zenodo.7346828)** será nuestro dataset de ejemplo con los valores de salida por defecto. Haciendo referencia a aquellos matemáticos que obtuvieron su doctorado especializándose en ciencias de la computación en una universidad española.

## Uso del ejecutable:

En primer lugar, antes de llevar a cabo la ejecución principal conviene revisar que contemos con las versiones adecuadas del código para la ejecución. Aparte de comprobar que contamos con la versión del chromedriver que se adapta a nuestro navegador, podremos instalar los requerimientos de código mediante el comando:

```bash
python3 install -r requierements.txt
```

Una vez contamos con los requerimientos podemos ejecutar el script principal que se encuentra en la carpeta *source*.

El script podrá recibir hasta tres parámetros como argumentos:

- **subject**: Añadiendo `--subject` al final seguido del valor numérico que referencia al tema de estudio.
- **year**: Añadiendo `--year` al final seguido del valor del año en que se realizó la tesis que se referencia.
- **country**: Añadiendo `--country` al final seguido del valor del país en el que se realizó la tesis.

Aunque es recomendable añadir algún parámetro de búsqueda para no saturar el servidor con peticiones muy grandes, cabe destacar que no serán realmente necesarios.

A continuación se muestran un par de ejemplos de como deberíamos ejecutar el código, siempre desde un directorio dentro de la carpeta *source/*:

Tesis sobre computer scientis en Estados Unidos durante 2022:

```bash
python3 scraper.py --year '2022' --subject '68' --country 'UnitedStates'
```

Tesis realizadas en 1997 en el tema de estadística:

```bash
python3 scraper.py --year '1997' --subject '62'
```

Otro dato reseñable es que como se mencionaba, no se necesitan obligatoriamente parámetros, pues por defecto en ausencia de estos generará el histórico de doctores españoles en el área del computer science.
Por ello ejecutar los siguientes dos comandos será equivalente:

```bash
python3 scraper.py --country 'spain' --subject '68'
```
```bash
python3 scraper.py
```

El país no discrimina entre minúsculas y mayúsculas. El año deberá estar escrito con 4 cifras numéricas y el código del tema habrá de corresponderse con la siguiente lista:

| Código | Nombre                                                 |
| ------ | ------------------------------------------------------ |
| 00     | General                                                |
| 01     | History and biography                                  |
| 03     | Mathematical logic and foundations                     |
| 05     | Combinatorics                                          |
| 06     | Order, lattices, ordered algebraic structures          |
| 08     | General algebraic systems                              |
| 11     | Number theory                                          |
| 12     | Field theory and polynomials                           |
| 13     | Commutative rings and algebras                         |
| 14     | Algebraic geometry                                     |
| 15     | Linear and multilinear algebra; matrix theory          |
| 16     | Associative rings and algebras                         |
| 17     | Nonassociative rings and algebras                      |
| 18     | Category theory, homological algebra                   |
| 19     | K-theory                                               |
| 20     | Group theory and generalizations                       |
| 22     | Topological groups, Lie groups                         |
| 26     | Real functions                                         |
| 28     | Measure and integration                                |
| 30     | Functions of a complex variable                        |
| 31     | Potential theory                                       |
| 32     | Several complex variables and analytic spaces          |
| 33     | Special functions                                      |
| 34     | Ordinary differential equations                        |
| 35     | Partial differential equations                         |
| 37     | Dynamical systems and ergodic theory                   |
| 39     | Finite differences and functional equations            |
| 40     | Sequences, series, summability                         |
| 41     | Approximations and expansions                          |
| 42     | Fourier analysis                                       |
| 43     | Abstract harmonic analysis                             |
| 44     | Integral transforms, operational calculus              |
| 45     | Integral equations                                     |
| 46     | Functional analysis                                    |
| 47     | Operator theory                                        |
| 49     | Calculus of variations and optimal control             |
| 51     | Geometry                                               |
| 52     | Convex and discrete geometry                           |
| 53     | Differential geometry                                  |
| 54     | General topology                                       |
| 55     | Algebraic topology                                     |
| 57     | Manifolds and cell complexes                           |
| 58     | Global analysis, analysis on manifolds                 |
| 60     | Probability theory and stochastic processes            |
| 62     | Statistics                                             |
| 65     | Numerical analysis                                     |
| 68     | Computer science                                       |
| 70     | Mechanics of particles and systems                     |
| 74     | Mechanics of deformable solids                         |
| 76     | Fluid mechanics                                        |
| 78     | Optics, electromagnetic theory                         |
| 80     | Classical thermodynamics, heat transfer                |
| 81     | Quantum Theory                                         |
| 82     | Statistical mechanics, structure of matter             |
| 83     | Relativity and gravitational theory                    |
| 85     | Astronomy and astrophysics                             |
| 86     | Geophysics                                             |
| 90     | Operations research, mathematical programming          |
| 91     | Game theory, economics, social and behavioral sciences |
| 92     | Biology and other natural sciences                     |
| 93     | Systems theory; control                                |
| 94     | Information and communication, circuits                |
| 97     | Mathematics education                                  |

