#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <vector>
#include <thread>
#include <chrono>
using namespace std;

bool close(double a, double b);

class Point{
    public:
        double x,y,z;
        Point(){}
        Point(double x_, double y_, double z_){
            x = x_;
            y = y_;
            z = z_;
        }

        double dotProduct(Point p){
            return x * p.x + y * p.y + z * p.z;

        }

        double normalize(){
            return sqrt(x*x + y*y + z*z);
        }

        string toString(){
            return "Point(" + to_string(x) + ", " + to_string(y) + ", " + to_string(z) + ")";
        }

        void copy(Point a){
            x = a.x;
            y = a.y;
            z = a.z;
        }

        bool same(Point a){
            if (x == a.x and y == a.y and z == a.z){
                return true;
            }
            else { return false;}
        }

        bool equals(Point p){
            if(close(x,p.x) and close(y,p.y) and close(z,p.z)){
                return true;
            }
            else{
                return false;
            }
        }
};

bool close(double a, double b){
    double comp = max(a,b) - min(a,b);
    return ((comp > -0.001) and (comp < 0.001));
}

class Line{
    public:
        Point p0, p1;

        Line(){}
        Line(Point a, Point b){
            p0.copy(a);
            p1.copy(b);
        }

        string toString(){
            return "Line( " + p0.toString() + ", " + p1.toString() + ")";
        }

        void reverse(){
            double x_ = p0.x;
            double y_ = p0.y;
            double z_ = p0.z;
            p0.x = p1.x;
            p1.x = x_;
            p0.y = p1.y;
            p1.y = y_;
            p0.z = p1.z;
            p1.z = z_;
        }

};


bool pointInLine(Point p, Line line){
    if(close(p.x, line.p0.x) and close(p.y, line.p0.y) and close(p.z, line.p0.z)){
        return true;
    }
    else if(close(p.x, line.p1.x) and close(p.y, line.p1.y) and close(p.z, line.p1.z)){
        return true;
    }
    else{
        return false;
    }
}

class Triangle{
    public:
        Point p0,p1,p2,norm;

        Triangle(Point a, Point b, Point c, Point n){
            p0.copy(a);
            p1.copy(b);
            p2.copy(c);
            norm.copy(n);
        }

        string toString(){
            return "Triangle( " + p0.toString() + ", " + p1.toString() + ", " + p2.toString() + ")";
        }
};

bool triangleEqual(Triangle t1, Triangle t2){
    if ((t1.p0.equals(t2.p0) and t1.p1.equals(t2.p1) and t1.p2.equals(t2.p2))
            or (t1.p0.equals(t2.p0) and t1.p1.equals(t2.p2) and t1.p2.equals(t2.p1))
            or (t1.p0.equals(t2.p1) and t1.p1.equals(t2.p0) and t1.p2.equals(t2.p2))
            or (t1.p0.equals(t2.p1) and t1.p1.equals(t2.p2) and t1.p2.equals(t2.p0))
            or (t1.p0.equals(t2.p2) and t1.p1.equals(t2.p0) and t1.p2.equals(t2.p1))
            or (t1.p0.equals(t2.p2) and t1.p1.equals(t2.p1) and t1.p2.equals(t2.p0))){
            return true;
    }
    else{
        return false;
    }
}

vector<Triangle> fileToTriangle(vector<double> coordinates){
    vector<Triangle> triangles_asc;
    for(int i=0;i < coordinates.size();i+=12){
        Point n(coordinates[i],coordinates[i+1],coordinates[i+2]);
        Point a(coordinates[i+3],coordinates[i+4],coordinates[i+5]);
        Point b(coordinates[i+6],coordinates[i+7],coordinates[i+8]);
        Point c(coordinates[i+9],coordinates[i+10],coordinates[i+11]);
        Triangle t(a,b,c,n);
        triangles_asc.push_back(t);
    }
    return triangles_asc;
}

vector<double> readFile(){
    vector<double> asc;
    fstream filee;
    filee.open("Resources/temp/asc.txt");
    if(!filee){
        cout<<"Error with input file!"<<endl;
    }
    else{
        string a;
        filee>>a;
        while(!filee.eof()){
            asc.push_back(stod(a));
            filee>>a;
        }
    }
    if(asc.size()<1){
        cout<<"Blank input file!!"<<endl;
    }
    filee.close();
    return asc;
}

