#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

//  First divide the flows into two gruop (0,100KB],(100KB,inf).
//  Then plot the average fct of the two group.

using namespace std;

char basepath[100];
char  buffer[1024];

// kind: DCTCP or pFabric or D2TCP or LPD or others
void statistics(char* inputfile, char* smalloutputfile, char* largeoutputfile, char* kind) {
   
   int load;
   double small_fct,large_fct;

   // first check the file exits,if exits, delete the old one
   if(access(smalloutputfile,0)==0) {
     cout << "delete the old "<<smalloutputfile<<" file now ..." << endl;
     remove(smalloutputfile);
   }
   if(access(largeoutputfile,0)==0) {
     cout << "delete the old "<<largeoutputfile<<" file now ..." << endl;
     remove(largeoutputfile);
   }
   
   //  statistics the load one by one 
   for(load = 1; load < 10; load++) {
      small_fct = 0;
      large_fct = 0;

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
     int smallrow = 0;
     int largerow = 0;

     while(infile.getline(buffer,sizeof(buffer))){
        double flowsize,fct;
        sscanf(buffer,"%lf %lf",&flowsize,&fct);
        cout <<flowsize <<" "<<fct << endl;
        if(flowsize < 100){
           small_fct+=fct;
           smallrow++;
        }
        else {
        large_fct += fct;
        largerow++;
      }
     }


     // get the average fct for the small flows and the large flows
     small_fct = small_fct/(double)smallrow;
     large_fct = large_fct/(double)largerow;
     //cout <<"The average fct is " << average_fct << endl;
 
     // write the average fct into the statistics file
    
     ofstream smalloutfile(smalloutputfile,ios::app);
     double ofload = (double)load/10.0;
     smalloutfile << ofload <<" " << small_fct << endl; 
     ofstream largeoutfile(largeoutputfile,ios::app);
     largeoutfile << ofload <<" " << large_fct << endl; 
     
   }    
   
}

int main(){

   char  inputfile[100];
   char  smalloutputfile[100];
   char  largeoutputfile[100];
   char  kind[100];
   char  totalkind[10][100];
  
   strcpy(basepath,"/home/zhanghan/pfabric-mahanmod/project");
   //For DCTCP
   strcpy(kind,"DCTCP");
   strcpy(totalkind[0],kind);
   sprintf(smalloutputfile,"%s/%s/small_%s_fct.result",basepath,kind,kind);
   sprintf(largeoutputfile,"%s/%s/large_%s_fct.result",basepath,kind,kind);
   statistics(inputfile,smalloutputfile,largeoutputfile,kind);

  
   //For pFabric
   strcpy(kind,"pFabric");
   strcpy(totalkind[1],kind);
   sprintf(smalloutputfile,"%s/%s/small_%s_fct.result",basepath,kind,kind);
   sprintf(largeoutputfile,"%s/%s/large_%s_fct.result",basepath,kind,kind);
   statistics(inputfile,smalloutputfile,largeoutputfile,kind);

   //For D2TCP

       //For pFabric
   strcpy(kind,"D2TCP");
   strcpy(totalkind[2],kind);
   sprintf(smalloutputfile,"%s/%s/small_%s_fct.result",basepath,kind,kind);
   sprintf(largeoutputfile,"%s/%s/large_%s_fct.result",basepath,kind,kind);
   statistics(inputfile,smalloutputfile,largeoutputfile,kind);

    // call the gnuplot to plot the result
    FILE* smallgp = popen("gnuplot", "w");
    if(smallgp == NULL) {
       printf("can not open the pipe of gnuplot\n");
       exit(1);
     } 
     fprintf(smallgp, "set terminal postscript eps color \n"); 
     fprintf(smallgp, "set size 0.5,0.5 \n");
     fprintf(smallgp, "set output  \"smallflowFCT.eps\" \n");
     fprintf(smallgp, "set xlabel \"load\" \n");
     fprintf(smallgp, "set ylabel \"AFCT\" \n");
     fprintf(smallgp, "set xrange [0:1] \n");
     fprintf(smallgp, "set yrange [0:0.0008] \n");
     fprintf(smallgp ,"plot  \"%s/%s/small_%s_fct.result\" using 1:2   with linespoints linecolor 1 linewidth 3 pointtype 1 pointsize 2 title \"%s\" , \"%s/%s/small_%s_fct.result\" using 1:2   with linespoints linecolor 2 linewidth 3 pointtype 2 pointsize 2 title \"%s\" , \"%s/%s/small_%s_fct.result\" using 1:2   with linespoints linecolor 3 linewidth 3 pointtype 3 pointsize 2 title \"%s\"  \n",basepath,totalkind[0],totalkind[0],totalkind[0],basepath,totalkind[1],totalkind[1],totalkind[1],basepath,totalkind[2],totalkind[2],totalkind[2]);

    pclose(smallgp);   

    FILE* largegp = popen("gnuplot", "w");
    if(largegp == NULL) {
       printf("can not open the pipe of gnuplot\n");
       exit(1);
     } 
     fprintf(largegp, "set terminal postscript eps color \n"); 
     fprintf(largegp, "set size 0.5,0.5 \n");
     fprintf(largegp, "set output  \"largeflowFCT.eps\" \n");
     fprintf(largegp, "set xlabel \"load\" \n");
     fprintf(largegp, "set ylabel \"AFCT\" \n");
     fprintf(largegp, "set xrange [0:1] \n");
     fprintf(largegp, "set yrange [0:0.06] \n");
     fprintf(largegp ,"plot  \"%s/%s/large_%s_fct.result\" using 1:2   with linespoints linecolor 1 linewidth 3 pointtype 1 pointsize 2 title \"%s\" , \"%s/%s/large_%s_fct.result\" using 1:2   with linespoints linecolor 2 linewidth 3 pointtype 2 pointsize 2 title \"%s\", \"%s/%s/large_%s_fct.result\" using 1:2   with linespoints linecolor 3 linewidth 3 pointtype 3 pointsize 2 title \"%s\"  \n",basepath,totalkind[0],totalkind[0],totalkind[0],basepath,totalkind[1],totalkind[1],totalkind[1],basepath,totalkind[2],totalkind[2],totalkind[2]);

    pclose(largegp);    

    
  return 0;
}
