import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.interpolate import interp1d
from fractions import Fraction

################ Personalización de estilo #####################

st.markdown("""
    <style>
    /* Fondo y sidebar */
    .css-18e3th9 {background-color: lavenderblush; color: lavenderblush;}
    .css-1y4v4l9 {background-color: lavenderblush; color: lavenderblush;}
    .css-1v0mbdj {background-color: lavenderblush;}
    .css-1l0l5lz {color: white;}

    /* Estilo para centrar el título */
    
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: hotpink;  
    }
    
    [data-testid="stSidebar"] {
        background-color: mistyrose;
    
    .subheader {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: palevioletred;
        text-align: center; 
    }
    
    .stButton button {
        background-color: deeppink;
        color: white;
        border: none;
    }
    

    
        /* Cambiar color de fondo de la página completa */
    .main {
        background-color: white;
    }
    
    </style>
    """, unsafe_allow_html=True)


################################ Definiciones de las señales

def signal_1(t):
    return np.where((t >= -2) & (t < -1), 2*t + 4,
            np.where((t >= -1) & (t < 1), 2,
            np.where((t >= 1) & (t <= 2), -2*t + 4, 0)))

def signal_2(t):
    return np.where((t >= -3) & (t < -2), t + 3,
            np.where((t >= -2) & (t < -1), 2,
            np.where((t >= -1) & (t < 0), t + 3,
            np.where((t >= 0) & (t < 2), 3 - t,
            np.where((t >= 2) & (t < 3), 1,0)))))

def signal_3(t):
    return np.array([0,0,0,0,0,-3,0,5,4,-2,-4,-1,2,5,7,4,-2,0,0,0,0,0])

def signal_4(n):
    return np.where((n >= -10) & (n <= -6), 0,
            np.where((n >= -5) & (n <= 0), (2/3)**n,
            np.where((n >= 1) & (n <= 5), (8/5)**n,
            np.where((n >= 6) & (n <= 10), 0, 0))))

t1 = np.linspace(-2, 2, 1000)
func1 = signal_1(t1)

t2 = np.linspace(-3, 3, 1000)
func2 = signal_2(t2)

n3 = np.arange(-5, 17)
func3 = signal_3(n3)

n4 = np.arange(-10, 11)
func4 = signal_4(n4)

################################# Transformaciones

def transform_cont_method1(tiempo, a, to):
    td = tiempo - to
    tnew = td / a
    return tnew

def plot_transform_cont_method1(signal,tiempo, a, to):
    
    st.write('**El metodo 1 consiste en primero desplazar y luego escalar la señal.**')
    
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, signal, color='palevioletred',linewidth=3)
    plt.title('X(t)')
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.grid(True)
    st.pyplot(plt)

    td = tiempo - to
    tn = td / a
    
    if to > 0 and a > 1:
      st.write('**Se adelanta y se comprime la señal.**')
    elif to > 0 and a < 1:
      st.write('**Se adelanta, se refleja y se expande la señal.**')
    elif to > 0 and a ==1:
      st.write('**Se adelanta la señal.**')
    elif to < 0 and a > 1:
      st.write('**Se retarda y se comprime la señal.**')
    elif to < 0 and a < 1:
      st.write('**Se retarda, se refleja y se expande la señal.**')
    elif to < 0 and a ==1:
      st.write('**Se retrasa la señal.**')
    elif to == 0 and a > 1:
      st.write('**Se comprime la señal.**')
    elif to == 0 and a < 1:
      st.write('**Se refleja y se expande la señal.**')
      
    if to < 0:
      st.latex(rf'x(t {to})')
      plt.figure(figsize=(10, 6))
      plt.plot(td, signal, color='deeppink',linewidth=3)
      plt.xlabel('Tiempo')
      plt.ylabel('Amplitud')
      plt.grid(True)
      st.pyplot(plt)
      
    if to > 0:
      st.latex(rf'x(t + {to})')
      plt.figure(figsize=(10, 6))
      plt.plot(td, signal, color='deeppink',linewidth=3)
      plt.xlabel('Tiempo')
      plt.ylabel('Amplitud')
      plt.grid(True)
      st.pyplot(plt)

    if a != 1:
      if to > 0:
        st.latex(rf'x({a}t + {to})')
      if to < 0:
        st.latex(rf'x({a}t  {to})')
      if to == 0:
        st.latex(rf'x({a}t )')
      
      plt.figure(figsize=(10, 6))
      plt.plot(tn, signal, color='indigo',linewidth=3)
      plt.xlabel('Tiempo')
      plt.ylabel('Amplitud')
      plt.title('Señal Transformada')
      plt.xticks(np.arange(min(tn), max(tn) + 1, ))
      plt.grid(True)
      st.pyplot(plt)

def transform_cont_method2(tiempo, a, to):
    tesc = tiempo / a
    if a > 1:
      tnew = tesc - (to / a)
    if a < 1:
      tnew = tesc + (to / a)
    return tnew

