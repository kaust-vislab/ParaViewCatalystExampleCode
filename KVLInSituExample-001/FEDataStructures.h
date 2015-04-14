#ifndef FEDATASTRUCTURES_HEADER
#define FEDATASTRUCTURES_HEADER

#include <cstddef>
#include <vector>
#include <cmath>

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
private:
  unsigned int NumPoints[3];
  unsigned int Extent[6];
  double Spacing[3];
};

const float TWO_PI = 6.28318530718;

const float A = 1.50;
const float B = 2.30;
const float C = 1.85;

const float k1 = TWO_PI*1.5;
const float k2 = TWO_PI*1.0;
const float k3 = TWO_PI*0.6;

const float w1 = TWO_PI*0.5;
const float w2 = TWO_PI*0.8;
const float w3 = TWO_PI*2.5;



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

private:
  std::vector<double> Velocity;
  std::vector<float> Pressure;
  Grid* GridPtr;
};
#endif