Point intersectSlice(Line line, double plane, double *tant){
    //cout<<"called";
    if(line.p0.z == line.p1.z and line.p1.z == plane){
        *tant = 0;
        return line.p0;
    }
    else if(line.p0.z == line.p1.z){
        *tant = 123456789;
        return Point(-999999999,-999999999, -999999999);
    }
    else{
        Point slope = Point((line.p1.x-line.p0.x),(line.p1.y-line.p0.y),(line.p1.z-line.p0.z));
        double t = (plane - line.p0.z) / slope.z;
        if (t >= 0 and t <= 1){
            double testZ = line.p0.z + t*slope.z;
            double xy = sqrt(pow((line.p1.x - line.p0.x),2) + pow((line.p1.y - line.p0.y),2));

            if (max(line.p0.z, line.p1.z) >= testZ and testZ >= min(line.p0.z, line.p1.z)) {
                *tant = (line.p1.z - line.p0.z)/xy;
                return Point(line.p0.x + t*slope.x, line.p0.y + t*slope.y, line.p0.z + t*slope.z);
            }
            else{
                *tant = 123456789;
                return Point(-999999999,-999999999, -999999999);
            }
        }
        else{
            *tant = 123456789;
            return Point(-999999999,-999999999, -999999999);
        }
    }
}

double sign(Point p1, Point p2, Point p3){
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y);
}

vector<double> findBoundaries(vector<Triangle> triangles){
    double bottomZ = 9999999999;
    double topZ = -9999999999;
    for (int i =0; i<triangles.size(); i++){
        double maximum = max(max(triangles[i].p0.z, triangles[i].p1.z), triangles[i].p2.z);
        double minimum = min(min(triangles[i].p0.z, triangles[i].p1.z), triangles[i].p2.z);
        if(maximum > topZ){
            topZ = maximum;
        }
        if(minimum < bottomZ){
            bottomZ = minimum;
        }
    }
    vector<double> a{bottomZ, topZ};
    return a;
}

class Slice{
    public:
        double zValue;
        vector<Line> perimeter;
        bool isSurface;
        float layer_height;

        Slice(){}
        Slice(double z, vector<Line> peri, bool surf, float h=0.1){//, double tant){
            zValue = z;
            perimeter = peri;
            isSurface = surf;
            layer_height = h;
        }

        string present(){
            string s = "Slice: z: ";
            s += to_string(zValue);
            s += "\nSegments:\n";
            //return s;
            /*
            for(int i=0; i < perimeter.size(); i++){
                s += to_string(perimeter[i].p0.x) + " " + to_string(perimeter[i].p0.y) + " " + to_string(perimeter[i].p0.z);
                s += " ";
                s += to_string(perimeter[i].p1.x) + " " + to_string(perimeter[i].p1.y) + " " + to_string(perimeter[i].p1.z);
                s += "\n";
            }
            s += "isSurface: ";
            s += to_string(isSurface);
            s += "\n\n";*/
            //s += to_string(minAngle);
            s += "\n\n";
            return s;
        }
};

vector<int> ten_per(vector<Triangle> triangles_asc, double current_z);

int separateSlices(vector<Triangle> triangles_asc, vector<Slice> *seg, vector<double> slices){

    //vector<Slice> segments;
    //cout<<"Slicing model:"<<(bounds[1] - bounds[0])<<endl;

    //double total = bounds[1] - bounds[0];
    for (int i=0; i < slices.size(); i++){
        //cout<<i<<endl;
        vector<Line> currentSegment;
        bool currentSegmentSurface = false;
        //cout<<"\r"<<(i / (numSlices+1))*100<<"%";
        vector<double> tant;
        //vector<int> ten = ten_per(triangles_asc, slices[i]);
        //for (int m = ten[0]; m <= ten[1]; m++){
        for(int m = 0; m < triangles_asc.size(); m++){
            double t1, t2, t3;
            Point p1 = intersectSlice(Line(triangles_asc[m].p0, triangles_asc[m].p1), slices[i], &t1);
            Point p2 = intersectSlice(Line(triangles_asc[m].p1, triangles_asc[m].p2), slices[i], &t2);
            Point p3 = intersectSlice(Line(triangles_asc[m].p2, triangles_asc[m].p0), slices[i], &t3);
            //cout<<endl;
            vector<Point> points_ {p1,p2,p3};
            vector<double> tant_ {t1,t2,t3};
            vector<Point> points;

            Point nullPoint(-999999999, -999999999, -999999999);
            for(int j=0; j<3; j++){
                if (points_[j].same(nullPoint)){
                    points_.erase(points_.begin() + j);
                    tant_.erase(tant_.begin() + j);
                    break;
                }
            }

            int k;
            for (int l=0; l<points_.size(); l++){
                k = l + 1;
                bool unique = true;
                while(k < points_.size()){
                    if (points_[l].equals(points_[k])){
                        unique = false;
                    }
                    k += 1;
                }
                if (unique){
                    tant.push_back(tant_[l]);
                    points.push_back(points_[l]);
                }
            }

            if(points.size() == 2){
                currentSegment.push_back(Line(points[0], points[1]));
            }
            else if(points.size() == 3){
                Line s1 = Line(points[0], points[1]);
                Line s2 = Line(points[1], points[2]);
                Line s3 = Line(points[2], points[0]);
                currentSegmentSurface = true;

                currentSegment.push_back(s1);
                currentSegment.push_back(s2);
                currentSegment.push_back(s3);
            }


        }
        double mini = 999999;
        for (int p=0; p< tant.size();p++){
            if(tant[p]<mini){
                mini = tant[p];
            }
        }
        float h;
        if (abs(mini) < 0.5774){
            h = 0.1;
        }
        //else if(abs(mini) >= 0.4663 and abs(mini) < 0.7002){
        //    h = 0.15;
        //}
        else if(abs(mini) >=0.5773 and abs(mini) < 1.7320){
            h = 0.2;
        }
        //else if(abs(mini) >= 1.4281 and abs(mini) < 2.1445){
        //    h = 0.25;
        //}
        else{
            h = 0.3;
        }
        (*seg).push_back(Slice(slices[i],currentSegment,currentSegmentSurface,h));//, mini));
    }
    //*seg = segments;
    return 0;
}

