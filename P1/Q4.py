# Alunos: Bruno R. dos Santos e Luigi
import numpy as np

if __name__ == "__main__":
    np.set_printoptions(suppress = True)

    # Largura e altura do plano focal dividida por 2:
    Ox = 1024
    Oy = 1024

    # Dimensões dos pixels:
    Sy = Sx = 0.0075

    # Distância focal em mm (logo trata-se as coordenas x y z em mm):
    f = 5 

    M_translacao = np.zeros((3, 3))
    M_translacao[0][0] = 1
    M_translacao[1][1] = 1
    M_translacao[2][2] = 1
    M_translacao[0][2] = Ox
    M_translacao[1][2] = Oy

    print(M_translacao)

    M_escala = np.zeros((3, 3))
    M_escala[0][0] = 1/Sx
    M_escala[1][1] = 1/Sy
    M_escala[2][2] = 1

    M_rot = np.zeros((3,3))
    M_rot[0][0] = 1
    M_rot[1][1] = -1
    M_rot[2][2] = 1

    M_perspective = np.zeros((3, 4))
    M_perspective[0][0] = 1
    M_perspective[1][1] = 1
    M_perspective[2][2] = 1/f

    M_proj = np.dot(M_translacao, np.dot(M_escala, np.dot(M_rot, M_perspective)))
    
    print(M_proj)

    Point_a = np.zeros((4))
    Point_a[0] = 650.7
    Point_a[1] = 2000
    Point_a[2] = 1500
    Point_a[3] = 1
    # Point_a_projected = np.dot(M_proj, Point_a)
    Point_a_projected = (1/(np.dot(M_proj,Point_a)[2]))*np.dot(M_proj, Point_a)

    Point_b = np.zeros((4))
    Point_b[0] = 653.5
    Point_b[1] = 2000
    Point_b[2] = 1500
    Point_b[3] = 1
    Point_b_projected = (1/(np.dot(M_proj,Point_b)[2]))*np.dot(M_proj, Point_b)

    Point_c = np.zeros((4))
    Point_c[0] = 650.7
    Point_c[1] = 1990
    Point_c[2] = 1500
    Point_c[3] = 1
    Point_c_projected = (1/(np.dot(M_proj,Point_c)[2]))*np.dot(M_proj, Point_c)

    Point_d = np.zeros((4))
    Point_d[0] = 653.5
    Point_d[1] = 1990
    Point_d[2] = 1500
    Point_d[3] = 1
    Point_d_projected = (1/(np.dot(M_proj,Point_d)[2]))*np.dot(M_proj, Point_d)

    Point_e = np.zeros((4))
    Point_e[0] = 645.3
    Point_e[1] = 500.3
    Point_e[2] = 1500
    Point_e[3] = 1
    Point_e_projected = (1/(np.dot(M_proj,Point_e)[2]))*np.dot(M_proj, Point_e)

    Point_f = np.zeros((4))
    Point_f[0] = 645
    Point_f[1] = 500.3
    Point_f[2] = 1500
    Point_f[3] = 1
    Point_f_projected = (1/(np.dot(M_proj,Point_f)[2]))*np.dot(M_proj, Point_f)

    Point_g = np.zeros((4))
    Point_g[0] = 645.3
    Point_g[1] = 500
    Point_g[2] = 1500
    Point_g[3] = 1    
    Point_g_projected = (1/(np.dot(M_proj,Point_g)[2]))*np.dot(M_proj, Point_g)

    Point_h = np.zeros((4))
    Point_h[0] = 645
    Point_h[1] = 500
    Point_h[2] = 1500
    Point_h[3] = 1
    Point_h_projected = (1/(np.dot(M_proj,Point_h)[2]))*np.dot(M_proj, Point_h)

    print("Ponto a:")
    print(Point_a_projected[0:2])

    print("Ponto b:")
    print(Point_b_projected[0:2])

    print("Ponto c:")
    print(Point_c_projected[0:2])    

    print("Ponto d:")
    print(Point_d_projected[0:2])

    print("Ponto e:")
    print(Point_e_projected[0:2])

    print("Ponto f:")
    print(Point_f_projected[0:2])

    print("Ponto g:")
    print(Point_g_projected[0:2])

    print("Ponto h:")
    print(Point_h_projected[0:2])