#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <algorithm>

using namespace std;


#define SMALLNUMBER 100000
// This program gets the 99% of the small flow completion time

// define the flow information, this equals to the file of the flow.tr
struct flow {
   // In this experiments, we just care the fct of the flows, anyway, we can also define some other params
   double flowsize;
   double fct;
};

bool cmp(flow f1, flow f2)
{ 
   if(f1.fct < f2.fct)
     return true;
    return false;
}

struct flow totalflow[SMALLNUMBER];

char basepath[100];
char  buffer[1024];

// kind: DCTCP or pFabric or D2TCP or LPD or others
void statistics(char* inputfile, char* outputfile,char* kind) {
   
   int load;
   double average_fct;
   memset(totalflow,0,sizeof(totalflow));

   // first check the file exits,if exits, delete the old one
   if(access(outputfile,0)==0) {
     cout << "delete the old "<<outputfile<<" file now ..." << endl;
     remove(outputfile);
   }
   
   //  statistics the load one by one 
   for(load = 1; load < 10; load++) {
      average_fct = 0;


      // get the filename 
      sprintf(inputfile,"%s/%s/0.%d.Ex/flow.tr",basepath,kind,load);
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
       // cout <<flowsize <<" "<<fct << endl;
        if(flowsize < 100) {
           totalflow[row].flowsize = flowsize;
           totalflow[row].fct = fct;
           row++;
        }
     }
    
    // sort the array totalflow
     sort(totalflow,totalflow+row,cmp);

    // Remove the 1% of the totalflow;
    int start = row*0.005;
    int end   = row*0.995;
    cout << "99% size is "<< (end-start) <<"row size is "<< row << endl;
    average_fct = 0;
    int i;
    for(i = start; i < end; i++)
       average_fct +=totalflow[i].fct;

     // get the average fct of all the flows
     average_fct = average_fct/(double)(end-start);
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
   char  totalkind[10][100];
  
   strcpy(basepath,"/home/zhanghan/pfabric-mahanmod/project");
   //For DCTCP
   strcpy(kind,"DCTCP");
   strcpy(totalkind[0],kind);
   sprintf(outputfile,"%s/%s/%s_fct99th.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

  
   //For pFabric
   strcpy(kind,"pFabric");
   strcpy(totalkind[1],kind);
   sprintf(outputfile,"%s/%s/%s_fct99th.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

   strcpy(kind,"D2TCP");
   strcpy(totalkind[2],kind);
   sprintf(outputfile,"%s/%s/%s_fct99th.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

   //

    // call the gnuplot to plot the result
    FILE* gp = popen("gnuplot", "w");
    if(gp == NULL) {
       printf("can not open the pipe of gnuplot\n");
       exit(1);
     } 
     fprintf(gp, "set terminal postscript eps color \n"); 
     fprintf(gp, "set size 0.5,0.5 \n");
     fprintf(gp, "set output  \"99thFCT.eps\" \n");
     fprintf(gp, "set xlabel \"load\" \n");
     fprintf(gp, "set ylabel \"AFCT\" \n");
     fprintf(gp, "set xrange [0:1] \n");
     fprintf(gp, "set yrange [0:0.0006] \n");
     fprintf(gp ,"plot  \"%s/%s/%s_fct99th.result\" using 1:2   with linespoints linecolor 1 linewidth 3 pointtype 1 pointsize 2 title \"%s\" , \"%s/%s/%s_fct99th.result\" using 1:2   with linespoints linecolor 2 linewidth 3 pointtype 2 pointsize 2 title \"%s\", \"%s/%s/%s_fct99th.result\" using 1:2   with linespoints linecolor 3 linewidth 3 pointtype 3 pointsize 2 title \"%s\"  \n",basepath,totalkind[0],totalkind[0],totalkind[0],basepath,totalkind[1],totalkind[1],totalkind[1],basepath,totalkind[2],totalkind[2],totalkind[2]);

    pclose(gp);       
  return 0;
}
