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
double largeFCT[4][2][100][100];
double smallFCT[4][2][100][100];

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



     if(strcmp(kind,"DCTCP")==0) {
        largeFCT[0][type][x][load]=average_large_fct;
        smallFCT[0][type][x][load]=average_small_fct;
      }else if(strcmp(kind,"pFabric")==0){
        largeFCT[1][type][x][load]=average_large_fct;
        smallFCT[1][type][x][load]=average_small_fct;
      }else if(strcmp(kind,"L2DCT")==0){
        largeFCT[2][type][x][load]=average_large_fct;
        smallFCT[2][type][x][load]=average_small_fct;
      }else if(strcmp(kind,"LPD")==0){
        largeFCT[3][type][x][load]=average_large_fct;
        smallFCT[3][type][x][load]=average_small_fct;
      }



    
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

      // do analysis for large flows and for small flows


    char  outputfile1[100],outputfile2[100];

      int t,k;
      char type[100];
      double ofload,largeaverage,smallaverage;
      for(k=0;k<4;k++)
      {
        if(k==0)
          strcpy(kind,"DCTCP");
        else if(k==1)
          strcpy(kind,"pFabric");
        else if(k==2)
          strcpy(kind,"L2DCT");
        else if(k==3)
          strcpy(kind,"LPD");
        for(t=0;t<2;t++){
          if(t==0)
            strcpy(type,"SEARCH");
          if(t==1)
            strcpy(type,"DATA");
          sprintf(outputfile1,"%s/%s/%s_large_fct.%s",basepath,kind,kind,type);
          sprintf(outputfile2,"%s/%s/%s_small_fct.%s",basepath,kind,kind,type);
           // first check the file exits,if exits, delete the old one
            if(access(outputfile1,0)==0) {
               //cout << "delete the old "<<outputfile<<" file now ..." << endl;
                remove(outputfile1);
            }  
            if(access(outputfile2,0)==0) {
               //cout << "delete the old "<<outputfile<<" file now ..." << endl;
                remove(outputfile2);
            }  


          ofstream outfile1(outputfile1,ios::app);
          ofstream outfile2(outputfile2,ios::app);


          for(i=5;i<=30;i=i+5){
          
            // ofload = (double)j/10.0;
              double largemax=-100000;
              double smallmax=-100000;
              double largemin=1000000;
              double smallmin=1000000;
              largeaverage=0;
              smallaverage=0;
              int cycle=0;
            for(j=1;j<=9;j++){
               largeaverage+=largeFCT[k][t][i][j];
               smallaverage+=smallFCT[k][t][i][j];
               if(largemax<largeFCT[k][t][i][j])
                largemax=largeFCT[k][t][i][j];
               if(largemin>largeFCT[k][t][i][j])
                largemin=largeFCT[k][t][i][j];


              if(smallmax<smallFCT[k][t][i][j])
                smallmax=smallFCT[k][t][i][j];
               if(smallmin>smallFCT[k][t][i][j])
                smallmin=smallFCT[k][t][i][j];


               cycle++;
             }
             largeaverage/=cycle;
             smallaverage/=cycle;
             outfile1<<i<<" "<<largeaverage<<" "<<largemax<<" "<<largemin<<endl;
             outfile2<<i<<" "<<smallaverage<<" "<<smallmax<<" "<<smallmin<<endl;
          }
        }
      }




  return 0;
}