def plot_transform_cont_method2(signal,tiempo, a, to):
    
    st.write('**El metodo 2 consiste en primero escalar y luego desplazar.**')
    
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, signal, color='palevioletred',linewidth=3 )
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('X(t)')
    plt.grid(True)
    st.pyplot(plt)
    
    tesc = tiempo / a
    
    tn = tesc - (to/a)
      
    if to > 0 and a > 1:
      st.write('**Se adelanta y se comprime la señal.**')
    elif to > 0 and a < 1:
      st.write('**Se adelanta, se refleja y se expande la señal.**')
    elif to > 0 and a ==1:
      st.write('**Se adelanta la señal.**')
    elif to < 0 and a > 1:
      st.write('**Se retarda y se comprime la señal.**')
    elif to < 0 and a < 1:
      st.write('**Se retarda, se refleja y se expande la señal.**')
    elif to < 0 and a ==1:
      st.write('**Se retrasa la señal.**')
    elif to == 0 and a > 1:
      st.write('**Se comprime la señal.**')
    elif to == 0 and a < 1:
      st.write('**Se refleja y se expande la señal.**')

    if a != 1:
      st.latex(rf'x({a}t)')
      plt.figure(figsize=(10, 6))
      plt.plot(tesc, signal, color='deeppink',linewidth=3)
      plt.xlabel('Tiempo')
      plt.ylabel('Amplitud')
      plt.grid(True)
      st.pyplot(plt)
    
    if to != 0:
      
      to2 = abs(to)
      a2 = abs(a)
      
      if (to > 0 and a > 1) or (to < 0 and a < 1) or (to > 0  and a == 1):
       st.latex(rf'x({a}(t + {to2}/{a2}))')
      else:
       st.latex(rf'x({a}(t - {to2}/{a2}))')
      
      plt.figure(figsize=(10, 6))
      plt.plot(tn, signal, color='indigo',linewidth=3)
      plt.xticks(np.arange(min(tn), max(tn) + 1, ))
      plt.xlabel('Tiempo')
      plt.ylabel('Amplitud')
      plt.grid(True)
      st.pyplot(plt)

def transform_disc_method1 (x_n, n_values, M, n_o , scale): #type = Por ceros, escalo, lineal
  
  #DESPLAZAMIENTO
  size = len(x_n)

  if n_o < 0:
    n_values = n_values + abs(n_o)
  elif n_o > 0:
    n_values = n_values - n_o

  #ESCALAMIENTO
  reflejar = False
  if M < 0: #aqui lo reflejo
    reflejar = True
 
  M = abs(M)  

  if M > 1:
      n_esc = []
      x_esc = []
      for i in range(len(n_values)):
        if n_values[i] >= 0:
          if n_values [i] % M == 0:
            new_n = n_values[i] // M
            n_esc.append(new_n)
            x_esc.append(x_n[i])

  if M < 1:
    size = len(x_n)
    n_in = min(n_values)
    n_fin = max(n_values)
    Z = int(1/M)
    n_esc = np.arange(n_in * (Z), n_fin * (Z) + 1)
    size_esc = len(n_esc)
    x_esc = np.zeros(size_esc)

    if scale == "Ceros":
      for k in range(size_esc-1):
        if k % Z == 0:
          r = int(k * M)
          if r < size:
            x_esc[k] = x_n[r]
          else:
            x_esc[k] = 0

    elif scale == "Escalon":
      for k in range(size_esc):
        r = int(k * M)
        if r < size:
          x_esc[k] = x_n[r]
        else:
          x_esc[k] = x_esc[k-1]

    elif scale == "Lineal":
      k=0
      for i in range(size -1):
        x_esc[k] = x_n[i]
        for j in range(1,Z):
          dif = x_n[i+1] - x_n[i]
          A = j*M*dif + x_n[i]
          x_esc[k+1] = A
          k=k+1
        k=k+1
      x_esc[size_esc -1] = x_n[size-1]
     
  if reflejar == True:
    n_esc = - (n_esc)
  
  return n_esc, x_esc
      
