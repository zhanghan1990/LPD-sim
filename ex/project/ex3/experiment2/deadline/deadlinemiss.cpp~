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
void statistics(char* inputfile, char* outputfile,char* kind) {
   
   int load;
   int miss;

   // first check the file exits,if exits, delete the old one
   if(access(outputfile,0)==0) {
     cout << "delete the old "<<outputfile<<" file now ..." << endl;
     remove(outputfile);
   }
   
   //  statistics the load one by one 
   for(load = 1; load < 10; load++) {
      miss = 0;


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
        double flowsize,fct,rtt,deadline;
        sscanf(buffer,"%lf %lf %lf %lf",&flowsize,&fct,&rtt,&deadline);
        cout <<flowsize <<" "<<fct << " "<<rtt << " "<< deadline << endl;
        if(deadline < fct)
          miss++;
        row++;
     }


     // get the average fct of all the flows
     double miss_result = (double)miss/(double)row;
     cout <<"The percentage of miss deadline is " << miss_result << endl;
 
     // write the average fct into the statistics file
    
     ofstream outfile(outputfile,ios::app);
     double ofload = (double)load/10.0;
     outfile << ofload <<" " << miss_result << endl; 
     
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
   sprintf(outputfile,"%s/%s/%s_deadline.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

  
   //For pFabric
   strcpy(kind,"pFabric");
   strcpy(totalkind[1],kind);
   sprintf(outputfile,"%s/%s/%s_deadline.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

    //For D2TCP
   strcpy(kind,"D2TCP");
   strcpy(totalkind[2],kind);
   sprintf(outputfile,"%s/%s/%s_deadline.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

   //for LPD
   strcpy(kind,"LPD");
   strcpy(totalkind[3],kind);
   sprintf(outputfile,"%s/%s/%s_deadline.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

   //for Timely
   strcpy(kind,"Timely");
   strcpy(totalkind[4],kind);
   sprintf(outputfile,"%s/%s/%s_deadline.result",basepath,kind,kind);
   statistics(inputfile,outputfile,kind);

    // call the gnuplot to plot the result
    FILE* gp = popen("gnuplot", "w");
    if(gp == NULL) {
       printf("can not open the pipe of gnuplot\n");
       exit(1);
     } 
     fprintf(gp, "set terminal postscript eps color \n"); 
     fprintf(gp, "set size 0.5,0.5 \n");
     fprintf(gp, "set output  \"deadlinemiss.eps\" \n");
     fprintf(gp, "set xlabel \"load\" \n");
     fprintf(gp, "set ylabel \"Percentage of missing deadline\" \n");
     fprintf(gp, "set xrange [0:1] \n");
     fprintf(gp, "set yrange [0:0.005] \n");
     fprintf(gp ,"plot  \"%s/%s/%s_deadline.result\" using 1:2   with linespoints linecolor 1 linewidth 3 pointtype 1 pointsize 2 title \"%s\" , \"%s/%s/%s_deadline.result\" using 1:2   with linespoints linecolor 2 linewidth 3 pointtype 2 pointsize 2 title \"%s\"  ,\"%s/%s/%s_deadline.result\" using 1:2   with linespoints linecolor 3 linewidth 3 pointtype 3 pointsize 2 title \"%s\" ,\"%s/%s/%s_deadline.result\" using 1:2   with linespoints linecolor 4 linewidth 3 pointtype 4 pointsize 2 title \"%s\" , \"%s/%s/%s_deadline.result\" using 1:2   with linespoints linecolor 5 linewidth 3 pointtype 5 pointsize 2 title \"%s\"\n",basepath,totalkind[0],totalkind[0],totalkind[0],basepath,totalkind[1],totalkind[1],totalkind[1],basepath,totalkind[2],totalkind[2],totalkind[2],basepath,totalkind[3],totalkind[3],totalkind[3],basepath,totalkind[4],totalkind[4],totalkind[4]);

    pclose(gp);       
  return 0;
}
