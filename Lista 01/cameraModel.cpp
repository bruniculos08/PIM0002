#include <fstream>
#include<iostream>
#include<bits/stdc++.h>
#include <eigen3/Eigen/Dense>
using namespace Eigen;
using namespace std;

const int width = 1920, height = 1080;

class Point3D{
    public:
        double x, y, z;
};

class Edge2D{
    public:
        double x1, y1, x2, y2;
};

class Square{
    public:
        std::vector<Matrix<double, 4, 1>> vertices3D_list;
        std::vector<Matrix<double, 3, 1>> vertices2D_list;
        std::vector<Edge2D> edges2D_list;
        int r,g,b;
};

class ViewPlane{
    public:
        double height, width;
};

void build_square_proj2D(Matrix<double, 3, 4> &proj, Square &S, double d){
    Matrix<double, 3, 1> vertice2D;
    Edge2D e;
    for(Matrix<double, 4, 1> &v : S.vertices3D_list){
        vertice2D = (1/v(2,0)) * proj * v;
        S.vertices2D_list.push_back(vertice2D);
    }

    e.x1 = S.vertices2D_list[0](0,0);
    e.y1 = S.vertices2D_list[0](1,0);
    for(int i = 1; i <= S.vertices2D_list.size(); i++){
        if(i == S.vertices2D_list.size()){
            e.x2 = S.vertices2D_list[0](0,0);
            e.y2 = S.vertices2D_list[0](1,0);
        }
        else{
            e.x2 = S.vertices2D_list[i](0,0);
            e.y2 = S.vertices2D_list[i](1,0);
        }
        S.edges2D_list.push_back(e);
        e.x1 = e.x2;
        e.y1 = e.y2;
    }

}

bool RayCasting(double xp, double yp, vector<Edge2D> &edges){
    // implementar Ray Casting:
    int count = 0;
    for(Edge2D &e : edges){
        if( (yp < e.y1) != (yp < e.y2) && xp < e.x1 + (yp-e.y1)*(e.x2-e.x1)/(e.y2-e.y1) ) count++;
    }
    return (count%2 == 1);
}

void drawSquare(Matrix<double, 3, 4> &proj, Square &S){
    
    ofstream img("picture.ppm");
    img << "P3" << endl;
    img << width << " " << height << endl;
    img << "255" << endl;

    for(int y = 0; y < height; y++){
        for(int x = 0; x < width; x++){
            
            int r = 255;
            int g = 255;
            int b = 255;


            // if(RayCasting((double) -(x - width/2), (double) -(height/2 - y), S.edges2D_list)){
            //     r = S.r;
            //     g = S.g;
            //     b = S.b;
            // }

            if(RayCasting((double) x, (double) y, S.edges2D_list)){
                r = S.r;
                g = S.g;
                b = S.b;
            }

            // if(x > 100 && x < 900 && y > 100 && y < 900){
            //     r = S.r;
            //     g = S.g;
            //     b = S.b;
            // }
            
            img << r << " " << g << " " << b << endl;
        }
    }

    system("display picture.ppm");
}