def plot_transform_disc_method1 (x_n, n_values, M, n_o , scale): #type = Por ceros, escalo, lineal
  st.write('**El metodo 1 consiste en primero desplazar y luego escalar la señal.**')
  
  plt.figure(figsize=(10, 6))
  (markerline, stemlines, baseline) = plt.stem(n_values,x_n,linefmt='palevioletred', basefmt='black',markerfmt='o')
  plt.setp(markerline, 'markersize', 12)
  plt.setp(stemlines, 'linewidth', 3) 
  plt.xlabel('n')
  plt.ylabel('Amplitud')
  plt.xticks(np.arange(min(n_values), max(n_values) + 1, 1))
  plt.title('X(n)')
  plt.grid(True)
  plt.show()
  st.pyplot(plt)
      
  reflejar = False
  if M < 0:  
      reflejar = True
  M_text = abs(M)

  # cuando se adelanta
  if n_o > 0:
      if M_text > 1:
          if reflejar:
              st.write('**Se adelanta, se refleja y se diezma la señal.**')
          else:
              st.write('**Se adelanta y se diezma la señal.**')
      elif M_text < 1:
          if reflejar:
              st.write('**Se adelanta, se refleja y se interpola la señal.**')
          else:
              st.write('**Se adelanta y se interpola la señal.**')
      elif M_text == 1:
          if reflejar:
              st.write('**Se adelanta y se refleja la señal.**')
          else:
              st.write('**Se adelanta la señal.**')

  # cuando se retrasa
  elif n_o < 0:
      if M_text > 1:
          if reflejar:
              st.write('**Se retarda, se refleja y se diezma la señal.**')
          else:
              st.write('**Se retarda y se diezma la señal.**')
      elif M_text < 1:
          if reflejar:
              st.write('**Se retarda, se refleja y se interpola la señal.**')
          else:
              st.write('**Se retarda y se interpola la señal.**')
      elif M_text == 1:
          if reflejar:
              st.write('**Se retarda y se refleja la señal.**')
          else:
              st.write('**Se retarda la señal.**')

  # sin desp
  elif n_o == 0:
      if M_text > 1:
          if reflejar:
              st.write('**Se diezma y se refleja la señal.**')
          else:
              st.write('**Se diezma la señal.**')
      elif M_text < 1:
          if reflejar:
              st.write('**Se interpola y se refleja la señal.**')
          else:
              st.write('**Se interpola la señal.**')
      elif M_text == 1:
          if reflejar:
              st.write('**Se refleja la señal.**')
          else:
              st.write('**La señal no cambia.**')

  #DESPLAZAMIENTO
  size = len(x_n)

  if n_o < 0:
    n_values = n_values + abs(n_o)
  elif n_o > 0:
    n_values = n_values - n_o

  if n_o != 0:
    
    if n_o < 0:
      st.latex(rf'x(n {n_o})')
    if n_o > 0:
      st.latex(rf'x(n + {n_o})')
      
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_values,x_n,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 12)
    plt.setp(stemlines, 'linewidth', 3) 
    plt.xticks(np.arange(min(n_values), max(n_values) + 1, 1))
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)

  #ESCALAMIENTO

  
  M_org = M
  M = abs(M)  

  if M > 1:
      n_esc = []
      x_esc = []
      for i in range(len(n_values)):
        if n_values [i] % M == 0:
          new_n = n_values[i] // M
          n_esc.append(new_n)
          x_esc.append(x_n[i])

  if M < 1:
    size = len(x_n)
    n_in = min(n_values)
    n_fin = max(n_values)
    Z = int(1/M)
    n_esc = np.arange(n_in * (Z), n_fin * (Z) + 1)
    size_esc = len(n_esc)
    x_esc = np.zeros(size_esc)

    if scale == "Ceros":
      for k in range(size_esc-1):
        if k % Z == 0:
          r = int(k * M)
          if r < size:
            x_esc[k] = x_n[r]
          else:
            x_esc[k] = 0

    elif scale == "Escalon":
      for k in range(size_esc):
        r = int(k * M)
        if r < size:
          x_esc[k] = x_n[r]
        else:
          x_esc[k] = x_esc[k-1]

    elif scale == "Lineal":
      k=0
      for i in range(size -1):
        x_esc[k] = x_n[i]
        for j in range(1,Z):
          dif = x_n[i+1] - x_n[i]
          A = j*M*dif + x_n[i]
          x_esc[k+1] = A
          k=k+1
        k=k+1
      x_esc[size_esc -1] = x_n[size-1]
    
  if M != 1:
    
    M2 = Fraction(M).limit_denominator()
    
    if n_o < 0:
      st.latex(rf'x({M2}n {n_o})')
    if n_o > 0:
      st.latex(rf'x({M2}n + {n_o})')
    if n_o == 0:
      st.latex(rf'x({M2}n)')

    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_esc,x_esc,linefmt='indigo', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 4)
    plt.setp(stemlines, 'linewidth', 2) 
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
    
    if reflejar == True:
      
      n_esc = - np.array(n_esc)
      
      if n_o < 0:
        st.latex(rf'x(-{M2}n {n_o})')
      if n_o > 0:
        st.latex(rf'x(-{M2}n + {n_o})')
      if n_o == 0:
        st.latex(rf'x(-{M2}n)')
      
      plt.figure(figsize=(10, 6))
      (markerline, stemlines, baseline) = plt.stem(n_esc,x_esc,linefmt='darkcyan', basefmt='black',markerfmt='o')
      plt.setp(markerline, 'markersize', 4)
      plt.setp(stemlines, 'linewidth', 2) 
      plt.xlabel('n')
      plt.ylabel('Amplitud')
      plt.title('Señal reflejada')
      plt.grid(True)
      plt.show()
      st.pyplot(plt)
      
  if M_org == -1:
    
    M2 = Fraction(M).limit_denominator()
    
    if n_o < 0:
      st.latex(rf'x(-{M2}n {n_o})')
    if n_o > 0:
      st.latex(rf'x(-{M2}n + {n_o})')
    if n_o == 0:
      st.latex(rf'x(-{M2}n)')
    
    n_esc = - np.array(n_values)
    
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_esc,x_n,linefmt='darkcyan', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 4)
    plt.setp(stemlines, 'linewidth', 2) 
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.title('Señal reflejada')
    plt.xticks(np.arange(min(n_esc), max(n_esc) + 1, 1))
    plt.grid(True)
    plt.show()
    st.pyplot(plt)

