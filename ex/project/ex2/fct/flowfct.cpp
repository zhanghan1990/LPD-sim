#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

using namespace std;

char basepath[100][100];
char  buffer[1024];

// kind: DCTCP or pFabric or D2TCP or LPD or others
void statistics(char* inputfile, char* outputfile,char* kind,char* base, int x) {
   
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
      sprintf(inputfile,"%s/%s/%d0.%d.Ex/flow.tr",base,kind,x,load);
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
   char  totalkind[10][100];
  
   int x = 4;
   //For DCTCP
   strcpy(basepath[0],"/home/zhanghan/pfabric-mahanmod/project/ex2/DCTCP");  
   strcpy(kind,"DCTCP");
   strcpy(totalkind[0],kind);
   sprintf(outputfile,"%s/%s/%s_fct.result",basepath[0],kind,kind);
   statistics(inputfile,outputfile,kind,basepath[0],x);

  
  
   //For D2TCP
   strcpy(basepath[1],"/home/zhanghan/pfabric-mahanmod/project/ex2/D2TCP");  
   strcpy(kind,"D2TCP");
   strcpy(totalkind[1],kind);
   sprintf(outputfile,"%s/%s/%s_fct.result",basepath[1],kind,kind);
   statistics(inputfile,outputfile,kind,basepath[1],x);

   //For pFabric
    x=5;
   strcpy(basepath[2],"/home/zhanghan/pfabric-mahanmod/project/ex2/pFabric");  
   strcpy(kind,"pFabric");
   strcpy(totalkind[2],kind);
   sprintf(outputfile,"%s/%s/%s_fct.result",basepath[2],kind,kind);
   statistics(inputfile,outputfile,kind,basepath[2],x);
    //For LPD
   strcpy(basepath[3],"/home/zhanghan/pfabric-mahanmod/project/ex2/LPD");  
   strcpy(kind,"LPD");
   strcpy(totalkind[3],kind);
   sprintf(outputfile,"%s/%s/%s_fct.result",basepath[3],kind,kind);
   statistics(inputfile,outputfile,kind,basepath[3],x);
   //For Timely
   strcpy(basepath[4],"/home/zhanghan/pfabric-mahanmod/project/ex2/Timely");  
   strcpy(kind,"Timely");
   strcpy(totalkind[4],kind);
   sprintf(outputfile,"%s/%s/%s_fct.result",basepath[4],kind,kind);
   statistics(inputfile,outputfile,kind,basepath[4],x);


    // call the gnuplot to plot the result
    FILE* gp = popen("gnuplot", "w");
    if(gp == NULL) {
       printf("can not open the pipe of gnuplot\n");
       exit(1);
     } 
     fprintf(gp, "set terminal postscript eps color \n"); 
     fprintf(gp, "set size 0.5,0.5 \n");
     fprintf(gp, "set output  \"FCT.eps\" \n");
     fprintf(gp, "set xlabel \"load\" \n");
     fprintf(gp, "set ylabel \"AFCT\" \n");
     fprintf(gp, "set xrange [0:1] \n");
     fprintf(gp, "set yrange [0:0.03] \n");
     fprintf(gp ,"plot  \"%s/%s/%s_fct.result\" using 1:2   with linespoints linecolor 1 linewidth 3 pointtype 1 pointsize 2 title \"%s\" , \"%s/%s/%s_fct.result\" using 1:2   with linespoints linecolor 2 linewidth 3 pointtype 2 pointsize 2 title \"%s\"  ,\"%s/%s/%s_fct.result\" using 1:2   with linespoints linecolor 3 linewidth 3 pointtype 3 pointsize 2 title \"%s\", \"%s/%s/%s_fct.result\" using 1:2   with linespoints linecolor 4 linewidth 3 pointtype 4 pointsize 2 title \"%s\" , \"%s/%s/%s_fct.result\" using 1:2   with linespoints linecolor 5 linewidth 3 pointtype 5 pointsize 2 title \"%s\" \n",basepath[0],totalkind[0],totalkind[0],totalkind[0],basepath[1],totalkind[1],totalkind[1],totalkind[1],basepath[2],totalkind[2],totalkind[2],totalkind[2],basepath[3],totalkind[3],totalkind[3],totalkind[3],basepath[4],totalkind[4],totalkind[4],totalkind[4]);

    pclose(gp);       
  return 0;
}
