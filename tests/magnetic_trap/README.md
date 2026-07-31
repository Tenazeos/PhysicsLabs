# М3. Магнитная ловушка

## [Общая информация](/labs/magnetic_trap)

## Тест

Круговой контур радиуса $R$ с током $I$, лежащий в плоскости $xOy$.  
Нужно найти индукцию магнитного поля в точке $(0,0,z)$. Все расчёты в СГСМ.

---

Закон Био-Савара-Лапласа

$d\mathbf{B} = I \frac{[d\mathbf{l} \times \mathbf{r}]}{r^3}$

---
Заметим, что ввиду симметричности контура относительно $Oz$, вклад в $\mathbf{B}$ будет давать только вертикальная составяющая. 

Разложим на две части радиус-вектор:

$\mathbf{r} = \mathbf{r_{xy}} + \mathbf{r_z}$

$\mathbf{r_{xy}} = R$

$\mathbf{r_z} = z$

Нам нужно найти проекцию $\mathbf{B}$ на $Oz$, а $\mathbf{r_z}$ в векторном прозведении даст вектор, направленный в плоскости $xOy$, поэтому его можно сразу не учитывать.

Заметим, что $d\mathbf{l}$ перпендикулярен $\mathbf{r_{xy}}$, следовательно:

$|d\mathbf{l} \times \mathbf{r_{xy}}| = |\mathbf{dl}| \cdot |\mathbf{r_{xy}}| = |\mathbf{dl}| \cdot R$

$|dB_z| = I \frac{|d\mathbf{l} \times \mathbf{r_{xy}}|}{r^3} = \frac{I \cdot R \cdot |d\mathbf{l}|}{(R^2 + z^2)^{3/2}}$

$\oint |dB_z| = \oint \frac{I \cdot R \cdot |d\mathbf{l}|}{(R^2 + z^2)^{3/2}} = \frac{I \cdot R}{(R^2 + z^2)^{3/2}} \cdot \oint d\mathbf{l} = \frac{2 \pi \cdot I \cdot R^2}{(R^2 + z^2)^{3/2}}$