def plot_transform_disc_method2 (x_n, n_values, M, n_o , scale):
  
  st.write('**El metodo 2 consiste en primero escalar y luego desplazar la señal.**')
  
  M_org = M
  n_values_org = n_values
  x_n_org = x_n

  #grafico la original
  plt.figure(figsize=(10, 6))
  (markerline, stemlines, baseline) = plt.stem(n_values,x_n,linefmt='palevioletred', basefmt='black',markerfmt='o')
  plt.setp(markerline, 'markersize', 12)
  plt.setp(stemlines, 'linewidth', 3)
  plt.xlabel('n')
  plt.ylabel('Amplitud')
  plt.xticks(np.arange(min(n_values), max(n_values) + 1, 1))
  plt.title('X(n)')
  plt.grid(True)
  plt.show()
  st.pyplot(plt)
  
  reflejar = False
  if M < 0:  
      reflejar = True
  
  interp = 0
  diezmar = 0
  if abs (M) < 1:
    interp = True
  elif abs(M) > 1:
    diezmar = True
  
  M_text = abs(M)
      
  if n_o > 0:
      if M_text > 1:
          if reflejar:
              st.write('**Se adelanta, se refleja y se diezma la señal.**')
          else:
              st.write('**Se adelanta y se diezma la señal.**')
      elif M_text < 1:
          if reflejar:
              st.write('**Se adelanta, se refleja y se interpola la señal.**')
          else:
              st.write('**Se adelanta y se interpola la señal.**')
      elif M_text == 1:
          if reflejar:
              st.write('**Se adelanta y se refleja la señal.**')
          else:
              st.write('**Se adelanta la señal.**')

  # cuando se retrasa
  elif n_o < 0:
      if M_text > 1:
          if reflejar:
              st.write('**Se retarda, se refleja y se diezma la señal.**')
          else:
              st.write('**Se retarda y se diezma la señal.**')
      elif M_text < 1:
          if reflejar:
              st.write('**Se retarda, se refleja y se interpola la señal.**')
          else:
              st.write('**Se retarda y se interpola la señal.**')
      elif M_text == 1:
          if reflejar:
              st.write('**Se retarda y se refleja la señal.**')
          else:
              st.write('**Se retarda la señal.**')

  # sin desp
  elif n_o == 0:
      if M_text > 1:
          if reflejar:
              st.write('**Se diezma y se refleja la señal.**')
          else:
              st.write('**Se diezma la señal.**')
      elif M_text < 1:
          if reflejar:
              st.write('**Se interpola y se refleja la señal.**')
          else:
              st.write('**Se interpola la señal.**')
      elif M_text == 1:
          if reflejar:
              st.write('**Se refleja la señal.**')
          else:
              st.write('**La señal no cambia.**')

  M2 = Fraction(abs(M)).limit_denominator()
  
  if M != 1 and M_org != -1:
    st.latex(rf'x({M2}n)')
    
  M = abs(M)

  # DIEZMADOOOO

  if M > 1:
    
    # AQUI QUEDA IGUAL PARA PODER GRAFICAR EL ESCALAMIENTO
    n_aux = []
    x_aux = []

    for i in range(len(n_values)):
      if n_values [i] % M == 0:
        new_n = n_values[i] // M
        n_aux.append(new_n)
        x_aux.append(x_n[i])

    #GRAFICO SEÑAL DIEZMADA
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_aux,x_aux,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 12)
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.xticks(np.arange(min(n_aux), max(n_aux) + 1, 1))
    plt.grid(True)
    plt.show()
    st.pyplot(plt)

    # ESTA ES LA QUE USAREMOS AL DESPLAZAR
    n_esc = []
    x_esc = []

    for i in range(len(n_values)):
        new_n = n_values[i] / M
        n_esc.append(new_n)
        x_esc.append(x_n[i])

    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_esc,x_esc,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 12)
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.title('para depsues')
    plt.xticks(np.arange(min(n_esc), max(n_esc) + 1, ))
    plt.grid(True)
    plt.show()
    #st.pyplot(plt) ESTA SE USA PARA REVISAR ERRORESPERO NO HACE PARTE DE LA INTERFAZ
  
  #interpolo
  if M < 1:
    
    size = len(x_n)
    n_in = min(n_values)
    n_fin = max(n_values)
    Z = int(1/M)
    n_esc = np.arange(n_in * (Z), n_fin * (Z) + 1)
    size_esc = len(n_esc)
    x_esc = np.zeros(size_esc)

    if scale == "Ceros":
      for k in range(size_esc-1):
        if k % Z == 0:
          r = int(k * M)
          if r < size:
            x_esc[k] = x_n[r]
          else:
            x_esc[k] = 0

    elif scale == "Escalon":
      for k in range(size_esc):
        r = int(k * M)
        if r < size:
          x_esc[k] = x_n[r]
        else:
          x_esc[k] = x_esc[k-1]

    elif scale == "Lineal":
      k=0
      for i in range(size -1):
        x_esc[k] = x_n[i]
        for j in range(1,Z):
          dif = x_n[i+1] - x_n[i]
          A = j*M*dif + x_n[i]
          x_esc[k+1] = A
          k=k+1
        k=k+1
      x_esc[size_esc -1] = x_n[size-1]

    # GRAFICO SEÑAL INTERPOLADA
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_esc,x_esc,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 7)
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud') 
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
  
  #REFLEJAR PARA M=-1
  
  if M_org == -1:
  
    st.latex(rf'x(-{M2}n)')
    
    n_esc = - np.array(n_values)
    x_esc = x_n
    
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_esc,x_n,linefmt='darkcyan', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 4)
    plt.setp(stemlines, 'linewidth', 2) 
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.title('Señal reflejada')
    plt.xticks(np.arange(min(n_esc), max(n_esc) + 1, 1))
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
    
  #REFLEJAR PARA M FRACCION
    
  if reflejar == True and interp == True:
    st.latex(rf'x(-{M2}n)')
    n_esc = - np.array(n_esc)

    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_esc,x_esc,linefmt='darkcyan', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 4)
    plt.setp(stemlines, 'linewidth', 2) 
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.title('Señal reflejada')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
    
    x_esc = np.flip(x_esc)
    
  #REFLEJADA PARA M INT
  if reflejar == True and diezmar == True: 
    
    st.latex(rf'x(-{M2}n)')
    n_aux= - np.array(n_aux)
    n_esc = -np.array(n_esc)
    
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_aux,x_aux,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 12)
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.title('Señal reflejada')
    plt.xticks(np.arange(min(n_aux), max(n_aux) + 1, 1 ))
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
    
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_esc,x_esc,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 12)
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.title('Señal reflejada COMPLETAAA')
    plt.xticks(np.arange(min(n_aux), max(n_aux) + 1, 1 ))
    plt.grid(True)
    plt.show()
    #st.pyplot(plt) ESTA SE USA PARA REVISAR ALGUN ERROR PERO NO HACE PARTE DE LA INTERFAZ

  # DESPLAZAMIENTO
  n_o2 = abs(n_o)
  
  # PARA M=1
  
  if n_o != 0 and M_org == 1:
    
    x_fin = x_n_org
    if n_o < 0:
      st.latex(rf'x(n - {n_o2})')
      n_fin = n_values_org + abs(n_o)
    elif n_o > 0:
      st.latex(rf'x(n + {n_o2})')
      n_fin = n_values_org - abs(n_o)

    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_fin,x_fin,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 5)
    plt.xticks(np.arange(min(n_fin), max(n_fin) + 1,  ))
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
    
  if reflejar == True : #o sea que M<1
    if n_o > 0:
      st.latex(rf'x({-M2}(n - {n_o2}/{M2}))')
    elif n_o < 0:
      st.latex(rf'x({-M2}(n + {n_o2}/{M2}))')
  elif reflejar == False and M!= 1:
    if n_o > 0:
      st.latex(rf'x({M2}(n + {n_o2}/{M2}))')
    elif n_o < 0:
      st.latex(rf'x({M2}(n +-{n_o2}/{M2}))')
  
  # PARA M = -1
  
  if n_o !=0  and M_org == -1:
    
    x_fin = np.flip(x_esc)
    if n_o < 0:
      n_desp = n_esc - (abs(n_o)/M)
    elif n_o > 0:
        n_desp = n_esc + (abs(n_o)/M)
    
    n_fin =n_desp
  
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_fin,x_fin,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 5)
    plt.xticks(np.arange(min(n_fin), max(n_fin) + 1,  ))
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
  
  #PARA M FRACCIONARIO
   
  if n_o != 0 and interp == True:
    
    if reflejar == True:
      x_esc = np.flip(x_esc)
      if n_o < 0:
        n_desp = n_esc - (abs(n_o)/M)
      else:
        n_desp = n_esc + (abs(n_o)/M)
    else:
      if n_o < 0:
        n_desp = n_esc + (abs(n_o)/M)
      else:
        n_desp = n_esc - (abs(n_o)/M)
    
    x_desp = []
    for i in range(len(n_desp)):
      x_desp.append(x_esc[i])
    
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n_desp,x_desp,linefmt='indigo', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 6)
    plt.setp(stemlines, 'linewidth', 3)
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
  
  #PARA M ENTERO
  
  if n_o != 0 and diezmar == True:
    
    n_esc = np.array(n_esc)
    
    # PARA VALORES POSITIVOS
    if reflejar == False:
      if n_o < 0:
        n_desp = n_esc + (abs(n_o)/M)
      else:
        n_desp = n_esc - (abs(n_o)/M)
      
      x_fin = []
      n_fin = []
      for i in range(len(n_desp)):
        if n_desp [i] % 1  == 0:
          new_n = n_desp[i]
          n_fin.append(new_n)
          x_fin.append(x_esc[i])

      plt.figure(figsize=(10, 6))
      (markerline, stemlines, baseline) = plt.stem(n_fin,x_fin,linefmt='indigo', basefmt='black',markerfmt='o')
      plt.setp(markerline, 'markersize', 6)
      plt.setp(stemlines, 'linewidth', 3)
      plt.xticks(np.arange(min(n_fin), max(n_fin) + 1, 1 ))
      plt.xlabel('n')
      plt.ylabel('Amplitud')
      plt.grid(True)
      plt.show()
      st.pyplot(plt)
    
    #PARA VALORES NEGATIVOS
    if reflejar == True:
      
      if n_o < 0:
        n_desp = n_esc - (abs(n_o)/M)
      elif n_o >0:
        n_desp = n_esc + (abs(n_o)/M)
      
      x_fin = []
      n_fin = []
      for i in range(len(n_desp)):
        if n_desp [i] % 1  == 0:
          new_n = n_desp[i]
          n_fin.append(new_n)
          x_fin.append(x_esc[i])

      plt.figure(figsize=(10, 6))
      (markerline, stemlines, baseline) = plt.stem(n_fin,x_fin,linefmt='indigo', basefmt='black',markerfmt='o')
      plt.setp(markerline, 'markersize', 6)
      plt.setp(stemlines, 'linewidth', 3)
      plt.xticks(np.arange(min(n_fin), max(n_fin) + 1, 1 ))
      plt.xlabel('n')
      plt.ylabel('Amplitud')
      plt.grid(True)
      plt.show()
      st.pyplot(plt)

