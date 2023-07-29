#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)//only allowing 2 inputs in CLI
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open FILE.\n");
        return 2;
    }
    //the variables to be used
    BYTE buffer [512];
    int imgCNT = 0;
    FILE *output = NULL;
    char *filename = malloc(8 * sizeof(char));

    while (fread(buffer, 1, 512, file) == 512)//main loop
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)//checking for starting of jpg
        {
            if (imgCNT > 0)//checking if there is an image already made or not
            {
                fclose(output);
            }
            sprintf(filename, "%03i.jpg", imgCNT);//assigning name
            output = fopen(filename, "w");
            imgCNT++;
        }
        if (output != NULL)
        {
            fwrite(buffer, 1, 512, output);
        }
    }
    //closing and freeing the files and memory
    free(filename);
    fclose(output);
    fclose(file);
    return 0;
}