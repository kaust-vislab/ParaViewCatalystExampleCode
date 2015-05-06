#include "FEDataStructures.h"


#include <assert.h>

extern Logger* LOG;

Grid::Grid()
{
  this->NumPoints[0] = this->NumPoints[1] = this->NumPoints[2] = 0;
  this->Spacing[0] = this->Spacing[1] = this->Spacing[2] = 0;
}

void Grid::Initialize(const unsigned int numPoints[3], const double spacing[3] )
{
  if(numPoints[0] == 0 || numPoints[1] == 0 || numPoints[2] == 0)
    {
    std::cerr << "Must have a non-zero amount of points in each direction.\n";
    }
  for(int i=0;i<3;i++)
    {
    this->NumPoints[i] = numPoints[i];
    this->Spacing[i] = spacing[i];
    }
  mpiRank = 0, mpiSize = 1;
  MPI_Comm_rank(MPI_COMM_WORLD, &mpiRank);
  MPI_Comm_size(MPI_COMM_WORLD, &mpiSize);
  this->Extent[0] = mpiRank*numPoints[0]/mpiSize;
  this->Extent[1] = (mpiRank+1)*numPoints[0]/mpiSize;
  if(mpiSize != mpiRank+1)
    {
    this->Extent[1]++;
    }
  this->Extent[2] = this->Extent[4] = 0;
  this->Extent[3] = numPoints[1];
  this->Extent[5] = numPoints[2];
}

unsigned int Grid::GetNumberOfLocalPoints()
{
  return (this->Extent[1]-this->Extent[0]+1)*(this->Extent[3]-this->Extent[2]+1)*
    (this->Extent[5]-this->Extent[4]+1);
}

unsigned int Grid::GetNumberOfLocalCells()
{
  return (this->Extent[1]-this->Extent[0])*(this->Extent[3]-this->Extent[2])*
    (this->Extent[5]-this->Extent[4]);
}

void Grid::GetLocalPoint(unsigned int pointId, double* point)
{
  unsigned int logicalX = pointId%(this->Extent[1]-this->Extent[0]+1);
  assert(logicalX <= this->Extent[1]);
  point[0] = this->Spacing[0]*logicalX;
  unsigned int logicalY = pointId%((this->Extent[1]-this->Extent[0]+1)*(this->Extent[3]-this->Extent[2]+1));
  logicalY /= this->Extent[1]-this->Extent[0]+1;
  assert(logicalY <= this->Extent[3]);
  point[1] = this->Spacing[1]*logicalY;
  unsigned int logicalZ = pointId/((this->Extent[1]-this->Extent[0]+1)*
                                   (this->Extent[3]-this->Extent[2]+1));
  assert(logicalZ <= this->Extent[5]);
  point[2] = this->Spacing[2]*logicalZ;
}

unsigned int* Grid::GetNumPoints()
{
  return this->NumPoints;
}

unsigned int* Grid::GetExtent()
{
  return this->Extent;
}

double* Grid::GetSpacing()
{
  return this->Spacing;
}

Attributes::Attributes()
{
  this->GridPtr = NULL;
}

void Attributes::Initialize(Grid* grid)
{
  this->GridPtr = grid;
}


void Attributes::UpdateFields(double time)
{
    unsigned int numPoints = this->GridPtr->GetNumberOfLocalPoints();

    this->Velocity.resize(numPoints*3);
    char buffer[80];
    sprintf(buffer,"Timestep: %f", time);
    LOG->write(buffer);

    for(unsigned int pt=0;pt<numPoints;pt++)
    {
        double coord[3];
        this->GridPtr->GetLocalPoint(pt, coord);

        this->Velocity[pt] = 0.1*(coord[2]-512.0)*time;
        this->Velocity[pt+numPoints] = 0.054*(coord[0]-256.0)*time;
        this->Velocity[pt+2*numPoints] = 0.085*(coord[1]-256.0)*time;

        //sprintf(buffer,"%03d: %f %f %f",pt, coord[0], coord[1], coord[2]);
        //LOG->write(buffer);
    }

    unsigned int numCells = this->GridPtr->GetNumberOfLocalCells();
    this->Pressure.resize(numCells);
    std::fill(this->Pressure.begin(), this->Pressure.end(), 1.);
 }

void Attributes::SaveFields(double time){
    //Gather all partial results to the root process
    double *_velocity=NULL;
    //_velocity.resize(0);
    if(this->GridPtr->mpiRank == 0){
        _velocity = new double[this->Velocity.size()*this->GridPtr->mpiSize];
    }

    char buffer[80];
    for(int i=0;i<this->Velocity.size();++i){
        sprintf(buffer,"%f",Velocity[i]);
        //LOG->write(buffer);
    }

    MPI_Gather(&Velocity[0], Velocity.size(), MPI_DOUBLE,_velocity,
               Velocity.size(), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if(this->GridPtr->mpiRank == 0){
        LOG->write("Rank 0 finished collecting all data");
        /*for(int i=0;i<this->Velocity.size()*this->GridPtr->mpiSize;++i){
            sprintf(buffer,"%f",_velocity[i]);
            LOG->write(buffer);
            }*/
    }
}

/*
void Attributes::UpdateFields(double time)
{
  unsigned int numPoints = this->GridPtr->GetNumberOfLocalPoints();
  this->Velocity.resize(numPoints*3);
  for(unsigned int pt=0;pt<numPoints;pt++)
    {
    double coord[3];
    this->GridPtr->GetLocalPoint(pt, coord);
    this->Velocity[pt] = coord[1]*time;
    }
  std::fill(this->Velocity.begin()+numPoints, this->Velocity.end(), 0.);
  unsigned int numCells = this->GridPtr->GetNumberOfLocalCells();
  this->Pressure.resize(numCells);
  std::fill(this->Pressure.begin(), this->Pressure.end(), 1.);
}
*/


double* Attributes::GetVelocityArray()
{
    if(this->Velocity.empty())
    {
        return NULL;
    }
    return &this->Velocity[0];
}


float* Attributes::GetPressureArray()
{
  if(this->Pressure.empty())
    {
    return NULL;
    }
  return &this->Pressure[0];
}
