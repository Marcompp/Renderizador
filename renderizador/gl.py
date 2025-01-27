#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# pylint: disable=invalid-name

"""
Biblioteca Gráfica / Graphics Library.

Desenvolvido por: <SEU NOME AQUI>
Disciplina: Computação Gráfica
Data: <DATA DE INÍCIO DA IMPLEMENTAÇÃO>
"""

import time         # Para operações com tempo
import gpu          # Simula os recursos de uma GPU
import math         # Funções matemáticas
import numpy as np  # Biblioteca do Numpy
import matplotlib.pyplot as plt

def quattorot(a,b,c,d):
    qr = math.cos(d/2)
    qi = math.sin(d/2)*a
    qj = math.sin(d/2)*b
    qk = math.sin(d/2)*c
    rot1 = [1-2*((qj*qj)+(qk*qk)),2*(qi*qj-qk*qr),2*(qi*qk-qj*qr),0]
    rot2 = [2*(qi*qj+qk*qr),1-2*((qi*qi)+(qk*qk)),2*(qj*qk-qi*qr),0]
    rot3 = [2*(qi*qk-qj*qr),2*(qj*qk-qi*qr),1-2*((qi*qi)+(qj*qj)),0]
    rot4 = [0,0,0,1]
    rotta = [rot1,rot2,rot3,rot4]
    return rotta

# == 0: colineares; > 0: horario; < 0: anti-horario
def ordem(pontos,tri = 3):
    bax = pontos[0] - pontos[0+tri]
    bay = pontos[1] - pontos[1+tri]
    bcx = pontos[0+tri*2] - pontos[0+tri]
    bcy = pontos[1+tri*2] - pontos[1+tri]

    return (bax * bcy - bay * bcx)


def horario(pontos,tri=3):
    #print(f"TRI={tri}")
    #print(len(pontos))
    if ordem(pontos,tri) < 0:
        return pontos
    else:
        npontos = pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri]
        if ordem(npontos,tri) < 0:
            return npontos
        else:
            return pontos[0:tri]+pontos[tri*2:tri*3]+pontos[tri:tri*2]
        
def horario_z(pontos,zlist,tri=3):
    #print(f"TRI={tri}")
    #print(len(pontos))
    if ordem(pontos,tri) < 0:
        return pontos,zlist
    else:
        npontos = pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri]
        if ordem(npontos,tri) < 0:
            nzlist = [zlist[2],zlist[1],zlist[0]]
            return (npontos, nzlist)
        else:
            npontos = pontos[0:tri]+pontos[tri*2:tri*3]+pontos[tri:tri*2]
            nzlist = [zlist[0],zlist[2],zlist[1]]
            return (npontos, nzlist)

def horario_cz(pontos,colors,zlist, tri=3):
    #print(f"TRI={tri}")
    if len(colors) < 9:
        ctri = 2
    else:
        ctri = 3
    if ordem(pontos,tri) < 0:
        return pontos,colors,zlist
    else:
        npontos = pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri]
        ncolors = colors[ctri*2:ctri*3]+colors[ctri:ctri*2]+colors[0:ctri]
        if ordem(npontos,tri) < 0:
            return npontos,ncolors, [zlist[2],zlist[1],zlist[0]]
        else:
            npontos = pontos[0:tri]+pontos[tri*2:tri*3]+pontos[tri:tri*2]
            ncolors = colors[0:ctri]+colors[ctri*2:ctri*3]+colors[ctri:ctri*2]
            return npontos,ncolors, [zlist[0],zlist[2],zlist[1]]

            
def horario_c(pontos,colors, tri=3):
    #print(f"TRI={tri}")
    if len(colors) < 9:
        ctri = 2
    else:
        ctri = 3
    if ordem(pontos,tri) < 0:
        return pontos,colors
    else:
        npontos = pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri]
        ncolors = colors[ctri*2:ctri*3]+colors[ctri:ctri*2]+colors[0:ctri]
        if ordem(npontos,tri) < 0:
            return npontos,ncolors
        else:
            npontos = pontos[0:tri]+pontos[tri*2:tri*3]+pontos[tri:tri*2]
            ncolors = colors[0:ctri]+colors[ctri*2:ctri*3]+colors[ctri:ctri*2]
            return npontos, ncolors
        
def antihorario_cz(pontos,colors,zlist,tri=3):
    if len(colors) < 9:
        ctri = 2
    else:
        ctri = 3
    pontos,colors,zlist = horario_cz(pontos,colors,zlist,tri)
    npontos = pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri]
    ncolors = colors[ctri*2:ctri*3]+colors[ctri:ctri*2]+colors[0:ctri]
    nzlist = [zlist[2],zlist[1],zlist[0]]
    return  npontos,ncolors,nzlist 

def antihorario_c(pontos,colors,tri=3):
    if len(colors) < 9:
        ctri = 2
    else:
        ctri = 3
    pontos,colors = horario_c(pontos,colors,tri)
    return pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri] , colors[ctri*2:ctri*3]+colors[ctri:ctri*2]+colors[0:ctri]

def antihorario_z(pontos,zlist = None,tri=3):
    #print("AAAAAAAAAA")
    #print(horario_z(pontos,zlist,tri))
    pontos,zlist = horario_z(pontos,zlist,tri)
    npontos = pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri]
    return  npontos, [zlist[2],zlist[1],zlist[0]]   

def antihorario(pontos,tri=3):
    pontos = horario(pontos,tri)
    return pontos[tri*2:tri*3]+pontos[tri:tri*2]+pontos[0:tri]

def baricenter(pontos):
    b = []
    b.append((pontos[0]+pontos[2]+pontos[4])/3)
    b.append((pontos[1]+pontos[3]+pontos[5])/3)
    return b

