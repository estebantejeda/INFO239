 # 1. Sistemas de comunicación

## 1.1 Modelo de Shannon

![Screenshot_20210419_232204](.images/Screenshot_20210419_232204.png)

* __Mensaje__: Información que se envía.
* __Transmisor__: Transforma, codifica y transmite el mensaje. La transformación debe hacer la transmisión eficiente.
* __Ruido__: Va en la señal, pero no tiene relación con la información a enviar. Contamina el mensaje.
* __Señal__: Mensaje convertido por el transmisor que viaja por el canal.
* __Canal__: medio por el cual se envía el mensaje.
* __Receptor__: Captura la señal del transmisor para obtener el mensaje.

# 2. Señales

## 2.1 ¿Qué es una señal?

​	Una señal es una función del tiempo que entrega información sobre un fenómeno físico.
$$
f: x \rightarrow y
$$
​	Con:

* $x$ variable independiente. Tiempo, superficie o volumen
* $y$ variable dependiente: Potencial eléctrico, presión en el aire, intensidad de un pixel, etc.

## 2.2 Características de una señal

### 2.2.1 Energía

​	Es una medida del tamaño/área de la señal.
$$
E_g = ||g||=\int_0^T |g(t)|^2 dt
$$

### 2.2.2 Potencia

​	Mide la fuerza o intensidad de la señal.
$$
P_g = \lim_{T\rightarrow\infty} \frac{1}{T}E_g
$$

### 2.2.3 Razón señal a ruido (SNR)

​	Es una medida de la calidad de la señal.

## 2.3 Clasificación de señales

### 2.3.1 Clasificación #1	

El dominio de una señal se refiere al espacio en que corresponde.

* Señales continuas o tiempo discreto
* Señal análoga o digital

### 2.3.2 Clasificación #2

* Determinística: Puede describirse por una ecuación matemática
* Estocástica: Solo puede ser descrita probabilísticamente.

### 2.3.3 Clasificación #3

​	Se puede clasificar según su comportamiento en el tiempo.

* __Periódica__: Se repite luego de un cierto tiempo $P$. El tiempo se denomina __periodo__.
* __Aperiódica__: No se repite regularmente en el tiempo.

# 3. Análisis de señales

## 3.1 Notación

* Función tiempo continuo: $g(t)$.
* Función de tiempo discreto: $g[n]=g(t_n), t_n = nT_s, n \in [0,N]$ 

* Tiempo o intervalo de muestreo: $T_s$

## 3.2 Comparando señales: Covarianza y correlación cruzada

### 3.2.1 Covarianza

$$
\text{COV}_{gf}[m] = \frac{1}{N} \sum_{n=1}^N (g[n] - \bar g)(f[n+m] - \bar f)
\\
\bar g = \frac{1}{N} \sum_{n=1}^N g[n]
$$

### 3.2.2 Correlación cruzada

$$
\rho_{gf}[m] = \frac{\text{COV}_{gf}[m]}{\hat \sigma_g \hat \sigma_f}
\\
\hat \sigma_g = \frac{1}{N} \sqrt{\sum_{n=1}^N (g[n] - \bar g)^2}
$$

### 3.2.3 Resolución conda

~~~python
crosscorr = np.correlate(y1, y2, mode='full')/(len(x)*np.std(y1)*np.std(y2))
~~~

## 3.3 Autocorrelación

​	Permite analizar la __periodicidad__ de una función
$$
\rho_{gg}[m] = \frac{\text{COV}_{gg}[m]}{\hat \sigma_g^2}= \frac{1}{(N-m) \hat \sigma_g^2} \sum_{n=1}^{N-m} (g[n] - \bar g)(g[n+m] - \bar g)
$$

### 3.3.1 Resolución conda

~~~python
autocorr = np.correlate(y, y, mode='full')[len(x)-1:]/(len(x)*np.var(y))
~~~

## 3.4 Convolución

​	Es el producto punto entre versiones desplazadas de funciones.
$$
(f*g)[m] = \sum_n f[n] g[n-m]
$$

### 3.4.1 Resolución conda

~~~python
conv_s = np.convolve(functionA(t), functionB(t), mode='same')
~~~

## 3.5 Transformada de Fourier

