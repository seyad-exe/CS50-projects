#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

//start
int main(int argc, string argv[])
{
    if (argc != 2) //only 2 values
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0, len = strlen(argv[1]) ; i < len ; i++)
    {
        if (!isdigit(argv[1][i])) //checks for digit
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(argv[1]); // convert char to int
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++) // main part
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", (((plaintext[i] - 65) + key) % 26) + 65);
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", (((plaintext[i] - 97) + key) % 26) + 97);
        }
        else
        {
            printf("%c",plaintext[i]);
        }
    }
    printf("\n");
}
