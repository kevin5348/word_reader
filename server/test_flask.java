import java.util.scanner;
public class test_flask {


public static void main(String args[])
{   int[] array1 = {1,2,3,4};
    int count1 = array1.length;
    int[][] array= new int[array1.length][array1.length];

    for (int i=0; i<array.length;i++){
        int num=array1[i];
        for(int j=0;j<array[i].length;j++){
            
            array[i][j]=num;       
        }
    }
    int count =0;
   while (count1>0){
    for (int i=0; i<array.length;i++){
        
        for(int j=1;j<array[i].length;j++){
            int sum_plus=array[i][0]+array[i][j];  
            int sum_minus=array[i][0]-array[i][j];  
            if(sum_minus==3||sum_plus==3){
                String position = i + " " + j;
                count++;
            }
        }
    }
    count1--;
   }
} 


}

    