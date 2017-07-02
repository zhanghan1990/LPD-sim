#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

using namespace std;

char basepath[100];
char  buffer[1024];

// This is the FCT[kind][type][x][load]
double FCT[4][2][100][100];

// kind: DCTCP or pFabric or D2TCP or LPD or others
void statistics(char* inputfile, char* outputfile,char* kind,int test,int x,int type) {
   
   int load;
   double average_large_fct;
   double average_small_fct;
   char dir[100];

   // first check the file exits,if exits, delete the old one
   if(access(outputfile,0)==0) {
     //cout << "delete the old "<<outputfile<<" file now ..." << endl;
     remove(outputfile);
   }
   
   //  statistics the load one by one 
   for(load = 1; load < 10; load++) {
      average_small_fct=0;
      average_large_fct=0;

      if(type==0)
        sprintf(dir,"%s","SEARCH");
      if(type==1)
        sprintf(dir,"%s","DATA");
      // get the filename 
      sprintf(inputfile,"%s/%s/%s/%s-%d-%d-0.%d-Ex-flow.tr",basepath,kind,dir,kind,test,x,load);
      ifstream infile(inputfile);


      // if file does not exit, then exits
      if(!infile)
      {
         cout << "can not open the file: "<<inputfile<<endl;
         exit(1);
      }


     // read the line of the file
     int largerow = 0;
     int smallrow=0;
     while(infile.getline(buffer,sizeof(buffer))){
        double flowsize,fct;
        sscanf(buffer,"%lf %lf",&flowsize,&fct);
        //cout <<flowsize <<" "<<fct << endl;
        if(flowsize<10)
        {
          average_small_fct+=fct;
          smallrow++;
        }
        else if(flowsize>50)
        {
          largerow++;
          average_large_fct+=fct;
        }
     }


     // get the average fct of all the flows
     average_large_fct = average_large_fct/(double)largerow;
     average_small_fct=average_small_fct/(double)smallrow;
     //cout <<"The average fct is " << average_fct << endl;
 
     // write the average fct into the statistics file
    
     ofstream outfile(outputfile,ios::app);
     double ofload = (double)load/10.0;
     outfile << ofload <<" " << average_large_fct <<" "<<average_small_fct<< endl;
     
   }    
   
}



int main(){

   char  inputfile[100];
   char  outputfile[100];
   char  kind[100];
   int x=10;
   int test=1;

   int i,j;
  
   strcpy(basepath,"/Users/zhanghan/Documents/文件资料/LPD/ex/FCT");

   for(j=0;j<test;j++)

      for(i = 5; i <=50; i=i+5) {
      // For DCTCP
      strcpy(kind,"DCTCP");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);


      strcpy(kind,"pFabric");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);


      //For D2TCP
      strcpy(kind,"L2DCT");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);


       //For LPD
      strcpy(kind,"LPD");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.Diff_DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);
      }
  return 0;
}