vector<int> ten_per(vector<Triangle> triangles_asc, double current_z){
    int low = 0;
    double biggest = triangles_asc[low].p2.z;
    while(biggest < current_z){
        low++;
        biggest = triangles_asc[low].p2.z;
    }
    int high = triangles_asc.size();
    double smallest = triangles_asc[high].p0.z;
    while(smallest > current_z){
        high--;
        smallest = triangles_asc[high].p0.z;
    }
    vector<int> a = {low, high};
    return a;
}

vector<double> slice2model(vector<Slice> slices){ //, vector<int> *shades){
    vector<double> ret_value;
    for (int i=0; i<slices.size(); i++){
        vector<Line> peri = slices[i].perimeter;
        float k = slices[i].layer_height;
        //cout<<"Min-Angle: "<<slices[i].minAngle<<endl;
        //if(peri.size() == 0){
        //    continue;
        //}

        //cout<<k<<endl;


        for (int j=0;j<peri.size();j++){
            ret_value.push_back(peri[j].p0.x);
            ret_value.push_back(peri[j].p0.y);
            ret_value.push_back(peri[j].p0.z);
            ret_value.push_back(peri[j].p1.x);
            ret_value.push_back(peri[j].p1.y);
            ret_value.push_back(peri[j].p1.z);
            ret_value.push_back(peri[j].p0.x);
            ret_value.push_back(peri[j].p0.y);
            ret_value.push_back(peri[j].p0.z + k);
            ret_value.push_back(peri[j].p0.x);
            ret_value.push_back(peri[j].p0.y);
            ret_value.push_back(peri[j].p0.z + k);
            ret_value.push_back(peri[j].p1.x);
            ret_value.push_back(peri[j].p1.y);
            ret_value.push_back(peri[j].p1.z);
            ret_value.push_back(peri[j].p1.x);
            ret_value.push_back(peri[j].p1.y);
            ret_value.push_back(peri[j].p1.z + k);
            /*
            if(round(k*10)==3){
                (*shades).push_back(3);
                (*shades).push_back(3);
            }
            else if(round(k*10)==2){
                (*shades).push_back(2);
                (*shades).push_back(2);
            }
            else{
                (*shades).push_back(1);
                (*shades).push_back(1);
            }*/
            //colors.push_back(colors[trunc(k*10)]);

        }
    }
    return ret_value;
}

