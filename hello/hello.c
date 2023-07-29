#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Getting input from user
    string name = get_string("Enter name: ");
    //Showing output
    printf("hello,%s\n", name);
}