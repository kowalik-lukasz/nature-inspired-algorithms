/*
  This generator generates 3-regular planar graphs
  author: Di Lu.

  **/
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#define DEG 3
#define NMAX 512
#define MAX_NUM_LENGTH 100


void printGraphAdjMat(int (*graph)[DEG], int n_nodes, FILE * fp) {
    int i = 0, j = 0;
    int adj_mat_row[n_nodes];

    for (i = 0; i < n_nodes; i ++) {
        for (j = 0; j < n_nodes; j ++) {
            adj_mat_row[j] = 0;
        }

        for (j = 0; j < DEG; j ++)
            adj_mat_row[graph[i][j]] = 1;

        for (j = 0; j < n_nodes; j ++) {
            if (j == 0) {
                fprintf(fp, "%d", adj_mat_row[j]);
            }
            else {
                fprintf(fp, ",%d", adj_mat_row[j]);
            }
        }
        fprintf(fp, "\n");
    }
    fprintf(fp, "\n");
}

void printGraph(int (*graph)[DEG], int n_nodes, FILE * fp) {
    int i = 0, j = 0;
    fprintf(fp, "%d\n", n_nodes);

    for (i = 0; i < n_nodes; i ++) {
        fprintf(fp, "%d ", DEG);
        for (j = 0; j < DEG; j ++) {
            fprintf(fp, "%d ", graph[i][j]);
        }
        fprintf(fp, "\n");
    }
    fprintf(fp, "\n");
}


void gen_graph(int (*basegraph)[], int *n_nodes);
void create_basegraph(int (*k4)[DEG]);
int main(int argc, char * argv[])
{
    FILE *fp= fopen("di_randGraphs.txt", "w+");
    if (fp == NULL) {
        fprintf(stderr, "Can't open input file di_randGraphs.txt\n");
        exit(1);
    }
    int n_nodes = 4;
    int min_nodes = 0, max_nodes  = 10;
    if (argc == 3) { // if it has exactly 2 arguments
        min_nodes = atoi(argv[1]);
        max_nodes = atoi(argv[2]);
    }

    int (*basegraph)[DEG] = malloc(sizeof(int[DEG]) * NMAX);
    create_basegraph(basegraph); //the base graph here is k4.
//    int (*nextgraph)[DEG] = malloc(sizeof(int[DEG]) * NMAX);
    int *ptr = &n_nodes;
    while (n_nodes < min_nodes) {
        gen_graph(basegraph, ptr);
    }
    if (max_nodes > NMAX) {
        printf("the maximun nodes are greater than upper bound, please modify value of NMAX.\n");
        exit(1);
    }
    while (n_nodes <= max_nodes) {
        char *size;
        char buffer[MAX_NUM_LENGTH];
        if (asprintf(&size, "%d", n_nodes) == -1) {
            perror("asprintf");
        } 
        else {
            strcat(strcpy(buffer, "size"), size);
            strcat(buffer, "_instance.csv");
            printf("%s\n", buffer);
            free(size);
        }

        FILE *fp= fopen(buffer, "w+");
        printGraphAdjMat(basegraph, n_nodes, fp);
        fclose(fp);
        gen_graph(basegraph, ptr);
    }
    return 0;
}

void create_basegraph(int (*k4)[DEG]) {
    k4[0][0] = 2;
    k4[0][1] = 1;
    k4[0][2] = 3;
    k4[1][0] = 0;
    k4[1][1] = 2;
    k4[1][2] = 3;
    k4[2][0] = 3;
    k4[2][1] = 1;
    k4[2][2] = 0;
    k4[3][0] = 0;
    k4[3][1] = 1;
    k4[3][2] = 2;
}

void gen_graph(int (*basegraph)[DEG], int *n_nodes) {
    /* random a starting edge (u,v) */
    srand (time(NULL));
    int row = rand() % *n_nodes;
    int col = rand() % DEG;
    int u = row;
    int v = basegraph[row][col];
    /* I simplify the step of walking face, I only take
    one step walk and then split this face. */
    int i = 0, j = 0, next_u = 0;
    while (basegraph[v][i] != u) i ++; //loop until
    if (i == DEG - 1) { //if it is the largest elem in this array, loop back
        next_u = basegraph[v][0];
    }
    else {
        next_u = basegraph[v][i + 1];
    }
    /*iterate the adjacency list of v until it finds the next cyclic
    node of u */
    // add two new nodes: new_a and new_b
    int new_a = *n_nodes; // new_a is the vertex subdividing u,v
    int new_b = *n_nodes + 1; // new_b is the vertex subdividing v, new_u
    for (i = 0; i < *n_nodes; i ++) {
        if (i == u)  {    //hard coding here, applies only to 3-regular
            for (j = 0; j < DEG; j ++) {
                if (basegraph[i][j] == v) basegraph[i][j] = new_a;
            }
        }
        else if (i == next_u) {
            for (j = 0; j < DEG; j ++) {
                if (basegraph[i][j] == v) basegraph[i][j] = new_b;
            }
        }
        else if (i == v) {
            for (j = 0; j < DEG; j ++) {
                if (basegraph[i][j] == u) {
                    basegraph[i][j] = new_a;
                }
                else if (basegraph[i][j] == next_u) {
                    basegraph[i][j] = new_b;
                }
            }
        }
    }
    *n_nodes = *n_nodes + 2;

 //   printGraph(basegraph, *n_nodes);
  //  memcpy(nextgraph, basegraph, sizeof(int) * (*n_nodes - 2) * DEG);

    basegraph[new_a][0] = u;
    basegraph[new_a][1] = new_b;
    basegraph[new_a][2] = v;
    basegraph[new_b][0] = v;
    basegraph[new_b][1] = new_a;
    basegraph[new_b][2] = next_u;
 //   memcpy(nextgraph, basegraph, sizeof(int) * (*n_nodes) * DEG);
//    printGraph(basegraph, *n_nodes);
}