void writeSliceData(vector<double> model){

    vector<string> data;
    data.push_back("solid Adap");
    string temp ="";
    for(int m=0; m < model.size();m+=9){
        temp = "  facet normal ";
        temp += to_string(((model[m+4] - model[m+1]) * (model[m+8] * model[m+2])) - ((model[m+5] - model[m+2]) * (model[m+7] - model[m+1])));
        temp += " ";
        temp += to_string(((model[m+5] - model[m+2]) * (model[m+6] * model[m+0])) - ((model[m+3] - model[m+0]) * (model[m+8] - model[m+2])));
        temp += " ";
        temp += to_string(((model[m+3] - model[m+0]) * (model[m+7] * model[m+1])) - ((model[m+3] - model[m+0]) * (model[m+8] - model[m+2])));
        data.push_back(temp);
        data.push_back("    outer loop");
        temp = "      vertex ";
        temp += to_string(model[m+0]);
        temp += " ";
        temp += to_string(model[m+1]);
        temp += " ";
        temp += to_string(model[m+2]);
        data.push_back(temp);
        temp = "      vertex ";
        temp += to_string(model[m+3]);
        temp += " ";
        temp += to_string(model[m+4]);
        temp += " ";
        temp += to_string(model[m+5]);
        data.push_back(temp);
        temp = "      vertex ";
        temp += to_string(model[m+6]);
        temp += " ";
        temp += to_string(model[m+7]);
        temp += " ";
        temp += to_string(model[m+8]);
        data.push_back(temp);
        data.push_back("    endloop");
        data.push_back("  endfacet");
        temp ="";
    }
    data.push_back("endsolid Adap");
    //cout<<"here"<<endl;
    /*
    vector<double> data;
    for(int m=0;m<model.size();m+=9){
        //data.push_back(((model[m+4] - model[m+1]) * (model[m+8] * model[m+2])) - ((model[m+5] - model[m+2]) * (model[m+7] - model[m+1])));
        //data.push_back(((model[m+5] - model[m+2]) * (model[m+6] * model[m+0])) - ((model[m+3] - model[m+0]) * (model[m+8] - model[m+2])));
        //data.push_back(((model[m+3] - model[m+0]) * (model[m+7] * model[m+1])) - ((model[m+3] - model[m+0]) * (model[m+8] - model[m+2])));
        data.push_back(model[m]);
        data.push_back(model[m+1]);
        data.push_back(model[m+2]);
        data.push_back(model[m+3]);
        data.push_back(model[m+4]);
        data.push_back(model[m+5]);
        data.push_back(model[m+6]);
        data.push_back(model[m+7]);
        data.push_back(model[m+8]);
    }
    */
    ofstream filee;
    filee.open("Resources/temp/adap.stl", ios::out | ios::trunc);;
    //file.open
    if(!filee){
        cout<<"Error creating output file!!"<<endl;
    }
    else{
        for (int i=0;i<data.size();i++){
            filee<<data[i]<<endl;
            //cout<<data[i]<<endl;
        }
        /*
        for (int i=0;i<data.size();i+=3){
            file<<
        }*/

    }
    filee.close();
    //cout<<"done writing"<<endl;
}

bool lineEqual(Line l1, Line l2){
    if ((close(l1.p0.x, l2.p0.x) and close(l1.p0.y,l2.p0.y) and close(l1.p1.x, l2.p1.x) and close(l1.p1.y, l2.p1.y))
    or (close(l1.p0.x, l2.p1.x) and close(l1.p0.y, l2.p1.y) and close(l1.p1.x, l2.p0.x) and close(l1.p1.y, l2.p0.y))){
        return true;
    }
    else{
        return false;
    }
}

Slice cleanPerimeter(Slice segments){
    vector<Line> setPerimeter = segments.perimeter;
    int i = 0;
    while (i < setPerimeter.size()){
        int j = i +1;
        while(j < setPerimeter.size()){
            if(lineEqual(setPerimeter[i], setPerimeter[j])){
                //setPerimeter.remove(setPerimeter[j]);
                setPerimeter.erase(setPerimeter.begin() + j);
            }
            else{
                j += 1;
            }
        }
        i += 1;
    }
    return Slice(segments.zValue,setPerimeter,segments.isSurface);
}


vector<double> shift2origin(vector<double> coords){
    double temp = 99999999;
    //For X:
    for(int i=0;i<coords.size();i+=12){
        temp = min(temp, coords[i+3]);
        temp = min(temp, coords[i+6]);
        temp = min(temp, coords[i+9]);
    }
    //cout<<temp<<endl;
    for(int i=0;i<coords.size();i+=12){
        //cout<<coords[i+3]<<" ";
        coords[i+3] -= temp;
        //cout<<coords[i+3]<<endl;
        coords[i+6] -= temp;
        coords[i+9] -= temp;
    }

    temp = 99999999;
    //For Y:
    for(int i=0;i<coords.size();i+=12){
        temp = min(temp, coords[i+4]);
        temp = min(temp, coords[i+7]);
        temp = min(temp, coords[i+10]);
    }
    for(int i=0;i<coords.size();i+=12){
            coords[i+4] -= temp;
            coords[i+7] -= temp;
            coords[i+10] -= temp;
    }
    temp = 99999999;
    //For Z:

    for(int i=0;i<coords.size();i+=12){
        temp = min(temp, coords[i+5]);
        temp = min(temp, coords[i+8]);
        temp = min(temp, coords[i+11]);
    }

    for(int i=0;i<coords.size();i+=12){
            //cout<<coords[i+5]<<" ";
            coords[i+5] -= temp;
            //cout<<coords[i+5]<<endl;
            coords[i+8] -= temp;
            coords[i+11] -= temp;
    }
    return coords;
}