def baricalc(pixel,pontos):
    #print(pontos)
    alpha = (-(pixel[0]-pontos[2])*(pontos[5]-pontos[3]) + (pixel[1]-pontos[3])*(pontos[4]-pontos[2]) )
    alpha /= (-(pontos[0]-pontos[2])*(pontos[5]-pontos[3]) + (pontos[1]-pontos[3])*(pontos[4]-pontos[2]) )
    beta = (-(pixel[0]-pontos[4])*(pontos[1]-pontos[5]) + (pixel[1]-pontos[5])*(pontos[0]-pontos[4]) )
    beta /=  (-(pontos[2]-pontos[4])*(pontos[1]-pontos[5]) + (pontos[3]-pontos[5])*(pontos[0]-pontos[4]) )
    gamma = 1-alpha-beta
    return [alpha,beta,gamma]

def baricolor(barivars,colors,curr_z = 1):
    ncolor = [0,0,0]
    for a in range(3):
        for b in range(3):
            ncolor[b]+=colors[a*3+b]*barivars[a]/curr_z
    return [int(i * 255) for i in ncolor]

def baritex(barivars,texture,u_list,v_list,z=[1,1,1],curr_z=1):
    #barivars = baricalc(pixel,pontos)
    for a in range(3):
        barivars[a] = barivars[a]/z[a]
    x_tex = int( curr_z*( (barivars[0] * u_list[0] + barivars[1] * u_list[1] + barivars[2] * u_list[2]) * texture.shape[1]-2 ) )
    #print(f"x_tex:{x_tex}")
    if x_tex >= 256:
        x_tex = 255
    y_tex = int( curr_z*( (barivars[0] * v_list[0] + barivars[1] * v_list[1] + barivars[2] * v_list[2]) * (texture.shape[0]-2) ) )
    if y_tex >= 256:
        y_tex = 255
    #print(f"y_tex:{y_tex}")
    return list(texture[y_tex][x_tex][0:3])

def normaltri(pontos,z,curr_z,height,width):

    difx = max( [abs(pontos[0]-pontos[2]),abs(pontos[0]-pontos[4]),abs(pontos[2]-pontos[4])]   )
    dify = max( [abs(pontos[1]-pontos[3]),abs(pontos[1]-pontos[5]),abs(pontos[3]-pontos[5])]   )
    difz = max( [abs(z[0]-z[1]),abs(z[0]-z[2]),abs(z[1]-z[2])])
    x = [pontos[0]/difx,pontos[2]/difx,pontos[4]/width]
    y = [pontos[1]/dify,pontos[3]/dify,pontos[5]/dify]
    z = [int(i/difz) for i in z]
    v1 = [x[0]-x[1],y[0]-y[1],z[0]-z[1]]
    v2 = [x[0]-x[2],y[0]-y[2],z[0]-z[2]]

    #v1 = [pontos[0]-pontos[2],pontos[1]-pontos[3],z[0]-z[1]]
    #v2 = [pontos[0]-pontos[4],pontos[1]-pontos[5],z[0]-z[2]]

    normal = np.cross(v1,v2)
    return normal

def lightcalc(light,pixel,curr_z,vertices,z,ncolor,height,width):
    normal = normaltri(vertices,z,curr_z,height,width)

    if light['dir']:
        res = [i * -1 for i in light['direction']]

        resul = np.dot(normal,res)
        resul *= -1/2
        lightcolor = [ light['color'][0] * resul * light['intensity'],
                      light['color'][1] * resul * light['intensity'],
                      light['color'][2] * resul * light['intensity'] ]

    for a in range(3):
        ncolor[a] *= abs(lightcolor[a])
        if ncolor[a] >= 255:
            ncolor[a] = 254
    return ncolor

def minimap(image,maxLevel = None):
        w, h = image.shape[:2]
        
        # Calculate amount of necessary levels
        level = int(np.log2(max(w, h)))
        if maxLevel is None: 
            maxLevel = level
        
        # Dictionary to store mipmapped texture.
        _map = {0 : image}
        
        # Construct each level
        for step in range(0, min(level, maxLevel)):
            _map[step+1] = halve_image(_map[step])
        return _map, level

