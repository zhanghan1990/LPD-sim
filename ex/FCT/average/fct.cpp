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
   double average_fct;
   char dir[100];

   // first check the file exits,if exits, delete the old one
   if(access(outputfile,0)==0) {
     //cout << "delete the old "<<outputfile<<" file now ..." << endl;
     remove(outputfile);
   }
   
   //  statistics the load one by one 
   for(load = 1; load < 10; load++) {
      average_fct = 0;

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
     int row = 0;
     while(infile.getline(buffer,sizeof(buffer))){
        double flowsize,fct;
        sscanf(buffer,"%lf %lf",&flowsize,&fct);
        //cout <<flowsize <<" "<<fct << endl;
        average_fct += fct;
        row++;
     }


     // get the average fct of all the flows
     average_fct = average_fct/(double)row;
     //cout <<"The average fct is " << average_fct << endl;
 
     // write the average fct into the statistics file
    
     ofstream outfile(outputfile,ios::app);
     double ofload = (double)load/10.0;
     outfile << ofload <<" " << average_fct << endl;
     if(strcmp(kind,"DCTCP")==0){
      FCT[0][type][x][load]=average_fct;}
      else if(strcmp(kind,"L2DCT")==0){
      FCT[1][type][x][load]=average_fct;}
      else if(strcmp(kind,"pFabric")==0){
      FCT[2][type][x][load]=average_fct;}
      else if(strcmp(kind,"LPD")==0){
      FCT[3][type][x][load]=average_fct;}
     
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
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);


      strcpy(kind,"pFabric");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);


      //For D2TCP
      strcpy(kind,"L2DCT");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);


       //For LPD
      strcpy(kind,"LPD");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.SEARCH",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,0);
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.DATA",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i,1);
      }

      
      int t,k;
      char type[100];
      double ofload,average;
      for(k=0;k<4;k++)
      {
        if(k==0)
          strcpy(kind,"DCTCP");
        else if(k==1)
          strcpy(kind,"L2DCT");
        else if(k==2)
          strcpy(kind,"pFabric");
        else if(k==3)
          strcpy(kind,"LPD");
        for(t=0;t<2;t++){
          if(t==0)
            strcpy(type,"SEARCH");
          if(t==1)
            strcpy(type,"DATA");
          sprintf(outputfile,"%s/%s/%s_fct.%s",basepath,kind,kind,type);
           // first check the file exits,if exits, delete the old one
            if(access(outputfile,0)==0) {
               //cout << "delete the old "<<outputfile<<" file now ..." << endl;
                remove(outputfile);
            }  
          ofstream outfile(outputfile,ios::app);
          for(i=5;i<=40;i=i+5){
          
            // ofload = (double)j/10.0;
              double max=-100000;
              double min=1000000;
              average=0;
              int cycle=0;
            for(j=1;j<=9;j++){
               average+=FCT[k][t][i][j];
               if(max<FCT[k][t][i][j])
                max=FCT[k][t][i][j];
               if(min>FCT[k][t][i][j])
                min=FCT[k][t][i][j];
               cycle++;
               cout <<FCT[k][t][i][j]<<" ";
             }
             cout << endl;
             average/=cycle;
             outfile<<i<<" "<<average<<" "<<max<<" "<<min<<endl;
          }
        }
      }

  return 0;
}