################################ SUMAS

def plot_suma_cont1 (transform_cont_method1, t):
  
  st.write('**En esta sección encontará un ejemplo de como sumar dos señales, tomando como base X(t)**')
  st.write('**A la cual se le realizarán dos tranformaciones, para luego sumarlas.**')
  
  signal_org = signal_1(t)

  plt.figure(figsize=(10, 6))
  plt.plot(t,signal_org, color= 'palevioletred', linewidth=2)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.title('X(t)')
  plt.legend()
  plt.grid(True)
  st.pyplot(plt)

  time1 = transform_cont_method1(t,-1/3,1/4)
  time2 = transform_cont_method1(t,1/2,-1/3)
  
  st.text('Transformación 1 ----> X1 ----> Color: azul')
  st.text('Transformación 2 ----> X2 ----> Color: rosa')
  
  st.latex(r'x\left(\frac{1}{4} - \frac{t}{3}\right) + x\left(\frac{t}{2} - \frac{1}{3}\right)')

  plt.figure(figsize=(10, 6))
  plt.plot(time1,signal_org, color= 'lightseagreen', label= 'X_1', linewidth=2)
  plt.plot(time2,signal_org, color='deeppink', linestyle='--', label= 'X_2',linewidth=2)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.legend()
  plt.grid(True)
  st.pyplot(plt)

  f1_c1 = interp1d(time1,signal_org,kind='linear',fill_value=0,bounds_error=False)
  f2_c1 = interp1d(time2,signal_org,kind='linear',fill_value=0,bounds_error=False)

  delta_c1 = np.linspace(-6,7.5,10000)

  x1_c1 = f1_c1(delta_c1)
  x2_c1 = f2_c1(delta_c1)
  
  st.text('Se deben ajustar las señales para que tengan la misma cantidad de espacios en t:')
  plt.subplot(1,2,1)
  plt.figure(figsize=(10, 6))
  plt.plot(delta_c1,x1_c1, color= 'lightseagreen', label='X_1', linewidth=2)
  plt.plot(delta_c1,x2_c1, color='deeppink', linestyle='--',label='X_2', linewidth=2)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.legend()
  plt.grid(True)
  st.pyplot(plt)

  suma_c1 = x1_c1 + x2_c1
  
  
  st.write('**Suma:**')
  plt.subplot(1,2,2)
  plt.figure(figsize=(10, 6))
  plt.plot(delta_c1,suma_c1, color='mediumorchid', linewidth=5)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.title('X = X_1 +X_2')
  plt.legend()
  plt.grid(True)
  st.pyplot(plt)
  
