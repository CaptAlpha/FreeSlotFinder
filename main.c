#include <stdio.h>
#include <stdlib.h>
#include<time.h>

void swap(int *a, int *b) {
  int temp = *a;
  *a = *b;
  *b = temp;
}

void bubbleSort(int array[], int size) {
    
  for (int step = 0; step < size - 1; ++step) {
    for (int i = 0; i < size - step - 1; ++i) { 
      if (array[i] > array[i + 1]) {
    
        int temp = array[i];
        array[i] = array[i + 1];
        array[i + 1] = temp;
      }
    }
  }
 
}


void selectionSort(int array[], int size) {

  for (int step = 0; step < size - 1; step++) {
    int min_idx = step;
    for (int i = step + 1; i < size; i++) {

    
      if (array[i] < array[min_idx])
        min_idx = i;
    }
    swap(&array[min_idx], &array[step]);
  }

}
void insertionSort(int array[], int size) {


  for (int step = 1; step < size; step++) {
    int key = array[step];
    int j = step - 1;

    
    while (key < array[j] && j >= 0) {
      array[j + 1] = array[j];
      --j;
    }
    array[j + 1] = key;
  }

}


void merge(int arr[], int p, int q, int r) {
  


  int n1 = q - p + 1;
  int n2 = r - q;

  int L[n1], M[n2];

  for (int i = 0; i < n1; i++)
    L[i] = arr[p + i];
  for (int j = 0; j < n2; j++)
    M[j] = arr[q + 1 + j];

  int i, j, k;
  i = 0;
  j = 0;
  k = p;

  while (i < n1 && j < n2) {
    if (L[i] <= M[j]) {
      arr[k] = L[i];
      i++;
    } else {
      arr[k] = M[j];
      j++;
    }
    k++;
  }

  while (i < n1) {
    arr[k] = L[i];
    i++;
    k++;
  }

  while (j < n2) {
    arr[k] = M[j];
    j++;
    k++;
  }
  
}

void mergeSort(int arr[], int l, int r) {
  
  if (l < r) {

    int m = l + (r - l) / 2;

    mergeSort(arr, l, m);
    mergeSort(arr, m + 1, r);

    merge(arr, l, m, r);
  }
  
}

int partition(int array[], int low, int high) {
  
  int pivot = array[high];
  
  int i = (low - 1);

  for (int j = low; j < high; j++) {
    if (array[j] <= pivot) {

      i++;
 
      swap(&array[i], &array[j]);
    }
  }

  swap(&array[i + 1], &array[high]);

  return (i + 1);
}

void quickSort(int array[], int low, int high) {
  if (low < high) {
    

    int pi = partition(array, low, high);
    
    quickSort(array, low, pi - 1);
    
    quickSort(array, pi + 1, high);
  }
}


void bubbleSortMachine(){
  int SM[] = {1000, 5000, 10000, 50000, 100000, 200000};

  for(int j = 0; j < 6; j++) {
    int data[SM[j]];
    for(int i = 0; i < SM[j]; i++) {
      
      data[i] = rand();
    }
    int size = sizeof(data) / sizeof(data[0]);

    
      clock_t t;
      t = clock();
      bubbleSort(data, size);
      t = clock() - t;
      double time_taken = ((double)t)/CLOCKS_PER_SEC;
      printf("Bubble Sort | Sample Size: %d | Time Taken: %lf\n", SM[j], time_taken);
       
    }
}

void selectionSortMachine(){
  int SM[] = {1000, 5000, 10000, 50000, 100000, 200000};

  for(int j = 0; j < 6; j++) {
    int data[SM[j]];
    for(int i = 0; i < SM[j]; i++) {
      
      data[i] = rand();
    }
    int size = sizeof(data) / sizeof(data[0]);

    
      clock_t t;
      t = clock();
      selectionSort(data, size);
      t = clock() - t;
      double time_taken = ((double)t)/CLOCKS_PER_SEC;
      printf("Selection Sort | Sample Size: %d | Time Taken: %lf\n", SM[j], time_taken);
       
    }
}

void insertionSortMachine(){
  int SM[] = {1000, 5000, 10000, 50000, 100000, 200000};

  for(int j = 0; j < 6; j++) {
    int data[SM[j]];
    for(int i = 0; i < SM[j]; i++) {
      
      data[i] = rand();
    }
    int size = sizeof(data) / sizeof(data[0]);

    
      clock_t t;
      t = clock();
      insertionSort(data, size);
      t = clock() - t;
      double time_taken = ((double)t)/CLOCKS_PER_SEC;
      printf("Insertion Sort | Sample Size: %d | Time Taken: %lf\n", SM[j], time_taken);
       
    }
}


void mergeSortMachine(){
  int SM[] = {1000, 5000, 10000, 50000, 100000, 200000};

  for(int j = 0; j < 6; j++) {
    int data[SM[j]];
    for(int i = 0; i < SM[j]; i++) {
      
      data[i] = rand();
    }
    int size = sizeof(data) / sizeof(data[0]);

    
      clock_t t;
      t = clock();
      mergeSort(data, 0,size-1);
      t = clock() - t;
      double time_taken = ((double)t)/CLOCKS_PER_SEC;
      printf("Merge Sort | Sample Size: %d | Time Taken: %lf\n", SM[j], time_taken);
       
    }
}

void quickSortMachine(){
  int SM[] = {1000, 5000, 10000, 50000, 100000, 200000};

  for(int j = 0; j < 6; j++) {
    int data[SM[j]];
    for(int i = 0; i < SM[j]; i++) {
      
      data[i] = rand();
    }
    int size = sizeof(data) / sizeof(data[0]);

    
      clock_t t;
      t = clock();
      quickSort(data, 0,size-1);
      t = clock() - t;
      double time_taken = ((double)t)/CLOCKS_PER_SEC;
      printf("Quick Sort | Sample Size: %d | Time Taken: %lf\n", SM[j], time_taken);
       
    }
}






int main() {



  bubbleSortMachine();
  printf("\n=======================================================\n");
  selectionSortMachine();
  printf("\n=======================================================\n");
  insertionSortMachine();
  printf("\n=======================================================\n");
  mergeSortMachine();
  printf("\n=======================================================\n");
  quickSortMachine();
 

}