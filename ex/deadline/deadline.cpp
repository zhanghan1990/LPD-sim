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

// kind: DCTCP or pFabric or D2TCP or LPD or others
void statistics(char* inputfile, char* outputfile,char* kind,int test,int x) {
   
   int load;
   double per;

   // first check the file exits,if exits, delete the old one
   if(access(outputfile,0)==0) {
     //cout << "delete the old "<<outputfile<<" file now ..." << endl;
     remove(outputfile);
   }
   
   //  statistics the load one by one 
   for(load = 1; load < 10; load++) {
      per = 0;


      // get the filename 
      sprintf(inputfile,"%s/%s/%s-%d-%d-0.%d-Ex-flow.tr",basepath,kind,kind,test,x,load);
      ifstream infile(inputfile);


      // if file does not exit, then exits
      if(!infile)
      {
         cout << "can not open the file: "<<inputfile<<endl;
         exit(1);
      }


     // read the line of the file
     int row = 0;
     int number= 0;
     while(infile.getline(buffer,sizeof(buffer))){
        double flowsize,fct,t,deadline;
        sscanf(buffer,"%lf %lf %lf %lf",&flowsize,&fct,&t,&deadline);
        //cout <<flowsize <<" "<<fct << endl;
        if(deadline < fct)
          number++;
        row++;
     }


     // get the average fct of all the flows
     per = number/(double)row;
     //cout <<"The average fct is " << average_fct << endl;
 
     // write the average fct into the statistics file
    
     ofstream outfile(outputfile,ios::app);
     double ofload = (double)load/10.0;
     outfile << ofload <<" " << per << endl;
     //cout <<test<<" "<<x<<" "<<ofload <<" " << per << endl;
     
   }    
   
}




// kind: DCTCP or pFabric or D2TCP or LPD or others
void avstatistics(char* inputfile, char* outputfile,char* kind,int x,int test) {
   
   double average_fct[100];
   double max_fct[100];
   double min_fct[100];

   memset(average_fct,0,sizeof(average_fct));
   int i;

   for(i=0;i<100;i++){
    max_fct[i]=-10000;
    min_fct[i]=10000;
   }

   // first check the file exits,if exits, delete the old one
   if(access(outputfile,0)==0) {
     cout << "delete the old "<<outputfile<<" file now ..." << endl;
     remove(outputfile);
   }
   
   for(i = 1; i <test; i++) {
      // get the filename 
      sprintf(inputfile,"%s/%s/%s_fct_%d_%d.result",basepath,kind,kind,i,x);
      ifstream infile(inputfile);
      // if file does not exit, then exits
      if(!infile)
      {
         cout << "can not open the file: "<<inputfile<<endl;
         exit(1);
      }

     int row = 0;
     while(infile.getline(buffer,sizeof(buffer))){
        double load,fct;
        sscanf(buffer,"%lf %lf",&load,&fct);
        average_fct[row] += fct;
        if(max_fct[row]<=fct)
          max_fct[row]=fct; 
        if(min_fct[row]>=fct)
          min_fct[row]=fct; 
        row++;
     }
     
   } 

  for(int load= 1;load<10;load++){
     average_fct[load-1] =  average_fct[load-1]/test;
     //cout <<"The average fct is " << average_fct << endl;
     ofstream outfile(outputfile,ios::app);
     double ofload = (double)load/10.0;
     outfile << ofload <<" " << average_fct[load-1] <<" "<<max_fct[load-1]<<" "<<min_fct[load-1]<< endl;  
    } 
   
}



int main(){

   char  inputfile[100];
   char  outputfile[100];
   char  kind[100];
   int x=10;
   int test=10;

   int i,j;
  
   strcpy(basepath,"/Users/zhanghan/Documents/文件资料/LPD/ex/deadline");
   for(j=0;j<test;j++){

      for(i = 1; i <=x; i++) {
      // For DCTCP
      strcpy(kind,"DCTCP");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.result",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i);
      //For pFabric
      strcpy(kind,"pFabric");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.result",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i);

      //For D2TCP
      strcpy(kind,"D2TCP");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.result",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i);

       //For LPD
      strcpy(kind,"LPD");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.result",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i);

       //For LPD
      strcpy(kind,"L2DCT");
      sprintf(outputfile,"%s/%s/%s_fct_%d_%d.result",basepath,kind,kind,j,i);
      statistics(inputfile,outputfile,kind,j,i);
      }

   }


   // Get the final result of total files
  for(i = 1; i <= x; i++){

      strcpy(kind,"DCTCP");
      sprintf(outputfile,"%s/%s/%s_fct_%d.final",basepath,kind,kind,i);
      avstatistics(inputfile,outputfile,kind,i,test);
      //For pFabric
      strcpy(kind,"pFabric");
      sprintf(outputfile,"%s/%s/%s_fct_%d.final",basepath,kind,kind,i);
      avstatistics(inputfile,outputfile,kind,i,test);

      //For D2TCP
      strcpy(kind,"D2TCP");
      sprintf(outputfile,"%s/%s/%s_fct_%d.final",basepath,kind,kind,i);
      avstatistics(inputfile,outputfile,kind,i,test);

       //For LPD
      strcpy(kind,"LPD");
      sprintf(outputfile,"%s/%s/%s_fct_%d.final",basepath,kind,kind,i);
      avstatistics(inputfile,outputfile,kind,i,test);


      //For L2DCT
      strcpy(kind,"L2DCT");
      sprintf(outputfile,"%s/%s/%s_fct_%d.final",basepath,kind,kind,i);
      avstatistics(inputfile,outputfile,kind,i,test);


   }

  return 0;
}
