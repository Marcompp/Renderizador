import numpy as np
import matplotlib.pyplot as plt

# Faz o setup para desenhar gráficos
def graph():
    fig = plt.figure()
    ax = plt.axes()
    plt.grid()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-9, 5)
    ax.axhline(0, color='black') # deixa o X do eixo 0 em destaque
    ax.axvline(0, color='black') # deixa o Y do eixo 0 em destaque
    ax.set_aspect('equal') # Não suportado em todas as plataformas
    ax.set(xlabel='x', ylabel='y')
    fig.tight_layout()
    return ax

# Desenha um quadrado a partir dos vértices e cor fornecida
def draw_square(points, color="red"):
    plt.scatter(points[0], points[1], s=5, color=color)
    patch = plt.Polygon(points.transpose()[:,0:2], color=color)
    plt.gca().add_patch(patch)
    
def quadradoh(x=1.0, y=1.0):
    # Pontos de um quadrado em coordenadas homogêneas centrado na origem
    p_quadrado = np.array([[ x/2, -x/2, -x/2,  x/2],
                           [ y/2,  y/2, -y/2, -y/2],
                           [ 1.0,  1.0,  1.0,  1.0]])
    return p_quadrado

def identity():
    m = np.array([[ 1.0, 0.0, 0.0],
                  [ 0.0, 1.0, 0.0],
                  [ 0.0, 0.0, 1.0]])
    return m

def translate(x, y):
    m = np.array([[ 1.0, 0.0,  x ],
                  [ 0.0, 1.0,  y ],
                  [ 0.0, 0.0, 1.0]])
    return m
    
def rotate(angle):
    m = np.array([[ np.cos(angle), -np.sin(angle), 0.0],
                  [ np.sin(angle),  np.cos(angle), 0.0],
                  [ 0.0, 0.0, 1.0]])
    return m

def scale(x, y):
    m = np.array([[  x , 0.0, 0.0],
                  [ 0.0,  y , 0.0],
                  [ 0.0, 0.0, 1.0]])
    return m


ax = graph() # configura o espaço para desenhar um gráfico 2D

# Função para empilhar uma matriz
def pushmatrix(m):
    #### Implemente a rotina de empilhar uma matriz na pilha ####
    pass

# Função para desempilhar uma matriz
def popmatrix():
    #### Implemente a rotina para desempilhar uma matriz da pilha ####
    # return m
    pass

# Identidade
m = identity()


#### Espaço para as suas rotinas ####

#####################################


# Tronco
vertices = quadradoh(2,4)
vertices = np.matmul(m, vertices)
draw_square(vertices, "green") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Cabeça
r = rotate(0.3)
m = np.matmul(r, m)
t = translate(0,3)
m = np.matmul(t, m)
vertices = quadradoh(1,1.3)
vertices = np.matmul(m, vertices)
draw_square(vertices, "blue") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Braço esquerdo
t = translate(-1.5,0.6)
m = np.matmul(t, m)
vertices = quadradoh(0.5,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "chocolate") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Antebraço esquerdo
t = translate(0.0,-2.8)
m = np.matmul(t, m)
vertices = quadradoh(0.5,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "rebeccapurple") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Mão esquerda
t = translate(0.0,-1.6)
m = np.matmul(t, m)
vertices = quadradoh(0.5,0.2)
vertices = np.matmul(m, vertices)
draw_square(vertices, "purple") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Braço direito
t = translate(1.5,0.6)
m = np.matmul(t, m)
vertices = quadradoh(0.5,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "chocolate") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Antebraço direito
t = translate(0.0,-2.8)
m = np.matmul(t, m)
vertices = quadradoh(0.5,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "rebeccapurple") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Mão direito
t = translate(0.0,-1.6)
m = np.matmul(t, m)
vertices = quadradoh(0.5,0.2)
vertices = np.matmul(m, vertices)
draw_square(vertices, "purple") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Perna esquerda
t = translate(-0.5,-3.5)
m = np.matmul(t, m)
vertices = quadradoh(0.6,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "red") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Canela esquerda
t = translate(0.0,-2.8)
m = np.matmul(t, m)
vertices = quadradoh(0.6,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "gold") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Pé esquerdo
t = translate(0.0,-1.6)
m = np.matmul(t, m)
vertices = quadradoh(0.6,0.2)
vertices = np.matmul(m, vertices)
draw_square(vertices, "teal") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Perna esquerda
t = translate(0.5,-3.5)
m = np.matmul(t, m)
vertices = quadradoh(0.6,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "red") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Canela esquerda
t = translate(0.0,-2.8)
m = np.matmul(t, m)
vertices = quadradoh(0.6,2.5)
vertices = np.matmul(m, vertices)
draw_square(vertices, "gold") # Desenha o quadrado


#### Espaço para as suas rotinas ####

#####################################


# Pé esquerdo
t = translate(0.0,-1.6)
m = np.matmul(t, m)
vertices = quadradoh(0.6,0.2)
vertices = np.matmul(m, vertices)
draw_square(vertices, "teal") # Desenha o quadrado

plt.show()