def plot_suma_cont2 (transform_cont_method1, t):
  
  st.write('**En esta sección encontará un ejemplo de como sumar dos señales, tomando como base X(t)**')
  st.write('**A la cual se le realizarán dos tranformaciones, para luego sumarlas.**')

  signal_org = signal_2(t)
  
  plt.figure(figsize=(10, 6))
  plt.plot(t,signal_org, color= 'palevioletred', linewidth=2)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.title('X(t)')
  plt.legend()
  plt.grid(True)
  st.pyplot(plt)

  time1 = transform_cont_method1(t,-1/3,1/4)
  time2 = transform_cont_method1(t,1/2,-1/3)
  
  st.text('Transformación 1 ----> X1 ----> Color: azul')
  st.text('Transformación 2 ----> X2 ----> Color: rosa')
  
  st.latex(r'x\left(\frac{1}{4} - \frac{t}{3}\right) + x\left(\frac{t}{2} - \frac{1}{3}\right)')

  plt.figure(figsize=(10, 6))
  plt.plot(time1,signal_org, color= 'lightseagreen', label= 'X_1',linewidth=2)
  plt.plot(time2,signal_org, color='deeppink', linestyle='--', label= 'X_2',linewidth=2)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.legend()
  plt.grid(True)
  st.pyplot(plt)

  f1_c1 = interp1d(time1,signal_org,kind='linear',fill_value=0,bounds_error=False)
  f2_c1 = interp1d(time2,signal_org,kind='linear',fill_value=0,bounds_error=False)

  delta_c1 = np.linspace(-10,11,10000)

  x1_c1 = f1_c1(delta_c1)
  x2_c1 = f2_c1(delta_c1)
  
  st.text('Se deben ajustar las señales para que tengan la misma cantidad de espacios en t:')
  plt.figure(figsize=(10, 6))
  plt.plot(delta_c1,x1_c1, color= 'lightseagreen', label='X_1',linewidth=2)
  plt.plot(delta_c1,x2_c1, color='deeppink', linestyle='--',label='X_2',linewidth=2)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.legend()
  plt.grid(True)
  st.pyplot(plt)

  suma_c1 = x1_c1 + x2_c1
  
  st.write('**Suma:**')
  plt.figure(figsize=(10, 6))
  plt.plot(delta_c1,suma_c1, color='mediumorchid',linewidth=5)
  plt.xlabel('Tiempo')
  plt.ylabel('Amplitud')
  plt.legend()
  plt.title('X = X_1 +X_2')
  plt.grid(True)
  st.pyplot(plt)

def suma_disc (transform_disc_method1, signal_org, n_values, scale2):
  
  st.write('**En esta sección encontará un ejemplo de como sumar dos señales, tomando como base x[n]**')
  st.write('**A la cual se le realizarán dos tranformaciones, para luego sumarlas.**')
  
  plt.figure(figsize=(12, 6))
  (markerline, stemlines, baseline) = plt.stem(n_values,signal_org,linefmt='palevioletred', basefmt='black',markerfmt='o')
  plt.setp(markerline, 'markersize', 12)
  plt.setp(stemlines, 'linewidth', 3) 
  plt.legend()
  plt.grid(True)
  plt.title('x[n]')
  plt.xticks(np.arange(min(n_values), max(n_values) + 1, 1))
  plt.xlabel('n')
  plt.ylabel('Amplitud')
  plt.show()
  st.pyplot(plt)
  
  st.text('Transformación 1 ----> X1 ----> Color: azul')
  st.text('Transformación 2 ----> X2 ----> Color: rosa')
  
  st.latex(r'x\left[ 4 - \frac{n}{3}\right] + x\left[\frac{n}{4} - 3\right]')

  n1_values, x1 = transform_disc_method1(signal_org, n_values, M=-1/3, n_o = 4, scale = scale2 )
  n2_values, x2 = transform_disc_method1(signal_org, n_values, M=1/4, n_o =-3, scale = scale2)

  col1, col2 = st.columns(2)
  
  with col1:
    plt.figure(figsize=(12, 6))
    (markerline, stemlines, baseline) = plt.stem(n1_values,x1,linefmt='lightseagreen', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 8)
    plt.setp(stemlines, 'linewidth', 2) 
    plt.title('X1[n]')
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.xticks(np.arange(min(n1_values), max(n1_values) + 1, 3))
    plt.legend()
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
    
    x1 = np.flip(x1)
    
  with col2:
    plt.figure(figsize=(12, 6))
    (markerline, stemlines, baseline) = plt.stem(n2_values,x2,linefmt='deeppink', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 8)
    plt.setp(stemlines, 'linewidth', 2) 
    plt.xticks(np.arange(min(n2_values), max(n2_values) + 1,3))
    plt.title('X2[n]')
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.legend()
    plt.grid(True)
    plt.show()
    st.pyplot(plt)
    
  # Alinear las señales para la suma (asegurarse de que tengan el mismo rango de índices)
  min_n1 = min(n1_values)
  min_n2 = min(n2_values)
  max_n1 = max(n1_values)
  max_n2 = max(n2_values)
  
  n_combined = np.arange(min(min_n1,min_n2),max(max_n1,max_n2)+1)   

  # Extender las señales transformadas a este rango
  x1_extended = np.zeros(len(n_combined),dtype=float)
  x2_extended = np.zeros(len(n_combined),dtype=float)


  # Llenar los valores de las señales transformadas en los nuevos índices combinados
  x1_extended[np.isin(n_combined, n1_values)] = x1 
  x2_extended[np.isin(n_combined, n2_values)] = x2

  # Suma de las señales transformadas
  suma_x = x1_extended + x2_extended

  # Graficar la señal resultante de la suma
  plt.figure(figsize=(12, 6))
  (markerline, stemlines, baseline) = plt.stem(n_combined,suma_x,linefmt='mediumorchid', basefmt='black',markerfmt='o')
  plt.setp(markerline, 'markersize', 6)
  plt.setp(stemlines, 'linewidth', 2) 
  plt.xticks(np.arange(min(n_combined), max(n_combined) + 1,4))
  plt.title('X1[n] + X2[n]')
  plt.xlabel('n')
  plt.ylabel('Amplitud')
  plt.grid()  
  plt.show()
  st.pyplot(plt)

