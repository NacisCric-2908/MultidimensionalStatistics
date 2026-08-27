# Estadística Multidimensional — Proyecto

Análisis multidimensional sobre el dataset **Synthetic Credit Card Customer Behavior**
(`n = 50 000` clientes, `p = 30` variables). El trabajo se desarrolla de forma
incremental por semanas del curso (S01, S02, S03, …).

## Estructura del repositorio

```
.
├── data/
│   ├── bronze/     Datos crudos e inmutables. NO se editan a mano. (fuente única de verdad)
│   ├── silver/     Datos limpios/transformados. Se regeneran por código (no se versionan).
│   └── gold/       Tablas finales listas para modelar/reportar (no se versionan).
│
├── analysis/       Documentos de análisis (.Rmd y .ipynb). Cada uno se ejecuta
│                   desde la raíz del proyecto (ver "Cómo reproducir").
│
├── src/
│   ├── R/          Funciones .R reutilizables (source() desde los .Rmd).
│   └── python/     Módulos .py reutilizables.
│
├── reports/        Entregables: resumen ejecutivo (.md) y renders (.html).
│
├── figures/        Gráficos exportados a disco.
│
├── clase/          Material del curso (clases y trabajo autónomo). Independiente del proyecto.
│
├── MultidimensionalStatistics.Rproj   Proyecto de RStudio.
└── requirements.txt                   Dependencias de Python.
```

### Convención de capas de datos (medallion)

- **bronze** → crudo, tal cual llegó. Única capa versionada en Git.
- **silver** → limpio: tipos corregidos, sin duplicados, NA tratados.
- **gold** → agregados/derivados para un análisis o modelo concreto.

Todo lo que esté en `silver/` y `gold/` debe poder reconstruirse ejecutando el código.

## Cómo reproducir

### R (RStudio)

1. Abrir `MultidimensionalStatistics.Rproj`.
2. Abrir el `.Rmd` en `analysis/` y pulsar **Knit**.

Los `.Rmd` fijan `knitr::opts_knit$set(root.dir = "..")` en el chunk `setup`,
por lo que las rutas a datos se escriben desde la raíz del proyecto, p. ej.
`data/bronze/synthetic_credit_card_customer_behavior_dataset.csv`.

### Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Los notebooks `.ipynb` de `analysis/` usan rutas relativas a esa carpeta
(`../data/bronze/...`).

## Archivos de análisis

| Archivo | Descripción |
|---|---|
| `analysis/analisis_synthetic_credit_card.Rmd` | Documento base del análisis (S01–S03). |
| `analysis/analisis_synthetic_credit_card_desde_ipynb.Rmd` | Conversión del notebook a Rmd para RStudio. |
| `analysis/analisis_synthetic_credit_card.ipynb` | Notebook (kernel R). |
| `reports/resumen_analisis_synthetic_credit_card.md` | Resumen ejecutivo y técnico. |
