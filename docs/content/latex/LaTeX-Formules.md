---
title: LaTeX Formules
last_modified_at: 2024-05-27 21:33:12 +0200
date: 2024-05-27 21:33:12 +0200
---

Er zijn online LaTeX editors gespecialiseerd in formules, voor onderstaande editors heb je **geen account** nodig:
- [https://latex.codecogs.com/eqneditor/editor.php](https://latex.codecogs.com/eqneditor/editor.php)
- [https://latexeditor.lagrida.com/](https://latexeditor.lagrida.com/)
- [https://math-editor.online/](https://math-editor.online/)
- [https://www.commontools.org/tool/latex-compiler-and-equation-writer-18](https://www.commontools.org/tool/latex-compiler-and-equation-writer-18)
- [LaTeX to SVG convertor](https://viereck.ch/latex-to-svg/)

# LaTeX-formule syntax

| Wiskundige notatie | LaTeX code |
|-------------------:|:-----------|
| ![](formules/2power3.svg){: .square } | `2^3` |
| ![](formules/minuspower.svg){: .square } | `2^{-1}` |
| ![](formules/powerdot.svg){: .square } | `2^{5 \cdot 1}` |
| ![](formules/dlowern.svg){: .square } | `D_N(x)` |
| ![](formules/powerlower.svg){: .square } | `3^2_5` |
| ![](formules/hatequal.svg){: .square } | `A\,{\widehat {=}}\,0` |
| ![](formules/hatx.svg){: .square } | `A\,{\widehat {x}}\,0` |
| ![](formules/dots.svg){: .square } | `\{1,\ldots ,q-1\}` |

## Dirac-vergelijking
![](formules/Dirac-vergelijking.svg){: .square }
```latex
\left(i\gamma^\mu \partial_\mu - m\right)\psi = 0
```

## Schrödingervergelijking
![](formules/Schrödingervergelijking.svg){: .square }
```latex
i\hbar\frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \left(-\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r},t)\right)\Psi(\mathbf{r},t)
```

## Maxwell-vergelijkingen
![](formules/Maxwell-vergelijkingen.svg){: .square }
```latex
\begin{align*}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{align*}
```