def plot_signal(signal, t):
    plt.figure(figsize=(10, 6))
    plt.plot(t, signal, color='palevioletred',linewidth=4)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.title('X(t)')
    plt.grid(True)
    st.pyplot(plt)

def stem (signal, n):
    plt.figure(figsize=(10, 6))
    (markerline, stemlines, baseline) = plt.stem(n, signal,linefmt='palevioletred', basefmt='black',markerfmt='o')
    plt.setp(markerline, 'markersize', 12)
    plt.setp(stemlines, 'linewidth', 3) 
    plt.xticks(np.arange(min(n), max(n) + 1, 1))
    plt.xlabel('n')
    plt.ylabel('Amplitud')
    plt.title('X[n]')
    plt.grid()
    plt.show()
    st.pyplot(plt)
    
########################## Interfaz de usuario

st.markdown('<div class="title">Transformación de Señales</div>', unsafe_allow_html=True)

st.sidebar.subheader('Autores')
st.sidebar.text('Juan David Barceló Barraza')
st.sidebar.text('Isabella María Chacón Villa')
st.sidebar.text('Elkin David Pulgar Arroyo')

st.sidebar.header('Opciones ')

# Selección de señal
signal_type = st.sidebar.selectbox('Selecciona la señal', ('Seleccionar','Señal Continua', 'Señal Discreta' ))

if signal_type == 'Señal Continua':
    # Rango de tiempo
    
    signal_option = st.sidebar.selectbox('Selecciona la señal continua', ('Seleccionar','Señal continua 1', 'Señal continua 2'))

    if signal_option == 'Señal continua 1':
        t = np.linspace(-5, 5, 1000)
        signal = signal_1(1)
    elif signal_option == 'Señal continua 2':
        t = t2 = np.linspace(-3, 3, 1000)
        signal = signal_2(2)
    
    action = st.sidebar.selectbox('Selecciona la acción', ('Ver', 'Transformar','Sumar'))
    
    if action == 'Ver':
        if signal_option == 'Señal continua 1':
            plot_signal(func1,t1)
        elif signal_option == 'Señal continua 2':
            plot_signal(func2,t2)
               
    elif action == 'Transformar':
        
        method = st.sidebar.selectbox('Selecciona el método de transformación', ('Método 1', 'Método 2'))

        # Lista de valores permitidos para el desplazamiento
        escalamiento_opciones = [-5, -4, -3, -2, -1,-1/2, -1/3,-1/4, -1/5, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5]
        # Lista de valores permitidos para el escalamiento
        desplazamiento_opciones = [0,1,2,3,4,5, 6, -6, -5, -4, -3, -2, -1]
        
        
        a = st.sidebar.select_slider('Escalamiento (a)', options=escalamiento_opciones, value=1)


        # Crear un slider para el escalamiento, basado en índices de la lista de opciones
        index_desplazamiento = st.sidebar.slider(
            'Desplazamiento (to)', 
            min_value=-6, 
            max_value = 6, 
            value=0  # Valor predeterminado (primer índice)
        )

        # Obtener el valor seleccionado basado en el índice
        to = desplazamiento_opciones[index_desplazamiento]
        
        a = Fraction(a).limit_denominator()
        to = Fraction(to).limit_denominator()

        # Mostrar los valores seleccionados (para depuración o verificación)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<p style="background-color: purple; text-align: center; border-radius: 10px; padding: 10px;color: white;"><strong>Escalamiento seleccionado: {a}</p>', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'<p style="background-color: #C71585; padding: 10px; border-radius: 10px; text-align: center;color: white;"><strong>Desplazamiento seleccionado: {to}</p>', unsafe_allow_html=True)

        if method == 'Método 1':
            st.subheader('Método 1')
            if signal_option == 'Señal continua 1':
                plot_transform_cont_method1(func1,t1, a, to)
            elif signal_option == 'Señal continua 2':
                plot_transform_cont_method1(func2,t2, a, to)
                
        elif method == 'Método 2':
            st.subheader('Método 2')
            if signal_option == 'Señal continua 1':
                plot_transform_cont_method2(func1,t1, a, to)
            elif signal_option == 'Señal continua 2':
                plot_transform_cont_method2(func2,t2, a, to)
        
    elif action == 'Sumar':

        if signal_option == 'Señal continua 1':
            t1 = np.linspace(-2, 2, 1000)
            plot_suma_cont1(transform_cont_method1, t1)
        elif signal_option == 'Señal continua 2':
            t2 = np.linspace(-3, 3, 1000)
            plot_suma_cont2(transform_cont_method1, t2)
            
