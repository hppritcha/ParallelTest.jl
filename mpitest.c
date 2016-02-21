//==============================================================
// C MPI example: mpitest.c
//==============================================================
#include
#include
int main(int argc, char** argv){
  int iproc;
  int nproc;
  int i;
  MPI_Init(&argc,&argv);
  MPI_Comm_rank(MPI_COMM_WORLD,&iproc);
  MPI_Comm_size(MPI_COMM_WORLD,&nproc);
  for ( i = 0; i <= nproc - 1; i++ ){
MPI_Barrier(MPI_COMM_WORLD);
if ( i == iproc ){
 printf("%s %d %s %d \n","Rank",iproc,"out of",nproc);
}
  }
  MPI_Finalize();
  return 0;
}