def halve_image(image):
        """
        Halves image size using bilinear filtering.
        Found at: https://stackoverflow.com/questions/14549696/mipmap-of-image-in-numpy
        """
        rows, cols, planes = image.shape
        image = image.astype('uint16')
        image = image.reshape(rows // 2, 2, cols // 2, 2, planes)
        image = image.sum(axis=3).sum(axis=1)
        return ((image + 2) >> 2).astype('uint8')
    
def plotmap(map,level):
        fig = plt.figure(figsize=(9,(level//3)*3))
        axList = []
        for step in map:
            axList.append(fig.add_subplot(level//3+1, 3, step+1))
            axList[step].imshow(map[step], interpolation='nearest')
            axList[step].get_xaxis().set_visible(False)
            axList[step].get_yaxis().set_visible(False)
            axList[step].set_title("Mipmap level: {} ({}x{})".format(step, *map[step].shape[:2]))
        plt.show()
        



class GL:
    """Classe que representa a biblioteca gráfica (Graphics Library)."""

    #width = 800   # largura da tela
    #height = 600  # altura da tela
    #near = 0.01   # plano de corte próximo
    #far = 1000    # plano de corte distante

    @staticmethod
    def setup(width, height, near=0.01, far=1000):
        """Definr parametros para câmera de razão de aspecto, plano próximo e distante."""
        GL.width = width
        GL.height = height
        GL.near = near
        GL.far = far

        GL.count = 0

        GL.model = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        GL.pilha = []

        GL.lights = []

        # GL.zbuffer = []
        # for x in range(GL.width*2):
        #     GL.zbuffer.append([])
        #     for y in range(GL.height*2):
        #         GL.zbuffer.append(99999)
        

        GL.zbuffer = np.matrix(np.ones((GL.width*2,GL.height*2)) * np.inf)

    @staticmethod
    def polypoint2D(point, colors):
        """Função usada para renderizar Polypoint2D."""
        # Nessa função você receberá pontos no parâmetro point, esses pontos são uma lista
        # de pontos x, y sempre na ordem. Assim point[0] é o valor da coordenada x do
        # primeiro ponto, point[1] o valor y do primeiro ponto. Já point[2] é a
        # coordenada x do segundo ponto e assim por diante. Assuma a quantidade de pontos
        # pelo tamanho da lista e assuma que sempre vira uma quantidade par de valores.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, para o Polypoint2D
        # você pode assumir inicialmente o desenho dos pontos com a cor emissiva (emissiveColor).

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.

        #print("Polypoint2D : pontos = {0}".format(point)) # imprime no terminal pontos
        #print("Polypoint2D : colors = {0}".format(colors)) # imprime no terminal as cores
        ncolor = [int(i * 255) for i in colors['emissiveColor']]
        #print(ncolor)
        # Exemplo:
        for a in range(int(len(point)/2)):
            #print(a)
            #gpu.GPU.set_pixel(int(point[a*2]),int(point[a*2+1]), ncolor[0], ncolor[1], ncolor[2]) # altera um pixel da imagem (u, v, r, g, b)
            gpu.GPU.draw_pixel([int(point[a*2]),int(point[a*2+1])], gpu.GPU.RGB8, ncolor)  # altera pixel


        # cuidado com as cores, o X3D especifica de (0,1) e o Framebuffer de (0,255)
        
    @staticmethod
    def polyline2D(lineSegments, colors):
        """Função usada para renderizar Polyline2D."""
        # Nessa função você receberá os pontos de uma linha no parâmetro lineSegments, esses
        # pontos são uma lista de pontos x, y sempre na ordem. Assim point[0] é o valor da
        # coordenada x do primeiro ponto, point[1] o valor y do primeiro ponto. Já point[2] é
        # a coordenada x do segundo ponto e assim por diante. Assuma a quantidade de pontos
        # pelo tamanho da lista. A quantidade mínima de pontos são 2 (4 valores), porém a
        # função pode receber mais pontos para desenhar vários segmentos. Assuma que sempre
        # vira uma quantidade par de valores.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, para o Polyline2D
        # você pode assumir inicialmente o desenho das linhas com a cor emissiva (emissiveColor).

        color = False
        ncolor = [int(i * 255) for i in colors['emissiveColor']]


        #print("Polyline2D : lineSegments = {0}".format(lineSegments)) # imprime no terminal
        #print("Polyline2D : colors = {0}".format(colors)) # imprime no terminal as cores
        
        # Exemplo:
        pos_x = GL.width//2
        pos_y = GL.height//2

        point = [int(lineSegments[0]),int(lineSegments[1])]
        end = [int(lineSegments[0+2]),int(lineSegments[1+2])]

        dx = abs(end[0]-point[0])
        if point[0]< end[0]:
            sx = 1
        else:
            sx = -1
        dy = abs(end[1]-point[1])
        if point[1]< end[1]:
            sy = 1
        else:
            sy = -1
        if dx > dy:
            err = dx / 2
        else:
            err = -dy / 2
        e2 = err
        while True:
            #print(f"{point}     {end}")
            if ((sx > 0 and point[0] >= end[0]) or (sx < 0 and point[0] <= end[0])) and ((sy > 0 and point[1] >= end[1]) or (sy < 0 and point[1] <= end[1])):
                gpu.GPU.draw_pixel([end[0],end[1]], gpu.GPU.RGB8, ncolor)  # altera pixel
                break
            gpu.GPU.draw_pixel([point[0],point[1]], gpu.GPU.RGB8, ncolor)  # altera pixel
            if point[0] == end[0] and point[1] == end[1]:
                break
            e2 = err
            if e2 > -dx:
                err -= dy
                point[0] += sx
            if e2 < dy:
                err += dx
                point[1] += sy




    @staticmethod
    def triangleSet2D(vertices, colors,z = [1,1,1],texture = None):
        """Função usada para renderizar TriangleSet2D."""
        # Nessa função você receberá os vertices de um triângulo no parâmetro vertices,
        # esses pontos são uma lista de pontos x, y sempre na ordem. Assim point[0] é o
        # valor da coordenada x do primeiro ponto, point[1] o valor y do primeiro ponto.
        # Já point[2] é a coordenada x do segundo ponto e assim por diante. Assuma que a
        # quantidade de pontos é sempre multiplo de 3, ou seja, 6 valores ou 12 valores, etc.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, para o TriangleSet2D

        # você pode assumir o desenho das linhas com a cor emissiva (emissiveColor).
        color = False

        ncolor = [0,0,0]
        bcolor = [0,0,0]

        if type(colors) is not dict:
            color = True
        # else:
        #     if len(GL.lights) > 0:
        #         bcolor =  [int(i * 255) for i in colors['diffuseColor']]
        #     else:
        #         bcolor = [int(i * 255) for i in colors['emissiveColor']]

        if texture is not None:
            #print(colors)
            u_list = colors[::2]
            v_list = colors[1::2]
            #print(f"u_list:{u_list}")
            #print(f"v_list:{v_list}")
            color = False

        #print("TriangleSet2D : vertices = {0}".format(vertices)) # imprime no terminal

        #print("TriangleSet2D : colors = {0}".format(colors)) # imprime no terminal as cores
        #print(ncolor)
        
        sample = []
        # for y in range(20):
        #     sample.append([])
        #     for x in range(30):
        #         sample[x].append(x + 0.5, y + 0.5)
        


        for x in range(int(min(vertices[0],vertices[2],vertices[4])),int(max(vertices[0],vertices[2],vertices[4]))+1):
            for y in range(int(min(vertices[1],vertices[3],vertices[5])),int(max(vertices[1],vertices[3],vertices[5]))+1):
                for a in range(3):
                    start = [vertices[2*a],vertices[2*a+1]]
                    if a != 2:
                        end = [vertices[2*a+2],vertices[2*a+1+2]]
                    else:
                        end = [vertices[0],vertices[1]]
                    test = np.dot([x+0.5-start[0],y+0.5-start[1]] , [end[1]-start[1],-(end[0]-start[0])])
                    if test < 0:
                        break
                    if a == 2:
                        if x < 0:
                            x = 0
                        if y < 0:
                            y = 0
                        barivars = baricalc([x,y],vertices)
                        curr_z = 1 / (barivars[0] * (1 / z[0]) + barivars[1] * (1 / z[1]) + barivars[2] * (1 / z[2]))


                        if curr_z < GL.zbuffer[x, y]:
                            if color:
                                ncolor = baricolor(barivars,colors,curr_z)
                            elif texture is not None:
                                ncolor = baritex(barivars,texture,u_list,v_list,z,curr_z)
                                #print(ncolor)
                            elif len(GL.lights) > 0:
                                    ncolor =  [int(i * 255) for i in colors['diffuseColor']]

                                    for light in GL.lights:
                                        ncolor = lightcalc(light,[x,y],curr_z,vertices,z,ncolor,GL.height,GL.width)
                            
                            else:
                                ncolor = [int(i * 255) for i in colors['emissiveColor']]
                                if (type(colors) is dict) and colors["transparency"] > 0:
                                    #print(f"ncolor:{ncolor}  ",end='')
                                    
                                    ocolor = gpu.GPU.read_pixel([x,y], gpu.GPU.RGB8)
                                    #print(f"ocolor:{ocolor}  ",end='')
                                    for b in range(3):
                                        ncolor[b] = int((ncolor[b] * colors["transparency"]) + (ocolor[b] * (1 - colors["transparency"])))
                                    #print(f"result:{ncolor}")


                            GL.zbuffer[x, y] = curr_z
                            gpu.GPU.draw_pixel([x,y], gpu.GPU.RGB8, ncolor)
                        


    @staticmethod
    def triangleSet(point, colors,texture = None):
        """Função usada para renderizar TriangleSet."""
        # Nessa função você receberá pontos no parâmetro point, esses pontos são uma lista
        # de pontos x, y, e z sempre na ordem. Assim point[0] é o valor da coordenada x do
        # primeiro ponto, point[1] o valor y do primeiro ponto, point[2] o valor z da
        # coordenada z do primeiro ponto. Já point[3] é a coordenada x do segundo ponto e
        # assim por diante.
        # No TriangleSet os triângulos são informados individualmente, assim os três
        # primeiros pontos definem um triângulo, os três próximos pontos definem um novo
        # triângulo, e assim por diante.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, você pode assumir
        # inicialmente, para o TriangleSet, o desenho das linhas com a cor emissiva
        # (emissiveColor), conforme implementar novos materias você deverá suportar outros
        # tipos de cores.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("TriangleSet : pontos = {0}".format(point)) # imprime no terminal pontos
        #print("TriangleSet : colors = {0}".format(colors)) # imprime no terminal as cores



        tris = [[point[0],point[3],point[6]],
                [point[0+1],point[3+1],point[6+1]],
                [point[0+2],point[3+2],point[6+2]],
                 [1,1,1]]
        tris = np.array(tris)

        
        ntri = np.matmul(GL.screen,GL.perspectiva)
        # XYZ

        ntri = np.matmul(ntri,GL.lookat)
        ntri = np.matmul(ntri,GL.model)
        
        tris = np.matmul(ntri,tris)
        #print(tris)
        #print("AAAAAAAAAAA")
        tris = tris.tolist()



        npoint = [0,0,0,0,0,0]
        zpoint = []

        for a in range(3):
            zpoint.append(tris[2][a])
            for b in range(2):
                npoint[b+a*2] = (tris[b][a]/tris[3][a])


        #print(f"npoint = {npoint}")
        #print(f"colors_preh:{colors}")

        if type(colors)==dict or texture is None:
            npoint,zpoint = antihorario_z(npoint,zpoint,2)
        else:
            npoint,colors,zpoint = antihorario_cz(npoint,colors,zpoint,2)
        #print(f"colors_posh:{colors}")

        GL.triangleSet2D(npoint, colors,zpoint,texture)

    @staticmethod
    def viewpoint(position, orientation, fieldOfView):
        """Função usada para renderizar (na verdade coletar os dados) de Viewpoint."""
        # Na função de viewpoint você receberá a posição, orientação e campo de visão da
        # câmera virtual. Use esses dados para poder calcular e criar a matriz de projeção
        # perspectiva para poder aplicar nos pontos dos objetos geométricos.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("Viewpoint : ", end='')
        #print("position = {0} ".format(position), end='')
        #print("orientation = {0} ".format(orientation), end='')
        #print("fieldOfView = {0} ".format(fieldOfView))

        orientation = quattorot(orientation[0],orientation[1],orientation[2],orientation[3])
        transla = [[1,0,0,-position[0]],[0,1,0,-position[1]],[0,0,1,-position[2]],[0,0,0,1]]

        #invert
        GL.lookat = np.matmul(np.array(orientation).T, np.array(transla))

        GL.resolu = GL.width/GL.height
        FOVy = 2*math.atan(math.tan(fieldOfView/2)*(GL.height/math.sqrt((GL.height*GL.height)+(GL.width*GL.width))))
        top = GL.near * math.tan(FOVy)
        bottom = -top
        right = top *GL.resolu
        left = -right
        GL.perspectiva = np.array([[GL.near/right,0,0,0],[0,GL.near/top,0,0],[0,0,-((GL.far+GL.near)/(GL.far-GL.near)),((-2)*GL.far*GL.near)/(GL.far-GL.near)],[0,0,-1,0]])
        GL.screen = np.array([[GL.width,0,0,GL.width],[0,-GL.height,0,GL.height],[0,0,1,0],[0,0,0,1]])
        viewpoint =[position[0],position[1],position[2],orientation]

        #print("Viewpoint : ", end='')
        #print("lookat = {0} ".format(GL.lookat), end='')
        #print("perspectiva = {0} ".format(GL.perspectiva), end='')
        #print("screen = {0} ".format(GL.screen))

    @staticmethod
    def transform_in(translation, scale, rotation):
        """Função usada para renderizar (na verdade coletar os dados) de Transform."""
        # A função transform_in será chamada quando se entrar em um nó X3D do tipo Transform
        # do grafo de cena. Os valores passados são a escala em um vetor [x, y, z]
        # indicando a escala em cada direção, a translação [x, y, z] nas respectivas
        # coordenadas e finalmente a rotação por [x, y, z, t] sendo definida pela rotação
        # do objeto ao redor do eixo x, y, z por t radianos, seguindo a regra da mão direita.
        # Quando se entrar em um nó transform se deverá salvar a matriz de transformação dos
        # modelos do mundo em alguma estrutura de pilha.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("Transform : ", end='')
        #if translation:
        #    print("translation = {0} ".format(translation), end='') # imprime no terminal
        #if scale:
        #    print("scale = {0} ".format(scale), end='') # imprime no terminal
        #if rotation:
        #    print("rotation = {0} ".format(rotation), end='') # imprime no terminal
        #print("")
        GL.count+=1
        #print(GL.count)

        GL.pilha.append(GL.model)

        GL.translation = np.array([[1,0,0,translation[0]],[0,1,0,translation[1]],[0,0,1,translation[2]],[0,0,0,1]])
        GL.scale = np.array([[scale[0],0,0,0],[0,scale[1],0,0],[0,0,scale[2],0],[0,0,0,1]])
        GL.rotation = np.array(quattorot(rotation[0],rotation[1],rotation[2],rotation[3]))

        ntri = np.matmul(GL.translation,GL.rotation)
        ntri = np.matmul(ntri,GL.scale)
        GL.model = np.matmul(GL.model, ntri)
        #print(f"MODEL:{GL.model}")

        

    @staticmethod
    def transform_out():
        """Função usada para renderizar (na verdade coletar os dados) de Transform."""
        # A função transform_out será chamada quando se sair em um nó X3D do tipo Transform do
        # grafo de cena. Não são passados valores, porém quando se sai de um nó transform se
        # deverá recuperar a matriz de transformação dos modelos do mundo da estrutura de
        # pilha implementada.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        GL.model = GL.pilha.pop()
        print("Saindo de Transform")

    @staticmethod
    def triangleStripSet(point, stripCount, colors):
        """Função usada para renderizar TriangleStripSet."""
        # A função triangleStripSet é usada para desenhar tiras de triângulos interconectados,
        # você receberá as coordenadas dos pontos no parâmetro point, esses pontos são uma
        # lista de pontos x, y, e z sempre na ordem. Assim point[0] é o valor da coordenada x
        # do primeiro ponto, point[1] o valor y do primeiro ponto, point[2] o valor z da
        # coordenada z do primeiro ponto. Já point[3] é a coordenada x do segundo ponto e assim
        # por diante. No TriangleStripSet a quantidade de vértices a serem usados é informado
        # em uma lista chamada stripCount (perceba que é uma lista). Ligue os vértices na ordem,
        # primeiro triângulo será com os vértices 0, 1 e 2, depois serão os vértices 1, 2 e 3,
        # depois 2, 3 e 4, e assim por diante. Cuidado com a orientação dos vértices, ou seja,
        # todos no sentido horário ou todos no sentido anti-horário, conforme especificado.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("TriangleStripSet : pontos = {0} ".format(point), end='')
        #for i, strip in enumerate(stripCount):
        #    print("strip[{0}] = {1} ".format(i, strip), end='')
        #print("")
        #print("TriangleStripSet : colors = {0}".format(colors)) # imprime no terminal as cores

        for i, strip in enumerate(stripCount):
            for a in range(strip-2):
                #print(point[a*3:a*3+9])
                npoint = point[a*3:a*3+9]
                GL.triangleSet(horario(npoint), colors)


        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        #gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel

    @staticmethod
    def indexedTriangleStripSet(point, index, colors):
        """Função usada para renderizar IndexedTriangleStripSet."""
        # A função indexedTriangleStripSet é usada para desenhar tiras de triângulos
        # interconectados, você receberá as coordenadas dos pontos no parâmetro point, esses
        # pontos são uma lista de pontos x, y, e z sempre na ordem. Assim point[0] é o valor
        # da coordenada x do primeiro ponto, point[1] o valor y do primeiro ponto, point[2]
        # o valor z da coordenada z do primeiro ponto. Já point[3] é a coordenada x do
        # segundo ponto e assim por diante. No IndexedTriangleStripSet uma lista informando
        # como conectar os vértices é informada em index, o valor -1 indica que a lista
        # acabou. A ordem de conexão será de 3 em 3 pulando um índice. Por exemplo: o
        # primeiro triângulo será com os vértices 0, 1 e 2, depois serão os vértices 1, 2 e 3,
        # depois 2, 3 e 4, e assim por diante. Cuidado com a orientação dos vértices, ou seja,
        # todos no sentido horário ou todos no sentido anti-horário, conforme especificado.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("IndexedTriangleStripSet : pontos = {0}, index = {1}".format(point, index))
        #print("IndexedTriangleStripSet : colors = {0}".format(colors)) # imprime as cores
        #print(len(point)/3)

        for a in range(int(len(index))-2):
            if (index[a+2] != -1) and (index[a] != -1) and (index[a+1] != -1):
                #print(point[a*3:a*3+9])
                npoint = point[index[a]*3:index[a]*3+3]+point[index[a+1]*3:index[a+1]*3+3]+point[index[a+2]*3:index[a+2]*3+3]
                #print(npoint)
                GL.triangleSet(horario(npoint), colors)

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        #gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel

    @staticmethod
    def box(size, colors):
        """Função usada para renderizar Boxes."""
        # A função box é usada para desenhar paralelepípedos na cena. O Box é centrada no
        # (0, 0, 0) no sistema de coordenadas local e alinhado com os eixos de coordenadas
        # locais. O argumento size especifica as extensões da caixa ao longo dos eixos X, Y
        # e Z, respectivamente, e cada valor do tamanho deve ser maior que zero. Para desenha
        # essa caixa você vai provavelmente querer tesselar ela em triângulos, para isso
        # encontre os vértices e defina os triângulos.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("Box : size = {0}".format(size)) # imprime no terminal pontos
        print("Box : colors = {0}".format(colors)) # imprime no terminal as cores

        box = [[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]]


        vertices = []
        for vert in range(8):
            for a in range(3):
                vertices.append((size[a]/2)*box[vert][a])
        print(f"vert:{vertices}")

        GL.indexedTriangleStripSet(vertices, [0,1,2,3,-1,-1,4,5,6,7,-1,-1,0,1,4,5,-1,-1,2,3,6,7,-1,-1,0,2,4,6,-1,-1,1,3,5,7], colors)

        #GL.indexedTriangleStripSet([vertices[:12]], [1,2,3,4], colors)
        #GL.indexedTriangleStripSet([vertices[12:]], [1,1,1,1], colors)
        #GL.indexedTriangleStripSet([vertices[:6]+vertices[12:18]], [1,2,3,4], colors)
        #GL.indexedTriangleStripSet([vertices[6:12]+vertices[18:]], [1,2,3,4], colors)
        #GL.indexedTriangleStripSet([vertices[3:6]+vertices[9:12]+vertices[15:18],vertices[21:]], [1,1,1,1], colors)
        #GL.indexedTriangleStripSet([vertices[:3]+vertices[6:9]+vertices[12:15],vertices[18:21]], [1,1,1,1], colors)

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel

    @staticmethod
    def indexedFaceSet(coord, coordIndex, colorPerVertex, color, colorIndex,
                       texCoord, texCoordIndex, colors, current_texture):
        """Função usada para renderizar IndexedFaceSet."""
        # A função indexedFaceSet é usada para desenhar malhas de triângulos. Ela funciona de
        # forma muito simular a IndexedTriangleStripSet porém com mais recursos.
        # Você receberá as coordenadas dos pontos no parâmetro cord, esses
        # pontos são uma lista de pontos x, y, e z sempre na ordem. Assim coord[0] é o valor
        # da coordenada x do primeiro ponto, coord[1] o valor y do primeiro ponto, coord[2]
        # o valor z da coordenada z do primeiro ponto. Já coord[3] é a coordenada x do
        # segundo ponto e assim por diante. No IndexedFaceSet uma lista de vértices é informada
        # em coordIndex, o valor -1 indica que a lista acabou.
        # A ordem de conexão será de 3 em 3 pulando um índice. Por exemplo: o
        # primeiro triângulo será com os vértices 0, 1 e 2, depois serão os vértices 1, 2 e 3,
        # depois 2, 3 e 4, e assim por diante.
        # Adicionalmente essa implementação do IndexedFace aceita cores por vértices, assim
        # se a flag colorPerVertex estiver habilitada, os vértices também possuirão cores
        # que servem para definir a cor interna dos poligonos, para isso faça um cálculo
        # baricêntrico de que cor deverá ter aquela posição. Da mesma forma se pode definir uma
        # textura para o poligono, para isso, use as coordenadas de textura e depois aplique a
        # cor da textura conforme a posição do mapeamento. Dentro da classe GPU já está
        # implementadado um método para a leitura de imagens.

        # Os prints abaixo são só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("IndexedFaceSet : ")
        if coord:
            print("\tpontos(x, y, z) = {0}, coordIndex = {1}".format(coord, coordIndex))
        print("colorPerVertex = {0}".format(colorPerVertex))
        if colorPerVertex and color and colorIndex:
            print("\tcores(r, g, b) = {0}, colorIndex = {1}".format(color, colorIndex))
        else:
            print(f"colors:{colors}")
        if texCoord and texCoordIndex:
            print("\tpontos(u, v) = {0}, texCoordIndex = {1}".format(texCoord, texCoordIndex))
        if current_texture:
            image = gpu.GPU.load_texture(current_texture[0])
            print("\t Matriz com image = {0}".format(image))
            print("\t Dimensões da image = {0}".format(image.shape))
        print("IndexedFaceSet : colors = {0}".format(colors))  # imprime no terminal as cores

        #if texCoord and texCoordIndex and current_texture:
        #    mipmap,level = minimap(gpu.GPU.load_texture(current_texture[0]))
        #    plotmap(mipmap,level)
        #    return
        
        if texCoord is not None:
            vertex_color = False
            texture = True
            image_texture = gpu.GPU.load_texture(current_texture[0])


        for a in range(int(len(coordIndex))-2):
            if (coordIndex[a+2] != -1) and (coordIndex[a] != -1) and (coordIndex[a+1] != -1):
                #print(point[a*3:a*3+9])
                npoint = coord[coordIndex[a]*3:coordIndex[a]*3+3]+coord[coordIndex[a+1]*3:coordIndex[a+1]*3+3]+coord[coordIndex[a+2]*3:coordIndex[a+2]*3+3]
                print("NPOINT")
                print(npoint)
                #print(npoint)
                if colorPerVertex and len(colorIndex) !=0:
                    #TO DO
                    print(f"colorIndex:{colorIndex}")
                    ncolor = color[colorIndex[a]*3:colorIndex[a]*3+3]+color[colorIndex[a+1]*3:colorIndex[a+1]*3+3]+color[colorIndex[a+2]*3:colorIndex[a+2]*3+3]
                    npoint, ncolor = horario_c(npoint, ncolor)
                    GL.triangleSet(npoint, ncolor)
                elif texCoord:
                    #print(f"c:{coord}")
                    #print(f"tc:{texCoord}")
                    #print(a)
                    uv = texCoord[texCoordIndex[a]*2:texCoordIndex[a]*2+2]+texCoord[texCoordIndex[a+1]*2:texCoordIndex[a+1]*2+2]+texCoord[texCoordIndex[a+2]*2:texCoordIndex[a+2]*2+2]
                    #print(f"uv:{uv}")
                    #print(f"uv:{uv}")
                    GL.triangleSet(horario(npoint), uv,gpu.GPU.load_texture(current_texture[0]))
                else:
                    GL.triangleSet(horario(npoint), colors)

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
    
        gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel

    @staticmethod
    def sphere(radius, colors):
        """Função usada para renderizar Esferas."""
        # A função sphere é usada para desenhar esferas na cena. O esfera é centrada no
        # (0, 0, 0) no sistema de coordenadas local. O argumento radius especifica o
        # raio da esfera que está sendo criada. Para desenha essa esfera você vai
        # precisar tesselar ela em triângulos, para isso encontre os vértices e defina
        # os triângulos.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("Sphere : radius = {0}".format(radius)) # imprime no terminal o raio da esfera
        print("Sphere : colors = {0}".format(colors)) # imprime no terminal as cores

        
        nsteps = 40
        nrings = int(nsteps/2)
        norm = nsteps/2

        points = []
        for d in range(nrings):
            ang2 = (d/norm)*math.pi
            z = math.cos(ang2)*radius
            for a in range(nsteps):
                ang = (a/norm)*math.pi
                points.append(math.cos(ang)*radius*math.sin(ang2))
                points.append(math.sin(ang)*radius*math.sin(ang2))
                points.append(z)
        #print(points)
        index = []
        for ring in range(nrings-1):
            for a in range(nsteps):
                index.append(ring*nsteps+a)
                index.append(((ring+1)*nsteps)+a)
                if a != nsteps-1:
                    index.append(ring*nsteps+a+1)
                    index.append(((ring+1)*nsteps)+a+1)
                else:
                    index.append(ring*nsteps+0)
                    index.append(((ring+1)*nsteps)+0)

        GL.indexedTriangleStripSet(points, index, colors)




    @staticmethod
    def navigationInfo(headlight):
        """Características físicas do avatar do visualizador e do modelo de visualização."""
        # O campo do headlight especifica se um navegador deve acender um luz direcional que
        # sempre aponta na direção que o usuário está olhando. Definir este campo como TRUE
        # faz com que o visualizador forneça sempre uma luz do ponto de vista do usuário.
        # A luz headlight deve ser direcional, ter intensidade = 1, cor = (1 1 1),
        # ambientIntensity = 0,0 e direção = (0 0 −1).

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        if headlight:

            GL.directionalLight( 0, [1,1,1],1,[0,0,-1] ) 

        print("NavigationInfo : headlight = {0}".format(headlight)) # imprime no terminal

    @staticmethod
    def directionalLight(ambientIntensity, color, intensity, direction):
        """Luz direcional ou paralela."""
        # Define uma fonte de luz direcional que ilumina ao longo de raios paralelos
        # em um determinado vetor tridimensional. Possui os campos básicos ambientIntensity,
        # cor, intensidade. O campo de direção especifica o vetor de direção da iluminação
        # que emana da fonte de luz no sistema de coordenadas local. A luz é emitida ao
        # longo de raios paralelos de uma distância infinita.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("DirectionalLight : ambientIntensity = {0}".format(ambientIntensity))
        print("DirectionalLight : color = {0}".format(color)) # imprime no terminal
        print("DirectionalLight : intensity = {0}".format(intensity)) # imprime no terminal
        print("DirectionalLight : direction = {0}".format(direction)) # imprime no terminal
        GL.lights.append({'intensity':intensity  , 'ambientIntensity':ambientIntensity , 'color' : color ,'dir':True, 'direction':direction})

        #achar normal do triangulo -- achar,  vetor ponto -- iluminação,   multiplicação dot

    @staticmethod
    def pointLight(ambientIntensity, color, intensity, location):
        """Luz pontual."""
        # Fonte de luz pontual em um local 3D no sistema de coordenadas local. Uma fonte
        # de luz pontual emite luz igualmente em todas as direções; ou seja, é omnidirecional.
        # Possui os campos básicos ambientIntensity, cor, intensidade. Um nó PointLight ilumina
        # a geometria em um raio de sua localização. O campo do raio deve ser maior ou igual a
        # zero. A iluminação do nó PointLight diminui com a distância especificada.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("PointLight : ambientIntensity = {0}".format(ambientIntensity))
        print("PointLight : color = {0}".format(color)) # imprime no terminal
        print("PointLight : intensity = {0}".format(intensity)) # imprime no terminal
        print("PointLight : location = {0}".format(location)) # imprime no terminal
        GL.lights.append({'intensity':intensity  , 'ambientIntensity':ambientIntensity , 'color' : color ,'dir':False, 'location':location})

    @staticmethod
    def fog(visibilityRange, color):
        """Névoa."""
        # O nó Fog fornece uma maneira de simular efeitos atmosféricos combinando objetos
        # com a cor especificada pelo campo de cores com base nas distâncias dos
        # vários objetos ao visualizador. A visibilidadeRange especifica a distância no
        # sistema de coordenadas local na qual os objetos são totalmente obscurecidos
        # pela névoa. Os objetos localizados fora de visibilityRange do visualizador são
        # desenhados com uma cor de cor constante. Objetos muito próximos do visualizador
        # são muito pouco misturados com a cor do nevoeiro.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("Fog : color = {0}".format(color)) # imprime no terminal
        print("Fog : visibilityRange = {0}".format(visibilityRange))

    @staticmethod
    def timeSensor(cycleInterval, loop):
        """Gera eventos conforme o tempo passa."""
        # Os nós TimeSensor podem ser usados para muitas finalidades, incluindo:
        # Condução de simulações e animações contínuas; Controlar atividades periódicas;
        # iniciar eventos de ocorrência única, como um despertador;
        # Se, no final de um ciclo, o valor do loop for FALSE, a execução é encerrada.
        # Por outro lado, se o loop for TRUE no final de um ciclo, um nó dependente do
        # tempo continua a execução no próximo ciclo. O ciclo de um nó TimeSensor dura
        # cycleInterval segundos. O valor de cycleInterval deve ser maior que zero.

        # Deve retornar a fração de tempo passada em fraction_changed

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("TimeSensor : cycleInterval = {0}".format(cycleInterval)) # imprime no terminal
        print("TimeSensor : loop = {0}".format(loop))

        # Esse método já está implementado para os alunos como exemplo
        epoch = time.time()  # time in seconds since the epoch as a floating point number.
        if loop:
            fraction_changed = (epoch % cycleInterval) / cycleInterval
        else:
            fraction_changed = (epoch) / cycleInterval
            if fraction_changed > 1:
                fraction_changed = 1
        return fraction_changed

    @staticmethod
    def splinePositionInterpolator(set_fraction, key, keyValue, closed, l = 3):
        """Interpola não linearmente entre uma lista de vetores 3D."""
        # Interpola não linearmente entre uma lista de vetores 3D. O campo keyValue possui
        # uma lista com os valores a serem interpolados, key possui uma lista respectiva de chaves
        # dos valores em keyValue, a fração a ser interpolada vem de set_fraction que varia de
        # zeroa a um. O campo keyValue deve conter exatamente tantos vetores 3D quanto os
        # quadros-chave no key. O campo closed especifica se o interpolador deve tratar a malha
        # como fechada, com uma transições da última chave para a primeira chave. Se os keyValues
        # na primeira e na última chave não forem idênticos, o campo closed será ignorado.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("SplinePositionInterpolator : set_fraction = {0}".format(set_fraction))
        print("SplinePositionInterpolator : key = {0}".format(key)) # imprime no terminal
        print("SplinePositionInterpolator : keyValue = {0}".format(keyValue))
        print("SplinePositionInterpolator : closed = {0}".format(closed))

        entrou = False
        T = []
        # Abaixo está só um exemplo de como os dados podem ser calculados e transferidos
        for a in range(len(key)):
            if not closed and (a == 0 or a == len(key)-1):
                T.append([])
                for n in range(l):
                    T[-1].append(0)
            elif closed and a == len(key)-1:
                T.append([])
                for n in range(l):
                    T[-1].append(keyValue[(0)*l+n]-keyValue[(a-1)*l+n])
            else:
                T.append([])
                for n in range(l):
                    T[-1].append(keyValue[(a+1)*l+n]-keyValue[(a-1)*l+n])
        for a in range(len(key)):
            if set_fraction >= key[a] and set_fraction < key[a+1]:
                #value_changed = [keyValue[a*l], keyValue[a*l+1], keyValue[a*l+2]]
                s = (set_fraction - key[a])/(key[a+1] - key[a])
                S = [s**3,s**2,s,1]
                C = [keyValue[a*l:(a+1)*l],keyValue[(a+1)*l:(a+2)*l],T[a],T[a+1]]
                entrou = True
                break
        if entrou:
            H = [[2,-2,1,1],[-3,3,-2,-1],[0,0,1,0],[1,0,0,0]]

            val = np.dot(H,C)
            value_changed = np.matmul(S,val)
        else:
            value_changed = [keyValue[(len(key)-1)*3:(len(key))*3]]
        return value_changed

    @staticmethod
    def orientationInterpolator(set_fraction, key, keyValue):
        """Interpola entre uma lista de valores de rotação especificos."""
        # Interpola rotações são absolutas no espaço do objeto e, portanto, não são cumulativas.
        # Uma orientação representa a posição final de um objeto após a aplicação de uma rotação.
        # Um OrientationInterpolator interpola entre duas orientações calculando o caminho mais
        # curto na esfera unitária entre as duas orientações. A interpolação é linear em
        # comprimento de arco ao longo deste caminho. Os resultados são indefinidos se as duas
        # orientações forem diagonalmente opostas. O campo keyValue possui uma lista com os
        # valores a serem interpolados, key possui uma lista respectiva de chaves
        # dos valores em keyValue, a fração a ser interpolada vem de set_fraction que varia de
        # zeroa a um. O campo keyValue deve conter exatamente tantas rotações 3D quanto os
        # quadros-chave no key.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("OrientationInterpolator : set_fraction = {0}".format(set_fraction))
        print("OrientationInterpolator : key = {0}".format(key)) # imprime no terminal
        print("OrientationInterpolator : keyValue = {0}".format(keyValue))

        value_changed = GL.splinePositionInterpolator(set_fraction, key, keyValue, True, 4)

        # Abaixo está só um exemplo de como os dados podem ser calculados e transferidos
        #value_changed = [0, 0, 1, 0]

        return value_changed

    # Para o futuro (Não para versão atual do projeto.)
    def vertex_shader(self, shader):
        """Para no futuro implementar um vertex shader."""

    def fragment_shader(self, shader):
        """Para no futuro implementar um fragment shader."""
