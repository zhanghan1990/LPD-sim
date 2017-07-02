#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{  
     pid_t dctcp,d2tcp,lpd,pfabric,timely;
   
    dctcp =fork();
    if(dctcp == 0)
    {
        sleep(5);
        printf("execting dctcp....\n");
        return 0;
    }
    
    d2tcp = fork();
    if(d2tcp ==0)
    {
        
        printf("execting d2tcp ...\n");
        return 0;
    }
    lpd = fork();
    if(lpd == 0)
    {
        printf("execting lpd...\n");
        return 0;
    }
    
    pfabric =fork();
    if(pfabric ==0)
    {
        printf("execting pfabric ...\n");
        return 0;
    }
    
    
    timely  =fork();
    if(timely ==0)
    {
        printf("execting timely...\n");
        return 0;
    }
    
    int st1,st2,st3,st4,st5,st6;
    waitpid(dctcp,&st1,0);
    waitpid(d2tcp,&st2,0);
    waitpid(lpd,&st3,0);
    waitpid(pfabric,&st4,0);
    waitpid(timely,&st5,0);
    return 0;
    
}