int main(){
    vector<double> fileData = readFile();
    vector<double> shifted = shift2origin(fileData);
    //cout<<"shifted"<<endl;
    vector<Triangle> triangles = fileToTriangle(shifted);
    //cout<<"converted to triangles"<<endl;
    vector<Slice> segments1;
    vector<Slice> segments2;
    vector<Slice> segments3;
    vector<Slice> segments4;
    //vector<Slice> segments5;
    vector<double> bounds = findBoundaries(triangles);
    int numSlices = (int)((bounds[1] - bounds[0]) / 0.1);
    //cout<<"NUm "<<numSlices<<endl;
    vector<double> slices1;
    vector<double> slices2;
    vector<double> slices3;
    vector<double> slices4;
    vector<double> slices5;
    for(int i=0; i<(int)numSlices*0.25; i++){
        slices1.push_back(bounds[0] + i*0.1);
    }
    for(int i=(int)numSlices*0.25; i<(int)numSlices*0.5; i++){
        slices2.push_back(bounds[0] + i*0.1);
    }
    for(int i=(int)numSlices*0.5; i<(int)numSlices*0.75; i++){
        slices3.push_back(bounds[0] + i*0.1);
    }
    for(int i=(int)numSlices*0.75; i<(int)numSlices; i++){
        slices4.push_back(bounds[0] + i*0.1);
    }/*
    for(int i=(int)numSlices*0.8; i<(int)numSlices; i++){
        slices5.push_back(bounds[0] + i*0.1);
    }*/
    //cout<<"Started slicing"<<endl;
    thread t1(separateSlices,triangles,&segments1,slices1);
    thread t2(separateSlices,triangles,&segments2,slices2);
    thread t3(separateSlices,triangles,&segments3,slices3);
    thread t4(separateSlices,triangles,&segments4,slices4);
    //thread t5(separateSlices,triangles,&segments5,slices5);
    t1.join();
    t2.join();
    t3.join();
    t4.join();
    //t5.join();
    //vector<Slice> segments {separateSlices(triangles)};
    /*vector<Slice> segmentsC;
    for (int i =0;i < segments.size();i++){
        segmentsC.push_back(cleanPerimeter(segments[i]));
    }
    //segments = cleanPerimeter(segments);*/
    //cout<<"Sliced"<<endl;
    vector<Slice> segments;
    //separateSlices(triangles,&segments);
    segments.reserve(segments1.size()*4);
    segments.insert(segments.end(), segments1.begin(), segments1.end());
    segments.insert(segments.end(), segments2.begin(), segments2.end());
    segments.insert(segments.end(), segments3.begin(), segments3.end());
    segments.insert(segments.end(), segments4.begin(), segments4.end());
    //segments.insert(segments.end(), segments5.begin(), segments5.end());
    int i = 0;
    vector<Slice> shortlist;

    while(i<segments.size()){
        float h = segments[i].layer_height;
        //cout<<"HH:  "<<h<<endl;
        if (i==segments.size()-1){
            segments[i].layer_height = bounds[1] - segments[i].zValue;
            shortlist.push_back(segments[i]);
            i++;
        }
        else{
            if (round(h*10)==1){
                shortlist.push_back(segments[i]);
                i++;
            }
            else if (round(h*10)==2){
                shortlist.push_back(segments[i]);
                i+=2;
            }
            else if (round(h*10)==3){
                shortlist.push_back(segments[i]);
                i+=3;
            }
        }
    }

    //vector<int> shades;
    vector<double> model = slice2model(shortlist); //, &shades);
    /*
    //cout<<"created model"<<endl;
    ofstream filee;
    filee.open("Resources/temp/shades.txt", ios::out | ios::trunc);;
    //file.open
    if(!filee){
        //cout<<"Error creating output file!!"<<endl;
    }
    else{
        for (int j=0; j<shades.size(); j++){
            filee<<shades[j]<<endl;
        }
    }
    filee.close();*/
    //cout<<"Colors added"<<endl;
    /*
    for(int p=0;p<model.size();p++){
        cout<<"DXC "<<model[p]<<endl;
    }
    */
    writeSliceData(model);

    return 0;
}