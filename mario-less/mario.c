#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //n is height
    int n = 0;
    do
    {
        n = get_int("Height: ");
    }
    while (8 < n || n < 1);
// r is for rows
    for (int r = 0; r < n; r++)
    {
        for (int s = n - r - 1; s > 0; s--) //for spaces
        {
            printf(" ");
        }

        for (int j = 0; j <= r; j++)//for the #
        {
            printf("#");
        }
        printf("\n");
    }
}