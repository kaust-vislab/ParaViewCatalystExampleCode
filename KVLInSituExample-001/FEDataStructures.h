#ifndef FEDATASTRUCTURES_HEADER
#define FEDATASTRUCTURES_HEADER

#include <mpi.h>
#include <cstddef>
#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>


class Logger{
 public:
    std::ofstream logfile;

    Logger(){
        if(logfile.is_open()){
            std::cout<<"Error: File already open !"<<std::endl;
        }
        else{
            int mpiRank = 0;
            MPI_Comm_rank(MPI_COMM_WORLD, &mpiRank);
            char filename[80];
            sprintf(filename,"logs/logfile-rank-%03d.log",mpiRank);
            logfile.open(filename);
        }
    }
    void write(const char* msg){
        logfile<<msg<<std::endl;
    }
    ~Logger(){
        logfile.close();
    }
};

class Grid
{
public:
  Grid();
  void Initialize(const unsigned int numPoints[3], const double spacing[3]);
  unsigned int GetNumberOfLocalPoints();
  unsigned int GetNumberOfLocalCells();
  void GetLocalPoint(unsigned int pointId, double* point);
  unsigned int* GetNumPoints();
  unsigned int* GetExtent();
  double* GetSpacing();

  int mpiRank;
  int mpiSize;
private:
  unsigned int NumPoints[3];
  unsigned int Extent[6];
  double Spacing[3];
};

const float TWO_PI = 6.28318530718;

const float A = 5.0;
const float B = 10.0;
const float C = 0.0;

const float k1 = 0.00032;
const float k2 = 0.0314;
const float k3 = 0.00124;

const float w1 = TWO_PI*0.0;
const float w2 = TWO_PI*0.0;
const float w3 = TWO_PI*0.0;



class Attributes
{
// A class for generating and storing point and cell fields.
// Velocity is stored at the points and pressure is stored
// for the cells. The current velocity profile is for a
// shearing flow with U(y,t) = y*t, V = 0 and W = 0.
// Pressure is constant through the domain.
public:
  Attributes();
  void Initialize(Grid* grid);
  void UpdateFields(double time);
  double* GetVelocityArray();
  float* GetPressureArray();
  void SaveFields(double time);
private:
  std::vector<double> Velocity;
  std::vector<float> Pressure;
  Grid* GridPtr;
};
#endif