elif signal_type == 'Señal Discreta':

    signal_option = st.sidebar.selectbox('Selecciona la señal discreta', ('Seleccionar','Señal Discreta 1', 'Señal Discreta 2'))
    
    action = st.sidebar.selectbox('Selecciona la acción', ('Ver', 'Transformar', 'Sumar'))

    if action == 'Ver':
        if signal_option == 'Señal Discreta 1':
            signal = signal_3(n3)
            stem (signal, n3)
        elif signal_option == 'Señal Discreta 2':
            signal = signal_4(n4)
            stem (signal, n4)
    
    elif action == 'Transformar':
      
        method = st.sidebar.selectbox('Selecciona el método de trasnformación', ('Método 1', 'Método 2'))
        
        interpolate = st.sidebar.selectbox('Selecciona el método de interpolación', ('Ceros', 'Escalon','Lineal'))
        
        escalamiento_opciones =  [-5, -4, -3, -2, -1,-1/2, -1/3,-1/4, -1/5, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5]

        # Lista de valores permitidos para el escalamiento
        desplazamiento_opciones =  [0,1,2,3,4,5, 6, -6, -5, -4, -3, -2, -1]
        

        
        M = st.sidebar.select_slider('Escalamiento (a)', options=escalamiento_opciones, value=1)
        M2 = M

        # Crear un slider para el escalamiento, basado en índices de la lista de opciones
        index_desplazamiento = st.sidebar.slider(
            'Desplazamiento (n_o)', 
            min_value= -6, 
            max_value= 6, 
            value=0  # Valor predeterminado (primer índice)
        )

        # Obtener el valor seleccionado basado en el índice
        n_o = desplazamiento_opciones[index_desplazamiento]
        n_o2 = n_o
        
        M = Fraction(M).limit_denominator()
        n_o = Fraction(n_o).limit_denominator()

        # Mostrar los valores seleccionados (para depuración o verificación)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<p style="background-color: purple; text-align: center; border-radius: 10px; padding: 10px;color: white;"><strong>Escalamiento seleccionado: {M}</p>', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'<p style="background-color: #C71585; padding: 10px; border-radius: 10px; text-align: center;color: white;"><strong>Desplazamiento seleccionado: {n_o}</p>', unsafe_allow_html=True)
        
        if method == 'Método 1':
          st.subheader('Método 1')
          if interpolate == 'Ceros':
              scale = 'Ceros'
              if signal_option == 'Señal Discreta 1':
                  plot_transform_disc_method1 (func3, n3, M2, n_o2 , scale)
              elif signal_option == 'Señal Discreta 2':
                  plot_transform_disc_method1 (func4, n4, M2, n_o2 , scale)
          elif interpolate == 'Escalon':
              scale = 'Escalon'
              if signal_option == 'Señal Discreta 1':
                  plot_transform_disc_method1 (func3, n3, M2, n_o2 , scale)
              elif signal_option == 'Señal Discreta 2':
                  plot_transform_disc_method1 (func4, n4, M2, n_o2 , scale)
          elif interpolate == 'Lineal':
              scale = 'Lineal'
              if signal_option == 'Señal Discreta 1':
                  plot_transform_disc_method1 (func3, n3, M2, n_o2 , scale)
              elif signal_option == 'Señal Discreta 2':
                  plot_transform_disc_method1 (func4, n4, M2, n_o2 , scale)
        elif method == 'Método 2':
          st.subheader('Método 2')
          if interpolate == 'Ceros':
              scale = 'Ceros'
              if signal_option == 'Señal Discreta 1':
                  plot_transform_disc_method2 (func3, n3, M2, n_o2 , scale)
              elif signal_option == 'Señal Discreta 2':
                  plot_transform_disc_method2 (func4, n4, M2, n_o2 , scale)
          elif interpolate == 'Escalon':
              scale = 'Escalon'
              if signal_option == 'Señal Discreta 1':
                  plot_transform_disc_method2 (func3, n3, M2, n_o2 , scale)
              elif signal_option == 'Señal Discreta 2':
                  plot_transform_disc_method2 (func4, n4, M2, n_o2 , scale)
          elif interpolate == 'Lineal':
              scale = 'Lineal'
              if signal_option == 'Señal Discreta 1':
                  plot_transform_disc_method2 (func3, n3, M2, n_o2 , scale)
              elif signal_option == 'Señal Discreta 2':
                  plot_transform_disc_method2 (func4, n4, M2, n_o2 , scale)

        
    elif action == 'Sumar':
        
        interpolate = st.sidebar.selectbox('Selecciona el método de interpolación', ('Ceros', 'Escalon','Lineal'))
        
        if interpolate == 'Ceros':
            scale2 = 'Ceros'
            if signal_option == 'Señal Discreta 1':
                suma_disc (transform_disc_method1, signal_3(n3),n3, scale2)
            elif signal_option == 'Señal Discreta 2':
                suma_disc (transform_disc_method1, signal_4(n4),n4, scale2)
        elif interpolate == 'Escalon':
            scale2 = 'Escalon'
            if signal_option == 'Señal Discreta 1':
                suma_disc (transform_disc_method1, signal_3(n3), n3,scale2)
            elif signal_option == 'Señal Discreta 2':
                suma_disc (transform_disc_method1, signal_4(n4), n4,scale2)
        elif interpolate == 'Lineal':
            scale2 = 'Lineal'
            if signal_option == 'Señal Discreta 1':
                suma_disc (transform_disc_method1, signal_3(n3),n3, scale2)
            elif signal_option == 'Señal Discreta 2':
                suma_disc (transform_disc_method1, signal_4(n4),n4, scale2)

            
        
        
        
        