int main(void){
    double Sx, Sy, Ox, Oy, d;
    Sx = 1;
    Sy = 1;
    // Note que apesador do centro de câmera ter coordena x = 0, para o novo sistema de cooordenadas devemos deslocar 1920/2 pois...
    // ... os pontos com coordenadas negativas devem ficar com coordenadas positivas. 
    Ox = width/2; 
    Oy = height/2;
    d = 1;

    Square S;
    S.r = 0;
    S.g = 180;
    S.b = 0;
    Matrix<double, 4, 1> vertice3D;
    
    vertice3D(0,0) = 250;
    vertice3D(1,0) = -250;
    vertice3D(2,0) = 5;
    vertice3D(3,0) = 1;
    S.vertices3D_list.push_back(vertice3D);
    
    vertice3D(0,0) = 250;
    vertice3D(1,0) = 250;
    vertice3D(2,0) = 5;
    vertice3D(3,0) = 1;
    S.vertices3D_list.push_back(vertice3D);

    vertice3D(0,0) = -250;
    vertice3D(1,0) = 250;
    vertice3D(2,0) = 7;
    vertice3D(3,0) = 1; 
    S.vertices3D_list.push_back(vertice3D);

    vertice3D(0,0) = -250;
    vertice3D(1,0) = -250;
    vertice3D(2,0) = 7;
    vertice3D(3,0) = 1; 
    S.vertices3D_list.push_back(vertice3D);
    
    Eigen::Matrix<double, 3, 4> perspec;
    perspec.setZero();
    perspec(0,0) = 1;
    perspec(1,1) = 1;
    perspec(2,2) = 1/d;
    
    Eigen::Matrix<double, 3, 3> rot_padrao;
    rot_padrao.setZero();
    rot_padrao(0, 0) = 1;
    rot_padrao(1, 1) = -1;
    rot_padrao(2, 2) = 1;

    Eigen::Matrix<double, 3, 3> escala_padrao;
    escala_padrao.setZero();
    escala_padrao(0, 0) = 1/Sx;
    escala_padrao(1, 1) = 1/Sy;
    escala_padrao(2, 2) = 1;

    Eigen::Matrix<double, 3, 3> tr_padrao;
    tr_padrao.setZero();
    tr_padrao(0, 0) = 1;
    tr_padrao(1, 1) = 1;
    tr_padrao(2, 2) = 1;
    tr_padrao(0, 2) = Ox;
    tr_padrao(1, 2) = Oy;

    Matrix<double, 3, 4> proj;
    // Note que a rotação ocorre antes da translação, isto é, a coordenada y primeiro fica negativa e depois...
    // ... é somada a height, assim temos a conversão para o sistema de coordenadas da tela (eixo y aponta pra baixo).
    proj = (tr_padrao * escala_padrao * rot_padrao * perspec);

    // Obs.: o sistema de coordenadas da ppm tem o y invertido.

    build_square_proj2D(proj, S, d);

    // Obs.: Lembrar que estamos considerando o centro do plano da câmera como (0,540,5).

    cout << S.vertices3D_list[0] << endl;
    cout << "---------" << endl;
    cout << S.vertices2D_list[0] << endl;
    cout << "---------" << endl;

    cout << S.vertices3D_list[1] << endl;
    cout << "---------" << endl;
    cout << S.vertices2D_list[1] << endl;

    drawSquare(proj, S);

    return 0;
}

// Interseção de ponto em reta
// p = (xp, yp)
// r(x) = (dy/dx)*x + y0
// ou podemos montar como vetor, e ai temos a seguintes:
// r = t*v + v0  
// r = t*(v1-v0) + v0
// a equação a se resolver é:
// p = r  
// (xp, yp) = t*(v1-v0) + v0
// note que separando as coordenadas temos  
// xp = t*(x1-x0) + x0 => (xp-x0)/(x1-x0) = t
// yp = t*(y1-y0) + y0 => (yp-y0)/(y1-y0) = t
// note que:
// (1) se o sistema tiver solução os dois valores de t serão iguais
// (2) se v0 e v1 são vértices de um quadrado só haverá intersecção se 0 <= t <= 1
// agora caso tenhamos uma reta horizontal (para raycasting 2D) note que nossa reta será da seguinte forma:
// h = t*v + v0 
// h = t*(v1-v0) + v0
// separando as coordenadas teremos:
// xh = t*(x1-x0) + x0
// yh = t*(y1-y0) + y0
// como sabemos que y não varia e visto que x não nos interessa, dado que pode assumir qualquer valor, temos:
// yh = y0
// isto é, basta verificarmos se a reta horizontal passa por um valor de y no qual a reta também passa, porém para...
// verificar se o ponto está dentro dp.