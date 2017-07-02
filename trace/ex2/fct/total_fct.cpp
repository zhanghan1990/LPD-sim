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
void statistics(char* inputfile, char* outputfile,char* kind,int x) {
   
   int load;
   double average_fct;

   // first check the file exits,if exits, delete the old one
   if(access(outputfile,0)==0) {
     cout << "delete the old "<<outputfile<<" file now ..." << endl;
     remove(outputfile);
   }
   
   //  statistics the load one by one 
   for(load = 1; load < 10; load++) {
      average_fct = 0;


      // get the filename 
      sprintf(inputfile,"%s/%s/%d0.%d.Ex/flow.tr",basepath,kind,x,load);
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
        cout <<flowsize <<" "<<fct << endl;
        average_fct += fct;
        row++;
     }


     // get the average fct of all the flows
     average_fct = average_fct/(double)row;
     cout <<"The average fct is " << average_fct << endl;
 
     // write the average fct into the statistics file
    
     ofstream outfile(outputfile,ios::app);
     double ofload = (double)load/10.0;
     outfile << ofload <<" " << average_fct << endl; 
     
   }    
   
}

int main(){

   char  inputfile[100];
   char  outputfile[100];
   char  kind[100];
   int x=10;
  
   strcpy(basepath,"/Users/zhanghan/Documents/file/ex2");
  
   for(int i = 1; i <=x; i++) {
    // For DCTCP
    strcpy(kind,"DCTCP");
    sprintf(outputfile,"%s/%s/%s_fct_%d.result",basepath,kind,kind,i);
    statistics(inputfile,outputfile,kind,i);
    //For pFabric
    strcpy(kind,"pFabric");
    sprintf(outputfile,"%s/%s/%s_fct_%d.result",basepath,kind,kind,i);
    statistics(inputfile,outputfile,kind,i);

     //For D2TCP
    strcpy(kind,"D2TCP");
    sprintf(outputfile,"%s/%s/%s_fct_%d.result",basepath,kind,kind,i);
    statistics(inputfile,outputfile,kind,i);

    //For LPD
    strcpy(kind,"LPD");
    sprintf(outputfile,"%s/%s/%s_fct_%d.result",basepath,kind,kind,i);
    statistics(inputfile,outputfile,kind,i);
   }

  return 0;
}
