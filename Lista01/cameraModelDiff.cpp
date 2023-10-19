#include <fstream>
#include<iostream>
#include<bits/stdc++.h>
#include<math.h>
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
        std::vector<Matrix<double, 4, 1>> vertices2D_list;
        std::vector<Edge2D> edges2D_list;
        int r,g,b;
};

class ViewPlane{
    public:
        double height, width;
};

void build_square_proj2D(Matrix<double, 4, 4> &proj, Square &S, double d){
    Matrix<double, 4, 1> vertice2D;
    Edge2D e;
    for(Matrix<double, 4, 1> &v : S.vertices3D_list){
        vertice2D = (proj * v);
        vertice2D = (1/vertice2D(2)) * vertice2D;
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

void drawSquare(Square &S){
    
    ofstream img("picture.ppm");
    img << "P3" << endl;
    img << width << " " << height << endl;
    img << "255" << endl;

    for(int y = 0; y < height; y++){
        for(int x = 0; x < width; x++){
            
            int r = 255;
            int g = 255;
            int b = 255;

            if(RayCasting((double) 1920 - x, (double) 1080 - y, S.edges2D_list)){
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
    double d, f, fov_h, fov_v;
    d = 1;
    f = 20;
    fov_h = fov_v = 90;


    Square S;
    S.r = 0;
    S.g = 180;
    S.b = 0;
    Matrix<double, 4, 1> vertice3D;
    
    vertice3D(0,0) = 250;
    vertice3D(1,0) = 250;
    vertice3D(2,0) = -5;
    vertice3D(3,0) = 1;
    S.vertices3D_list.push_back(vertice3D);
    
    vertice3D(0,0) = 250;
    vertice3D(1,0) = 500;
    vertice3D(2,0) = -5;
    vertice3D(3,0) = 1;
    S.vertices3D_list.push_back(vertice3D);

    vertice3D(0,0) = -250;
    vertice3D(1,0) = 500;
    vertice3D(2,0) = -7;
    vertice3D(3,0) = 1; 
    S.vertices3D_list.push_back(vertice3D);

    vertice3D(0,0) = -250;
    vertice3D(1,0) = 250;
    vertice3D(2,0) = -7;
    vertice3D(3,0) = 1; 
    S.vertices3D_list.push_back(vertice3D);

    Matrix<double, 4, 4> proj;
    proj.setZero();
    proj(0,0) = 1/(tan((fov_h*M_PI)/(2*360)));
    proj(1,1) = 1/(tan((fov_v*M_PI)/(2*360)));
    proj(2,2) = -f/(f-d);
    proj(2,3) = -f*d/(f-d);
    proj(3,2) = -1;

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

    drawSquare(S);

    // ofstream img("picture.ppm");
    // img << "P3" << endl;
    // img << width << " " << height << endl;
    // img << "255" << endl;

    // for(int y = 0; y < height; y++){
    //     for(int x = 0; x < width; x++){
    //         int r = x % 255;
    //         int g = y % 255;
    //         int b = (x*y) % 255;

    //         img << r << " " << g << " " << b << endl;
    //     }
    // }

    // system("display picture.ppm");
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