$$
\begin{align}
G(f) &= \mathcal{F}[g(t)] = \int_{-\infty}^{\infty} g(t) \exp(-j2\pi f t) \,dt \\
&= \int_{-\infty}^{\infty} g(t) \cos(2\pi f t) \,dt - j \int_{-\infty}^{\infty} g(t) \sin(2\pi f t) \,dt
\end{align}
$$



​	La transformada de fourier es aplicada a una función en el tiempo, la cuál da como resultado otra función, pero que está en frecuencia.

​	Usaremos la siguiente función a modo de ejemplo:
$$
g(t)=\cos(2\pi \cdot 1 t) + \cos(2\pi \cdot 1.5t) + h(t)
$$
​	Siendo $h(t)$ ruido.

![Screenshot_20210420_011900](.images/Screenshot_20210420_011900.png)

​	En la imagen de la izquierda se puede ver una función en el tiempo. En la imagen de la derecha está la función después de aplicarle la transformada de Fourier.

​	El dominio de la imagen de la derecha ya no está en el tiempo, sino que está en frecuencia. Esto es conocido como el __espectro de amplitud__, e indica la distribución de energía que tiene la señal original. 

​	Se puede ver en el espectro de amplitud, que tiene picos en $1$ y $1.5$. Esto coincide con los componentes de la función. De esta manera, se puede descubrir fácilmente la __periodicidad__ de la función.

### 3.5.1 Propiedades

* La transformada de Fourier es invertible.

$$
g(t) = \mathcal{F}^{-1}[G(f)]
$$



* La convolución en el tiempo se convierte en multiplicación en frecuencia y viceverza.

$$
\mathcal{F}[g(t)*y(t)] = \mathcal{F}[g(t)] \mathcal{F}[y(t)] = G(f) Y(f)
$$

* La transformada de Fourier es lineal.

$$
\mathcal{F}[a g_1(t) + b g_2(t) ] = a G_1(f) + b G_2(f)
$$

### 3.5.2 Teoremas

* Teorema de Parseval: La energía de una señal se preserva. La transformada de Fourier no pierde información.
* Teorema de Wiener-Khinchin: la densidad espectral es la potencia asignada a cada frecuencia de señal.

## 3.6 Transformada de Fourier discreta (DFT)

$$
G[k] = \sum_{n=0}^{N-1} g[n] \exp \left( -j 2\pi \frac{k n}{N} \right)
$$

​	Esta transformada, la podemos escribir como:
$$
G[k] = \sum_{n=0}^{N-1} g[n] W_N^{kn}
$$
​	Siendo:
$$
W_N = \exp \left( -j \frac{2\pi}{N} \right)
$$
​	Lo anterior se puede expresar de forma matricial, obteniendo:
$$
\begin{align}
\begin{pmatrix} 
G[0] \\
G[1] \\
G[2] \\
\vdots \\
G[N-1] \\
\end{pmatrix} &=
\begin{pmatrix}
1 & 1 & 1 & \cdots & 1 \\
1 & W_N & W_N^2 & \cdots & W_N^{N-1} \\
1 & W_N^2 & W_N^4 & \cdots & W_N^{N-2} \\
\vdots & \dots & \dots & \ddots &  \vdots \\
1 & W_N^{N-1} & W_N^{N-2} & \cdots & W_N \\
\end{pmatrix} 
\begin{pmatrix} 
g[0] \\
g[1] \\
g[2] \\
\vdots \\
g[N-1] \\
\end{pmatrix} \nonumber  \\
G &= \Omega g,
\end{align}
$$

### 3.6.1 Resolución conda

~~~python
def matrix_DFT(signal):
    N = len(signal)
    W_N = np.exp(-1j*2*np.pi/N)
    n = np.arange(N)
    Omega = W_N**(n*n.reshape(1,-1).T)
    S = np.dot(Omega, signal)
    return S
~~~

## 3.7 Transformada rápida de Fourier

Es un algoritmo que permite ahorrar costo de cómputo al calcularla.
$$
G[k] =  G_E[k] + \exp \left( -j2\pi \frac{k}{N} \right) G_O[k], ~~~ \forall k \in [0,N/2] 
\\
G[k + N/2] =  G_E[k] - \exp \left( -j2\pi \frac{k}{N} \right) G_O[k] \\
$$

### 3.7.1 Resolución conda

~~~python
G = fft.fft(g)
freq = fft.fftfreq(n=len(g), d=1/Fs)
ax.plot(freq, np.abs(G))
~~~



