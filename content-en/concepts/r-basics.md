---
title: "R Basics (tooling reference)"
type: concept
status: mature
tags: [r, tooling, reference]
sources: ["[[sources/slides-0-r-basics]]"]
related: ["[[concepts/linear-regression-model]]"]
updated: 2026-08-29
---

A tooling reference page (not a separate Topic in the Course Outline) — used throughout the practice sessions. Unlike the other concept pages, this is just a lookup table, with no meaningful "exam traps" or "theoretical connections".

## RStudio interface

3 main panes: **Source** (write code), **Console** (run commands, the command prompt), **Environment** (view the objects currently in the session). Save code in an `.R` file (File → New file → R Script, then File → Save as). Run one line: place the cursor on the line, `Ctrl+Enter`. Run multiple lines: select them, `Ctrl+Enter`. Comment (exclude a line from running): put `#` at the start of the line.

## Data types and objects

Basic data types: **Integer**, **Floating point number**, **String**.

Commonly used object types:
- **Vector** — a one-dimensional sequence of values of the same data type.
- **Dataframe** — a two-dimensional data table (rows = observations, columns = variables), where each column can have a different data type; this is the object type used to hold a dataset when running a regression.

## Basic math functions (base R)

|Command |Meaning |
|---|---|
| `abs(a)` |absolute value |
| `sqrt(a)` |square root |
| `round(a, 3)` |round to 3 decimal places |
| `exp(a)` |the base-e exponential function |
| `log(a)` |natural logarithm (base e) |
| `log10(a)` |base-10 logarithm |

## Basic statistical functions

Applied to a variable (vector) `a`:

|Command |Meaning |
|---|---|
| `sum(a)` |sum of the elements |
| `min(a)` / `max(a)` |minimum / maximum value |
| `mean(a)` |mean |
| `sd(a)` |standard deviation |
| `median(a)` |median |
| `summary(a)` |prints a summary statistics table (min, Q1, median, mean, Q3, max) |
| `sort(a)` |sorts the elements in ascending order |

For a specific value `a` — related to the normal distribution:
- `dnorm(a)` — the value of the probability density function (pdf) of the standard normal distribution at point a.
- `pnorm(a)` — the value of the cumulative distribution function (cdf) of the standard normal distribution at point a.
- `A = rnorm(10, mean=0, sd=1)` — generates 10 random numbers from a normal distribution with mean 0 and SD 1.

## Packages outside base R

Base R only contains core functionality; packages like `psych` (data summarization) need to be installed before use:

- `install.packages("psych")` — installs the package, **only needs to be run once** on a given machine.
- `library(psych)` — loads the package into the session; must be called again **every time a new R/RStudio session is opened**, before using the package's functions (e.g. `describe`).

## Workflow for working with data

The common sequence of steps when working with a dataset in R:

1. Clear the working environment and change the working folder if needed.
2. Import the data (from a file or directly from a URL).
3. View summary statistics.
4. Build a one-way frequency table and a two-way table.
5. Draw charts: histogram, scatter plot.
6. Run the regression.
7. Generate new variables in the dataframe if variable transformation/creation is needed for the analysis.

## Connections

The operational foundation for all the empirical examples in [[concepts/linear-regression-model]] and the other concept pages — it carries no econometric theory content of its own.
